import string
import traceback
from time import sleep
import subprocess
import celery
from django.test import TestCase
import epicbox
from django.contrib.auth.models import User
from celery import Celery, shared_task
from .models import *
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
testCaseLimit=10

#Constants representing limits of code executation
TIME_LIMIT=2
COMPILE_TIME_LIMIT=15
MEM_LIMIT=512
LIMITS ={'cputime':TIME_LIMIT,'memory':MEM_LIMIT,'processes':100}
COMPILE_LIMITS ={'cputime':COMPILE_TIME_LIMIT,'memory':MEM_LIMIT,'processes':100}

#Flags representing corresponding status
EXECUTED=0
TIME_LIMIT_EXCEEDED = 1
RUNTIME_ERROR = 2
COMPILATION_FAILED= 3
MEMORY_LIMIT_EXCEEDED= 4
celery = Celery(__name__)
celery.config_from_object(__name__)

PROFILES=[]
for language in ProgrammingLanguage.objects.all():
    PROFILES.append(epicbox.Profile(language.name,language.dockerImage))
epicbox.configure(profiles=PROFILES)
@shared_task(acks_late=True)
def executeTask(queueid):
    def runCode(language:ProgrammingLanguage,codeFile,executableName,inputFile,outputFile):
        files=[{'name':codeFile.name,'content':bytes(codeFile.read(),'utf-8')}]
        if language.compileCommand!='NA':
            toExecute=language.compileCommand.replace('filename',codeFile.name)+' -o '+executableName
            with epicbox.working_directory() as work_dir:
                result=epicbox.run(language.name, toExecute, files=files, limits=COMPILE_LIMITS,workdir=work_dir)
                if result['exit_code']!=0:
                    if result['timeout'] or result['oom_killed']:
                        outputFile.write("Error: Compilation exceeded time limit or memory limit")
                    else:
                        outputFile.write(result['stderr'].decode('utf-8'))
                    return COMPILATION_FAILED, result['duration']
                toExecute="./"+executableName
                if inputFile!=None:
                    result=epicbox.run(language.name, toExecute, files=files, limits=LIMITS, stdin=inputFile.read() ,workdir=work_dir)
                else:
                    result=epicbox.run(language.name, toExecute, files=files, limits=LIMITS ,workdir=work_dir)
                if result['timeout']:
                    outputFile.write("Time Limit Exceeded")
                    return TIME_LIMIT_EXCEEDED, result['duration']
                if result['oom_killed']:
                    outputFile.write("Memory Limit Exceeded")
                    return MEMORY_LIMIT_EXCEEDED, result['duration']
                if result['exit_code']!=0:
                    outputFile.write(result['stderr'].decode('utf-8'))
                    return RUNTIME_ERROR, result['duration']
                outputFile.write(result['stdout'].decode('utf-8'))
                return EXECUTED,result['duration']
        toExecute= language.executeCommand.replace('filename',codeFile.name)
        if inputFile!=None:
            result=epicbox.run(language.name, toExecute, files=files, limits=LIMITS, stdin=inputFile.read())
        else:
            result=epicbox.run(language.name, toExecute, files=files, limits=LIMITS)
        if result['timeout']:
            outputFile.write("Time Limit Exceeded")
            return TIME_LIMIT_EXCEEDED, result['duration']
        if result['oom_killed']:
            outputFile.write("Memory Limit Exceeded")
            return MEMORY_LIMIT_EXCEEDED, result['duration']
        if result['exit_code']!=0:
            outputFile.write(result['stderr'].decode('utf-8'))
            return RUNTIME_ERROR, result['duration']
        outputFile.write(result['stdout'].decode('utf-8'))
        return EXECUTED,result['duration']
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
            newTest.executable=newExecutable
            newTest.userCPUtime=0
            newTest.editorialCPUtime=0
            newTest.generatorCPUtime=0
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
            editorialFile=open(editorialFile.name,'r')

            exitCode,cpuTime= runCode(generatorLanguage,generatorFile,'generator',None,generatedInput)
            generatedInput.close()
            generatedInput=open(generatedInput.name,'r')
            newTest.generatedTest=generatedInput.read()
            generatedInput.seek(0)

            if exitCode!=EXECUTED:
                if exitCode==TIME_LIMIT_EXCEEDED:
                    newTest.verdict='Time Limit Exceeded'
                elif exitCode==COMPILATION_FAILED:
                    newTest.verdict='Compilation Error'
                elif exitCode==MEMORY_LIMIT_EXCEEDED:
                    newTest.verdict='Memory Limit Exceeded'
                elif exitCode==RUNTIME_ERROR:
                    newTest.verdict= 'Runtime Error'
                newTest.generatorCPUtime=cpuTime
                newTest.save()
                break

            exitCode,cpuTime=runCode(userLanguage,userFile,'user',generatedInput,userOutput)
            userOutput.close()
            userOutput=open(userOutput.name,'r')
            newTest.userOutput=userOutput.read()
            userOutput.seek(0)
            if exitCode!=EXECUTED:
                if exitCode==TIME_LIMIT_EXCEEDED:
                    newTest.verdict='Time Limit Exceeded'
                elif exitCode==COMPILATION_FAILED:
                    newTest.verdict='Compilation Error'
                elif exitCode==MEMORY_LIMIT_EXCEEDED:
                    newTest.verdict='Memory Limit Exceeded'
                elif exitCode==RUNTIME_ERROR:
                    newTest.verdict= 'Runtime Error'
                newTest.userCPUtime=cpuTime
                newTest.save()
                break
            generatedInput.seek(0)

            exitCode,cpuTime=runCode(editorialLanguage,editorialFile,'editorial',generatedInput,editorialOutput)
            editorialOutput.close()
            editorialOutput=open(editorialOutput.name,'r')
            newTest.editorialoutput=editorialOutput.read()
            editorialOutput.seek(0)

            if exitCode!=EXECUTED:
                if exitCode==TIME_LIMIT_EXCEEDED:
                    newTest.verdict='Time Limit Exceeded'
                elif exitCode==COMPILATION_FAILED:
                    newTest.verdict='Compilation Error'
                elif exitCode==MEMORY_LIMIT_EXCEEDED:
                    newTest.verdict='Memory Limit Exceeded'
                elif exitCode==RUNTIME_ERROR:
                    newTest.verdict= 'Runtime Error'
                newTest.editorialCPUtime=cpuTime
                newTest.save()
                break

            
            
            generatedInput.seek(0)
            
            newTest.verdict=checkOutput(newTest.generatedTest,newTest.userOutput,newTest.editorialoutput)
            newTest.save()
            if newTest.verdict!='Accepted':
                break
        newExecutable.status='Completed'
    except Exception as errorMessage:
        newExecutable.status='Failed'
        open('ErrorMessage.txt','w').write(str(traceback.format_exc()))
    newExecutable.save()