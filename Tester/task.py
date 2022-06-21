import string
from time import sleep
import subprocess
import celery

from django.contrib.auth.models import User
from celery import Celery, shared_task
from .models import *
import os
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
testCaseLimit=10
celery = Celery(__name__)
celery.config_from_object(__name__)
        #outputFile.write(str(len(p.stdout.decode('utf-8'))))
@shared_task(acks_late=True)
def executeTask(queueid):
    def runCode(language:ProgrammingLanguage,codeFile,executableName,inputFile,outputFile):
        if language.compileCommand!='NA':
            toExecute=language.compileCommand.replace('filename',codeFile.name)+' '+executableName
            subprocess.call(toExecute,shell=True)
        if language.executeCommand=='NA':
            if inputFile!=None:
                toExecute=executableName
            else:
                toExecute=executableName
        else:
            if inputFile!=None:
                toExecute=language.executeCommand.replace('filename',codeFile.name)
            else:
                toExecute=language.executeCommand.replace('filename',codeFile.name)
        subprocess.call(toExecute,shell=True,stdout=outputFile,stdin=inputFile)
    def checkOutput(test,userOutput,editorialOutput):
        if userOutput.split()==editorialOutput.split():
            return 'Accepted'
        else:
            return 'Wrong Answer' 
    newExecutable=Executable.objects.get(queueNo=queueid)
    try:
        newExecutable.status='Running'
        newExecutable.save()
        for testcase in range(testCaseLimit):
            newTest=Test()
            generatorLanguage=ProgrammingLanguage.objects.get(id=newExecutable.generatorLanguage)
            generatorFile=open('./ProgramFiles/generator'+generatorLanguage.fileExtension,'w+')
            generatorFile.write(newExecutable.generatorCode)
            editorialLanguage=ProgrammingLanguage.objects.get(id=newExecutable.editorialLanguage)
            editorialFile=open('./ProgramFiles/editorial'+editorialLanguage.fileExtension,'w+')
            editorialFile.write(newExecutable.editorialCode)
            userLanguage=ProgrammingLanguage.objects.get(id=newExecutable.userLanguage)
            userFile=open('./ProgramFiles/user'+userLanguage.fileExtension,'w+')
            userFile.write(newExecutable.userCode)
            generatedInput=open('./IOFiles/input.txt','w+')
            userOutput=open('./IOFiles/UserOutput.txt','w+')
            editorialOutput=open('./IOFiles/EditorialOutput.txt','w+')
            generatorFile.close()
            generatorFile=open(generatorFile.name,'r')
            userFile.close()
            userFile=open(userFile.name,'r')
            editorialFile.close()
            generatorFile=open(generatorFile.name,'r')
            runCode(generatorLanguage,generatorFile,'./ProgramFiles/generator',None,generatedInput)
            generatedInput.close()
            generatedInput=open(generatedInput.name,'r')
            runCode(userLanguage,userFile,'./ProgramFiles/user',generatedInput,userOutput)
            generatedInput.seek(0)
            runCode(editorialLanguage,editorialFile,'./ProgramFiles/editorial',generatedInput,editorialOutput)
            userOutput.close()
            userOutput=open(userOutput.name,'r')
            editorialOutput.close()
            editorialOutput=open(editorialOutput.name,'r')
            generatedInput.seek(0)
            newTest.generatedTest=generatedInput.read()
            newTest.userOutput=userOutput.read()
            newTest.editorialoutput=editorialOutput.read()
            newTest.executable=newExecutable
            newTest.verdict=checkOutput(newTest.generatedTest,newTest.userOutput,newTest.editorialoutput)
            newTest.save()
            if newTest.verdict!='Accepted':
                break
        newExecutable.status='Completed'
    except:
        newExecutable.status='Failed'
    newExecutable.save()