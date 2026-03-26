#Goal: Read SSQL -> connect to database -> execute SQL -> create tables

from pathlib import Path
import sqlite3

def main() -> None: #None means that the function returns nothing
    #Path to build path to project root (powerlifting-ml/), this structure enables script 
    #to work no matter where it is run from
    project_root = Path(__file__).resolve().parents[2] 
    db_path = project_root / "powerlifting.db"
    schema_path = project_root / "sql" / "schema.sql"

    #open SQL file and reads everything into a string
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()
  
    #create a database file automatically and connect it to the database 
    conn = sqlite3.connect(db_path) #This is the database
    try:
        conn.executescript(schema_sql) #runs all the multiple SQL statements 
        conn.commit() #writes everything permanently to the database
        print(f"Database initialized successfully at: {db_path}")

    # Always close connection
    finally:
        conn.close()
#run the script
if __name__ == "__main__":
    main()