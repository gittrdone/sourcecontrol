from django.db import models

# Create your models here.
class GitStore(models.Model):
	gitRepositoryURL = models.CharField(max_length=200);
	numFiles = models.IntegerField(default=0);