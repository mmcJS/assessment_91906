# imports
# importing secrets is for generating random numbers
import secrets
import string
import tkinter

# installed pyperclip, which was to allow my program access to changing clipboard data
# pyperclip is a module that can be downloaded in this IDE (Pycharm)
# by going from Python Packages -> searching "pyperclip" and installing.
import pyperclip
# tkinter msgboxes and scroll ( used for the Help page )
from tkinter import messagebox, scrolledtext
# tkinter ttk allows the user to right click on the rows and delete/copy previously saved passwords
from tkinter import ttk

# can create the "logged password" .txt documnts with this
import os

# all the gui and buttons mostly using tkinter
root = tkinter.Tk()
root.title("Password Generator (version 4)")

# places the password_log.txt in the same directory as the python file for easy access
current_directory = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(current_directory, "password_log.txt")

# directory check for debugging purposes
print(f"{log_file_path}")

# generating password function
def generate_password(length, use_uppercase, use_numbers, use_special):
    characters = string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_numbers:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    password = ''.join(secrets.choice(characters) for _ in range(length))
    name = name_entry.get()
    description = description_entry.get()
    log_password(password, name, description)
    return password

# writes the name (optional), password, description (optional) to the .txt
def log_password(password, name="", description=""):
    with open(log_file_path, "a") as f:
        f.write(f"{name}\t{password}\t{description}\n")

# this function lets you see the logged passwords from that tab
def view_logged_passwords():
    global tree
    for widget in root.winfo_children():
        widget.grid_forget()

    frame = tkinter.Frame(root, bd=2, relief='groove')
    frame.grid(row=0, column=0, padx=10, pady=10, columnspan=3, sticky='nsew')

    tree = ttk.Treeview(frame, columns=("Name", "Password", "Description"), show="headings")
    tree.heading("Name", text="Name")
    tree.heading("Password", text="Password")
    tree.heading("Description", text="Description")

    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) == 1:
                    name, password, description = "", parts[0], ""
                elif len(parts) == 2:
                    name, password, description = parts[0], parts[1], ""
                else:
                    name, password, description = parts[0], parts[1], parts[2]
                tree.insert("", "end", values=(name, password, description))

    tree.bind("<Button-3>", on_right_click)
    tree.grid(row=0, column=0, sticky='nsew')

    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

# when u right click a row the two options will show
def on_right_click(event):
    item = tree.identify_row(event.y)
    if item:
        popup_menu = tkinter.Menu(root, tearoff=0)
        popup_menu.add_command(label="Copy Password", command=lambda: copy_password(item))
        popup_menu.add_command(label="Delete Row", command=lambda: delete_row(item))
        popup_menu.post(event.x_root, event.y_root)

# uses pyperclip to add the password to your clipboard
def copy_password(item):
    password = tree.item(item, "values")[1]
    pyperclip.copy(password)
    messagebox.showinfo("Copied!", "Password has been copied to your clipboard!")

# deletes the entire row from the .txt
def delete_row(item):
    password_to_delete = tree.item(item, "values")[1]
    tree.delete(item)
    with open(log_file_path, "r") as f:
        lines = f.readlines()
    with open(log_file_path, "w") as f:
        for line in lines:
            parts = line.strip().split('\t')
            if len(parts) == 1:
                name, password, description = "", parts[0], ""
            elif len(parts) == 2:
                name, password, description = parts[0], parts[1], ""
            else:
                name, password, description = parts[0], parts[1], parts[2]
            if password != password_to_delete:
                f.write(line)

# displays the tickable boxes, uppercase, numbers, special
def generate_and_display_password():
    try:
        length = int(length_entry.get())
        use_uppercase = uppercase_var.get()
        use_numbers = numbers_var.get()
        use_special = special_var.get()

        # checks for input of 0 and wont allow it
        if length < 1:
            raise ValueError("Character length must be greater than 0, with a recommended length of 6+ for strength.")

        password = generate_password(length, use_uppercase, use_numbers, use_special)
        password_entry.delete(0, tkinter.END)
        password_entry.insert(0, password)
    except ValueError:
        # error messagebox (non number)
        messagebox.showerror("Invalid Input", "Password length may only be numbers above 0.")

