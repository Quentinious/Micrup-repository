"""Validate the API document, its examples, privacy boundary and Kotlin DTO parity."""
from pathlib import Path
import copy
import json
import subprocess
import sys
import yaml
from openapi_spec_validator import validate_spec
from openapi_schema_validator import OAS30Validator, oas30_format_checker

ROOT = Path(__file__).resolve().parents[2]


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f'Duplicate YAML key: {key}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)


def expand(value, spec, chain=()):
    if isinstance(value, list):
        return [expand(item, spec, chain) for item in value]
    if not isinstance(value, dict):
        return value
    if '$ref' in value:
        reference = value['$ref']
        if not reference.startswith('#/') or reference in chain:
            raise ValueError(f'External or cyclic ref is not supported in v0: {reference}')
        target = spec
        for part in reference[2:].split('/'):
            target = target[part.replace('~1', '/').replace('~0', '~')]
        return expand(copy.deepcopy(target), spec, chain + (reference,))
    return {key: expand(item, spec, chain) for key, item in value.items()}


def validator(schema, spec):
    return OAS30Validator(expand(schema, spec), format_checker=oas30_format_checker)


def check(spec, fixtures_dir):
    validate_spec(spec)
    fixtures = json.loads((fixtures_dir / 'index.json').read_text())
    for fixture in fixtures:
        value = json.loads((fixtures_dir / fixture['file']).read_text())
        schema = spec['components']['schemas'][fixture['schema']]
        errors = list(validator(schema, spec).iter_errors(value))
        if bool(errors) == fixture['expectedValid']:
            raise ValueError(f'Fixture {fixture["file"]}: expectedValid={fixture["expectedValid"]}, errors={errors}')
        if fixture['expectedValid']:
            name = Path(fixture['file']).stem
            if spec['components']['examples'][name]['value'] != value:
                raise ValueError(f'Embedded example drift: {name}')
    implemented = []
    ids = set()
    operations = 0
    sensitive = {'contacts', 'email', 'phone', 'telegram', 'evidenceUrl', 'documentUrl', 'paymentToken'}

    def check_public(schema):
        expanded = expand(schema, spec)

        def visit(node):
            if isinstance(node, dict):
                leaked = sensitive.intersection(node.get('properties', {}))
                if leaked:
                    raise ValueError(f'Private fields in public response: {leaked}')
                for item in node.values():
                    visit(item)
            elif isinstance(node, list):
                for item in node:
                    visit(item)
        visit(expanded)

    for path, methods in spec['paths'].items():
        for method, operation in methods.items():
            if method not in {'get','post','put','patch','delete'}:
                continue
            operations += 1
            operation_id = operation['operationId']
            if operation_id in ids:
                raise ValueError(f'Duplicate operationId: {operation_id}')
            ids.add(operation_id)
            if operation['x-implementation-status'] == 'implemented':
                implemented.append((method, path))
            for response in operation['responses'].values():
                response = expand(response, spec)
                for media in response.get('content', {}).values():
                    schema = media['schema']
                    if operation.get('security') == []:
                        check_public(schema)
                    if 'example' in media:
                        validator(schema, spec).validate(media['example'])
                    for example in media.get('examples', {}).values():
                        validator(schema, spec).validate(expand(example, spec)['value'])
    if implemented != [('get','/api/health')]:
        raise ValueError(f'Sprint 0 implementation boundary changed: {implemented}')
    print(f'OpenAPI OK: {operations} operations, {len(fixtures)} valid/invalid fixtures; public schemas exclude private fields')


if __name__ == '__main__':
    spec = yaml.load((ROOT / 'docs/api/openapi.yaml').read_text(), Loader=UniqueKeyLoader)
    check(spec, ROOT / 'docs/api/examples')
    subprocess.run([sys.executable, str(ROOT / 'tools/api/generate_contract_dtos.py'), '--check'], check=True)
