# Установка и обновление 1c-testing

Канонический исходник skill находится в этом Git-репозитории. Не устанавливайте его из временного каталога `C:\Temp`.

## Глобальная установка

Чтобы `1c-testing` был доступен во всех новых чатах текущего пользователя:

```powershell
& "F:\Work\1c-testing-skill\install-or-update.ps1" -Scope Global
```

По умолчанию skill устанавливается в `%USERPROFILE%\.codex\skills\1c-testing`. Если задана переменная `CODEX_HOME`, используется каталог из неё.

Явный путь можно передать так:

```powershell
& "F:\Work\1c-testing-skill\install-or-update.ps1" `
  -Scope Global `
  -CodexHome "D:\CodexHome"
```

Глобальная установка не изменяет `USER-RULES.md`, `AGENTS.md` и конфигурацию MCP конкретных проектов.

## Установка в проект

Project-local установка нужна, когда правила тестирования должны храниться и версионироваться вместе с проектом:

```powershell
& "F:\Work\1c-testing-skill\install-or-update.ps1" `
  -Scope Project `
  -ProjectRoot "F:\erGitBase\114"
```

Она:

- обновляет `.codex\skills\1c-testing`;
- добавляет или заменяет только размеченный блок `1c-testing` в `USER-RULES.md`;
- не изменяет `AGENTS.md`;
- не изменяет `.codex\config.toml` и `v8project.yaml`.

Если `-Scope` не указан, используется `Project` и текущий каталог считается корнем проекта.

## Что настраивается отдельно

Skill не содержит реквизитов тестовой базы и не включает MCP автоматически. В каждом проекте отдельно настраиваются:

- `v8project.yaml` или `v8project.local.yaml`;
- `v8_runner` MCP;
- Vanessa Automation MCP, если он используется;
- пути к YAxUnit, Vanessa и тестовой информационной базе.

Без Vanessa MCP skill использует встроенный каталог `vendor/va-ai` для поиска известных шагов и проверки `.feature`. Реальный запуск Vanessa всё равно требует настроенного тестового окружения.

## Обновление после изменений

После получения новой версии репозитория:

```powershell
git -C "F:\Work\1c-testing-skill" pull
& "F:\Work\1c-testing-skill\install-or-update.ps1" -Scope Global
& "F:\Work\1c-testing-skill\install-or-update.ps1" -Scope Project -ProjectRoot "F:\erGitBase\114"
```

Устанавливайте только нужные области. После установки откройте новый чат или перезапустите Codex.

## Проверка

```powershell
Test-Path "$env:USERPROFILE\.codex\skills\1c-testing\SKILL.md"
Test-Path "F:\erGitBase\114\.codex\skills\1c-testing\SKILL.md"
```

Для проверки структуры skill:

```powershell
$env:PYTHONUTF8 = '1'
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" `
  "F:\Work\1c-testing-skill\1c-testing"
```

## Работа с Git

Изменения сначала вносятся в `F:\Work\1c-testing-skill`, проверяются, коммитятся и только затем устанавливаются в проекты или глобальный каталог:

```powershell
git -C "F:\Work\1c-testing-skill" status
git -C "F:\Work\1c-testing-skill" diff --check
git -C "F:\Work\1c-testing-skill" add .
git -C "F:\Work\1c-testing-skill" commit -m "Описание изменения"
```

Remote-репозиторий можно добавить позже:

```powershell
git -C "F:\Work\1c-testing-skill" remote add origin <URL-РЕПОЗИТОРИЯ>
git -C "F:\Work\1c-testing-skill" push -u origin main
```
