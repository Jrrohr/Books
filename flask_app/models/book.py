from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:
    def __init__(self , data ):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorited = []

    @classmethod
    def save( cls , data ):
        query = "INSERT INTO books ( title , num_of_pages , created_at , updated_at ) VALUES (%(title)s,%(num_of_pages)s,NOW(),NOW());"
        return connectToMySQL('books_schema').query_db( query, data)

    @classmethod
    def get_all_books(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL('books_schema').query_db(query)
        # Create an empty list to append our instances of dojos
        books = []
        for book in results:
            books.append( cls(book) )
        return books

    @classmethod
    def show_book(cls, data):
        query = "SELECT * FROM books WHERE id = %(id)s;"
        result = connectToMySQL('books_schema').query_db(query,data)
        return cls(result[0])

    @classmethod
    def get_all_favorited(cls, data):
        query = "SELECT * FROM books LEFT JOIN favorites ON favorites.book_id = books.id LEFT JOIN authors ON favorites.author_id = authors.id WHERE books.id = %(id)s;"
        results = connectToMySQL('books_schema').query_db(query,data)
        # Create an empty list to append our instances of ninjas
        book = cls(results[0])
        for row in results:
            author_data = {
                'id' : row['authors.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'created_at' : row['authors.created_at'],
                'updated_at' : row['authors.updated_at'],
            }
            book.favorited.append( author.Author( author_data ) )
        return book