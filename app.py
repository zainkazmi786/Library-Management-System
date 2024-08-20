from flask import Flask, render_template, request, redirect, session , jsonify
from flask_mysqldb import MySQL
from config import Config  # Import the Config class



# Lists to store users and books


# def generate_user_id():
#     return len(users) + 1  # Simple ID generation based on the current number of users

# def add_user(user_name, user_id, books=None):
#     if books is None:
#         books = []
#     users.append([user_name, user_id, books])

# def add_book(book_name, author_name):
#     books_in_catalogue.append([book_name, author_name])

# def display_users():
#     for user in users:
#         print(f"Username: {user[0]}")
#         print(f"ID: {user[1]}")
#         print("Books issued:", user[2] if user[2] else "No books issued")
#         print()

# def display_users_with_books():
#     for user in users:
#         print(f"Username: {user[0]}")
#         print(f"ID: {user[1]}")
#         print(f"Books issued: {user[2] if user[2] else 'No books issued'}")
#         print()

# def issue_a_book(user, book):
#     user[2].append(book)

# def return_a_book(user, book):
#     if book in user[2]:
#         user[2].remove(book)

# def display_books_in_catalogue():
#     if not books_in_catalogue:
#         print("No books in the catalogue.")
#     else:
#         for i, value in enumerate(books_in_catalogue):
#             print(f"{i + 1}. {value[0]} by {value[1]}")
#     print()

# def validate_integer_input(prompt):
#     while True:
#         try:
#             value = int(input(prompt))
#             return value
#         except ValueError:
#             print("Invalid input. Please enter a valid integer.")

# def validate_book_selection(prompt, max_selection):
#     while True:
#         selection = validate_integer_input(prompt)
#         if 1 <= selection <= max_selection:
#             return selection
#         else:
#             print(f"Invalid selection. Please enter a number between 1 and {max_selection}.")

#  get_valid_string(str):
#     while True:
#         
#         if any(char.isdigit() for char in str):
#             return ("Input cannot have numbers. Please enter a valid string.")
#         elif not all(char.isalpha() or char.isspace() for char in str):
#             return ("Input cannot have specials. Please enter a valid string.")

#         else:
#             return str.lstrip(" ").rstrip(" ")

# print("Welcome to Library Management System")
# while True:
#     print("\nPress 1 to Add a User")
#     print("Press 2 to Add a Book to catalogue")
#     print("Press 3 to Issue a Book")
#     print("Press 4 to Return a Book")
#     print("Press 5 to View all Users")
#     print("Press 6 to View all Books in catalog")
#     print("Press 7 to Exit")

#     choice = validate_integer_input("Enter your choice: ")
    
#     if choice == 1:
#         user_name = get_valid_string_input("Enter username: ")
#         user_id = generate_user_id() 
#         add_user(user_name, user_id)
#         print(f"User '{user_name}' added successfully.")

#     elif choice == 2:
#         book_name = get_valid_string_input("Enter book name: ")
#         author_name = get_valid_string_input("Enter author name: ")
#         add_book(book_name, author_name)
#         print(f"Book '{book_name}' by '{author_name}' added to the catalogue.")

#     elif choice == 3:
#         display_users()
#         user_id = validate_integer_input("Enter user ID to issue a book: ")
#         if 1 <= user_id <= len(users):
#             display_books_in_catalogue()  
#             book_index = validate_book_selection("Enter book number to issue: ", len(books_in_catalogue)) - 1
#             issue_a_book(users[user_id - 1], books_in_catalogue[book_index][0])
#             print(f"Book '{books_in_catalogue[book_index][0]}' issued to '{users[user_id - 1][0]}'.")
#         else:
#             print("Invalid user ID.")

#     elif choice == 4:
#         display_users()
#         user_id = validate_integer_input("Enter user ID to return a book: ")
#         if 1 <= user_id <= len(users):
#             book_name = get_valid_string_input("Enter the name of the book to return: ")
#             return_a_book(users[user_id - 1], book_name)
#             print(f"Book '{book_name}' returned by '{users[user_id - 1][0]}'.")
#         else:
#             print("Invalid user ID.")

#     elif choice == 5:
#         display_users_with_books()

#     elif choice == 6:
#         display_books_in_catalogue()

#     elif choice == 7:
#         print("Exiting the Library Management System.")
#         break

#     else:
#         print("Invalid choice. Please try again.")

app = Flask(__name__)

app.config.from_object(Config)

mysql = MySQL(app)

 
def get_valid_string(str):
    while True:
        
        if any(char.isdigit() for char in str):
            return (False)
        elif not all(char.isalpha() or char.isspace() for char in str):
            return (False)

        else:
            return str.lstrip(" ").rstrip(" ")

userid = 0
bookid = 0


def generate_userid():
    global userid  
    userid += 1
    return userid

def generate_bookid():
    global bookid
    bookid += 1
    return bookid
 
@app.route('/')
def hello():
    return 'Welcome to Library Management System'

@app.route('/showusersform')
def showusersform():
    return render_template("viewusers.html")

@app.route('/showusers')
def showusers():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users')
    users =  cursor.fetchall()

    userlist = []
    for user in users:
        user_dict= {
            "id" : user[0],
            "name" : user[1]
        }
        userlist.append(user_dict)

    cursor.close()
    return jsonify(userlist)

@app.route("/showbooks")
def showbooks():
    return render_template("viewbooks.html")

