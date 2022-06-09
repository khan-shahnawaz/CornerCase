from django.shortcuts import render
from django.http import HttpResponse
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
        newExecutable.generatorLanguge=request.POST['GeneratorLanguage']
        newExecutable.status="In queue"
        newExecutable.save()
    return  render(request,'index.html',{'ProgrammingLanguages':languages})