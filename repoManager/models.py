from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class GitStore(models.Model):
    gitRepositoryURL = models.CharField(max_length=200)
    numFiles = models.IntegerField(default=0)
    repoName = models.CharField(max_length=30)
    repoDescription = models.CharField(max_length=1000, default="")

    def __unicode__ (self):
        return self.gitRepositoryURL
        
class SourceControlUser(models.Model):
	user = models.OneToOneField(User)
	ownedRepos = models.ManyToManyField(GitStore) 