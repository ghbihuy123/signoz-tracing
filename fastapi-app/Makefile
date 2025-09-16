run-api:
	export PATH="./api/.venv/bin:$PATH"
	python -m uvicorn api.app:app --host 0.0.0.0 --port 8000

run-worker:
	export PATH="./worker/.venv/bin:$PATH"
	python -m celery -A worker.celery_app.celery_app worker --loglevel=info -Q default

build-api:
	docker build -f ./api/Dockerfile -t computer-api:latest .

build-worker:
	docker build -f ./worker/Dockerfile -t computer-worker:latest .
