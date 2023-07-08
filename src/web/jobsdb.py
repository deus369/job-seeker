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
from web.web_scanner import *
from data.job_state import JobState

def scan_job_page(job_data, base_url, page_no, on_add_job):
    url = base_url + "/" + str(page_no)
    # Navigate to website
    print("Navigating [" + str(len(job_data.job_ids)) + "] to URL [" + url + "]")
    globals.driver.get(url)
    wait = WebDriverWait(globals.driver, globals.load_timeout)
    if (globals.driver.current_url == base_url):
        print("URL [" + base_url + "] ended on Page [" + str(page_no - 1) + "]")
        return False
    # print("Arrived at url: " + globals.driver.current_url)
    # Find all span elements
    span_elements = globals.driver.find_elements(By.XPATH, "//span")
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
    login_to_seek(email_cache, password_cache, None)

def login_to_seek(email, password, on_logged_in):
    global email_cache
    email_cache = email
    global password_cache
    password_cache = password
    # first go to page
    print(" > Navigating to Seek Page.")
    globals.driver.get(globals.seek_url)
    wait = WebDriverWait(globals.driver, globals.load_timeout)
    print(" > Seek Page Arrived.")
    login_element = globals.driver.find_element(By.XPATH, "//*[contains(@title, 'Login')]")
    if not login_element:
        print("Login element null.")
        return False
    print(" > Clicking Login Page Link.")
    login_element.click()
    wait = WebDriverWait(globals.driver, globals.load_timeout)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='text']")))
    print(" > Login Page Arrived.")
    try:
        email_element = globals.driver.find_element(By.XPATH, "//input[@type='text']")
    except NoSuchElementException:
        print("email_element not found.")
        return False
    try:
        password_element = globals.driver.find_element(By.XPATH, "//input[@type='password']")
    except NoSuchElementException:
        print("password_element not found.")
        return False
    email_element.clear()
    email_element.send_keys(email)
    password_element.clear()
    password_element.send_keys(password)
    button_elements = globals.driver.find_elements(By.XPATH, "//button")
    for element in button_elements:
        if (element.text == "Log in" and check_parents(element, "div", "fieldset", "div")):
            print(" > Clicking Login Button.")
            element.click()
            break
    wait = WebDriverWait(globals.driver, globals.load_timeout)
    print(" > Logged in to [" + globals.seek_url + "].")
    driver = globals.driver
    wait.until(lambda driver: globals.driver.current_url == globals.seek_url)
    if on_logged_in != None:
        on_logged_in()
    return True

# Returns the job state enum value, 0, 1, 2
def apply_for_job(apply_url):
    check_driver_status()
    driver = globals.driver
    globals.driver.get(apply_url)
    wait = WebDriverWait(globals.driver, globals.load_timeout)
    print(" > Job Page Arrived\n[" + globals.driver.current_url + "]")
    try:
        apply_button = globals.driver.find_element(By.XPATH, "//a[@data-automation='applyNowButton']")
    except NoSuchElementException:
        print("apply_button not found.")
        return 0
    # Get the current window handles
    original_handles = globals.driver.window_handles
    try:
        apply_button.click()
    except: # WebDriverException:
        print("apply_button.click had a exception.")
        return 0
    wait = WebDriverWait(globals.driver, globals.load_timeout)
    # Get the new window handles
    new_handles = globals.driver.window_handles
    if original_handles == new_handles:
        print("New tab did not open.")
        return 0
    # check new tab
    new_tab = list(set(new_handles) - set(original_handles))[0] # Get the new window handle
    globals.driver.switch_to.window(new_tab)
    try:
        wait.until(lambda driver: globals.driver.current_url != "about:blank")  # Wait for the new tab to load
    except TimeoutException:
        print("Timed out waiting for about:blank to redirect")
        return 0
    
    new_url = globals.driver.current_url
    # If the link is external
    if "PopUpJobApplicationExternalLink" in new_url or not "hk.jobsdb.com" in new_url:
        print(" > New job tab was not on website [" + new_url + "]")
        globals.driver.close()  # Close the tab
        globals.driver.switch_to.window(globals.driver.window_handles[0])  # Switch to first tab
        return int(JobState.EXTERNAL_LINK.value)

    # continue loading new tab
    wait = WebDriverWait(globals.driver, globals.load_timeout) # wait for new tab to load
    # wait.until(EC.visibility_of_element_located((By.ID, "btn-submit")))
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@id='txt-upload-coverLetter']")))
    except TimeoutException:
        print("Timed out waiting for txt-upload-coverLetter to load")
        return 0
    
    print(" > Job Apply Page!\n[" + globals.driver.current_url + "]")
    time.sleep(1.2) # wait for it to load the cover letters
    # chose cover letter - click open cover letter selector
    try:
        add_cover_letter_span = globals.driver.find_element(By.XPATH, "//span[@id='txt-upload-coverLetter']")
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
        radio_button = globals.driver.find_element(By.XPATH, "//div[contains(text(), '" + globals.cover_letter_name + "')]")
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
        done_button = globals.driver.find_element(By.XPATH, "//button[*/*[text()='Done']]")
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
            submit_button = globals.driver.find_element(By.XPATH, '//button[@type="submit"]')
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
        wait = WebDriverWait(globals.driver, globals.load_timeout)
        try:
            wait.until(lambda driver: "apply-success" in globals.driver.current_url)
        except TimeoutException:
            print("Timed out waiting for apply-success to load")
            return 0
    
    print(" > Success Applying for job.")
    globals.driver.close()  # Close the tab
    globals.driver.switch_to.window(globals.driver.window_handles[0])  # Switch to first tab
    return int(JobState.APPLIED.value)
