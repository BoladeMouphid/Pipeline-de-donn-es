# Pipeline-de-donn-es

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)]()
[![Airflow](https://img.shields.io/badge/Apache%20Airflow-2.7-red)]()
[![Docker](https://img.shields.io/badge/Docker-Compose-blue)]()

---

## 📋 À propos du projet

Ce projet présente un pipeline de données ETL pour automatiser le traitement des données financiers dans le cadre de la supervision prudentielle des institutions de microfinance de la Direction de la Reglementation et de la Supervision des Systemes Financiers decentralisés (DRS-SFD).

**Contexte :** Mémoire de fin d'études - ESMT Dakar (2025) pour l'obtention du diplome d'Ingenieur de conception des Telecommunications spécialisé en Ingenierie des données et Intelligence Artificielle 

**Problématique :** La DRS SFD s'appuie sur un systeme d'alerte precoce (SAP) pour la supervision financiere des institutions de microfinance mais le système existant repose sur Excel avec des traitements manuels, entraînant :
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

**2- CREATION DES REPERTOIRES POUR AIRFLOW**
<img width="301" height="350" alt="WORKSPACE" src="https://github.com/user-attachments/assets/081ead6b-4fae-4dfa-818a-eca20c71a4b0" />

L’espace de travail est constitué d’un repertoire principal Airflow-docker contenant plusieurs sous repertoires. Cette organisation favorise une meilleure lisibilité du pipeline automatisé, une traçabilité complète des traitements ainsi qu’une évolutivité de la solution. Chaque composant peut être modifié ou amélioré indépendamment des autres, sans impacter l’ensemble du système.

**Rôle des principaux répertoires**

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


Une fois l'implementation des scripts terminée on se connecte a l'ui d'apache airflow et executer notre DAG

**Commande pour demarrer les services airflow** 

1- initialiser airflow

docker compose up airflow-init

2-Demarrer tous les services d'airflow

sudo docker compose up -d

3-Verifier l'etat des services (tous les services doivent etre en mode "up")

sudo docker compose ps 

4-Acceder a l'interface d'airflow

URL : http://localhost:8080
Login / mot de passe : airflow / airflow

5- Execution du DAG  
La figure ci-dessous illustre l’exécution du DAG du pipeline automatisé déployé pour le traitement des données du système d’alerte précoce de la DRS, montrant que l’ensemble des tâches a été exécuté avec succès, validant la robustesse et la fiabilité du pipeline automatisé.

<img width="945" height="501" alt="image" src="https://github.com/user-attachments/assets/e554c4c1-4cbf-43d8-8827-691a52952dbc" />






**INTERFACE UTILISATEUR**

L'interface utilisateur a été developpée a l'aide de streamlit pour permettre une utilisation facile de la solution proposéé. Cette interface permet a l'utilisateur de :

1- Charger le fichier source

2-Lancer le traitement des donneés automatisés via le declenchement du DAG 

3-Visualiser les dashboards 

4- Telecharger les fichiers generés 

5- Filter les differentes institutions de micrifiance en fonction de leurs situation par rapports aux differents indicateurs financiers.


**APPERCU DE L'INTERFACE UTILISATEUR**


<img width="957" height="481" alt="PLATEFORME DRS SFD GENERALE " src="https://github.com/user-attachments/assets/0ae88920-b8ba-4dad-9daa-df3834d62434" />



Note: Comme vous povez le constater sur l'immage , l'utilisateur charge un fichier "ratios" constituant le fichier souce en suite une fois le fichier chargé , il lance le traitement au cous duquel il sera redirigé automatiquement vers l'UI d'airflow pour declencher le DAG et une fois le DAG executé , il peut visualiser les graphiques analytiques(selectionner les differentes piriodes qu'il désire visualiser)  puis telecharger l'ensemble des fichers génerés sous format archive ZIP puis ensuite effectuer des filtres sur les differents institutions de microfinances en fonction de leurs situatuions par rappport aux differents indicateurs financiers.

NB: Pour des raisions de confidentialité je ne pourrai pas mettre a disposition le code source de ce projet

Merci pour la comprehension !!!



















 














