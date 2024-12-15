from database.connection import get_db, engine
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    # Create the tables if they do not exist
    from database.setup import create_tables
    create_tables()

    # Collect user input (optional, can be used alongside sample data)
    author_name = input("Enter author's name: ")  # User input for author name
    magazine_name = input("Enter magazine name: ")  # User input for magazine name
    magazine_category = input("Enter magazine category: ")  # User input for magazine category
    article_title = input("Enter article title: ")  # User input for article title
    article_content = input("Enter article content: ")  # User input for article content

    # Sample data for testing (with your provided values)
    authors_data = ["Blessed", "John Doe", "Jane Smith"]
    magazines_data = [("National Geographic Science", "Science"), ("Nature Geography", "Geography")]
    article_data = ("Exploring the Secrets of the Ocean", "This article explores the mysteries of the ocean.")

    # Connect to the database
    db = next(get_db())

    # Create authors using the SQLAlchemy ORM (from the sample authors data)
    authors = []
    for author_name in authors_data:
        author = Author(name=author_name)
        db.add(author)
        db.commit()
        db.refresh(author)  # Refresh to get the author's id
        authors.append(author)  # Keep track of created authors for later use

    # Create magazines using the SQLAlchemy ORM (from the sample magazines data)
    magazines = []
    for magazine_name, magazine_category in magazines_data:
        magazine = Magazine(name=magazine_name, category=magazine_category)
        db.add(magazine)
        db.commit()
        db.refresh(magazine)  # Refresh to get the magazine's id
        magazines.append(magazine)  # Keep track of created magazines for later use

    # Create an article using the SQLAlchemy ORM (from the sample article data)
    article_title, article_content = article_data
    # For simplicity, we'll associate the first author and first magazine with the article
    article = Article(title=article_title, content=article_content, author_id=authors[0].id, magazine_id=magazines[0].id)
    db.add(article)
    db.commit()

    # Query the database for inserted records using SQLAlchemy
    magazines = db.query(Magazine).all()
    authors = db.query(Author).all()
    articles = db.query(Article).all()

    # Display results
    print("\nMagazines:")
    for magazine in magazines:
        print(f"Magazine ID: {magazine.id}, Name: {magazine.name}, Category: {magazine.category}")

    print("\nAuthors:")
    for author in authors:
        print(f"Author ID: {author.id}, Name: {author.name}")

    print("\nArticles:")
    for article in articles:
        print(f"Article ID: {article.id}, Title: {article.title}, Content: {article.content}, Author ID: {article.author_id}, Magazine ID: {article.magazine_id}")

if __name__ == "__main__":
    main()
