from tkinter import ttk
import tkinter as tk
import globals
# from ui.treeview import *

def set_visibility_load_ui(is_visible):
    if globals.load_ui is None:
        return
    if is_visible:
        globals.load_ui.pack(fill=tk.BOTH, expand=True)
    else:
        globals.load_ui.pack_forget()

def toggle_treeview(event):
    print("Toggling tree visibility.")
    is_visible = not globals.tree.winfo_ismapped()
    set_visibility_treeview(is_visible)

def toggle_loading_ui(event):
    tree_window = event.widget
    set_visibility_load_ui(globals.progress_bar.winfo_ismapped())
    set_visibility_treeview(not globals.progress_bar.winfo_ismapped())

def update_loading_bar(percentage):
    globals.progress_bar['value'] = percentage

def update_loading_label(text):
    globals.load_label['text'] = text

def update_loading_label2(text):
    globals.load_label2['text'] = text

def create_load_ui(tree_window):
    if (tree_window == None):
        return
    ttk.Style().configure("TProgressbar", foreground=globals.foreground_color, background=globals.background_color)
    load_ui = tk.Frame(tree_window)
    globals.load_ui = load_ui
    load_ui.pack(fill=tk.BOTH, expand=True)
    load_ui.configure(background=globals.background_color)
    globals.load_label = tk.Label(load_ui, text='Loading [1 out of 1]', font=("Monocraft", 14, "bold"))
    globals.load_label.configure(bg=globals.background_color, foreground=globals.font_color)
    globals.load_label.pack(pady=20, side=tk.TOP, expand=True, anchor="center")
    globals.load_label2 = tk.Label(load_ui, text='A description of loading', font=("Monocraft", 8, "bold"))
    globals.load_label2.configure(bg=globals.background_color, foreground=globals.font_color)
    globals.load_label2.pack(pady=20, side=tk.TOP, expand=True, anchor="center")
    globals.progress_bar = ttk.Progressbar(load_ui, orient="horizontal", length=200, mode="determinate")
    globals.progress_bar.pack(pady=20, side=tk.TOP, expand=True, anchor="center")
    # globals.progress_bar.start()
    set_visibility_load_ui(False)

#load_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky='nsew')
# progress_bar.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky='nsew')
# progress_bar.configure(bg=globals.background_color, foreground=globals.font_color)

# def update_loading_label2(text):
#     print(" > " + text)
#     loading_label.config(text=text)

# def hide_loading_ui2():
#     if loading_window.winfo_exists():
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
        #globals.load_ui.config(state='disabled')
        #load_label.grid_remove()
    # set_visibility_treeview(not is_visible)
    # global progress_bar
        #globals.load_ui.grid()
        #load_label.grid()
        #globals.load_ui.grid_remove()
