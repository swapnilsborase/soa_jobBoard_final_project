# config.py

import os

class Config:
   MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/jobBoard_register_database")

#import os
#from dotenv import load_dotenv

# Load environment variables from .env file
#load_dotenv()

#class Config:
 #   MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://ssb:visa1421@cluster0.xc20d.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
  #  MONGO_DBNAME = "jobBoard_register"




