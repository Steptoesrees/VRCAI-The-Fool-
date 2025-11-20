import yaml
import os


class Config_Manager():
    def __init__(self):
        self.service_name = "TheFoolVRCAI"
        with open('Core/config/config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)



    def get(self, id_path):
        with open('Core/config/config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)
        ids = id_path.split(".")

        value = self.config
        try:
            for id in ids:
                value = value[id]
            return value
        
        except(TypeError, ValueError):
            return 
        
    def set(self, id_path, new_val):
        with open('Core/config/config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)
        ids = id_path.split('.')
        value = self.config 
        value[ids[0]] [ids[1]] = new_val
        with open('Core/config/config.yaml', 'w') as file:
            yaml.dump(value, file, default_flow_style=False)
