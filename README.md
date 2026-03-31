# Pipeline-de-donn-es

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)]()
[![Airflow](https://img.shields.io/badge/Apache%20Airflow-2.7-red)]()
[![Docker](https://img.shields.io/badge/Docker-Compose-blue)]()

---

## 📋 À propos du projet

Ce projet présente un pipeline de données ETL pour automatiser le traitement des données financiers dans le cadre de la supervision prudentielle des institutions de microfinance de la Direction de la Reglementation et de la Supervision des Systemes Financiers decentralisés (DRS-SFD).

**Contexte :** Mémoire de fin d'études - ESMT Dakar (2025) pour l'obtention du diplome d'Ingenieur de conception des Telecommunications spécialisé en Ingenierie des données et Intelligence Artificielle 

**Problématique :** La DRS SFD s'appuie sur un systeme d'alerte precoce (SAP) pour la supervision financiere des instittions de microfinance mais le système existant repose sur Excel avec des traitements manuels, entraînant :
- Risque élevé d'erreurs
- Temps de traitement long
- Absence de traçabilité
  

**Solution :** Pipeline ETL pour automatiser le traitement des données du systeme d'alerte precoce.

**Outils technologiques utilisés**

**Apache Airflow**: Orchestrateur du flux ETL

**Docker**: Conteunerisation d'apache airflow 

**Python**: Moteur de traitement des données

**PostgreSQL**: Systeme de stockage des données 

**Streamlit**: Visualisation interactive et interface utilisateur 

**MISE EN OEUVRE DE LA SOLUTION**

**1- INSTALLATIONS ET PREREQUIS**  
-Docker,

-docker compose,

-python 3.10+,

-PostgreSQL,

-Une distribution linux sous windows comme environnement de travail (Ubuntu, WSL2, etc...).

**2- CREATION DES REPERTOIRE POUR AIRFLOW**
<img width="301" height="350" alt="WORKSPACE" src="https://github.com/user-attachments/assets/081ead6b-4fae-4dfa-818a-eca20c71a4b0" />

L’espace de travail est constitué d’un repertoire principal Airflow-docker contenant plusieurs sous repertoires. Cette organisation favorise une meilleure lisibilité du pipeline automatisé, une traçabilité complète des traitements ainsi qu’une évolutivité de la solution. Chaque composant peut être modifié ou amélioré indépendamment des autres, sans impacter l’ensemble du système.

Rôle des principaux répertoires

•	dags/
Ce répertoire contient les DAGs Apache Airflow. Le fichier pca_pipeline_complet définit l’enchaînement des tâches du pipeline , assurant l’orchestration complète du processus de traitement.

•	scripts/
Il regroupe les scripts Python implémentant la logique métier appliqué au differentes tables. 

•	data/input/
Ce dossier contient les fichiers de données sources, notamment les ratios financiers (ratios) et les fichiers de classification utilisés lors des traitements (classification).

•	data/output/
Il stocke les fichiers générés par le pipeline, tels que les scores et les tableaux de synthèse, qui constituent les livrables finaux destinés aux utilisateurs.

•	docker-compose.yaml
Ce fichier définit l’ensemble des services indispensables au fonctionnement d’Apache Airflow (scheduler, webserver, workers, base de données des métadonnées). Il garantit un déploiement cohérent et reproductible de l’environnement Airflow.

•	plugins/
Ce répertoire est destiné à contenir des composants personnalisés d’Apache Airflow, tels que des opérateurs, capteurs ou hooks spécifiques. Son utilisation permet d’étendre les fonctionnalités natives d’Airflow.

•	logs/
Le dossier logs centralise l’ensemble des journaux générés lors de l’exécution des tâches du pipeline. Il joue un rôle essentiel dans le suivi des traitements, la détection des erreurs et l’analyse des incidents techniques.

•	config/
Ce répertoire regroupe les fichiers de configuration du système, notamment les paramètres d’Airflow, les variables d’environnement et les éléments liés à la sécurité. 








 














