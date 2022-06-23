from django.db import models

# Create your models here.
class ProgrammingLanguage(models.Model):
    name=models.CharField(max_length=255)
    id= models.AutoField(unique=True, primary_key=True, null=False)
    compileCommand=models.TextField(null=True)
    executeCommand=models.TextField(null=True)
    dockerImage=models.TextField(null=True)
    fileExtension = models.CharField(default='.cpp',max_length=255)

class Executable(models.Model):
    status=models.CharField(max_length=100)
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
    generatorCPUtime=models.FloatField(default=0)
    userOutput=models.TextField()
    userCPUtime=models.FloatField(default=0)
    editorialoutput=models.TextField()
    editorialCPUtime=models.FloatField(default=0)
    verdict=models.CharField(default='Running',max_length=25)
    executable=models.ForeignKey(Executable,on_delete=models.CASCADE,default=None)
    def get_admin_url(self):
        return "/admin/Tester/test/%d/" %self.id
