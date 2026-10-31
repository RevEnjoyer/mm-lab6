"""
Скрипт автоматической сборки фоторедактора в исполняемый файл.

ЛР 4.2, вариант 1: базовая сборка PyInstaller с флагом --onefile.

Использование:
    python build.py             # финальная сборка (без консоли, --windowed)
    python build.py --debug     # отладочная сборка (с консолью)
"""

import os
import subprocess
import sys

# Имя приложения (и итогового файла) и главный файл проекта.
APP_NAME = 'PhotoEditor'
ENTRY_POINT = 'photo_editor.py'

# Модули, которые точно не нужны приложению: их исключение уменьшает размер.
# numpy исключать нельзя - он нужен OpenCV.
EXCLUDES = ['tkinter', 'matplotlib']

# Скрытые импорты: модули, которые PyInstaller может не найти сам.
HIDDEN_IMPORTS = ['cv2', 'PyQt6']


def get_build_command(debug=False):
    """Сформировать команду PyInstaller (список аргументов, не строка)."""
    # sys.executable + "-m PyInstaller" запускает PyInstaller из текущего
    # (виртуального) окружения, а не из глобального.
    command = [sys.executable, '-m', 'PyInstaller']

    command += ['--onefile']                 # один файл вместо папки
    command += ['--name', APP_NAME]          # имя .exe
    command += ['--noconfirm', '--clean']    # перезаписывать dist/ и очищать кэш

    if not debug:
        # Без консольного окна: для финальной GUI-версии.
        command += ['--windowed']

    for module in HIDDEN_IMPORTS:
        command += ['--hidden-import', module]
    for module in EXCLUDES:
        command += ['--exclude-module', module]

    # Иконка добавляется, только если файл icon.ico лежит рядом (вариант 2).
    if os.path.exists('icon.ico'):
        command += ['--icon', 'icon.ico']

    command.append(ENTRY_POINT)
    return command


def run_build(debug=False):
    """Запустить процесс сборки. Возвращает True при успехе."""
    command = get_build_command(debug)
    print('Команда сборки:')
    print('  ' + ' '.join(command))

    try:
        # check=True: при ненулевом коде возврата будет исключение.
        subprocess.run(command, check=True)
    except FileNotFoundError:
        print('Ошибка: не найден Python/PyInstaller. '
              'Установите: pip install pyinstaller')
        return False
    except subprocess.CalledProcessError as error:
        print(f'Ошибка сборки, код возврата: {error.returncode}')
        return False
    return True


def test_executable():
    """Проверить собранный файл: существует ли он и какого он размера."""
    # На Windows результат - dist/PhotoEditor.exe, на Linux/macOS - без .exe.
    exe_name = APP_NAME + ('.exe' if sys.platform == 'win32' else '')
    exe_path = os.path.join('dist', exe_name)

    if not os.path.isfile(exe_path):
        print(f'Файл {exe_path} не найден')
        return False

    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print('Дистрибутив:')
    print(f'  файл:   {exe_path}')
    print(f'  размер: {size_mb:.1f} МБ')
    return True


if __name__ == '__main__':
    debug_mode = '--debug' in sys.argv[1:]

    print('Начинаю сборку...')
    if not run_build(debug_mode):
        sys.exit(1)
    if not test_executable():
        sys.exit(1)
    print('Сборка завершена!')
