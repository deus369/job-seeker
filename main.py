from web_scanner import *
from job_seeker_ui import *
from treeview import *
from job_datas import JobDatas
from job_state import JobState
from selected_job import SelectedJob
from login_ui import *
import time

# keys: (z) apply jobs (x) apply job  (c) scan

# z to apply for multiple jobs
# b to open scanner and scan more jobs
# need to make scanning background thread
# need a delete button
# also, make ui for actions hide treeview and just be fullscreen in window, instead of the hack solution i have

is_clear = False        # False True
is_scan = False         # False True
is_headless = True      # False True 

# apply for a job when clicked ui
def job_clicked(job_data, job_index, job_title, url, is_confirm):
    if job_data.job_states[job_index] != int(JobState.NONE.value):
        print(" !!! Job already applied for [" + job_title + "] is [" + JobState(job_data.job_states[job_index]).name + "]")
        return 0
    response = (not is_confirm) or messagebox.askyesno("Confirm", "Apply for [" + job_title + "]?")
    if response:
        apply_response = apply_for_job(url)
        if apply_response != int(JobState.NONE.value):
            job_data.job_states[job_index] = apply_response
            job_data.save_data()
            return apply_response
    return 0

def job_applied_clicked(job_data, job_index, job_title):
    if (job_data.job_states[job_index] == int(JobState.APPLIED.value)):
        print(" !!! Job is already in JobState.APPLIED state.")
        return False
    response = messagebox.askyesno("Confirm", "Applied before for [" + job_title + "]?")
    if response:
        job_data.job_states[job_index] = int(JobState.APPLIED.value)
        job_data.save_data()
        return True
    return False

def apply_jobs_thread(job_data, selected_jobs, job_clicked, update_row_job_state, update_label, on_background_action_end):
    i = 0
    jobs_count = str(len(selected_jobs))
    for selected_job in selected_jobs:
        i = i + 1
        if selected_job.index != -1:
            update_label("Applying for Job [" + str(i) + "/" + jobs_count + "]: " + selected_job.job_title)
            job_response = job_clicked(job_data, selected_job.index, selected_job.job_title, selected_job.url, False)
            update_row_job_state(job_response, selected_job.row)
        else:
            update_label("Job Bad Index [" + str(i) + "/" + jobs_count + "]")
            time.sleep(2)
        time.sleep(0.5)
    on_background_action_end()

def apply_job_thread(job_data, selected_job, job_clicked, update_row_job_state, update_label, on_background_action_end):
    if selected_job.index != -1:
        update_label("Applying for job: " + selected_job.job_title)
        job_response = job_clicked(job_data, selected_job.index, selected_job.job_title, selected_job.url, False)
        update_row_job_state(job_response, selected_job.row)
        update_label("Finished Applying for job")
    else:
        update_label("Job not selected.")
    time.sleep(1)
    on_background_action_end()

def on_logged_in(email, password):
    # todo: make login in background
    if not login_to_seek(email, password):
        close_web_driver()
        return
    ui = create_jobs_ui(globals.job_data, job_clicked, job_applied_clicked, apply_job_thread, apply_jobs_thread, scan_all_seek_terms)
    ui.mainloop() # update or mainloop or update_idletasks

# "https://hk.jobsdb.com/hk/search-jobs/game-designer")
def main():
    if not is_clear:
        globals.job_data.load_data()
        # print("Totally found [" + str(len(job_data.job_ids)) + "] jobs.")
    global driver
    driver = open_web_driver(is_headless)
    login_ui = spawn_login_ui(on_logged_in)
    login_ui.mainloop()
    close_web_driver()

main()

# apply for jobs? print out info in a ui and ask if apply
# i = 0
# for job_id in new_job_ids:
#     # print(" + [" + job_id + "] " + element.text)
#     job_title = job_titles[i]
#     response = messagebox.askyesno(job_title, "Company [Generic X]\nSalary [Uknown]\n\nApply?")
#     if response:
#         applied_job_ids.append(job_id)
#         job_url = job_urls[i]
#         print("Applying for job at url: " + job_url)
#     # else:
#     #    print("Denied Job!")
#     i = i + 1
#     if (i == 6):
#         break

# after click this might be useful
#driver.current_url

# listbox.insert(tk.END,f"{id}")
# #label = tk.Label(listbox, text=f"{id}")
# #label.grid(row=i, column=0,padx=5,pady=5,sticky="w")
# button = tk.Button(listbox, text="Action", command=lambda:print("Clicked" + id))
# button.grid(row=i, column=1,padx=5,pady=5,sticky="e")
# listbox.insert(tk.END, button)
# # button.
# link = tk.Label(listbox, text=f"{url}", fg="blue", cursor="hand2")
# link.grid(row=i, column=2,padx=5,pady=5,sticky="e") # w
# link.bind("<Button-1>", lambda event, url=url: webbrowser.open(url))
# listbox.create_window(0, i * 20, window=button, ancmhor='nw')
# listbox.itemconfig(tk.END, window=link)

        # row = tree.identify_row(event.y)
        # column = tree.identify_column(event.x)
        # if (column == "#0"):
        #     print("Action clicked!")
        #     # webbrowser.open(url)
        # id = tree.item(row, column)["text"]
        # print("Item Row clicked: " + id + "::" + (column)) # str


    # update_label("Setting zoxel website")
    # driver.get("http://zoxel.duckdns.org")
    # time.sleep(3)
    # update_label("Url is: " + driver.current_url)
    # print("Url is: " + driver.current_url)
    # messagebox.showinfo("Success", "Long running action has finished.")
        # if is_scan:
        #     scan_all_seek_terms(job_data, job_seek_terms, 0)
        #     job_data.save_data()
        
# is_clear = True        # False True
# is_scan = True         # False True
# job_seek_terms = [ "game-designer" ] # , "3d-artist"
# "3d-artist", "ui-designer" 
# "Game Designer"
# "programmer", "robotics-engineer", "coder"