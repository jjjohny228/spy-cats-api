## **Installation**

Usage

1. Clone the repository:

```python
https://github.com/jjjohny228/spy-cats-api

```

1. Go to the project directory:

```python
cd spy-cats-api

```

1. Create .env file in project. Use .env.exaple as a template.
2. Run docker compose file

```python
docker compose up --build

```

## **API Endpoints:**
https://app.getpostman.com/join-team?invite_code=7230813e202e4f611b769a32bee222b7&target_code=0c72604cbce63f521fa0017f62cae6e1

**Cats:**

- GET `/api/cats/`: List all cats
- GET `/api/cats/{id}/`: Get single cat
- POST `/api/cats/`: Create cat
- PATCH `/api/cats/{id}/`: Update cat salary
- DELETE `/api/cats/{id}/`: Delete cat

**Missions**

- GET `/api/missions/`: List all missions
- GET `/api/missions/{id}/`: Get single mission
- POST `/api/missions/`: Create mission with targets
- POST `/api/missions/{id}/assign_cat/`: Assign cat to mission
- POST `/api/missions/{id}/update_target/`: Update target
- DELETE `/api/missions/{id}/`: Delete mission