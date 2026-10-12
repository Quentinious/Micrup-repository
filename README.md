# Micrup

Micrup — учебный командный проект: Android-приложение для покупки и продажи небольших работающих интернет-проектов. Договор и расчёты за сам проект проходят вне Micrup.

## С чего начать участнику команды

1. Найдите задачу на [доске Micrup в Jira](https://andrewalexxeev.atlassian.net/jira/software/projects/SCRUM/boards/1).
2. Прочитайте цель, acceptance criteria, зависимости и границы задачи. Неоднозначности запишите в задаче до реализации.
3. Поднимите нужный модуль и создайте ветку от актуального main.
4. Откройте небольшой PR с Jira key, описанием результата и проверками. Другой участник проверяет код и критерии задачи.

Подробные правила: [CONTRIBUTING.md](CONTRIBUTING.md).

## Текущее состояние и этапы

В main merged foundation (PR #1): стартовый Android-экран, Spring Boot с `GET /api/health`, PostgreSQL/Docker Compose, техническая миграция Flyway и CI. Бизнес-сценарии пока не реализованы.

| Этап | Результат |
| --- | --- |
| Sprint 0 — Foundation | Scope, архитектура, модель данных, API-контракт, skeleton, CI и командный процесс. Описание операции в OpenAPI не означает её реализацию. |
| Sprint 1 — Catalog | Миграции/модель чтения проектов, API каталога/карточки, Android-экраны и интеграция (SCRUM-24–29). |
| Последующие этапы MVP | Профиль, размещение/модерация, фильтры, рекомендации, подписочный доступ к контактам, аукцион с тестовыми оплатами услуг площадки. |

Веб-клиент, внутренний чат, сложная ML-модель, приём стоимости проекта и эскроу внутри Micrup в текущий MVP не входят. Согласование полного scope: [SCRUM-1](https://andrewalexxeev.atlassian.net/browse/SCRUM-1).

## Как работает команда

| Область | Ответственность | С кем согласует результат |
| --- | --- | --- |
| Android | UI, navigation, ViewModel/UI state, загрузка и ошибки | Backend: DTO/API; QA: сценарии |
| Backend | REST API, права, бизнес-правила, данные и миграции | Android: контракт; продукт: спорные правила |
| Продукт/исследования | Scope, use cases, интервью, прототип, acceptance criteria | Команда: приоритеты и объём итерации |
| QA/review | Happy path/ошибки, воспроизводимые дефекты, проверка PR | Разработчики: данные и окружение |
| Координация | Зависимости, распределение задач, демонстрация итерации | Участники: доступное время и ограничения |

Роли могут совмещаться. Конкретный исполнитель фиксируется в Jira; таблица не назначает людей. Автор PR не заменяет независимого reviewer.

- **Jira**: задачи, приоритеты, исполнители, acceptance criteria и блокеры.
- **GitHub**: код, технические документы, обсуждение PR и CI.
- **main**: интеграционная ветка. Работа идёт в `feature/SCRUM-<номер>-short-name`; изменения попадают в main через PR.
- До параллельной работы Android/backend согласуют API. Изменение поля, типа, enum или ошибки требует обновления контракта и проверки обоих модулей.
- Блокер описывается в Jira: что мешает, какое решение нужно, какие задачи заблокированы. Замечания к коду остаются в PR.
- На планировании учитываются доступные часы и резерв на review/исправления. Итерация заканчивается демонстрацией результата и обсуждением улучшений.

Статусы: **К выполнению → В работе → В процессе проверки → Готово**. Done требует acceptance criteria, согласований и проверок; для изменений репозитория — merged PR. Зелёный CI не заменяет проверку пользовательского сценария.

## Структура и стек

| Каталог | Назначение |
| --- | --- |
| android/ | Kotlin, Jetpack Compose, Navigation Compose, ViewModel, Coroutines/Flow |
| backend/ | Kotlin, Spring Boot, Web/Security/Data JPA, Flyway, PostgreSQL |
| infra/ | Docker Compose для локальной PostgreSQL |
| docs/architecture/ | [Архитектура](docs/architecture/README.md) и модель данных |
| docs/api/ | [API](docs/api/README.md), контракт и примеры |
| docs/requirements/ | [Требования](docs/requirements/README.md); актуальные задачи/статусы — в Jira |
| .github/ | PR template и GitHub Actions |

## Локальное окружение

Нужны Git, **JDK 17**, Docker с Compose v2 (Windows: Docker Desktop), Android Studio/SDK для Android. Gradle запускается через Wrapper, отдельная установка не нужна. Команды ниже начинаются из корня репозитория.

```bash
git clone https://github.com/Quentinious/Micrup-repository.git
cd Micrup-repository
docker compose -f infra/docker-compose.yml up -d
docker compose -f infra/docker-compose.yml ps
```

Дождитесь PostgreSQL healthy. Локальные БД/пользователь/пароль — micrup, порт 5432. Это значения для разработки; секреты реальных окружений не коммитятся.

### Backend

Linux/macOS:

```bash
cd backend
./gradlew bootRun
```

Windows PowerShell:

```powershell
cd backend
.\gradlew.bat bootRun
```

Backend: http://localhost:8080. Flyway применяет миграции при старте. В другом терминале: `curl http://localhost:8080/api/health`; в PowerShell — `Invoke-RestMethod http://localhost:8080/api/health`. Ожидается `{"status":"UP"}`. Остановка backend: Ctrl+C.

| Переменная | По умолчанию | Назначение |
| --- | --- | --- |
| DB_URL | jdbc:postgresql://localhost:5432/micrup | Адрес/порт/имя БД |
| DB_USERNAME | micrup | Пользователь БД |
| DB_PASSWORD | micrup | Пароль БД |
| SERVER_PORT | 8080 | Порт backend |

Пример: Bash `export DB_URL='jdbc:postgresql://localhost:5433/micrup'`; PowerShell `$env:DB_URL = 'jdbc:postgresql://localhost:5433/micrup'`. Backend запускается из того же терминала. При смене порта PostgreSQL измените и host-port в локальной Compose-конфигурации: одна DB_URL порт контейнера не меняет.

### Android

Откройте android/ в Android Studio, дождитесь Gradle Sync и запустите app на эмуляторе/устройстве. Сейчас работает foundation-экран; сетевой интеграции ещё нет.

Сборка из android/: Linux/macOS `./gradlew assembleDebug`; PowerShell `.\gradlew.bat assembleDebug`. APK: `android/app/build/outputs/apk/debug/app-debug.apk`.

Для SCRUM-29: backend компьютера доступен из стандартного Android Emulator через 10.0.2.2, а не localhost. Сетевой клиент и настройка локального HTTP относятся к задаче интеграции.

### Остановка и сброс БД

Из корня репозитория остановка с сохранением данных:

```bash
docker compose -f infra/docker-compose.yml down
```

**Сброс удаляет данные этой локальной БД.** Остановите backend, выполните команды и запустите backend заново для применения Flyway:

```bash
docker compose -f infra/docker-compose.yml down --volumes
docker compose -f infra/docker-compose.yml up -d
```

## Проверки и CI

| Проверка | Linux/macOS из каталога модуля | PowerShell из каталога модуля |
| --- | --- | --- |
| Android build | ./gradlew assembleDebug | .\gradlew.bat assembleDebug |
| Backend build | ./gradlew assemble | .\gradlew.bat assemble |
| Backend tests | ./gradlew test | .\gradlew.bat test |

Backend integration test использует Testcontainers: нужен Docker. Сейчас стоит disabledWithoutDocker=true, поэтому без Docker тест может быть пропущен; это не подтверждает работу приложения с БД.

[CI](https://github.com/Quentinious/Micrup-repository/actions/workflows/ci.yml) запускается на push и PR: android-build, backend-build, backend-tests. Ошибка команды завершает job с failure. Результат смотрите в Checks PR.

Требуемая [защита main](docs/github-workflow.md) проверяется в SCRUM-23. Документация не означает, что настройки GitHub уже включены.
