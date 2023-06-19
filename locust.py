from locust import HttpUser, TaskSet, task, between
from random import choice, uniform
from datetime import datetime
import json

currentID = 0

vals = {
    "pulse": {
        "top":170,
        "bottom":100
    },
    "systolic_bp": {
        "top":125,
        "bottom":80
    },
    "diastolic_bp": {
        "top":95,
        "bottom":65
    },
    "sugar": {
        "top":115,
        "bottom":70
    },
    # "breaths": {
    #     "top":16,
    #     "bottom":12
    # },
    "temperature": {
        "top":37,
        "bottom":36
    },
    "oxygen": {
        "top":100,
        "bottom":36,
        "max": 100
    },
    "co2": {
        "top":29,
        "bottom":23
    },
    "alcohol": {
        "top":0.05,
        "bottom":0
    },
    "cortizol": {
        "top":23,
        "bottom":6
    },
    "wbc": {
        "top":0.15,
        "bottom":0
    },
}


class RandomWalkDataGenerator:
    def __init__(self):
        self.step_size = { key: [-((vals[key]["top"] - vals[key]["bottom"])/7), 0,0, ((vals[key]["top"] - vals[key]["bottom"])/7) ] for key in vals.keys()}
        self.data = { key: (vals[key]["top"] + vals[key]["bottom"])/2 for key in vals.keys()}
        
        
    def generate_data(self):
        
        self.data["timestamp"] = datetime.now().isoformat()

        for param in self.step_size.keys():
            self.data[param] = min(max(self.data[param] + (choice(self.step_size[param]) * choice([1.,0.75,1.25,1.,1.,1.5,0.3])), vals[param]["bottom"]*0.3), vals[param]["top"]*2)
            

        return self.data


class UserBehavior(TaskSet):
    
    currentUserID = None
    
    def on_start(self):
        global currentID
        self.currentUserID = currentID
        currentID += 1
    
    def __init__(self, parent):
        super().__init__(parent)
        self.data_generator = RandomWalkDataGenerator()

    @task
    def send_request(self):
        user_id = self.currentUserID
        data = self.data_generator.generate_data()
        url = f'/rest/person/{user_id}'
        self.client.put(url, json=data)


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 1000
    max_wait = 5000

# http://161.156.199.29:9080/com.ibm.cicsdev.mimuw02