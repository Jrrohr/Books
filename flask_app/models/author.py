from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class Author:
    def __init__(self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorites = []

    @classmethod
    def save( cls , data ):
        query = "INSERT INTO authors ( first_name , last_name , created_at , updated_at ) VALUES (%(first_name)s,%(last_name)s,NOW(),NOW());"
        return connectToMySQL('books_schema').query_db( query, data)

    @classmethod
    def get_all_authors(cls):
        query = "SELECT * FROM authors;"
        results = connectToMySQL('books_schema').query_db(query)
        # Create an empty list to append our instances of dojos
        authors = []
        for author in results:
            authors.append( cls(author) )
        return authors

    @classmethod
    def show_author(cls, data):
        query = "SELECT * FROM authors WHERE id = %(id)s;"
        result = connectToMySQL('books_schema').query_db(query,data)
        return cls(result[0])

    @classmethod
    def get_all_favorites_for_author(cls, data):
        query = "SELECT * FROM authors LEFT JOIN favorites ON favorites.author_id = authors.id LEFT JOIN books ON favorites.book_id = books.id WHERE authors.id = %(id)s;"
        results = connectToMySQL('books_schema').query_db(query,data)
        # Create an empty list to append our instances of ninjas
        author = cls(results[0])
        for row in results:
            book_data = {
                'id' : row['books.id'],
                'title' : row['title'],
                'num_of_pages' : row['num_of_pages'],
                'created_at' : row['books.created_at'],
                'updated_at' : row['books.updated_at'],
            }
            author.favorites.append( book.Book( book_data ) )
        return author

    @classmethod
    def add_favorite(cls, data):
        query = "INSERT INTO favorites (book_id, author_id) VALUES (%(book_id)s,%(author_id)s)"
        return connectToMySQL('books_schema').query_db( query, data)