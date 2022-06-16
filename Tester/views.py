from django.shortcuts import render
from django.http import HttpResponse
import datetime
from Tester.task import executeTask
from .models import *
# Create your views here.
def index(request):
    languages= ProgrammingLanguage.objects.all()
    if request.method=='POST':
        newExecutable=Executable()
        newExecutable.userCode=request.POST['UserCode']
        newExecutable.userLanguage=int(request.POST['UserLanguage'])
        newExecutable.editorialCode=request.POST['EditorialCode']
        newExecutable.editorialLanguage=int(request.POST['EditorialLanguage'])
        newExecutable.generatorCode=request.POST['GeneratorCode']
        newExecutable.generatorLanguage=int(request.POST['GeneratorLanguage'])
        newExecutable.status="In queue"
        newExecutable.datetime=datetime.datetime.now()
        newExecutable.save()
        
        executeTask.delay(newExecutable.queueNo)
    return  render(request,'index.html',{'ProgrammingLanguages':languages})
def StatusPage(request,id):
    return HttpResponse('Hello')