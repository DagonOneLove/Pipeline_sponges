import subprocess
import os
import sys

# Получаем путь к текущему скрипту
script_dir = os.path.dirname(os.path.abspath(__file__))

# Абсолютные пути к входному и выходному файлу
input_file = os.path.abspath(os.path.join(script_dir, "../results/concatenated/supermatrix.faa"))
output_file = os.path.abspath(os.path.join(script_dir, "../results/trees/tree.nwk"))
output_dir = os.path.dirname(output_file)

# Проверяем, существует ли входной файл
if not os.path.exists(input_file):
    print(f"Ошибка: файл не найден: {input_file}")
    sys.exit(1)

# Создаём выходную папку, если нужно
os.makedirs(output_dir, exist_ok=True)

# Команда FastTree
cmd = ["FastTree", "-lg", "-gamma", input_file]

print("Запуск FastTree...")
try:
    with open(output_file, "w") as out:
        subprocess.run(cmd, stdout=out, stderr=subprocess.PIPE, check=True)
    print(f"Готово! Дерево сохранено в: {output_file}")
except subprocess.CalledProcessError as e:
    print("FastTree завершился с ошибкой.")
    print("Код возврата:", e.returncode)
    print("Сообщение об ошибке:")
    print(e.stderr.decode())
