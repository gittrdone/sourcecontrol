from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class GitStore(models.Model):
    gitRepositoryURL = models.CharField(max_length=200)
    numFiles = models.IntegerField(default=0)
    numCommits = models.IntegerField(default=0)

    repoName = models.CharField(max_length=30)
    repoDescription = models.CharField(max_length=1000, default="", null=True, blank=True)

    def __unicode__ (self):
        return self.gitRepositoryURL
        
class SourceControlUser(models.Model):
    user = models.OneToOneField(User)
    ownedRepos = models.ManyToManyField(GitStore)

class CodeAuthor(models.Model):
    name = models.CharField(max_length=100)
    num_commits = models.IntegerField(default=0)
    repository = models.ForeignKey(GitStore)

    def __unicode__ (self):
        return unicode(self.repository) + self.name

class Patch(models.Model):
    repository = models.ForeignKey(GitStore)
    filename = models.CharField(max_length=100)
    addition = models.IntegerField(default=0)
    deletion = models.IntegerField(default=0)
    next = models.ForeignKey("Patch", null=True, blank=True)

    def __unicode__(self):
        return unicode(self.repository) + ":" + self.filename

class Commit(models.Model):
    #Try many authors later
    #authors = models.ManyToManyField(CodeAuthor)
    repository = models.ForeignKey(GitStore)
    author = models.ForeignKey(CodeAuthor)
    patches = models.ManyToManyField(Patch)
    commit_time = models.DateTimeField()
    num_patches = models.IntegerField(default = 0)

    def num_files_change(self):
        return self.num_patches

    def __unicode__ (self):
        return unicode(self.repository) + unicode(self.author)