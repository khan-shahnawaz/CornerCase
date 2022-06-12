import string
from time import sleep
import subprocess
from django.contrib.auth.models import User
from celery import shared_task
from .models import *
import os
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
testCaseLimit=1
def runCode(language:ProgrammingLanguage,file,executableName,inputFile,outputFile):
        if language.compileCommand!='NA':
            toExecute=language.compileCommand.replace('filename',file.name)+' '+executableName
            subprocess.call(toExecute,shell=True)
        if language.executeCommand=='NA':
            if inputFile!=None:
                toExecute=executableName+' < '+inputFile.name +' > '+outputFile.name
            else:
                toExecute=executableName+' > '+outputFile.name
        else:
            if inputFile!=None:
                toExecute=language.executeCommand.replace('filename',file.name)+' < '+inputFile.name +' > '+outputFile.name
            else:
                toExecute=language.executeCommand.replace('filename',file.name)+' > '+outputFile.name
        subprocess.call(toExecute,shell=True)
        #outputFile.write(toExecute)
@shared_task()
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
        userOutput=open('./IOFiles/UserOutput.txt','w')
        editorialOutput=open('./IOFiles/EditorialOutput.txt','w')
        runCode(generatorLanguage,generatorFile,'./ProgramFiles/generator',None,generatedInput)
