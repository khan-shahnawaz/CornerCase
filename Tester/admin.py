from django.contrib import admin
from django.test import TestCase
from .models import *
# Register your models here.
admin.site.register(ProgrammingLanguage)
admin.site.register(Executable)
admin.site.register(Test)