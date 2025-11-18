import yaml
import os
import keyring


class Config_Manager():
    def __init__(self):
        self.service_name = "TheFoolVRCAI"
        with open('Core/config/config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)



    def get(self, id_path):
        ids = id_path.split(".")

        value = self.config
        try:
            for id in ids:
                value = value[id]
            return value
        
        except(TypeError, ValueError):
            return 
        
    def set(self, id_path, new_val):
        ids = id_path.split('.')
        value = self.config 
        value[ids[0]] [ids[1]] = new_val
        with open('Core/config/config.yaml', 'w') as file:
            yaml.dump(value, file, default_flow_style=False)

    def get_keyring(self,key_name):
        return keyring.get_password(self.service_name, key_name)
        
    
    def set_keyring(self, key_name, value):
        keyring.set_password(self.service_name, key_name, value)
        return True