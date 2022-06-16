from django.contrib import admin
from django.test import TestCase
from .models import *
from django.utils.html import format_html
# Register your models here.
admin.site.register(ProgrammingLanguage)
#admin.site.register(Executable)
admin.site.register(Test)

class ExecutableAdmin(admin.ModelAdmin):
    def testcases(self):
        tests=Test.objects.filter(executable=self)
        html=''
        for test in tests:
            html+='<p><a href="%s">%s</a></p>' %(test.get_admin_url(), test.id)
        return format_html(html)
    testcases.allow_html = True
    list_display = ('queueNo', 'datetime',testcases)
admin.site.register(Executable,ExecutableAdmin)