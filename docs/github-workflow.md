# Защита main и PR-процесс

Связано с [SCRUM-23](https://andrewalexxeev.atlassian.net/browse/SCRUM-23).

## Исходный статус

На 12.10.2026 после PR #1 main имеет protected=false, rulesets отсутствуют. PR #1 merged без APPROVED. Этот документ не включает настройки GitHub.

Текущее подключение умеет менять файлы и создавать PR, но не имеет операции изменения branch protection; чтение подробной защиты возвращает 403. Настройку выполняет владелец с административным доступом.

## Требуемые настройки

В [Settings → Branches](https://github.com/Quentinious/Micrup-repository/settings/branches) создайте protection rule для main (либо эквивалентный active ruleset без bypass для обычной работы):

- Require a pull request before merging.
- Require approvals: **1**, от другого участника с необходимыми правами.
- Dismiss stale pull request approvals when new commits are pushed.
- Require conversation resolution before merging.
- Require status checks to pass: **android-build, backend-build, backend-tests**.
- Не разрешать force pushes и удаление ветки; включить применение защиты для администраторов без повседневного bypass.

После SCRUM-21 и первого успешного запуска добавьте **api-contract** в обязательный набор. Выбирайте названия из фактических Checks. Naming проверяет reviewer; PR template не обеспечивает его технически.

## Приёмка SCRUM-23

1. Команда согласовала naming; подтверждение записано в задаче.
2. PR template merged и появляется при создании следующего PR.
3. Защита main включена, обязательные Checks выбраны.
4. На следующем обычном PR merge заблокирован до approval и успешных проверок. Не нужно специально ломать main или обходить защиту.
5. Независимое APPROVED, успешные Checks, закрытые conversations и merge подтверждены ссылками в Jira.

До выполнения всех пунктов SCRUM-23 не переводится в Done.

Источник: [GitHub — About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).