# function that copies the password to clipboard upon press of the "copy the clipboard button" using the
# pyperclip module.
def copy_to_clipboard():
    password = password_entry.get()
    pyperclip.copy(password)
    messagebox.showinfo("Copied!", "Password has been copied to your clipboard!")

# function to show the generate password (home) page
def show_generate_page():
    for widget in root.winfo_children():
        widget.grid_forget()

    tkinter.Label(root, text="Password Length:", font=('Calibri', 12)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
    length_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

    tkinter.Checkbutton(root, text="Include Uppercase Letters?", variable=uppercase_var, font=('Calibri', 12)).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='w')
    tkinter.Checkbutton(root, text="Include Numbers?", variable=numbers_var, font=('Calibri', 12)).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='w')
    tkinter.Checkbutton(root, text="Include Special Characters?", variable=special_var, font=('Calibri', 12)).grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='w')

    tkinter.Label(root, text="Name:", font=('Calibri', 12)).grid(row=4, column=0, padx=10, pady=10, sticky='w')
    name_entry.grid(row=4, column=1, padx=10, pady=10, sticky='ew')

    tkinter.Label(root, text="Description:", font=('Calibri', 12)).grid(row=5, column=0, padx=10, pady=10, sticky='w')
    description_entry.grid(row=5, column=1, padx=10, pady=10, sticky='ew')

    tkinter.Button(root, text="Generate Password", command=generate_and_display_password, font=('Calibri', 12)).grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

    tkinter.Label(root, text="Generated Password:", font=('Calibri', 12)).grid(row=7, column=0, padx=10, pady=10, sticky='w')
    password_entry.grid(row=7, column=1, padx=10, pady=10, sticky='ew')

    tkinter.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, font=('Calibri', 12)).grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

# shows the help page
def show_help_page():
    for widget in root.winfo_children():
        widget.grid_forget()

    text_area = scrolledtext.ScrolledText(root, wrap=tkinter.WORD, width=50, height=20, font=('Calibri', 12))
    text_area.grid(column=0, row=0, padx=10, pady=10, columnspan=2, sticky='nsew')

    help_text = """
    First time using the Password Generator?
    
    This application intends to help you generate secure passwords with the customisation options provided.
    Below are the detailed instructions on how to use each feature of the application.

    1. Generate Password:
    Password Length: Enter the desired length of the password. Minimum length is 1, however at least 6+ is recommended for a strong password.
    Include Uppercase Letters?: Check this box to include uppercase letters in the password.
    Include Numbers?: Check this box to include numbers in the password.
    Include Special Characters?: Check this box to include special characters (e.g., !, @, #) in the password.
    Name (optional): You can enter a name to identify the password later on in the Logged Passwords.
    Description (optional): You can enter a description to provide more context about the password.
    Click on "Generate Password" to generate and display the password.
    Click on "Copy to Clipboard" to copy the generated password to your clipboard.

    2. View Logged Passwords:
    Navigate to "Logged Passwords" to view all the saved passwords.
    Right-click on any row to either copy the password to clipboard or delete the row.
    The table displays Name, Password, and Description columns.

    Additional Features:
    The generated passwords and their details are logged in a text file named 'password_log.txt' located in the same directory as this script.
    You can right-click on any row in the "Logged Passwords" section to copy the password to your clipboard or delete the row.
    Deleting a row will remove the corresponding entry from the text file as well.

    Thank you for using the Password Generator!
    """

    text_area.insert(tkinter.INSERT, help_text)
    text_area.config(state=tkinter.DISABLED)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    # resizing the help text within the window size
    text_area.grid(row=0, column=0, sticky='nsew')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

# navigation bar menu at the top
menu = tkinter.Menu(root)
root.config(menu=menu)
menu.add_command(label="Generate", command=show_generate_page)
menu.add_command(label="Logged Passwords", command=view_logged_passwords)
menu.add_command(label="Help!", command=show_help_page)

length_entry = tkinter.Entry(root, font=('Calibri', 12))
name_entry = tkinter.Entry(root, font=('Calibri', 12))
description_entry = tkinter.Entry(root, font=('Calibri', 12))
uppercase_var = tkinter.BooleanVar()
numbers_var = tkinter.BooleanVar()
special_var = tkinter.BooleanVar()
password_entry = tkinter.Entry(root, width=50, font=('Calibri', 12))

# to initially show the generate home page when the app is opened
show_generate_page()

root.mainloop()
