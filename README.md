

# Rag quiz 

Web app to generate & schedule flashcards based on knowledge base. 




# Fundemental ideas

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

