from django.shortcuts import render
from django.http import HttpResponse

from Tester.task import checkOutput
from .models import *
# Create your views here.
def index(request):
    languages= ProgrammingLanguage.objects.all()
    if request.method=='POST':
        newExecutable=Executable()
        newExecutable.userCode=request.POST['UserCode']
        newExecutable.userLanguage=request.POST['UserLanguage']
        newExecutable.editorialCode=request.POST['EditorialCode']
        newExecutable.editorialLanguage=request.POST['EditorialLanguage']
        newExecutable.generatorCode=request.POST['GeneratorCode']
        newExecutable.generatorLanguage=request.POST['GeneratorLanguage']
        newExecutable.status="In queue"
        checkOutput.delay()
        newExecutable.save()
    return  render(request,'index.html',{'ProgrammingLanguages':languages})
def StatusPage(request,id):
    return HttpResponse('Hello')