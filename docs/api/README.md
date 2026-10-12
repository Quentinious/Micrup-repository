# REST API v0 — SCRUM-21

**Статус: Draft для совместного review Android/backend.** [openapi.yaml](openapi.yaml) — источник имён, типов, nullable, enum и ошибок. Все domain operations помечены planned; **работает только GET /api/health**. Этот PR не создаёт controllers/services, authentication, JPA, миграции или продуктовые экраны.

Модель для совместного согласования: [SCRUM-20 / PR #3](https://github.com/Quentinious/Micrup-repository/pull/3). Физическая модель каталога и работающие GET реализуются в SCRUM-24–26, Android UI/HTTP — в SCRUM-27–29.

## Контракт операций

| Операция | Доступ | Результат/этап |
| --- | --- | --- |
| GET /api/health | Публичный | 200 Health, реализован foundation |
| GET /api/v1/projects | Публичный | 200 ProjectPage, SCRUM-25 |
| GET /api/v1/projects/{projectId} | Публичный | 200 ProjectDetails, SCRUM-26 |
| GET /api/v1/users/{userId}/profile | Публичный | 200 SellerProfile без контактов, следующий этап MVP |
| GET /api/v1/me/profile | Пользователь | 200 UserProfile, следующий этап MVP |
| PUT /api/v1/me/profile | Пользователь | 200 UserProfile, полная замена профиля |
| POST /api/v1/me/projects | Пользователь | 201 ProjectDraft, создать неполный draft |
| GET /api/v1/me/projects/{projectId} | Владелец | 200 ProjectDraft, свои данные объявления |
| PUT /api/v1/me/projects/{projectId} | Владелец | 200 ProjectDraft, заменить содержимое DRAFT/REJECTED |
| POST /api/v1/me/projects/{projectId}/submit | Владелец | 200 ProjectDraft со статусом PENDING_REVIEW; не публикация |
| POST /api/v1/projects/{projectId}/views | Пользователь | 204 без тела, запись просмотра с eventId |

Bearer transport описывает потребность в authenticated user, а не выбор JWT/провайдера. Регистрация, выпуск токенов, контакты, оплата, аукцион, модераторские операции и рекомендации здесь не реализуются. Их contract extension выполняется в соответствующих задачах после SCRUM-7. Сейчас SecurityConfig разрешает только health; Swagger runtime и domain endpoints остаются закрытыми. YAML можно открыть в OpenAPI viewer без запуска backend; сгенерированная Springdoc-схема текущих controllers не заменяет этот будущий контракт.

## Форматы и единицы

| JSON | Kotlin transport | Семантика |
| --- | --- | --- |
| string/uuid | String | UUID доменного объекта; владелец/пользователь write operation определяется сервером |
| string/date-time | String | UTC RFC 3339; преобразование в Instant — в реализации |
| string/date | String | Граница периода показателей |
| Money/Price.amountMinor, integer/int64 | Long | Копейки; без float; Price > 0, Money >= 0 |
| Currency | Currency enum | RUB для v0 |
| supportHoursPerWeek, number | Double | Часы поддержки в неделю, 0..168 |
| enum | Одноимённый Kotlin enum | Значения одинаковы в обоих модулях |

250 000 ₽ = amountMinor 25 000 000. Приоритетный ценовой сегмент не ограничивает размещение. Показатели доходов/расходов имеют явный periodStart/periodEnd; неизвестное поле не становится нулём.

В публичном ProjectDetails metrics обязательно присутствует и может быть null; это baseline до согласования disclosure/consent. Даже при раскрытии summary-показателей закрытые подтверждения и контакты не включаются в DTO. Проверка права доступа выполняется сервером, скрытие UI не является защитой.

## Nullable и изменения

- ProjectSummary — опубликованная карточка: обязательные поля заполнены, technologies не пустой.
- ProjectDraftInput допускает {}, чтобы сохранять неполный draft. PUT заменяет полный набор editable полей: отсутствие очищает значение. Необязательные поля не принимают JSON null, кроме nullable metrics.
- ProfileInput требует displayName; отсутствующий/null bio при PUT очищает описание. PATCH не введён, поэтому не требуется различать omitted и explicit null для частичного обновления.
- Kotlin nullable у необязательного поля обозначает отсутствие; это не разрешение отправить null в JSON. Будущий serializer/mapper должен соблюдать OpenAPI, включая required nullable поля ответа.
- Сервер назначает id/ownerId/status/timestamps. Причина отклонения доступна владельцу в ProjectDraft.rejectionReason и не задаётся write request. При submit проверяются обязательные поля и меняется только состояние модерации. API модератора и редактирование опубликованного проекта — дальнейший этап.
- Конкурентное редактирование draft, выбор auth provider и обязательность дополнительных показателей — вопросы перед реализацией listings/auth. Предложенный контракт остаётся Draft до их review.

## Пагинация, фильтры и повторы

page с нуля, size 1..100 (default 20). Сортировка publishedAt DESC, id ASC. Страница вне диапазона возвращает пустой items с реальными totals. Пагинация offset не гарантирует snapshot при изменениях каталога.

Предложены фильтры type, minPriceMinor/maxPriceMinor, maxSupportHoursPerWeek и technologyIds. Цены в RUB/копейках, min <= max; список технологий через запятую, AND-семантика. Доходные фильтры требуют согласованного периода и disclosure; они не включены молча.

Просмотры: userId из auth, projectId из URL, время назначает сервер. Повтор eventId для того же пользователя/проекта — 204 без дубликата; тот же ID для другого проекта — 409. Анонимная история не записывается в v0; сам каталог остаётся публичным.

Создание draft POST не заявляет idempotency: при неоднозначном сетевом результате автоматический retry может создать второй draft. Полная замена PUT повторяема; повтор submit для PENDING_REVIEW не создаёт повторную модерацию. Это контракт будущей реализации, не готовые механизмы.

## Ошибки

Единый ApiError для будущих domain operations: code, message, fieldErrors[], traceId. 400 — неверные данные; 401 — нужен аккаунт; 403 — нет права; 404 — неизвестный/недоступный объект; 409 — конфликт; 500 — внутренняя ошибка без деталей реализации. Конкретные ответы перечислены у каждой операции. Foundation health ещё не реализует общий error handler.

Публичный GET не раскрывает наличие черновика/архивного объявления: одинаковая 404. Контракт ошибок тоже должен быть реализован и протестирован в feature-задачах.

## Проверка и генерация DTO

Нужен Python 3.12. Из корня репозитория:

```bash
python -m venv .venv-api
```

Активация Bash: `source .venv-api/bin/activate`; PowerShell: `.\.venv-api\Scripts\Activate.ps1`. Затем:

```bash
python -m pip install -r tools/api/requirements.txt
python tools/api/check_contract.py
```

Проверяются OpenAPI/$ref, отсутствие повторных YAML keys, 19 положительных/отрицательных JSON fixtures, inline examples, приватные поля публичных схем и одинаковые Kotlin DTO. Примеры синтетические: [examples/index.json](examples/index.json) задаёт schema и expectedValid для каждого файла. Файлы invalid-* специально должны отклоняться.

После согласованного изменения YAML:

```bash
python tools/api/generate_contract_dtos.py
python tools/api/check_contract.py
```

Генератор обновляет один и тот же ContractDtos.kt в Android/backend с package com.micrup.contract.v0. Это transport shapes без runtime validators, сетевого клиента и бизнес-логики. Они ещё не используются продуктовым потоком. Формат/nullable/minimum constraints проверяются контрактом; интеграционные serializer tests добавляются вместе с выбором сетевого слоя.

Job **api-contract** добавлен в CI. После merge/первого успешного запуска владелец включает его в protection main вместе с существующими тремя Checks.

## Что нужно для завершения SCRUM-21

Совместный review модели/API: подтвердить поля, типы, публикацию, публичные/закрытые данные, authenticated ViewEvent и ошибки. Зелёная проверка YAML подтверждает согласованность документа, но не согласование команды и не работающий каталог. До этого задача не переводится в Done.

Спецификация формата: [OpenAPI 3.0.3](https://spec.openapis.org/oas/v3.0.3).
