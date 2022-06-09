from asyncio.windows_events import NULL
from statistics import mode
from django.db import models

# Create your models here.
class ProgrammingLanguage(models.Model):
    name=models.CharField(max_length=255)
    id= models.AutoField(unique=True, primary_key=True, null=False)
    compileCommand=models.TextField(default=NULL)
    executeCommand=models.TextField(null=False)
class Executable(models.Model):
    status=models.CharField(max_length=255)
    userCode=models.TextField()
    userLanguage=models.IntegerField()
    generatorCode=models.TextField()
    generatorLanguge=models.IntegerField()
    editorialCode=models.TextField()
    editorialLanguage=models.IntegerField()
    queueNo=models.AutoField(primary_key=True)
