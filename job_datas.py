import json
from job_state import JobState

def save_json(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file)
        print(" - Data [" + str(len(data)) + "] was saved to [" + file_name + "]")

def load_json(file_name):
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
            print(" - Data [" + str(len(data)) + "] was loaded from [" + file_name + "]")
            return data
    except:
        print("File not found [" + file_name + "]")
        return []

# keeps the data for each job
class JobDatas:
    def __init__(self):
        self.job_ids = [ ]
        self.job_titles = [ ]
        self.job_urls = [ ]
        self.job_states = [ ]
        #self.new_job_states = [ ]

    def load_data(self):
        json_ext = '.json'
        self.job_ids = load_json('job_ids' + json_ext)
        self.job_titles = load_json('job_titles' + json_ext)
        self.job_urls = load_json('job_urls' + json_ext)
        self.job_states = load_json('job_states' + json_ext)
        job_ids_length = len(self.job_ids)
        if (job_ids_length != len(self.job_titles)):
            print("  Resetting job_titles as length not right [" + str(len(self.job_titles)) + " not " + str(job_ids_length) + "].")
            self.job_titles = [ ]
            for job_id in self.job_ids:
                self.job_titles.append('-')
        # time.sleep(56)
        if (not (job_ids_length == len(self.job_titles) and job_ids_length == len(self.job_urls) and job_ids_length == len(self.job_states))):
            print("Length of loaded data not equal to [" + str(job_ids_length) + "].")
            print("  job_titles [" + str(len(self.job_titles)) + "].")
            print("  job_urls [" + str(len(self.job_urls)) + "].")
            print("  job_states [" + str(len(self.job_states)) + "].")
            return False
        #for job_id in self.job_ids:
        #    self.new_job_states.append(0)
        return True

    def save_data(self):
        json_ext = '.json'
        save_json('job_ids' + json_ext, self.job_ids)
        save_json('job_titles' + json_ext, self.job_titles)
        save_json('job_urls' + json_ext, self.job_urls)
        save_json('job_states' + json_ext, self.job_states)