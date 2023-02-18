from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
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

def open_web_driver(geckodriver_filepath, is_headless):
    global driver
    firefox_filepath = "/usr/bin/firefox"
    # log_path = "/var/log/" # os.path.expanduser("~/geckodriver.log")
    log_path = "/dev/null" # None # "/tmp/geckodriver.log"
    driver_headless = is_headless
    print("Firefox filepath is [" + firefox_filepath + "]")
    print("Geckodriver filepath is [" + geckodriver_filepath + "]")
    print("Log filepath is [" + str(log_path) + "]")
    options = webdriver.FirefoxOptions()
    options.binary_location = firefox_filepath
    # options.log_path= "./Log/geckodriver.log"
    # options.log_path = log_path
    #options.add_argument('--disable-logging') 
    #options.add_argument('--log-level 3') 
    # options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.profile = None
    if (is_headless):
        options.add_argument("--headless")
    service = Service(geckodriver_filepath + "geckodriver") # globals.geckodriver_path)
    # service.start() # Initialize web driver
    driver = webdriver.Firefox(service=service, options=options, log_path = log_path)
    print(" + Opened Firefox driver.")
    return driver

def check_driver_status():
    try:
        test_url = driver.current_url
        return True
    except: # (NoSuchWindowException, InvalidSessionIdException): # selenium.common.exceptions. NoSuchWindowException
        print("check_driver_status: Driver broken, restarting driver.")
        open_web_driver(driver_headless)
        if login_to_seek_again():
            return True
    return False

def close_web_driver():
    driver.quit()   # Close the browser

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

def scan_job_page(job_data, base_url, page_no, on_add_job):
    url = base_url + "/" + str(page_no)
    # Navigate to website
    print("Navigating [" + str(len(job_data.job_ids)) + "] to URL [" + url + "]")
    driver.get(url)
    wait = WebDriverWait(driver, 12)
    if (driver.current_url == base_url):
        print("URL [" + base_url + "] ended on Page [" + str(page_no - 1) + "]")
        return False
    # print("Arrived at url: " + driver.current_url)
    # Find all span elements
    span_elements = driver.find_elements(By.XPATH, "//span")
    for element in span_elements:
        try:
            element_text = element.text
        except StaleElementReferenceException:
            continue
        if (element_text != ""):
            if (check_parents(element, "div", "a", "h1")):
                link_element = get_parent(get_parent(element))
                job_link = link_element.get_attribute("href")
                job_id = job_link.rsplit('-', 1)[-1].split('?')[0]
                job_title = element.text
                if job_id in job_data.job_ids:
                    index = job_data.job_ids.index(job_id)
                    job_data.job_titles[index] = job_title
                    job_data.job_urls[index] = job_link
                else:
                    i = len(job_data.job_ids)
                    job_data.job_ids.append(job_id)
                    job_data.job_titles.append(job_title)
                    job_data.job_urls.append(job_link)
                    job_data.job_states.append(0)
                    if callable(on_add_job):
                        on_add_job(i, job_id, job_title, job_link)


                #else:
                #    print(" ~ duplicate job id [" + job_id + "]")
                # get url for link of job
    return True

def scan_jobs(job_data, seek_term, on_add_job):
    url = globals.seek_url + globals.search_addition_url + seek_term # url_hk_jobsdb
    print("Jobs URL: " + url)
    i = 0
    while (True):
        i = i + 1
        if (not scan_job_page(job_data, url, i, on_add_job)):
            break

def scan_all_seek_terms(job_data, job_seek_terms, on_add_job):
    for seek_term in job_seek_terms:
        print("Seeking jobs with search term [" + seek_term + "]")
        scan_jobs(job_data, seek_term, on_add_job)

def login_to_seek_again():
    login_to_seek(email_cache, password_cache)

def login_to_seek(email, password):
    global email_cache
    email_cache = email
    global password_cache
    password_cache = password
    # first go to page
    driver.get(globals.seek_url)
    wait = WebDriverWait(driver, 12)
    print(" > Seek Page Arrived.")
    login_element = driver.find_element(By.XPATH, "//*[contains(@title, 'Login')]")
    if not login_element:
        print("Login element null.")
        return False
    print(" > Clicking Login Page Link.")
    login_element.click()
    wait = WebDriverWait(driver, 12)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='text']")))
    print(" > Login Page Arrived.")
    try:
        email_element = driver.find_element(By.XPATH, "//input[@type='text']")
    except NoSuchElementException:
        print("email_element not found.")
        return False
    try:
        password_element = driver.find_element(By.XPATH, "//input[@type='password']")
    except NoSuchElementException:
        print("password_element not found.")
        return False
    email_element.clear()
    email_element.send_keys(email)
    password_element.clear()
    password_element.send_keys(password)
    button_elements = driver.find_elements(By.XPATH, "//button")
    for element in button_elements:
        if (element.text == "Log in" and check_parents(element, "div", "fieldset", "div")):
            print(" > Clicking Login Button.")
            element.click()
            break
    wait = WebDriverWait(driver, 12)
    print(" > Logged in to [" + globals.seek_url + "].")
    wait.until(lambda driver: driver.current_url == globals.seek_url)
    return True

