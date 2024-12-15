from .connection import get_db_connection

def create_tables():
    try:
        # Establish a connection to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Enable foreign key constraints
        cursor.execute('PRAGMA foreign_keys = ON')

        # Create the authors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')

        # Create the magazines table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS magazines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL
            )
        ''')

        # Create the articles table with foreign keys referencing authors and magazines
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                author_id INTEGER,
                magazine_id INTEGER,
                FOREIGN KEY (author_id) REFERENCES authors (id),
                FOREIGN KEY (magazine_id) REFERENCES magazines (id)
            )
        ''')

        # Commit the changes to the database
        conn.commit()
        print('Tables created successfully.')

    except Exception as e:
        # Handle any errors that occur during table creation
        print(f'An error occurred while creating tables: {e}')

    finally:
        # Ensure the database connection is closed
        if conn:
            conn.close()