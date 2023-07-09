import tkinter as tk
import os
from util.encrypter import *
import globals

def set_visibility_login_ui(is_visible):
    if is_visible:
        print("Showing LoginUI")
        globals.login_ui.pack(fill=tk.BOTH, expand=True)
    else:
        print("Hiding LoginUI")
        globals.login_ui.pack_forget()

def save_login(username, password):
    if not os.path.exists(os.path.dirname(globals.login_directory)):
        os.makedirs(os.path.dirname(globals.login_directory))
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    with open(globals.login_directory, "w") as f:
        f.write(username + "\n")
        f.write(encrypted_password.decode())

def load_login():
    if os.path.exists(globals.login_directory):
        with open(globals.login_directory, "r") as f:
            username = f.readline().strip()
            encrypted_password = f.readline().strip()
        fernet = Fernet(key)
        decrypted_password = fernet.decrypt(encrypted_password.encode()).decode()
        return (username, decrypted_password)
    else:
        return ("", "")

def on_submit_login():
    username = globals.username_var.get()
    password = globals.password_var.get()
    print(f"Username: {username}") #  - Password: {password}")
    save_login(username, password)
    set_visibility_login_ui(False)
    globals.start_login_thread_(username, password)

def create_login_ui(tree_window, start_login_thread):
    globals.start_login_thread_ = start_login_thread
    login_ui = tk.Frame(tree_window)
    login_ui.pack(fill=tk.BOTH, expand=True)
    # login_ui.title("Login")
    login_data = load_login()
    globals.username_var = tk.StringVar()
    globals.password_var = tk.StringVar()
    globals.username_var.set(login_data[0])
    globals.password_var.set(login_data[1])
    print("Loaded username: " + login_data[0]) # + " :: " + login_data[1])
    username_label = tk.Label(login_ui, text="Username", font=("Monocraft", 14, "bold"))
    username_entry = tk.Entry(login_ui, textvariable=globals.username_var, width=24, font=("Monocraft", 12), justify="center")
    password_label = tk.Label(login_ui, text="Password", font=("Monocraft", 14, "bold"))
    password_entry = tk.Entry(login_ui, textvariable=globals.password_var, width=24, show="*", font=("Monocraft", 12), justify="center")
    submit_button = tk.Button(login_ui, text="Login", command=on_submit_login, font=("Monocraft", 12, "bold"))
    username_label.pack(pady=20, side=tk.TOP, expand=True, anchor="center")
    username_entry.pack(pady=20, side=tk.TOP, expand=True, anchor="center")
    password_label.pack(pady=20, side=tk.TOP, expand=True, anchor="center")
    password_entry.pack(pady=20, side=tk.TOP, expand=True, anchor="center")
    submit_button.pack(pady=20, side=tk.TOP, expand=True, anchor="center")
    login_ui.configure(background=globals.background_color)
    username_label.configure(background=globals.background_color, foreground=globals.foreground_color)
    username_entry.configure(background=globals.background_color, foreground=globals.font_color)
    password_label.configure(background=globals.background_color, foreground=globals.foreground_color)
    password_entry.configure(background=globals.background_color, foreground=globals.font_color)
    submit_button.configure(background=globals.background_color, foreground=globals.foreground_color, activebackground=globals.active_color)
    globals.login_ui = login_ui
    return login_ui

# login_ui.destroy()
# login_ui.grid_remove()
