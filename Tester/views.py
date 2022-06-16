from django.shortcuts import redirect, render
from django.http import HttpResponse
import datetime
from Tester.task import executeTask
from .models import *
from django.utils import timezone
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
        newExecutable.datetime=datetime.datetime.now(tz=timezone.utc)
        newExecutable.save()
        executeTask.delay(newExecutable.queueNo)
        return redirect ('/status/{}'.format(newExecutable.queueNo))
    return  render(request,'index.html',{'ProgrammingLanguages':languages})
def StatusPage(request,id):
    return  render(request,'status.html',{'executable':Executable.objects.get(queueNo=id)})