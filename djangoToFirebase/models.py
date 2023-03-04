from django.db import models
from django.utils import timezone
# Create your models here.  
class SmartBin(models.Model):
    binName = models.CharField(max_length=20)
    binDate = models.DateField(auto_now=True)
    binTime = models.TimeField(auto_now=True)
    battery = models.IntegerField("Battery")
    binLevel1 = models.IntegerField("Bin Level 1")
    binLevel2 = models.IntegerField("Bin Level 2")
