from tkinter import ttk
import tkinter as tk
from treeview import *
import globals

def set_visibility_load_ui(is_visible):
    global progress_bar
    if is_visible:
        progress_bar.grid()
        load_label.grid()
    else:
        progress_bar.grid_remove()
        load_label.grid_remove()
    set_visibility_treeview(not is_visible)

def show_load_ui():
    set_visibility_load_ui(True)

def hide_load_ui():
    set_visibility_load_ui(False)

def toggle_treeview(event):
    print("Toggling tree visibility.")
    global tree
    is_visible = not tree.winfo_ismapped()
    set_visibility_treeview(is_visible)

def toggle_loading_ui(event):
    tree_window = event.widget
    if progress_bar.winfo_ismapped():
        hide_load_ui()
    else:
        show_load_ui()

def update_loading_bar(percentage):
    global progress_bar
    progress_bar['value'] = percentage

def update_loading_label(text):
    global load_label
    load_label['text'] = text

def create_load_ui(tree_window):
    global progress_bar
    global load_label
    load_label = tk.Label(tree_window, text='Loading...')
    load_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky='nsew')
    load_label.configure(bg=globals.background_color, foreground=globals.font_color)
    progress_bar = ttk.Progressbar(tree_window, orient="horizontal", length=200, mode="determinate")
    progress_bar.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky='nsew')
    progress_bar.start()
    hide_load_ui()


# def update_loading_label2(text):
#     print(" > " + text)
#     loading_label.config(text=text)

# def hide_loading_ui2():
#     if loading_window.winfo_exists():
#         global tree_window
#         tree_window.unbind("<Configure>")
#         loading_window.destroy()

# def create_load_ui2(tree_window):
#     # Create a new window with a loading message
#     global loading_window
#     global loading_label
#     loading_window = tk.Toplevel(tree_window)
#     loading_window.configure(bg=globals.background_color)
#     loading_window.attributes("-alpha", 0.5)
#     # Get the main window's geometry
#     loading_window.overrideredirect(True)
#     loading_window.lift()
#     loading_window.transient(tree_window)
#     # loading_window.place(relx=0, rely=0, relwidth=1, relheight=1)
#     def reposition_loading_window(event):
#         top_menu_bar_height = 36
#         geometry = tree_window.geometry()
#         x, y = map(int, geometry.split("+")[1:])
#         width, height = map(int, geometry.split("+")[0].split("x"))
#         loading_window.geometry(f"{width}x{height}+{x}+{y+top_menu_bar_height}")
#     tree_window.bind("<Configure>", reposition_loading_window)
#     reposition_loading_window(0)
#     frame = tk.Frame(loading_window, bg='#000000')
#     frame.place(relx=0.5, rely=0.5, anchor='center')
#     loading_label = tk.Label(frame, text="") # loading_window
#     loading_label.grid(row=0, column=0, sticky="nsew")
#     loading_label.config(anchor="center")
#     # loading_label.pack(expand=True)
#     loading_label.configure(background="#222222", foreground="white")
#     loading_label.pack()