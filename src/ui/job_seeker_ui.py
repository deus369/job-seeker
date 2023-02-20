import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import webbrowser
import time
import threading
import globals
from data.job_state import JobState
from data.selected_job import SelectedJob
from ui.loading_ui import *
from ui.treeview import *
from ui.login_ui import *
from web.web_scanner import *
from web.jobsdb import *
# from web.web_scanner import scan_all_seek_terms
from util.slug_converter import convert_text_to_slug
#sudo apt-get install python3-tk

def on_background_action_end():
    if globals.is_performing_action:
        globals.is_performing_action = False
        set_visibility_load_ui(False)
        set_visibility_treeview(True)

def open_text_input_popup(event, response_function):
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
    submit_button = tk.Button(popup, text="Submit", command=lambda:
        (response_function(convert_text_to_slug(text_input.get())), popup.destroy()))
    submit_button.pack()

def scan_submit_response(response_text):
    print("Text input received: " + response_text)
    response = messagebox.askyesno("Confirm", "Scan jobs for [" + response_text + "]?")
    if response:
        scan_all_seek_terms(job_data, [ response_text ], on_add_job)
        globals.job_data.save_data()

def on_add_job(i, job_id, job_title, job_link):
    create_ui_row(globals.tree, i, job_id, job_title, job_link, (JobState.NONE.value))

def apply_job_ui(event, apply_job_thread, job_clicked):
    if globals.is_performing_action or len(globals.tree.selection()) == 0:
        return
    globals.is_performing_action = True
    set_visibility_load_ui(True)
    set_visibility_treeview(False)
    # Start the action
    # threading.Thread(target=apply_job_thread).start()
    threading.Thread(target=apply_job_thread,
        args=(globals.selected_job, job_clicked, update_row_job_state, update_loading_label, on_background_action_end)).start()

#title, job_data, job_clicked, apply_job_thread, scan_all_seek_terms):

def on_logged_in():
    print("Finished Logging In.")
    set_visibility_load_ui(False)
    set_visibility_treeview(True)

def start_login_thread(email, password):
    set_visibility_load_ui(True)
    update_loading_label("Logging In")
    update_loading_label2("~")
    threading.Thread(target=login_to_seek, args=(email, password, on_logged_in)).start()

def set_icon(tree_window):
    # Load the PNG image as a PhotoImage object
    icon = tk.PhotoImage(file="icon.png")
    # Set the icon photo for the window
    tree_window.iconphoto(True, icon)
    
def create_window(job_clicked, job_applied_clicked, apply_job_thread, apply_jobs_thread):
    title = "Job Seeker"
    # tree_window = create_window("Job Viewer", job_data, job_clicked, apply_job_thread, scan_all_seek_terms)
    globals.tree_window = tk.Tk()
    tree_window = globals.tree_window
    set_icon(tree_window)
    tree_window.attributes("-zoomed", True)
    tree_window.configure(bg=globals.background_color)
    def on_closing():
        tree_window.destroy()
        tree_window.quit()
    tree_window.protocol("WM_DELETE_WINDOW", on_closing)
    tree_window.title(title)
    create_load_ui(tree_window)
    set_visibility_load_ui(False)
    create_treeview(tree_window, job_clicked, job_applied_clicked, apply_jobs_thread, bulk_apply, update_loading_label, on_background_action_end)
    set_visibility_treeview(False)
    create_login_ui(tree_window, start_login_thread)   # create a login ui here
    set_visibility_login_ui(False)
    # bindings for app
    tree_window.bind("<KeyPress-x>", lambda event,
        arg1=apply_job_thread, arg2=job_clicked: apply_job_ui(event, arg1, arg2)) #apply_job_ui)
    tree_window.bind("<KeyPress-c>", lambda event,
        arg1=scan_submit_response: open_text_input_popup(event, arg1))
    return tree_window

# def create_jobs_ui(job_data, job_clicked, job_applied_clicked, apply_job_thread, apply_jobs_thread, scan_all_seek_terms):
   

    # todo: make login in background
    # if not login_to_seek(email, password):
    #     # close main app? failure message first.
    #     # close_web_driver()
    #     set_visibility_login_ui(True)
    # else:
    #     set_visibility_treeview(True)

    # ui = create_jobs_ui(globals.job_data, job_clicked, job_applied_clicked, apply_job_thread, apply_jobs_thread, scan_all_seek_terms)
    # ui.mainloop() # update or mainloop or update_idletasks

# tree_window.bind("<KeyPress-b>", open_text_input_popup)
# tree_window.bind("<KeyPress-v>", apply_job_ui)
# tree_window.bind("<KeyPress-n>", toggle_loading_ui)
# tree_window.bind("<KeyPress-m>", toggle_treeview)