@app.route('/showbooksincatalogue' ,methods = ["GET"])
def showbooksincatalogue():
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    
    booklist = []
    for book in books:
        book_id = book[0]  # Assuming the first column is the book ID
        book_name = book[1]  # Assuming the second column is the book name
        author_name = book[2]  # Assuming the third column is the author name
        user_id = book[3]  # Assuming the fourth column is the user ID (if applicable)

        # If you want to fetch the user associated with the book
        user = None
        if user_id is not None:  # Check if user_id is not null
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()  # Fetch a single user

        # Prepare the book dictionary
        book_dict = {
            "id": book_id,
            "bookname": book_name,
            "authorname": author_name,
            "user": user[1] if user else None  # Assuming the second column is the user's name
        }
        booklist.append(book_dict)  # Add the book dictionary to the list

    cursor.close()  # Close the cursor
    return jsonify(booklist)  # Return the list of books as JSON

@app.route('/deletebook/<int:book_id>', methods=['DELETE'] )
def delbook(book_id):
    
    cursor = mysql.connection.cursor()
    
    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    
   
    if cursor.rowcount == 0:
        return jsonify({"message": "book not found"}), 404
    
    mysql.connection.commit()
    cursor.close()
    return  jsonify({"message" : "book deleted successfully"})



@app.route('/addusers', methods=['POST' , 'GET'])
def addusers():
    if request.method == 'POST':
        username = get_valid_string(request.form["name"])  
        if not username:
            return jsonify({"message" : "Invalid Username"})
        
        cursor = mysql.connection.cursor()
        cursor.execute(f"INSERT INTO users (id , name ) VALUES (%s,%s)",(generate_userid(),username))
        mysql.connection.commit()
        cursor.close()
        return jsonify({"message": "Users added successfully!", "users": username}), 201
    return render_template('adduser.html')

@app.route("/deleteall" , methods = ["Delete"])
def delall():
    cursor = mysql.connection.cursor()
    
    cursor.execute("DELETE FROM users")
    if cursor.rowcount == 0:
        return jsonify({"message": "noting to Delete"}), 404
    
    mysql.connection.commit()
    cursor.close()
    return  jsonify({"message" : " deleted successfully"})

@app.route('/deleteuser/<int:user_id>', methods=['DELETE'] )
def deluser(user_id):
    
    cursor = mysql.connection.cursor()
    
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    
   
    if cursor.rowcount == 0:
        return jsonify({"message": "User not found"}), 404
    
    mysql.connection.commit()
    cursor.close()
    return  jsonify({"message" : "user deleted successfully"})


@app.route('/user/<int:user_id>', methods=['GET'] )
def getoneuser(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone() 
    return jsonify(user)


@app.route('/edituser/<int:user_id>', methods=['PUT' ,'GET'] )
def edituser(user_id):
    if request.method == 'GET':
        return render_template("edituser.html")
    else:
        cursor = mysql.connection.cursor()
        user = request.get_json()
        user_data = get_valid_string(user.get('name'))
        if not user_data:
            return jsonify({"message" : "Invalid Input"})
        cursor.execute("UPDATE users SET name = %s WHERE id = %s", (user_data ,user_id))
        if cursor.rowcount == 0:
            return jsonify({"message": "User not found"}), 404
        mysql.connection.commit()
        cursor.close()
        return  jsonify({"message" : user_data})

@app.route('/addbookincatalogue',  methods=['POST','GET'])
def addbookincatalogue():
    if request.method == 'POST':
        bookname = request.form["name"] 
        authorname = get_valid_string(request.form["author"])
        if not authorname:
            return jsonify({"message" : "Invalid authorname"})

        cursor = mysql.connection.cursor()
        cursor.execute(f"INSERT INTO books (id , name ,author) VALUES (%s,%s,%s)",(generate_bookid(),bookname,authorname))
                
        mysql.connection.commit()
        cursor.close()
        return jsonify({"message": "books added successfully!", "users": bookname}), 201
    
    return render_template("addbook.html")



@app.route('/showbooksfromusers/<int:user_id>')
def showbooksfromusers(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = %s" , user_id)
    users = cursor.fetchall()

    cursor.execute("SELECT * FROM books WHERE user_id = %s", (user_id))
    books = cursor.fetchall()
    booklist = []
    for book in books:
        book_dict = {
            "id"     : book[0],
            "name"   : book[1],
            "author" : book[2],
         }
        booklist.append(book_dict)

    user_dictionary = {
        "id" : user_id,
        "name" : users[1],
        "books" : booklist
    }
    return jsonify(user_dictionary)
    

        


@app.route('/issuebooktouser/<int:user_id>/<int:book_id>', methods=['PUT'])
def addbook(user_id, book_id):
    cursor = mysql.connection.cursor()
    
    # Update the user_id for the specified book_id
    cursor.execute("UPDATE books SET user_id = %s WHERE id = %s", (user_id, book_id))
    

    if cursor.rowcount == 0:
        cursor.close() 
        return jsonify({"message": "Book not found or already issued to a user"}), 404

    mysql.connection.commit()  # Commit the changes to the database
    cursor.close()  # Close the cursor
    
    return jsonify({"message": f"Book successfully issued to user id: {user_id}"}), 200

@app.route('/returnbookfromuser/<int:book_id>', methods = ['PUT'])
def removebook( book_id):
    
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE books SET user_id = %s WHERE id = %s", (0 , book_id))
    if cursor.rowcount == 0:
        cursor.close()  # Close the cursor before returning
        return jsonify({"message": "Book not found or already issued to a user"}), 404
    
    mysql.connection.commit()
    cursor.close()
    return jsonify({"message" : f"Book deleted successfully" })



@app.route('/handle_post', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        a = (request.get_json())       
        return a
    

if __name__ == "__main__":
    app.run(debug=True)
