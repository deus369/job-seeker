

def test_login():
    open_web_driver(False)
    if login_to_seek(email, password):
        print("Login Success.")
    print("Finished login")
    time.sleep(15)
    close_web_driver()

def test_apply():
    # test_url = "https://hk.jobsdb.com/hk/en/job/machine-learning-engineer-autonomous-robotics-100003010003500"
    # test_url = "https://hk.jobsdb.com/hk/en/job/software-engineer-multimedia-and-robotics-fresh-graduates-welcome-100003009998403"
    # test_url = "https://hk.jobsdb.com/hk/en/job/senior-junior-control-engineer-robotics-and-automation-system-100003009982663"
    test_url = "https://hk.jobsdb.com/hk/en/job/senior-junior-mechanical-engineer-robotics-and-automation-system-100003009982664"
    open_web_driver(False)
    if login_to_seek(email, password):
        time.sleep(4)
        apply_for_job(test_url)
    print("Finished login")
    time.sleep(15)
    close_web_driver()
    
# test_login()
# test_apply()