
import subprocess
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("logs/pipeline.log")
DBT_PROJECT_DIR = "dataops_dbt"
DBT_PROFILES_DIR = str(Path.home() / ".dbt")

def log(message):
    LOG_FILE.parent.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    print(full_message)
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(full_message + "\n")

def run_command(command, step_name):
    log(f"START : {step_name}")
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    if result.stdout:
        log(result.stdout)
    if result.stderr:
        log(result.stderr)
    if result.returncode != 0:
        log(f"ERROR : {step_name}")
        raise Exception(f"Pipeline failed at : {step_name}")
    log(f"SUCCESS : {step_name}")

def main():
    log("PIPELINE STARTED")
    
    # Étape 1 : Upload vers l'émulateur Azurite (chemin direct sans préfixe)
    run_command("python scripts/upload_blob.py", "UPLOAD BLOB")
    
    # Étape 2 : Chargement vers SQLite staging (chemin direct sans préfixe)
    run_command("python scripts/load_blob_to_sql.py", "LOAD SQLITE")
    
    # Étape 3 : Transformation avec dbt
    run_command(f"dbt run --project-dir {DBT_PROJECT_DIR} --profiles-dir '{DBT_PROFILES_DIR}'", "DBT RUN")
    
    # Étape 4 : Validation de la qualité avec dbt
    run_command(f"dbt test --project-dir {DBT_PROJECT_DIR} --profiles-dir '{DBT_PROFILES_DIR}'", "DBT TEST")
    
    log("PIPELINE FINISHED")

if __name__ == "__main__":
    main()