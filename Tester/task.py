import string
from time import sleep
from django.contrib.auth.models import User
from celery import shared_task
from .models import *
@shared_task
def checkOutput():
    sleep(2)
    print("Done")
    sleep(2)