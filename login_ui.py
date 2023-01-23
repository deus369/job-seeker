import tkinter as tk
import os
from encrypter import *
login_directory = "~/.config/job_seeker.txt"

def save_login(username, password):
    if not os.path.exists(os.path.dirname(login_directory)):
        os.makedirs(os.path.dirname(login_directory))
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    with open(login_directory, "w") as f:
        f.write(username + "\n")
        f.write(encrypted_password.decode())

def load_login():
    if os.path.exists(login_directory):
        with open(login_directory, "r") as f:
            username = f.readline().strip()
            encrypted_password = f.readline().strip()
        fernet = Fernet(key)
        decrypted_password = fernet.decrypt(encrypted_password.encode()).decode()
        return (username, decrypted_password)
    else:
        return ("", "")

def spawn_login_ui(on_logged_in):
    login_ui = tk.Tk() # tk.Toplevel()
    def submit():
        username = username_var.get()
        password = password_var.get()
        print(f"Username: {username}") #  - Password: {password}")
        save_login(username, password)
        login_ui.destroy()
        on_logged_in(username, password)
    login_ui.title("Login")
    login_data = load_login()
    username_var = tk.StringVar()
    password_var = tk.StringVar()
    username_var.set(login_data[0])
    password_var.set(login_data[1])
    print("Loaded username: " + login_data[0]) # + " :: " + login_data[1])
    username_label = tk.Label(login_ui, text="Username:")
    username_entry = tk.Entry(login_ui, textvariable=username_var)
    password_label = tk.Label(login_ui, text="Password:")
    password_entry = tk.Entry(login_ui, textvariable=password_var, show="*")
    submit_button = tk.Button(login_ui, text="Submit", command=submit)
    username_label.grid(row=0, column=0)
    username_entry.grid(row=0, column=1)
    password_label.grid(row=1, column=0)
    password_entry.grid(row=1, column=1)
    submit_button.grid(row=2, column=1, pady=10)
    return login_ui