import os
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
db_path = os.path.join(os.path.dirname(__file__), "data", "library.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/")
def home():
    """Render the home page with books based on search query."""
    search_query = request.args.get("query", "")
    if search_query:
        # searching for books where title or isbn matches the search query
        books = Book.query.filter(
            Book.title.ilike(f"%{search_query}%") | Book.isbn.ilike(f"%{search_query}%")
        ).all()
    else:
        books = Book.query.all()

    return render_template("home.html", books=books)


@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    """Delete a book and possibly its author if no other books by the author exist."""
    book = Book.query.get_or_404(book_id)

    # Delete the book
    db.session.delete(book)
    db.session.commit()

    # Check if the author has other books
    author = Author.query.filter_by(id=book.author_id).first()
    if author and not Book.query.filter_by(author_id=author.id).first():
        db.session.delete(author)
        db.session.commit()

    flash("Book successfully deleted!")
    return redirect(url_for("home"))


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    """Add a new author to the database."""
    if request.method == "POST":
        author_name = request.form["author_name"]
        birth_date = request.form["birth_date"]
        date_of_death = request.form["date_of_death"]

        new_author = Author(
            author_name=author_name, birth_date=birth_date, date_of_death=date_of_death
        )
        db.session.add(new_author)
        db.session.commit()

        return render_template("add_author.html", success=True)

    return render_template("add_author.html", success=False)


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    """Add a new book to the database."""
    if request.method == "POST":
        isbn = request.form["isbn"]
        title = request.form["title"]
        publication_year = request.form["publication_year"]
        author_id = request.form["author_id"]

        # Create a new Book object with the selected author
        new_book = Book(
            isbn=isbn,
            title=title,
            publication_year=publication_year,
            # author_id=author_id,
        )
        db.session.add(new_book)
        db.session.commit()

        flash("Book successfully added!")
        return redirect(url_for("home"))

    # Fetch all authors to populate the dropdown
    authors = Author.query.all()
    return render_template("add_book.html", authors=authors, success=False)


@app.route("/sort_books/<sort_by>")
def sort_books(sort_by):
    """Sort and render books based on the specified sorting criterion."""
    if sort_by == "title":
        books = Book.query.order_by(Book.title).all()
    elif sort_by == "author":
        books = Book.query.join(Author).order_by(Author.author_name).all()
    else:
        books = Book.query.all()
    return render_template("home.html", books=books)


if __name__ == "__main__":
    app.run(debug=True)
