# ЛР 4.2 — Сборка и тестирование проекта

Дисциплина: «Проектирование и программирование мультимедийных приложений».
**Вариант 1** (номер в журнале 20: `20 % 5 + 1 = 1`) — базовая сборка.

Задача: упаковать фоторедактор из ЛР 3.1 в один исполняемый файл `PhotoEditor.exe`
(PyInstaller, флаг `--onefile`) и проверить его на системе без Python.

## Состав проекта

| Файл | Назначение |
| --- | --- |
| `photo_editor.py` | главное окно фоторедактора (точка входа) |
| `filters.py` | фильтры (оттенки серого) |
| `build.py` | скрипт автоматической сборки |
| `requirements.txt` | зависимости: PyQt6, opencv-python, pyinstaller |
| `.gitignore` | исключает `dist/`, `build/`, `*.spec`, `.venv/` |
| `INSTRUCTIONS.md` | пошаговая инструкция |

## Сборка

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

python build.py            # финальная сборка без консоли
python build.py --debug    # отладочная сборка с консолью
```

Результат: `dist\PhotoEditor.exe`.

## Эквивалентная ручная команда

```bash
python -m PyInstaller --onefile --windowed --name PhotoEditor photo_editor.py
```
