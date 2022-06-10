import string
from time import sleep
from django.contrib.auth.models import User
from celery import shared_task
from .models import *
testCaseLimit=1
@shared_task
def executeTask(queueid):
    newExecutable=Executable.objects.get(queueNo=queueid)
    for testcase in range(testCaseLimit):
        newTest=Test()
        generatorLanguage=ProgrammingLanguage.objects.get(id=newExecutable.generatorLanguage)
        generatorFile=open('./ProgramFiles/generator'+generatorLanguage.fileExtension,'w')
        generatorFile.write(newExecutable.generatorCode)
        editorialLanguage=ProgrammingLanguage.objects.get(id=newExecutable.editorialLanguage)
        editorialFile=open('./ProgramFiles/editorial'+editorialLanguage.fileExtension,'w')
        editorialFile.write(newExecutable.editorialCode)
        userLanguage=ProgrammingLanguage.objects.get(id=newExecutable.userLanguage)
        userFile=open('./ProgramFiles/user'+userLanguage.fileExtension,'w')
        userFile.write(newExecutable.userCode)

        generatedInput=open('./IOFiles/input.txt','w')
    def runCode(language,file):
        if language.compileCommand!='':
            pass