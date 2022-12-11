from flask_app import app
from flask import render_template,redirect,request
from flask_app.models.author import Author
from flask_app.models.book import Book

# @app.route("/")
# def index():
#     return render_template("index.html")

@app.route("/authors")
def read_all_authors():
    # call the get all classmethod to get all authors
    authors = Author.get_all_authors()
    return render_template("authors.html", authors=authors)

@app.route('/create/author', methods=["POST"])
def create_author():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
    }
    # We pass the data dictionary into the save method from the Dojo class.
    new_author_id = Author.save(data)
    return redirect('/authors/' + str(new_author_id))


@app.route("/authors/<int:id>")
def show_author_favorites(id):
    data ={ 
        "id":id
    }
    author=Author.get_all_favorites_for_author(data)
    books=Book.get_all_books()
    return render_template("single_author.html", author=author, books=books)

@app.route("/add/book", methods=["POST"])
def add_book():
    data ={ 
        "book_id": request.form['book_id'],
        "author_id" : request.form['author_id']
    }
    Author.add_favorite(data)
    return redirect('/authors/' + str(request.form['author_id']))