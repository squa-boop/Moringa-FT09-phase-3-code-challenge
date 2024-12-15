# Import the get_db_connection function from the database.connection module
from database.connection import get_db_connection

# Define the Author class
class Author:
    # Define the constructor (__init__) method to initialize Author instances
    def __init__(self, id, name=None):
        # Assign the id attribute
        self._id = id
        # If the name is provided, assign it directly
        if name is not None:
            self._name = name
        else:
            self._name = None

    # Define a property for the id attribute
    @property
    def id(self):
        return self._id
    
    # Define a property for the name attribute
    @property
    def name(self):
        # If name is not set, fetch it from the database
        if self._name is None:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM authors WHERE id = ?', (self._id,))
            result = cursor.fetchone()
            conn.close()
            if result:
                self._name = result[0]
            else:
                raise ValueError("Name not found in database")
        return self._name
    
    # Define a setter method for the name property
    @name.setter
    def name(self, value):
        # Check if the value is a string
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        # Check if the length of the name is greater than 0
        if len(value) == 0:
            raise ValueError("Name must be longer than 0 characters")
        # Set the name attribute
        self._name = value
    
    # Define a method to fetch articles associated with the author
    def articles(self):
        # Import the Article class
        from models.article import Article
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE author_id = ?', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        # Ensure the result is returned as Article instances
        return [Article(article[0], article[1], article[2], article[3], article[4]) for article in articles]
    
    # Define a method to fetch magazines associated with the author
    def magazines(self):
        # Import the Magazine class
        from models.magazine import Magazine
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT magazines.id, magazines.name, magazines.category 
            FROM magazines
            INNER JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        ''', (self._id,))
        magazines = cursor.fetchall()
        conn.close()
        # Ensure the result is returned as Magazine instances
        return [Magazine(magazine[0], magazine[1], magazine[2]) for magazine in magazines]

    # Define the string representation (__repr__) method for Author instances
    def __repr__(self):
        # Return a string representation of the Author object
        return f'<Author {self.name}>'
