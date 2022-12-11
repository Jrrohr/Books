from flask_app import app
from flask import render_template,redirect,request
from flask_app.models.author import Author
from flask_app.models.book import Book

# @app.route("/")
# def index():
#     return render_template("index.html")

@app.route("/books")
def read_all_books():
    # call the get all classmethod to get all books
    books = Book.get_all_books()
    return render_template("books.html", books=books)

@app.route('/create/book', methods=["POST"])
def create_book():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    data = {
        "title": request.form['title'],
        "num_of_pages": request.form['num_of_pages'],
    }
    # We pass the data dictionary into the save method from the Dojo class.
    new_book_id = Book.save(data)
    return redirect('/books')


@app.route("/books/<int:id>")
def show_book_authors(id):
    data ={ 
        "id":id
    }
    book=Book.get_all_favorited(data)
    authors=Author.get_all_authors()
    return render_template("single_book.html", authors=authors, book=book)

@app.route("/add/author", methods=["POST"])
def add_author():
    data ={ 
        "book_id": request.form['book_id'],
        "author_id" : request.form['author_id']
    }
    Author.add_favorite(data)
    return redirect('/books/' + str(request.form['book_id']))