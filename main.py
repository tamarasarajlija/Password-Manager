import sqlite3
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip

# ---------------------------- DATABASE SETUP ------------------------------- #

# Create a database connection and a table if it doesn't exist
def create_db():
    conn = sqlite3.connect('password_manager.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            website TEXT,
            email TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_db()

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        conn = sqlite3.connect('password_manager.db')
        c = conn.cursor()
        c.execute("INSERT INTO passwords (website, email, password) VALUES (?, ?, ?)",
                  (website, email, password))
        conn.commit()
        conn.close()

        website_entry.delete(0, END)
        password_entry.delete(0, END)
        website_label.focus()

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    conn = sqlite3.connect('password_manager.db')
    c = conn.cursor()
    c.execute("SELECT email, password FROM passwords WHERE website=?", (website,))
    result = c.fetchone()
    conn.close()

    if result:
        email, password = result
        messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
    else:
        messagebox.showinfo(title="Error", message=f"No details for {website} exists.")

# ---------------------------- VIEW ALL PASSWORDS ------------------------------- #
def view_all_passwords():
    conn = sqlite3.connect('password_manager.db')
    c = conn.cursor()
    c.execute("SELECT * FROM passwords")
    all_passwords = c.fetchall()
    conn.close()

    if all_passwords:
        all_passwords_message = ""
        for website, email, password in all_passwords:
            all_passwords_message += f"Website: {website}\nEmail: {email}\nPassword: {password}\n\n"
        messagebox.showinfo(title="All Saved Passwords", message=all_passwords_message)
    else:
        messagebox.showinfo(title="Error", message="No passwords saved yet.")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=30, pady=30, bg="lightblue")

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:", bg="lightblue")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:", bg="lightblue")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:", bg="lightblue")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

# Buttons
search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(row=1, column=2)
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

# Button for viewing all passwords
view_button = Button(text="View All Passwords", width=36, command=view_all_passwords)
view_button.grid(row=5, column=1, columnspan=2)

window.mainloop()
