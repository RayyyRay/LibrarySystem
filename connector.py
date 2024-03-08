import mysql.connector
import hashlib
import bcrypt
import tkinter as tk
from tkinter import messagebox
from ttkthemes import ThemedStyle
DB = mysql.connector.connect(
  host="52.207.184.60",
  user="RamonR",
  password="Ramonapril042004!@",
  database="test"
)
print(DB)
mycursor = DB.cursor()
def login_GUI(username,password,root):
    try:
        login_query='''SELECT * FROM User WHERE username=%s and password=%s'''
        mycursor.execute(login_query,(username,password))
        user=mycursor.fetchone()
        if user:
            return True
        else:
            return False
    except mysql.connector.Error as error:
        print("Error while connecting to database")
        messagebox.showerror("Database Error", "Error while connecting to database." + str(error))
def create_account_GUI(root):
    def create_account(login_screen_root):
        create_username=username_entry.get()
        create_password=password_entry.get()
        create_firstname=firstname_entry.get()
        create_lastname=lastname_entry.get()
        create_usertype=usertype_entry.get()
        hashed_password=hashlib.sha256(create_password.encode()).hexdigest()
        create_account_sql='''INSERT INTO User(username,password,first_name,last_name,user_type,hashed_password)
                                    VALUES(%s,%s,%s,%s,%s,%s)'''
        mycursor.execute(create_account_sql,(create_username,create_password,create_firstname,create_lastname,create_usertype,hashed_password))
        DB.commit()
        messagebox.showinfo("Account Created","Account has successfully been created!")
        create_account_window.destroy()
        login_screen_root.deiconify()
    create_account_window = tk.Toplevel(root)
    create_account_window.title("Account Creation")
    username_label = tk.Label(create_account_window, text="Username:")
    username_label.grid(row=0, column=0)
    username_entry = tk.Entry(create_account_window)
    username_entry.grid(row=0, column=1)

    password_label = tk.Label(create_account_window, text="Password:")
    password_label.grid(row=1, column=0)
    password_entry = tk.Entry(create_account_window, show="*")
    password_entry.grid(row=1, column=1)

    firstname_label = tk.Label(create_account_window, text="First Name:")
    firstname_label.grid(row=2, column=0)
    firstname_entry = tk.Entry(create_account_window)
    firstname_entry.grid(row=2, column=1)

    lastname_label = tk.Label(create_account_window, text="Last Name:")
    lastname_label.grid(row=3, column=0)
    lastname_entry = tk.Entry(create_account_window)
    lastname_entry.grid(row=3, column=1)

    usertype_label = tk.Label(create_account_window, text="User Type:")
    usertype_label.grid(row=4, column=0)
    usertype_entry = tk.Entry(create_account_window)
    usertype_entry.grid(row=4, column=1)

    create_account_button = tk.Button(create_account_window, text="Create Account", command=lambda:create_account(root))
    create_account_button.grid(row=5, column=1)
def login_screen():
    root = tk.Tk()
    root.title("Library Login")
    frame=tk.Frame(root)
    frame.pack(padx=10,pady=10)

    input_username=tk.StringVar()
    username_label=tk.Label(frame,text="Username")
    username_label.grid(row=0,column=0, sticky="w")
    username_entry=tk.Entry(frame, textvariable=input_username)
    username_entry.grid(row=0,column=1)

    input_password= tk.StringVar()
    password_label =tk.Label(frame,text="Password")
    password_label.grid(row=1,column=0,sticky="w")
    password_entry=tk.Entry(frame,show="*", textvariable=input_password)
    password_entry.grid(row=1,column=1)
    def on_login():
        username= username_entry.get()
        password= password_entry.get()
        if login_GUI(username,password,root):
            library_ui(username,root)
            root.destroy()
        elif create_account_GUI(root):
            root.withdraw()
            login_GUI(username,password,root)
        else:
            messagebox.showerror("Login Error","Invalid username or password, please try again!")
    login_button =tk.Button(frame, text="Login",command=on_login)
    login_button.grid(row=2,columnspan=2, pady=5)
    create_account_button=tk.Button(frame, text="Create Account",command=lambda:create_account_GUI(root))
    create_account_button.grid(row=3,columnspan=2, pady=5)
    root.mainloop()
def library_ui(username,root):
    def search_books():
        search_query=search_input.get()
        if search_query:
            search_book_sql='''SELECT * FROM books_table WHERE title LIKE %s'''
            mycursor.execute(search_book_sql,('%'+search_query+'%',))
        else:
            all_books='''SELECT * FROM books_table'''
            mycursor.execute(all_books)
        book_list.delete(0,tk.END)
        search_book=mycursor.fetchall()
        for book in search_book:
            book_list.insert(tk.END,book[1])
    def logout():
        library_window.destroy()
        login_screen()
    def return_book():
        return_query=return_input.get()
        return_book_sql='''UPDATE books_table SET Available_copies=Available_copies+1 WHERE title=%s'''
        mycursor.execute(return_book_sql,(return_query,))
        DB.commit()
        print("Book successfully returned!")
    def borrow_book():
        borrow_query=borrow_input.get()
        borrow_book_sql='''UPDATE books_table SET Available_copies=Available_copies-1 WHERE title=%s'''
        mycursor.execute(borrow_book_sql,(borrow_query,))
        DB.commit()
        print("Book successfully borrowed!")
    def all_books():
        all_book_sql='''SELECT * FROM books_table'''
        mycursor.execute(all_book_sql)
        all_books=mycursor.fetchall()
        book_list.delete(0,tk.END)
        for book in all_books:
            book_list.insert(tk.END,book[1])
    root.destroy()
    library_window=tk.Tk()
    library_window.title("Library Interface: ")
    intro_label=tk.Label(library_window,text=f"Welcome back, {username}")
    intro_label.pack(pady=10)

    search_frame=tk.Frame(library_window)
    search_frame.pack(pady=10)
    search_label=tk.Label(search_frame,text="Search Books: ")
    search_label.grid(row=0,column=0)
    search_input=tk.Entry(search_frame)
    search_input.grid(row=0,column=1)
    search_button=tk.Button(search_frame,text="Search",command=search_books)
    search_button.grid(row=0,column=2)

    book_list_frame=tk.Frame(library_window)
    book_list_frame.pack(pady=10)
    book_list_label=tk.Label(book_list_frame,text="Books: ")
    book_list_label.grid(row=0,column=0,padx=10)
    book_list=tk.Listbox(book_list_frame, width=50,height=10)
    book_list.grid(row=1,column=0,padx=10)

    borrow_input=tk.Entry(book_list_frame)
    borrow_book_button=tk.Button(book_list_frame,text="Borrow Book: ",command=borrow_book)
    borrow_book_button.grid(row=2,columnspan=2,pady=5)

    return_book_button=tk.Button(book_list_frame,text="Return Book: ",command=return_book)
    return_book_button.grid(row=3,columnspan=2,pady=5)
    return_input=tk.Entry(book_list_frame)

    logout_button=tk.Button(book_list_frame,text="Logout",command=logout)
    logout_button.grid(row=4,columnspan=2,pady=5)

    all_books()
    library_window.mainloop()
login_screen()