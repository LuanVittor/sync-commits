#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime, timedelta, timezone

# Configurações do repositório pessoal
PERSONAL_REPO_DIR = os.path.dirname(os.path.abspath(__file__))

def create_commits(date, num_commits):
    # Navegar até o diretório do repositório pessoal
    os.chdir(PERSONAL_REPO_DIR)

    # Puxar as últimas mudanças
    subprocess.run(["git", "pull"])

    for i in range(num_commits):
        # Converter a data e horário para o fuso horário de Brasília
        brt = timezone(timedelta(hours=-3))
        commit_date = date.astimezone(brt).strftime("%Y-%m-%d %H:%M:%S %Z")

        # Criar um commit fictício
        with open("DUMMY_FILE.txt", "a") as f:
            f.write(f"Commit from script on {commit_date}\n")

        # Adicionar e comitar as mudanças
        subprocess.run(["git", "add", "DUMMY_FILE.txt"])
        subprocess.run(["git", "commit", "--date", date.strftime("%Y-%m-%dT%H:%M:%S"), "-m", f"Dummy commit {i + 1} to reflect enterprise commit on {commit_date}"])

    # Empurrar para o repositório pessoal
    subprocess.run(["git", "push", "origin", "main"])

if __name__ == "__main__":
    date_input = input("Enter the date for the commits (YYYY-MM-DD) or press Enter to use today: ")
    num_commits_input = input("Enter the number of commits for this date or press Enter to use 1: ")
    
    # Validar a data
    if not date_input:
        commit_date = datetime.now(timezone.utc)
    else:
        try:
            commit_date = datetime.strptime(date_input, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
            exit(1)

    # Validar o número de commits
    if not num_commits_input:
        num_commits = 1
    else:
        try:
            num_commits = int(num_commits_input)
        except ValueError:
            print("Invalid number format. Please enter an integer.")
            exit(1)
    
    # Chamar a função para criar commits
    create_commits(commit_date, num_commits)
    print(f"Successfully created {num_commits} commits for {commit_date.astimezone(timezone(timedelta(hours=-3))).strftime('%Y-%m-%d %H:%M:%S %Z')}.")