# Returns the job state enum value, 0, 1, 2
def apply_for_job(apply_url):
    check_driver_status()
    driver.get(apply_url)
    wait = WebDriverWait(driver, 12)
    print(" > Job Page Arrived\n[" + driver.current_url + "]")
    try:
        apply_button = driver.find_element(By.XPATH, "//a[@data-automation='applyNowButton']")
    except NoSuchElementException:
        print("apply_button not found.")
        return 0
    # Get the current window handles
    original_handles = driver.window_handles
    try:
        apply_button.click()
    except: # WebDriverException:
        print("apply_button.click had a exception.")
        return 0
    wait = WebDriverWait(driver, 10)
    # Get the new window handles
    new_handles = driver.window_handles
    if original_handles == new_handles:
        print("New tab did not open.")
        return 0
    # check new tab
    new_tab = list(set(new_handles) - set(original_handles))[0] # Get the new window handle
    driver.switch_to.window(new_tab)
    try:
        wait.until(lambda driver: driver.current_url != "about:blank")  # Wait for the new tab to load
    except TimeoutException:
        print("Timed out waiting for about:blank to redirect")
        return 0
    
    new_url = driver.current_url
    # If the link is external
    if "PopUpJobApplicationExternalLink" in new_url or not "hk.jobsdb.com" in new_url:
        print(" > New job tab was not on website [" + new_url + "]")
        driver.close()  # Close the tab
        driver.switch_to.window(driver.window_handles[0])  # Switch to first tab
        return int(JobState.EXTERNAL_LINK.value)

    # continue loading new tab
    wait = WebDriverWait(driver, 10) # wait for new tab to load
    # wait.until(EC.visibility_of_element_located((By.ID, "btn-submit")))
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@id='txt-upload-coverLetter']")))
    except TimeoutException:
        print("Timed out waiting for txt-upload-coverLetter to load")
        return 0
    
    print(" > Job Apply Page!\n[" + driver.current_url + "]")
    time.sleep(1.2) # wait for it to load the cover letters
    # chose cover letter - click open cover letter selector
    try:
        add_cover_letter_span = driver.find_element(By.XPATH, "//span[@id='txt-upload-coverLetter']")
    except NoSuchElementException:
        print("add_cover_letter_span not found.")
        return 0
    try:
        add_cover_letter_span.click()
    except: #  WebDriverException:
        print("add_cover_letter_span.click had a exception.")
        return 0
    print(" > Clicked button for cover letter.")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//button[*/*[text()='Done']]")))  # wait for it to load
    # select cover letter for the job
    try:
        radio_button = driver.find_element(By.XPATH, "//div[contains(text(), '" + globals.cover_letter_name + "')]")
        # '//input[@name="r-documents-coverLetter"]')
    except NoSuchElementException:
        print("radio_button not found.")
        return 0
    try:
        radio_button.click()
    except: #  WebDriverException:
        print("radio_button.click had a exception.")
        return 0

    print(" > Selected cover letter.")
    # click done
    try:
        done_button = driver.find_element(By.XPATH, "//button[*/*[text()='Done']]")
    except NoSuchElementException:
        print("done_button not found.")
        return 0
    try:
        done_button.click()
    except: # WebDriverException:
        print("done_button.click had a exception.")
        return 0

    if not is_disable_submission:
        try:
            submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        except NoSuchElementException:
            print("submit_button not found.")
            return 0
        try:
            submit_button.click()
        except: #  WebDriverException:
            print("submit_button.click had a WebDriverException exception.")
            return 0
        print(" > Submit button clicked")

        # wait for tab to close?
        wait = WebDriverWait(driver, 22)
        try:
            wait.until(lambda driver: "apply-success" in driver.current_url)
        except TimeoutException:
            print("Timed out waiting for apply-success to load")
            return 0
    
    print(" > Success Applying for job.")
    driver.close()  # Close the tab
    driver.switch_to.window(driver.window_handles[0])  # Switch to first tab
    return int(JobState.APPLIED.value)

# new_tab = wait.until(EC.new_window_is_opened(original_handles))
# new_tab = wait.until(EC.new_window_is_opened(original_handles))
# # Switch to the new tab
# driver.switch_to.window(new_tab)
# if not "hk.jobsdb.com" in driver.current_url:
#     print("New job tab was not on website [" + driver.current_url + "]")
#     time.sleep(8)
#     return 2

# wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
# wait.until(EC.presence_of_element_located((By.ID, "element_id")))
# wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
# wait.until(EC.js_returns_value("return document.readyState === 'complete'"))
# wait.until(EC.new_window_is_opened(original_handles))
# wait.until(EC.number_of_windows_to_be(len(original_handles) + 1))
    # print("New Tab was opened.")
    # wait = WebDriverWait(driver, 16)
    # print("Switched tab [" + driver.current_url + "]")
# wait.until(lambda driver: driver.current_url != new_url)    # wait for the link url to redirect
# Wait for an element on the new tab to be visible

# input_elements = driver.find_elements(By.XPATH, "//input")
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
    # driver.switch_to.window(original_handles)   # Switch to the parent window

    # test closed tab
    # driver.get(globals.seek_url)
    # wait = WebDriverWait(driver, 22)
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