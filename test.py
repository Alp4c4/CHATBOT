from random import randint
import firebase_admin
from firebase_admin import credentials,storage
from firebase_admin import firestore
from matplotlib import image 
cred=credentials.Certificate("depreesion-4eb38-firebase-adminsdk-r6lnp-402912a06a.json")
firebase_admin.initialize_app(cred,{'storageBucket':'gs://depreesion-4eb38.appspot.com'})
import numpy as np
import cv2
bucket=storage.bucket()
image=bucket.get_blob('normal.png')
