# Micrup Monorepo

Инженерный фундамент учебного проекта Micrup.

## Структура

- `android/` — Android приложение (Kotlin, Jetpack Compose, Navigation Compose, ViewModel, Coroutines/Flow)
- `backend/` — Backend (Kotlin, Spring Boot, Spring Web, Spring Security, Spring Data JPA, Flyway)
- `infra/` — инфраструктура (Docker Compose с PostgreSQL)
- `docs/` — архитектура, требования, API
- `.github/workflows/` — CI

## Предварительные требования

- JDK 17
- Docker и Docker Compose
- Android SDK (для сборки Android)

## Запуск PostgreSQL

```bash
cd /home/runner/work/Micrup-repository/Micrup-repository/infra
docker compose up -d
```

## Запуск backend

```bash
cd /home/runner/work/Micrup-repository/Micrup-repository/backend
./gradlew bootRun
```

Проверка health endpoint:

```bash
curl http://localhost:8080/api/health
```

## Запуск Android

```bash
cd /home/runner/work/Micrup-repository/Micrup-repository/android
./gradlew assembleDebug
```

Для запуска на устройстве/эмуляторе можно использовать Android Studio.

## Запуск тестов

Backend unit/integration tests:

```bash
cd /home/runner/work/Micrup-repository/Micrup-repository/backend
./gradlew test
```

Backend full build:

```bash
cd /home/runner/work/Micrup-repository/Micrup-repository/backend
./gradlew build
```
