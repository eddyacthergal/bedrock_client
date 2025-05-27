# Bedrock Client Project

Ce projet est un client pour Amazon Bedrock.

## Développement

### Prérequis

- Python 3.11+
- [uv](https://github.com/astral-sh/uv): Un installateur et résolveur de paquets Python extrêmement rapide.

Installez `uv` en suivant les instructions de son dépôt.

### Installation des dépendances

Pour installer les dépendances du projet avec `uv`, exécutez :

```bash
uv sync
```

### Configuration des variables d'environnement AWS (Développement)

Avant de démarrer l'application en mode développement, assurez-vous d'avoir configuré vos informations d'identification AWS. Vous pouvez le faire en exportant les variables d'environnement suivantes dans votre terminal :

```bash
export AWS_ACCESS_KEY_ID="your_access_key_id"
export AWS_SECRET_ACCESS_KEY="your_secret_access_key"
```

Remplacez les valeurs `your_access_key_id`, et `your_secret_access_key` par vos propres informations.

### Démarrer le projet en mode développement

Pour démarrer l'application FastAPI en mode développement (avec rechargement automatique sur les modifications), utilisez `uv` pour exécuter la commande `fastapi dev` :

```bash
uv run fastapi dev
```

L'application sera accessible à l'adresse `http://localhost:8000`.

### Documentation API (Swagger UI)

Une fois l'application démarrée en mode développement, la documentation OpenAPI interactive (Swagger UI) est disponible à l'adresse :

[http://localhost:8000/docs](http://:8000/docs)

Vous pouvez utiliser cette interface pour visualiser et tester les différents endpoints de l'API.

## Docker

### Construire l'image Docker

Pour construire l'image Docker du projet, exécutez la commande suivante à la racine du projet (où se trouve le `Dockerfile`) :

```bash
docker build -t bedrock-client-app .
```

### Démarrer le conteneur Docker

Pour démarrer un conteneur à partir de l'image construite :

```bash
docker run -p 8080:8080 --name bedrock-app bedrock-client-app
```

L'application sera accessible à l'adresse `http://localhost:8080`.

Une fois l'application démarrée via Docker, la documentation OpenAPI interactive (Swagger UI) est disponible à l'adresse :

[http://localhost:8080/docs](http://localhost:8080/docs)

Vous pouvez utiliser cette interface pour visualiser et tester les différents endpoints de l'API.

Pour passer les variables d'environnement AWS nécessaires au client Bedrock :

```bash
docker run -p 8080:8080 --name bedrock-app \
  -e AWS_ACCESS_KEY_ID="your_access_key_id" \
  -e AWS_SECRET_ACCESS_KEY="your_secret_access_key" \
  bedrock-client-app
```

Remplacez les valeurs `your_access_key_id`, et `your_secret_access_key` par vos informations d'identification AWS.

## Docker Compose

Pour une gestion plus facile des conteneurs et des variables d'environnement, un fichier `docker-compose.yml` est fourni. Voir la section suivante.
