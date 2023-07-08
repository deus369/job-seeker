# global variables
import os
from data.selected_job import SelectedJob
from data.job_datas import JobDatas

# paths
# geckodriver_path = '/usr/local/bin/geckodriver'
# geckodriver_filepath = os.getcwd() + "/"    # current path is geckodriver path
geckodriver_filepath = "/usr/bin/"    # current path is geckodriver path
firefox_filepath = "/usr/bin/firefox"
seek_url = "https://hk.jobsdb.com/hk"
search_addition_url = "/search-jobs/"
cover_letter_name = "marz_tierney_cover_letter.pdf"
login_directory = "~/.config/job_seeker.txt"
# geckodriver
driver = None
# settings
background_color = '#111111'
foreground_color = "#666666" # "white" # '#111111'
font_color = "#AAAAAA" # "white" # '#111111'
active_color = "#333333" # "white" # '#111111'
# data
is_performing_action = False
selected_job = SelectedJob()
job_data = JobDatas()
# ui
tree_window = None
tree = None
login_ui = None
load_ui = None

# url_hk_jobsdb = "https://hk.jobsdb.com/hk/search-jobs/"
