from django.db import models

# Create your models here.  
class SmartBin(models.Model):
    binName = models.CharField(max_length=20)
    binDate = models.CharField(max_length=20)
    binTime = models.CharField(max_length=20)
    battery = models.IntegerField("Battery")
    binLevel1 = models.IntegerField("Bin Level 1")
    binLevel2 = models.IntegerField("Bin Level 2")
