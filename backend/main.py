from connections import get_postgres_db, get_postgres_conn
from sqlalchemy import text
from models import Base
from sqlalchemy import create_engine

def test_postgres_connection(db):
    try:
        # Query to get PostgreSQL version and current database name
        query = text("""
            SELECT version() as version, 
                   current_database() as database,
                   current_user as user;
        """)
        
        result = db.execute(query).first()
        
        print("Database connection successful!")
        print(f"PostgreSQL Version: {result.version}")
        print(f"Current Database: {result.database}")
        print(f"Current User: {result.user}")
        
        return True
    except Exception as e:
        print(f"Database connection failed: {str(e)}")
        return False


def list_databases(db):
    try:
        # Query to list all databases
        query = text("""
            SELECT datname FROM pg_database 
            WHERE datistemplate = false;
        """)
        
        results = db.execute(query).fetchall()
        
        print("\nAvailable databases:")
        rag_db_exists = False
        for result in results:
            print(f"- {result.datname}")
            if result.datname == 'rag_llm_db':
                rag_db_exists = True
        
        if rag_db_exists:
            print("\n'rag_llm_db' database found!")
        else:
            print("\nWarning: 'rag_llm_db' database not found!")
        
        return True
    except Exception as e:
        print(f"Failed to list databases: {str(e)}")
        return False

def list_tables(db):
    try:
        # Query to list all tables in the current schema
        query = text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        results = db.execute(query).fetchall()
        
        print("\nAvailable tables:")
        for result in results:
            print(f"- {result.table_name}")
        
        return True
    except Exception as e:
        print(f"Failed to list tables: {str(e)}")
        return False

if __name__ == "__main__":
    print('Running')
    engine = create_engine(get_postgres_conn())  # Create engine first
    db = next(get_postgres_db())  # Get session
    list_databases(db)

    # Change this line to use engine instead of db session
    Base.metadata.create_all(engine)

    list_tables(db)