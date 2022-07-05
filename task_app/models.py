from django.db import models
from django.db.models import JSONField
# Create your models here.
class Account_Module(models.Model):
    email_id=models.EmailField(max_length=100)
    account_id=models.CharField(max_length=100)
    account_name=models.CharField(max_length=100)
    App_secret_token=models.TextField()
    website=models.CharField(max_length=100,null=True,blank=True)

class Destination_Module(models.Model):
    URL=models.URLField(max_length=1000)
    http_method=models.CharField(max_length=100)
    headers=models.JSONField(default=dict)
    account=models.ForeignKey(Account_Module,on_delete=models.CASCADE)