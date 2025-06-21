import os
import subprocess
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Папка со скриптами
SCRIPTS_DIR = "scripts"  # Измените, если ваши скрипты находятся в другом месте

def run_script(script_name):
    """Запускает скрипт Python."""
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    if not os.path.exists(script_path):
        logging.error(f"Скрипт {script_name} не найден в папке {SCRIPTS_DIR}")
        return False

    logging.info(f"Запуск скрипта: {script_name}")
    try:
        subprocess.run(["python3", script_path], check=True)
        logging.info(f"Скрипт {script_name} успешно выполнен")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка при выполнении скрипта {script_name}: {e}")
        return False

def main():
    """Запускает все скрипты в пайплайне последовательно."""
    logging.info("Начало выполнения пайплайна")

    # Список скриптов для запуска (в порядке выполнения пайплайна)
    scripts = [
        "run_prodigal.py",
        "run_hmmsearch.py",
        "parse_hmmsearch_hits.py",
        "extract_best_hit_seqs.py",
        "align_genes_mafft.py",
        "concatenate_alignments.py",
        "run_fasttree.py",
    ]

    for script in scripts:
        if not run_script(script):
            logging.error(f"Пайплайн остановлен из-за ошибки в скрипте {script}")
            return

    logging.info("Пайплайн успешно завершен")

if __name__ == "__main__":
    main()