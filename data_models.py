from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "author"
    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(20))
    birth_date = db.Column(db.String(20))
    date_of_death = db.Column(db.String(20))

    def __repr__(self):
        return (
            f"<Author(id={self.id}, author='{self.author_name}', "
            f"birth_date='{self.birth_date}', date_of_death='{self.date_of_death}')>"
        )

    def __str__(self):
        return (
            f"Author: {self.author_name} "
            f"(Born: {self.birth_date}, Died: {self.date_of_death})"
        )


class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(30))
    title = db.Column(db.String)
    publication_year = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", backref="books")  #add relationship

    def __repr__(self):
        return (
            f"<Book(id={self.id}, isbn='{self.isbn}', title='{self.title}', "
            f"publication_year='{self.publication_year}', author_id='{self.author_id}')>"
        )

    def __str__(self):
        return (
            f"Book Title: {self.title}, ISBN: {self.isbn}, "
            f"Publication Year: {self.publication_year}"
        )

