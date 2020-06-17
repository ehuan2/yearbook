import os

# adding in the config class that will 
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')