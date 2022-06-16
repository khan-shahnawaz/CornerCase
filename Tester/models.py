from django.db import models

# Create your models here.
class ProgrammingLanguage(models.Model):
    name=models.CharField(max_length=255)
    id= models.AutoField(unique=True, primary_key=True, null=False)
    compileCommand=models.TextField(null=True)
    executeCommand=models.TextField(null=True)
    fileExtension = models.CharField(default='.cpp',max_length=255)

class Executable(models.Model):
    status=models.CharField(max_length=20)
    userCode=models.TextField()
    userLanguage=models.IntegerField()
    generatorCode=models.TextField()
    generatorLanguage=models.IntegerField()
    editorialCode=models.TextField()
    editorialLanguage=models.IntegerField()
    datetime=models.DateTimeField(default=None)
    queueNo=models.AutoField(primary_key=True)

class Test(models.Model):
    generatedTest=models.TextField()
    userOutput=models.TextField()
    editorialoutput=models.TextField()
    passed=models.BooleanField(default=False)
    executable=models.ForeignKey(Executable,on_delete=models.CASCADE,default=None)
    def get_admin_url(self):
        return "/admin/Tester/test/%d/" %self.id
