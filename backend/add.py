from connections import get_postgres_conn, get_postgres_db
from crud import create_concept, get_concept_by_name
from models import Base
from sqlalchemy import create_engine


def main():
    print('Running')
    # setup 
    engine = create_engine(get_postgres_conn())  # Create engine first
    db = next(get_postgres_db())  # Get session
    # Base.metadata.drop_all(engine) 
    Base.metadata.create_all(engine)

    running = True 
    while running: 
        inp = input('Press A to add concepts from txt. ')
        if inp.lower().strip() == 'a':

            with open('concepts.txt', 'r') as f:
                for line in f:
                    concept = line.strip()
                    if concept:  # Skip empty lines
                        # Check if concept already exists
                        existing_concept = get_concept_by_name(db, concept)
                        if existing_concept:
                            print(f"Skipping existing concept: {concept}")
                            continue
                            
                        print(f"Adding concept: {concept}")
                        result = create_concept(db, concept, user_created=True)
            running = False
            break

        running = False 

if __name__ == "__main__":
    main()

