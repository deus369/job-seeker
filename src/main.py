import time
import os
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
# b to open scanner and scan more jobs
# need to make scanning background thread
# need a delete button
# also, make ui for actions hide treeview and just be fullscreen in window, instead of the hack solution i have

is_clear = False        # False True
# is_scan = False         # False True
is_headless = True      # False True

# "https://hk.jobsdb.com/hk/search-jobs/game-designer")
def main():
    if not is_clear:
        globals.job_data.load_data()
        # print("Totally found [" + str(len(job_data.job_ids)) + "] jobs.")
    global driver
    #geckodriver_filepath = str(pathlib.Path(__file__).parent.parent.resolve()) + "/"
    geckodriver_filepath = os.getcwd() + "/"
    print("Current directory:", geckodriver_filepath)
    driver = open_web_driver(geckodriver_filepath, is_headless)
    if driver is None:
        return
    login_ui = spawn_login_ui(on_logged_in)
    login_ui.mainloop()
    close_web_driver()

main()