from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class GitStore(models.Model):
    gitRepositoryURL = models.CharField(max_length=200)
    numFiles = models.IntegerField(default=0)

    def __unicode__ (self):
        return self.gitRepositoryURL
        
class SourceControlUser(models.Model):
	user = models.OneToOneField(User)