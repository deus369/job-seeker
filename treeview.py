from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import threading
import globals
from job_state import JobState
from selected_job import SelectedJob
from loading_ui import *

# todo: Fix bulk_apply input passing.. a bit annoying

job_title_tag = "#0"
job_state_tag = "#1"
job_state_column = 0    # value index, -1 off normal index
apply_button_tag = "#2"
applied_button_tag = "#3"
url_column_tag = "#4"
id_tag = "#5"

def bulk_apply(event, tree, job_data, job_clicked, apply_jobs_thread, show_load_ui, update_loading_label, on_background_action_end):
    if globals.is_performing_action:
        return
    print(" > Bulk applying for jobs! Confirming?")
    tree_window = event.widget
    applying_count = str(len(tree.selection()))
    response = messagebox.askyesno("Confirm", "Apply for [" + applying_count + "] Jobs?")
    if response:
        globals.is_performing_action = True
        show_load_ui()
        selected_jobs = [ ]
        i = 0
        for row in tree.selection():
            item = tree.item(row)
            index = tree.index(row)
            values = item['values']
            # print("Applied for [" + str(i + 1) + "] out of [" + applying_count + "]")
            print(" -> Adding job [" + str(row) + "]") # - [" + str(values) + "]")
            job_title = get_cell_value(tree, item, row, job_title_tag)
            url = values[3] # tree.set(item, url_column_tag)
            job = SelectedJob()
            job.item = item
            job.row = row
            job.index = index
            job.job_title = job_title
            job.url = url
            selected_jobs.append(job)
            # job_response = job_clicked(job_data, index, job_title, url, False)
            # if job_response != 0:
            #    tree.set(row, column=job_state_column, value=JobState(job_response).name)
            i = i + 1
        threading.Thread(target=apply_jobs_thread, args=(job_data, selected_jobs, job_clicked, update_row_job_state, update_loading_label, on_background_action_end)).start()


def update_row_job_state(job_response, row):
    global tree
    if job_response != 0:
        tree.set(row, column=job_state_column, value=JobState(job_response).name)

def get_cell_value(tree, item, row, column):
    if (column == "#0"):
        return tree.item(row)["text"]
    try:
        return tree.set(item, column)
    except:
        return tree.item(row)["text"]

def toggle_treeview(event):
    print("Toggling tree visibility.")
    global tree
    is_visible = not tree.winfo_ismapped()
    set_visibility_treeview(is_visible)

def create_ui_row(tree, i, id, title, url, job_state): # , new_job):
    tree.insert("", tk.END, text=title, values=(JobState(job_state).name, "[Apply]", "[Applied]", url, id), tags=("odd" if i % 2 else "even", "applied" if job_state == JobState.APPLIED else "none"))
    # , "new" if new_job else "old",))

def set_visibility_treeview(is_visible):
    global tree
    global scrollbar_y
    global scrollbar_x
    if is_visible:
        tree.grid()
        scrollbar_x.grid()
        scrollbar_y.grid()
    else:
        tree.grid_remove()
        scrollbar_x.grid_remove()
        scrollbar_y.grid_remove()

def create_treeview(tree_window, job_data, job_clicked, job_applied_clicked, apply_jobs_thread, bulk_apply, show_load_ui, update_loading_label, on_background_action_end):
    # create our treeview
    global tree
    tree = ttk.Treeview(tree_window, columns=("title","state","action","set_applied","id","url"))
    # create scrollbars
    global scrollbar_y
    global scrollbar_x
    scrollbar_y = tk.Scrollbar(tree_window, orient="vertical", command=tree.yview)
    scrollbar_y.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    scrollbar_x = tk.Scrollbar(tree_window, orient="horizontal", command=tree.xview)
    scrollbar_x.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    #, background="#222222", bd=2, relief="solid")
    #, selectmode=tk.SINGLE, background="white", bd=2, relief="solid")
    tree.heading(job_title_tag, text="title", anchor="w")
    tree.heading(job_state_tag, text="state", anchor=tk.W)
    tree.heading(apply_button_tag, text="[apply]", anchor=tk.W)
    tree.heading(applied_button_tag, text="[applied]", anchor=tk.W)
    tree.heading(url_column_tag, text="url", anchor="w")
    tree.heading(id_tag, text="id", anchor="w")
    tree.column(job_title_tag, width=666)
    tree.column(job_state_tag, width=120)
    tree.column(apply_button_tag, width=120)
    tree.column(applied_button_tag, width=120)
    tree.column(url_column_tag, width=620)
    tree.column(id_tag, width=220)
    tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    # tree.configure(column=("jobstate", "action", "applied"), width=100)
    # tree.pack()
    # create our tree rows
    for i, id in enumerate(job_data.job_ids):
        create_ui_row(tree, i, id, job_data.job_titles[i], job_data.job_urls[i], job_data.job_states[i])

    tree.tag_configure("even", background="#222222", foreground=globals.font_color)
    tree.tag_configure("odd", background="#111111", foreground=globals.font_color)
    # tree.tag_configure("new", background="#331111")
    tree.tag_configure("applied", background="#661111")
    # for keypresses in our tree
    # def print_selection(event):
    #    print(tree.selection())
    # tree.bind("<KeyPress-x>", print_selection)
    # tree.bind("<KeyPress-z>", bulk_apply(tree_window))
    tree_window.bind("<KeyPress-z>", lambda event, arg1=tree, arg2=job_data, arg3=job_clicked, arg4=apply_jobs_thread, arg5=show_load_ui, arg6=update_loading_label, arg7=on_background_action_end: bulk_apply(event, arg1, arg2, arg3, arg4, arg5, arg6, arg7))

    # for clicking our tree
    def tree_clicked(event):
        if globals.is_performing_action:
            return
        item = tree.identify('item', event.x, event.y)
        if item:
            column = tree.identify_column(event.x)
            row = tree.identify_row(event.y)
            index = tree.index(row)
            url = tree.set(item, url_column_tag)
            job_title = get_cell_value(tree, item, row, job_title_tag)
            cell_value = get_cell_value(tree, item, row, column)
            print(f"cell {column}x{row} at {index} clicked: {cell_value}")
            # global selected_job
            globals.selected_job.item = item
            globals.selected_job.column = column
            globals.selected_job.row = row
            globals.selected_job.index = index
            globals.selected_job.job_title = job_title
            globals.selected_job.url = url
            # respond to clicks
            if (column == apply_button_tag):
                print("Action clicked [" + row + "] [" + job_title + "]")
                job_response = job_clicked(job_data, index, job_title, url, True)
                if job_response != 0:
                    tree.set(row, column=job_state_column, value=JobState(job_response).name)
            elif (column == url_column_tag):
                print("URL clicked [" + url + "]")
                # url = job_urls[int(row)]
                response = messagebox.askyesno("URL", "Open for [" + job_title + "]?")
                if response:
                    webbrowser.open(url)
            elif (column == applied_button_tag):
                print("Applied before clicked [" + row + "] [" + job_title + "]")
                if (job_applied_clicked(job_data, index, job_title)):
                    tree.set(row, column=job_state_column, value=JobState.APPLIED.name)
    tree.bind("<Button-1>", tree_clicked, "+")