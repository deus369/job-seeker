import time
from data.job_datas import JobDatas
from data.job_state import JobState
from data.selected_job import SelectedJob
from web.web_scanner import *
from web.jobsdb import *
from ui.job_seeker_ui import *
from ui.treeview import *
from ui.login_ui import *
from ui.loading_ui import *
from util.core_util import *
import globals

# apply for a job when clicked ui
def job_clicked(job_index, job_title, url, is_confirm):
    if globals.job_data.job_states[job_index] != int(JobState.NONE.value):
        print(" !!! Job already applied for [" + job_title + "] is [" + JobState(globals.job_data.job_states[job_index]).name + "]")
        return 0
    response = (not is_confirm) or messagebox.askyesno("Confirm", "Apply for [" + job_title + "]?")
    if response:
        apply_response = apply_for_job(url)
        if apply_response != int(JobState.NONE.value):
            globals.job_data.job_states[job_index] = apply_response
            globals.job_data.save_data()
            return apply_response
    return 0

def job_applied_clicked(job_index, job_title):
    if (globals.job_data.job_states[job_index] == int(JobState.APPLIED.value)):
        print(" !!! Job is already in JobState.APPLIED state.")
        return False
    response = messagebox.askyesno("Confirm", "Applied before for [" + job_title + "]?")
    if response:
        globals.job_data.job_states[job_index] = int(JobState.APPLIED.value)
        globals.job_data.save_data()
        return True
    return False

def apply_jobs_thread(selected_jobs, job_clicked, update_row_job_state, update_label, on_background_action_end):
    i = 0
    jobs_count = str(len(selected_jobs))
    for selected_job in selected_jobs:
        i = i + 1
        if selected_job.index != -1:
            update_label("Job [" + str(i) + "/" + jobs_count + "]")
            update_loading_label2(selected_job.job_title)
            job_response = job_clicked(selected_job.index, selected_job.job_title, selected_job.url, False)
            update_row_job_state(job_response, selected_job.row)
        else:
            update_label("Job Bad Index [" + str(i) + "/" + jobs_count + "]")
            update_loading_label2("~")
            time.sleep(2)
        # time.sleep(0.5)
    on_background_action_end()

def apply_job_thread(selected_job, job_clicked, update_row_job_state, update_label, on_background_action_end):
    if selected_job.index != -1:
        update_label("Applying for job: " + selected_job.job_title)
        job_response = job_clicked(selected_job.index, selected_job.job_title, selected_job.url, False)
        update_row_job_state(job_response, selected_job.row)
        update_label("Finished Applying for job")
    else:
        update_label("Job not selected.")
    time.sleep(1)
    on_background_action_end()

# def on_logged_in(email, password):
#     # todo: make login in background
#     if not login_to_seek(email, password):
#         close_web_driver()
#         return
#     ui = create_jobs_ui(globals.job_data, job_clicked, job_applied_clicked, apply_job_thread, apply_jobs_thread, scan_all_seek_terms)
#     ui.mainloop() # update or mainloop or update_idletasks
