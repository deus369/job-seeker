import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import webbrowser
#sudo apt-get install python3-tk
import time
import threading
import globals
from data.job_state import JobState
from data.selected_job import SelectedJob
from ui.loading_ui import *
from ui.treeview import *
from web.web_scanner import scan_all_seek_terms
from util.slug_converter import convert_text_to_slug

def on_background_action_end():
    if globals.is_performing_action:
        globals.is_performing_action = False
        hide_load_ui()

def open_text_input_popup(event, job_data, response_function):
    # Create a new window for the popup
    popup = tk.Toplevel()
    popup.title("Job Scanner")
    popup.geometry("400x200")
    # Create a label for the text input
    label = tk.Label(popup, text="Search Keywords:")
    label.pack()
    # Create a text input field
    text_input = tk.Entry(popup)
    text_input.pack()
    # Create a submit button
    submit_button = tk.Button(popup, text="Submit", command=lambda: (response_function(job_data, convert_text_to_slug(text_input.get())), popup.destroy()))
    submit_button.pack()

def scan_submit_response(job_data, response_text):
    print("Text input received: " + response_text)
    response = messagebox.askyesno("Confirm", "Scan jobs for [" + response_text + "]?")
    if response:
        scan_all_seek_terms(job_data, [ response_text ], on_add_job)
        job_data.save_data()

def on_add_job(i, job_id, job_title, job_link):
    create_ui_row(globals.tree, i, job_id, job_title, job_link, (JobState.NONE.value))

def apply_job_ui(event, job_data, apply_job_thread, job_clicked):
    if globals.is_performing_action:
        return
    globals.is_performing_action = True
    show_load_ui()
    # Start the action
    # threading.Thread(target=apply_job_thread).start()
    threading.Thread(target=apply_job_thread, args=(job_data, globals.selected_job, job_clicked, update_row_job_state, update_loading_label, on_background_action_end)).start()

def create_window(title, job_data, job_clicked, apply_job_thread, scan_all_seek_terms):
    globals.tree_window = tk.Tk()
    tree_window = globals.tree_window
    tree_window.attributes("-zoomed", True)
    tree_window.configure(bg=globals.background_color)
    def on_closing():
        tree_window.destroy()
        tree_window.quit()
    tree_window.protocol("WM_DELETE_WINDOW", on_closing)
    tree_window.title(title)
    tree_window.columnconfigure(0, weight=1)
    tree_window.rowconfigure(0, weight=1)
    tree_window.bind("<KeyPress-x>", lambda event, arg1=job_data, arg2=apply_job_thread, arg3=job_clicked: apply_job_ui(event, arg1, arg2, arg3)) #apply_job_ui)
    tree_window.bind("<KeyPress-c>", lambda event, arg1=job_data, arg2=scan_submit_response: open_text_input_popup(event, arg1, arg2))
    # tree_window.bind("<KeyPress-b>", open_text_input_popup)
    # tree_window.bind("<KeyPress-v>", apply_job_ui)
    # tree_window.bind("<KeyPress-n>", toggle_loading_ui)
    # tree_window.bind("<KeyPress-m>", toggle_treeview)
    return tree_window


def create_jobs_ui(job_data, job_clicked, job_applied_clicked, apply_job_thread, apply_jobs_thread, scan_all_seek_terms):
    tree_window = globals.tree_window
    tree_window = create_window("Job Viewer", job_data, job_clicked, apply_job_thread, scan_all_seek_terms)
    create_treeview(tree_window, job_data, job_clicked, job_applied_clicked, apply_jobs_thread, bulk_apply, show_load_ui, update_loading_label, on_background_action_end)
    create_load_ui(tree_window)
    return tree_window