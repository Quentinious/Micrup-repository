"""Generate identical transport types for the two independent Kotlin modules."""
from pathlib import Path
import argparse
import yaml

ROOT = Path(__file__).resolve().parents[2]
OUTPUTS = (
    ROOT / 'android/app/src/main/java/com/micrup/contract/v0/ContractDtos.kt',
    ROOT / 'backend/src/main/kotlin/com/micrup/contract/v0/ContractDtos.kt',
)


def render(spec):
    schemas = spec['components']['schemas']

    def kotlin_type(schema):
        nullable = schema.get('nullable', False)
        if '$ref' in schema:
            name = schema['$ref'].removeprefix('#/components/schemas/')
            if name not in schemas:
                raise ValueError(f'Unsupported reference: {schema["$ref"]}')
            result = name
            nullable = nullable or schemas[name].get('nullable', False)
        elif schema['type'] == 'array':
            result = f'List<{kotlin_type(schema["items"])}>'
        elif schema['type'] == 'integer':
            result = 'Long' if schema.get('format') == 'int64' else 'Int'
        else:
            result = {'string': 'String', 'number': 'Double', 'boolean': 'Boolean'}[schema['type']]
        return result + ('?' if nullable else '')

    lines = [
        '// Generated from docs/api/openapi.yaml; do not edit by hand.',
        '// Run: python tools/api/generate_contract_dtos.py',
        '// Transport shapes only. Constraints, auth and business rules are not implemented here.',
        '// Optional request fields represented by null must be omitted unless their schema is nullable.',
        'package com.micrup.contract.v0', '',
    ]
    for name, schema in schemas.items():
        if schema['type'] == 'string' and 'enum' in schema:
            lines += [f'enum class {name} {{', '    ' + ', '.join(schema['enum']), '}', '']
        elif schema['type'] == 'object':
            required = set(schema.get('required', []))
            lines.append(f'data class {name}(')
            for field, field_schema in schema['properties'].items():
                kind = kotlin_type(field_schema)
                default = ''
                if field not in required:
                    if not kind.endswith('?'):
                        kind += '?'
                    default = ' = null'
                lines.append(f'    val {field}: {kind}{default},')
            lines += [')', '']
        else:
            raise ValueError(f'Unsupported top-level schema: {name}')
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    spec = yaml.safe_load((ROOT / 'docs/api/openapi.yaml').read_text())
    content = render(spec)
    for path in OUTPUTS:
        if args.check:
            if not path.exists() or path.read_text() != content:
                raise SystemExit(f'DTO drift: {path.relative_to(ROOT)}; run the generator')
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    print('DTO parity OK' if args.check else 'Generated Android/backend DTOs')


if __name__ == '__main__':
    main()
