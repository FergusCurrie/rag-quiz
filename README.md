


`docker network create rag_quiz`

`poetry run python3 main.py`

poetry self add poetry-plugin-shell


Backend:
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload

Frontend:
cd frontend 
npm run dev