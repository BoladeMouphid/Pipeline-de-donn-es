# FONCTION ASSURANT LE DECLENCHEMENT ET SUIVI DU DAG
import subprocess
from datetime import datetime

DAG_ID = "pca_pipeline_complet"

def trigger_dag():
    """Déclenche le DAG Airflow via WSL depuis Windows."""
    try:
        result = subprocess.run(
            [
                "wsl", "bash", "-c",
                f"cd /home/bolade/airflow-docker && docker compose exec -T airflow-scheduler airflow dags trigger {DAG_ID}"
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return {
                "success": True,
                "message": "Pipeline lancé avec succès!",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            return {
                "success": False,
                "message": f"Erreur: {result.stderr}"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Erreur: {str(e)}"
        }

def get_dag_status():
    try:
        result = subprocess.run(
            [
                "wsl", "bash", "-c",
                f"""
                cd /home/bolade/airflow-docker && \
                docker compose exec -T postgres psql \
                -U airflow -d airflow -t -c "
                SELECT state
                FROM dag_run
                WHERE dag_id='{DAG_ID}'
                ORDER BY logical_date DESC
                LIMIT 1;
                "
                """
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

        state = result.stdout.strip().lower()
        state = ''.join(state.split())

        # ⛔ NE JAMAIS considérer vide comme échec
        if not state:
            return {
                "status": "starting",
                "message": "⏳ Initialisation du pipeline..."
            }

        if state in ["queued", "running"]:
            return {
                "status": "running",
                "message": "🟡 Pipeline en cours d'exécution..."
            }

        if state == "success":
            return {
                "status": "success",
                "message": "✅ Pipeline terminé avec succès"
            }

        if state == "failed":
            return {
                "status": "failed",
                "message": "❌ Pipeline en échec"
            }

        # Tout autre état = en cours
        return {
            "status": "running",
            "message": f"⏳ Statut intermédiaire : {state}"
        }

    except Exception as e:
        # ⛔ ERREUR TECHNIQUE ≠ ÉCHEC DU DAG
        return {
            "status": "running",
            "message": "⏳ Vérification du statut..."
        }


def get_dag_history(limit=10):
    """Retourne l'historique des derniers DAG Runs."""
    try:
        result = subprocess.run(
            [
                "wsl", "bash", "-c",
                f"""
                cd /home/bolade/airflow-docker && \
                docker compose exec -T postgres psql \
                -U airflow -d airflow -F ',' -A -c "
                SELECT
                    run_id,
                    state,
                    logical_date,
                    start_date,
                    end_date,
                    ROUND(EXTRACT(EPOCH FROM (end_date - start_date))/60, 2)
                FROM dag_run
                WHERE dag_id='{DAG_ID}'
                ORDER BY logical_date DESC
                LIMIT {limit};
                "
                """
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0 or not result.stdout.strip():
            return []

        rows = result.stdout.strip().splitlines()
        history = []

        for r in rows:
            run_id, state, logical_date, start_date, end_date, duration = r.split(",")

            history.append({
                "Run ID": run_id,
                "Statut": state,
                "Date logique": logical_date,
                "Début": start_date,
                "Fin": end_date if end_date else "-",
                "Durée (min)": duration if duration else "-"
            })

        return history

    except Exception:
        return []

def get_dag_progress():
    """
    Retourne la progression du DAG en % basée sur les task_instance.
    Compatible Airflow 3.x
    """
    try:
        query = f"""
        WITH latest_run AS (
            SELECT dag_id, run_id
            FROM dag_run
            WHERE dag_id = '{DAG_ID}'
            ORDER BY logical_date DESC
            LIMIT 1
        )
        SELECT
            COUNT(*) AS total_tasks,
            COUNT(*) FILTER (WHERE state IN ('success', 'failed')) AS done_tasks,
            COUNT(*) FILTER (WHERE state = 'running') AS running_tasks
        FROM task_instance
        WHERE dag_id = '{DAG_ID}'
          AND run_id = (SELECT run_id FROM latest_run);
        """

        result = subprocess.run(
            [
                "wsl", "bash", "-c",
                f"""
                cd /home/bolade/airflow-docker && \
                docker compose exec -T postgres psql \
                -U airflow -d airflow -t -c "{query}"
                """
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            return {"progress": 0, "message": "Erreur DB"}

        # Résultat du type :  10 | 4 | 1
        values = result.stdout.strip().split("|")
        total = int(values[0])
        done = int(values[1])
        running = int(values[2])

        if total == 0:
            return {"progress": 0, "message": "Initialisation..."}

        progress = int((done / total) * 100)

        return {
            "progress": progress,
            "message": f"{done}/{total} tâches terminées"
        }

    except Exception as e:
        return {"progress": 0, "message": str(e)}


# Pour tester depuis la ligne de commande
if __name__ == "__main__":
    print("=== Test de déclenchement du DAG ===")
    result = trigger_dag()
    
    if result["success"]:
        print(f"✅ {result['message']}")
        print(f"⏰ {result['timestamp']}")
        if result.get('output'):
            print(f"Output: {result['output']}")
    else:
        print(f"❌ {result['message']}")
