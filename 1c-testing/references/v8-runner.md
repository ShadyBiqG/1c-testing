# v8-runner — MCP-first build и запуск тестов

## Главное правило

`v8-runner` — основной оркестратор сборки и тестов проекта.

Если MCP-сервер `v8_runner` доступен в текущей Codex-сессии, используй MCP первым. CLI запускай только для отсутствующих в MCP операций, намеренного `--no-build`, диагностики самого транспорта или когда MCP недоступен.

Не выполняй одну и ту же проверку через MCP и CLI подряд без диагностической причины.

## Источник конфигурации

Перед запуском прочитай `v8project.yaml`. Не угадывай путь информационной базы, source-set тестового расширения, имя расширения и backend сборки.

При stdio-подключении Codex обычно запускает `v8-runner` уже с нужным `--config`, поэтому MCP-инструменты относятся к конкретному проекту. Не пытайся переключить один MCP-процесс на другой проект внутри tool call.

## MCP-поверхность

Текущая публичная MCP-поверхность v8-runner содержит 8 операций:

- `run_all_tests`
- `run_module_tests`
- `build_project`
- `dump_config`
- `launch_app`
- `check_syntax_edt`
- `check_syntax_designer_config`
- `check_syntax_designer_modules`

MCP намеренно не зеркалит весь CLI.

## Основной YAxUnit workflow

### Узкий прогон

Используй:

```text
run_module_tests
  moduleName: <РеальноеИмяМодуля>
  full: false
```

`run_module_tests` сам использует build prerequisite (`BuildFirst`). Отдельный `build_project` перед каждым тестом не нужен.

Если нужен полный отчёт/режим полного прогона для модуля:

```text
run_module_tests
  moduleName: <РеальноеИмяМодуля>
  full: true
```

### Все YAxUnit-тесты

```text
run_all_tests
  runner: yaxunit
```

Поле `runner` можно не задавать, если текущая версия MCP по умолчанию выбирает YAxUnit, но для явного workflow предпочтительно указывать `yaxunit`.

## Vanessa через MCP

Если `tests.va` настроен в `v8project.yaml`:

```text
run_all_tests
  runner: vanessa
```

Дополнительно MCP поддерживает `profile`, `feature`, `filterTag`, `ignoreTag`, `scenarioFilter`. Используй их только по реальному профилю проекта, не выдумывай значения.

Это основной цикл разработки Vanessa: сначала запускай один целевой feature или
сценарий с реальным фильтром, анализируй артефакты, исправляй файл и повторяй тот же
запуск. Vanessa MCP не является обязательным промежуточным runner. Используй его
только для точечного поиска шага или инспекции элемента, когда отчёта `v8_runner`,
кода формы и метаданных недостаточно.

Не подтверждай PASS выполнением отдельных шагов в уже открытом TestClient. После
диагностики всегда перезапускай целевой сценарий целиком через `v8_runner`.

## Отдельная сборка

`build_project` используй когда:

- пользователь просит только сборку;
- тестовый модуль ещё нельзя запускать;
- выполняется первичная настройка/диагностика source-set;
- нужно локально проверить сборку конкретного source-set без теста.

Параметры:

```text
build_project
  sourceSet: <имя из v8project.yaml>   # опционально
  fullRebuild: false                  # опционально
```

После успешного `run_module_tests` не запускай `build_project` отдельно: build уже был prerequisite теста.

## Когда нужен CLI

### Намеренный `--no-build`

MCP `run_module_tests` не предоставляет режим Skip Build; он всегда работает с build prerequisite.

Для специально подготовленной базы:

```powershell
v8-runner.exe test --no-build yaxunit module <Модуль>
```

Не используй `--no-build` как обычный цикл разработки после изменения исходников.

### Свойства тестового расширения

Текущая MCP-поверхность не публикует команду `extensions`, поэтому после первичной загрузки тестового extension source-set при необходимости:

```powershell
v8-runner.exe extensions --name <TestSourceSet>
```

Имя бери из `v8project.yaml`.

### CLI fallback тестов

Когда MCP недоступен:

```powershell
v8-runner.exe test yaxunit module <РеальноеИмяМодуля>
v8-runner.exe test yaxunit all
v8-runner.exe test va
```

## Stdio MCP для локального Codex

Для локального проекта предпочтителен stdio transport: Codex сам запускает процесс v8-runner, отдельный HTTP-порт и постоянно запущенный MCP-сервер не нужны.

Пример концепции конфигурации Codex:

```toml
[mcp_servers.v8_runner]
enabled = true
command = "v8-runner.exe"
args = [
    "--config",
    "<ABSOLUTE_PATH_TO_PROJECT>\\v8project.yaml",
    "mcp",
    "serve",
    "stdio"
]
startup_timeout_sec = 20
tool_timeout_sec = 1800
```

Не зашивай конкретный путь `114`/`115` в skill; это проектная настройка `.codex/config.toml`.

## Артефакты и результат

MCP возвращает структурированный результат выполнения и при ошибках может указывать diagnostics/artifacts. Используй эти данные прежде, чем строить догадки.

При CLI-прогоне каталог обычно имеет вид:

```text
build/temp/yaxunit/runs/<run-id>/
```

Ключевые файлы:

- `config.json` — фактически переданный фильтр;
- `runner.log` — лог YAxUnit;
- `report.xml` — JUnit;
- `enterprise.out.log` — запуск платформы.

## `junit_empty`

Если получен `junit_empty`, не делай вывод, что business-тест упал.

Если `runner.log` содержит `Загрузка сценариев завершена. 0 сценариев.`, проверь:

1. правильное ли реальное имя передано в `moduleName` / `module`;
2. существует ли такой общий модуль;
3. есть ли `ИсполняемыеСценарии() Экспорт`;
4. подходит ли контекст общего модуля;
5. загружено и активно ли тестовое расширение;
6. не отфильтрован ли модуль ошибочным фильтром.

Если `report.xml` содержит `<testsuites>` и свойства окружения, но нет `<testcase>`, это отсутствие выполненных тестов, а не business FAIL.

## Реальное имя модуля

Перед `run_module_tests` или CLI `module <name>` найди имя среди `tests/src/CommonModules/` или фактического пути source-set. Не выводи имя тестового модуля только из человеческого описания задачи.

Ошибка вида «0 сценариев» после запуска не является основанием сразу менять production-код: сначала перепроверь имя тестового модуля.

## Версия и live schema

Live schema MCP-инструмента и `v8-runner.exe ... --help` приоритетнее этого файла, если установленная версия отличается.

Перед неизвестной CLI-опцией:

```powershell
v8-runner.exe test --help
```

Не собирай вручную запуск `1cv8.exe`, если v8-runner уже покрывает сценарий.
