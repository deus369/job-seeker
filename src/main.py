import time
import pathlib
from data.job_datas import JobDatas
from data.job_state import JobState
from data.selected_job import SelectedJob
from web.web_scanner import *
from ui.job_seeker_ui import *
from ui.treeview import *
from ui.login_ui import *
from util.core_util import *

# keys: (z) apply jobs (x) apply job  (c) scan
# z to apply for multiple jobs
# c to open scanner and scan more jobs
# need to make scanning background thread
# need a delete button
# also, make ui for actions hide treeview and just be fullscreen in window, instead of the hack solution i have

is_clear = False        # False True
is_headless = True      # False True

# "https://hk.jobsdb.com/hk/search-jobs/game-designer")
def main():
    ui = create_window(job_clicked, job_applied_clicked, apply_job_thread, apply_jobs_thread)
    set_visibility_load_ui(True)
    update_loading_label("Loading")
    update_loading_label2("~")
    ui.update()
    if open_web_driver(is_headless) is None:
        return
    if not is_clear:
        globals.job_data.load_data()
        create_treeview_loaded_jobs(globals.job_data)
        # print("Totally found [" + str(len(job_data.job_ids)) + "] jobs.")
    set_visibility_load_ui(False)
    set_visibility_login_ui(True)
    ui.mainloop()
    close_web_driver()

main()

    
# change workflow to just a main app with a login page
#login_ui = spawn_login_ui(on_logged_in)
#login_ui.mainloop()
#geckodriver_filepath = str(pathlib.Path(__file__).parent.parent.resolve()) + "/"
# print("Current directory:", geckodriver_filepath)

# quick todo
# add middle label for loading ui, so i know what step the web actions is up to
# seperate files of jobs into seperate ones
# show loading ui for loading files, and show a proper progress 3 / 4802

# cover letters
# a check cover letters function
# a select cover letter drop down
# load / save cover letter options

# stats
# a pie chart for jobs applied to
# a pie chart for job applications that have been removed

# search terms
# save/load search terms
# a treeview of search terms
# delete search terms
# a refresh for search term where it scans in background thread
#   create a new geckodriver as a background thread for this operation
