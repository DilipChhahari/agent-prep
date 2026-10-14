# agent-prep

A small shop project built step by step to learn backend development and the basics of AI agents. It grew from plain Python classes into a REST API, an AI agent, and a containerized app running on Kubernetes.

## What's in it

- **Python and OOP**: `Product`, `Cart` and `DigitalProduct` classes (`product.py`).
- **Database**: SQLite, with the tables in `schema.sql` and starter data in `seed.sql`.
- **REST API**: a FastAPI app (`main.py`) with full CRUD for products.
- **AI agent**: an agent loop (`agent.py`, `tools.py`) that runs on a local model through Ollama and decides which tool to call.
- **Docker**: a `Dockerfile` that packages the API with its database.
- **Kubernetes**: manifests in `k8s/` (ConfigMap, Deployment, Service) that run two copies of the API on minikube.

## API endpoints

| Method | Path | What it does |
|--------|------|--------------|
| GET | `/` | Home |
| GET | `/products` | List all products |
| POST | `/products` | Create a product |
| GET | `/products/{product_id}` | Get one product |
| PUT | `/products/{product_id}` | Update a product |
| DELETE | `/products/{product_id}` | Delete a product |

Interactive docs are at `/docs` when the API is running.

## Run it locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sqlite3 shop.db < schema.sql
sqlite3 shop.db < seed.sql
uvicorn main:app --reload
```

Then open http://127.0.0.1:8000/docs.

## Run the agent

Start the local model server in one terminal, then run the agent in another:

```bash
ollama serve
python agent.py
```

## Run with Docker

```bash
docker build -t shop-api .
docker run -d -p 8000:8000 --name shop-api-container shop-api
```

Stop it with `docker stop shop-api-container`.

## Run on Kubernetes (minikube)

```bash
minikube start --driver=docker
eval $(minikube docker-env)        # build inside minikube's Docker
docker build -t shop-api:1.0 .
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get pods
minikube service shop-api-service --url
```

Open the printed URL with `/docs` on the end. Stop the cluster with `minikube stop`.

Notes:
- The Deployment runs 2 replicas. If a pod is deleted, Kubernetes starts a replacement.
- `imagePullPolicy: Never` makes Kubernetes use the locally built image.
- Each pod has its own SQLite file, so data created in one pod is not shared with the other. A real deployment would use a shared database such as Postgres.
