


`docker network create rag_quiz`

`poetry run python3 main.py`

poetry self add poetry-plugin-shell


Backend:
uvicorn backend.app:app --host 0.0.0.0 --port 8087 --reload

Frontend:
cd frontend 
npm run dev

# Fundemental ideas

- Hallucinations are a feature (critical thinking)
- 

Other thoughts 
- Anki is not a good tool. It lacks:
    - context
    - generalised cards 
    - too expensive to add 
    - no growth (cards should be added)


# Research 
Optimizing Spaced Repetition Schedule by Capturing the Dynamics of Memory
Jingyong Su , Junyao Ye , Liqiang Nie , Senior Member, IEEE, Yilong Cao , and Yongyong Chen


# Alembic 

1. alembic init migrations 

1. alembic revision -m "add time_taken to reviews"
    - alembic revision --autogenerate -m ""
2. alembic upgrade head

If things go wrong: 

Go back one upgrade: 
1. alembic downgrade -1 
2. delete migration file 
3. alembic history # checks on old version now 
4. alembic current # get <revision_id> of new head 
5. alembic stamp <revision_id> # set database to current 