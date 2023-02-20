from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.options import Log
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import InvalidSessionIdException
import time
import os
import globals
from data.job_state import JobState

driver_headless = True
is_disable_submission = False

def open_web_driver(is_headless):
    firefox_filepath = "/usr/bin/firefox"
    # log_path = "/var/log/" # os.path.expanduser("~/geckodriver.log")
    log_path = "/tmp/geckodriver.log" # "/dev/null" # None # "/tmp/geckodriver.log"
    driver_headless = is_headless
    print("Firefox filepath is [" + firefox_filepath + "]")
    print("Geckodriver filepath is [" + globals.geckodriver_filepath + "]")
    print("Log filepath is [" + str(log_path) + "]")
    options = webdriver.FirefoxOptions()
    options.binary_location = firefox_filepath
    options.profile = None
    if (is_headless):
        options.add_argument("--headless")
    service = Service(globals.geckodriver_filepath + "geckodriver", log_path=log_path) # globals.geckodriver_path)
    # service.start() # Initialize web globals.driver
    driver = webdriver.Firefox(service=service, options=options) #, log_path = log_path)
    print(" + Opened Firefox globals.driver.")
    globals.driver = driver
    return driver

def check_driver_status():
    try:
        test_url = globals.driver.current_url
        return True
    except: # (NoSuchWindowException, InvalidSessionIdException): # selenium.common.exceptions. NoSuchWindowException
        print("check_driver_status: Driver broken, restarting globals.driver.")
        open_web_driver(driver_headless)
        if login_to_seek_again():
            return True
    return False

def close_web_driver():
    globals.driver.quit()   # Close the browser

def get_parent(element):
    return element.find_element(By.XPATH, '..')

def check_tag(element, tag):
    if (not element is None and hasattr(element, 'tag_name') and element.tag_name == tag):
        return True
    else:
        return False

def check_parents(element, tag_a, tag_b, tag_c):
    parent = get_parent(element)
    if (check_tag(parent, tag_a)):
        parent2 = get_parent(parent)
        if (check_tag(parent2, tag_b)):
            parent3 = get_parent(parent2)
            if (check_tag(parent3, tag_c)):
                return True
    return False


# new_tab = wait.until(EC.new_window_is_opened(original_handles))
# new_tab = wait.until(EC.new_window_is_opened(original_handles))
# # Switch to the new tab
# globals.driver.switch_to.window(new_tab)
# if not "hk.jobsdb.com" in globals.driver.current_url:
#     print("New job tab was not on website [" + globals.driver.current_url + "]")
#     time.sleep(8)
#     return 2

# wait.until(lambda globals.driver: globals.driver.execute_script("return document.readyState") == "complete")
# wait.until(EC.presence_of_element_located((By.ID, "element_id")))
# wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
# wait.until(EC.js_returns_value("return document.readyState === 'complete'"))
# wait.until(EC.new_window_is_opened(original_handles))
# wait.until(EC.number_of_windows_to_be(len(original_handles) + 1))
    # print("New Tab was opened.")
    # wait = WebDriverWait(globals.driver, 16)
    # print("Switched tab [" + globals.driver.current_url + "]")
# wait.until(lambda globals.driver: globals.driver.current_url != new_url)    # wait for the link url to redirect
# Wait for an element on the new tab to be visible

# input_elements = globals.driver.find_elements(By.XPATH, "//input")
# for element in input_elements:
#     type_attr = element.get_attribute("type")
#     if (type_attr == "text"):
#         if (check_parents(element, "span", "div", "fieldset")):
#             email_element = element
#             print("Email Element Found.")
#     if (type_attr == "password"):
#         if (check_parents(element, "span", "div", "fieldset")):
#             password_element = element
# if email_element is None or password_element is None:
#     print("Input Elements not found.")
#     return False
                # if (job_id not in job_data.job_ids):
                #     job_data.job_ids.append(job_id)
                #     job_data.job_titles.append(job_title)
                #     job_data.job_urls.append(job_link)
                #     job_data.job_states.append(0)
                    # print(" + [" + job_id + "] " + element.text)
                    # job_data.new_job_states.append(1)
                    # apply for this job?
    # globals.driver.switch_to.window(original_handles)   # Switch to the parent window

    # test closed tab
    # globals.driver.get(globals.seek_url)
    # wait = WebDriverWait(globals.driver, 22)
    # print("Tab was closed. Finished applying for job.")

    # print("globals.geckodriver_path? " +  globals.geckodriver_path)
    #options = Options()
    #options.add_argument('--disable-dev-shm-usage')
    #options.add_argument('--no-sandbox')
    # profile_path = "" # '/path/to/firefox/profile'
    #options.profile = webdriver.FirefoxProfile(profile_path)
    # options.config
    # "/snap/firefox/current/firefox.launcher" # "/snap/bin/firefox"
    # options.binary_location = r'/usr/lib/firefox-esr/firefox-es'
    # Create a new service object and set the path of geckodriver binary to it
    # geckodriver_filepath = str(pathlib.Path(__file__).parent.resolve()) + "/"
    # firefox_filepath = "/usr/bin/firefox-esr"
    # print("Geckodriver filepath is [" + geckodriver_filepath + "]")
    #options.log.level = "NONE" # "TRACE"
    #options.log = Log() #.path = log_path
    # options.set_capability("moz:logging", None)
    # options.set_capability("moz:logging", {})  # Disable logging
    #del options.capabilities["moz:logging"]
    # options.log_path= "./Log/geckodriver.log"
    # options.log_path = log_path
    # options.service_log_path = log_path
    #options.add_argument('--disable-logging') 
    #options.add_argument('--log-level 3') 
    # options.add_experimental_option("excludeSwitches", ["enable-logging"])