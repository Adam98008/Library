from flask import Flask, render_template, request , redirect
import sqlite3
import  os
 


app = Flask(__name__)
 


# Set the database path relative to the project root #
DATABASE = os.path.join(os.getcwd(), 'Database.db')



# Connect to database #
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
  


# We want to discripe how the data be stored #
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL,
            description TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


init_db()


# Home Page #
@app.route("/")
def homePage():
    return render_template ("index.html") 



# Create book #
@app.route("/createBook", methods=["GET","POST"])
def create_book():
    if request.method == "GET":
        return render_template("createBook.html")
    
    elif request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        year = request.form["year"]
        description = request.form["description"]
        conn = get_db_connection()
        conn.execute("INSERT INTO books (title, author, year,description) VALUES (?, ?, ?, ?)", [title, author, year,description])
        conn.commit()
        conn.close()
        
        return redirect("/viewBooks")
  
 

# View all books #
@app.route("/viewBooks", methods=["GET"])
def view_books():
    conn = get_db_connection()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    return render_template("viewBooks.html", books=books)
 


# View only one book #
@app.route("/viewOneBook/<int:book_id>", methods=["GET"])
def view_book(book_id):
    conn = get_db_connection()
    book = conn.execute("SELECT * FROM books WHERE id = ?", [book_id]).fetchone()
    conn.close()
    if book is None:
        return "Book not found"
    return render_template("viewOneBook.html",book=book)



# Edit or Update book #
@app.route("/updateBook/<int:book_id>",methods=["GET","POST"])
def update_book(book_id):
    conn=get_db_connection()
    if request.method=="GET":
        book = conn.execute("SELECT * FROM books WHERE id = ?", [book_id]).fetchone()
        return render_template("updateBook.html",book = book)
    elif request.method=="POST":
        title = request.form["title"]
        author = request.form["author"]
        year = request.form["year"]
        description = request.form["description"]
        conn.execute("UPDATE books set title = ?, author = ?, year = ?, description = ? WHERE id = ?",[title,author,year,description,book_id])
        conn.commit()
        conn.close()
        return redirect("/viewBooks")
     


# Delete book #
@app.route("/DeleteBook/<int:id>",methods=["POST"])
def delete_book(id):
    conn=get_db_connection()
    if request.method == "POST":
        conn.execute("DELETE FROM books WHERE id = ?",[id])
        conn.commit()
        conn.close()
        return redirect("/viewBooks")

 
 
# Run the app #
if __name__ == "__main__":
   app.run(debug=True,port=5000)