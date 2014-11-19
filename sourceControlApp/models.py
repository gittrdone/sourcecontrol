from django.db import models
from django.contrib.auth.models import User
import json

# Create your models here.
class GitStore(models.Model):
    branch_name = models.CharField(max_length=50)
    gitRepositoryURL = models.CharField(max_length=300)
    numFiles = models.IntegerField(default=0)
    numCommits = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    branch_list = models.CharField(max_length=300) #please use getter and setter

    def set_branch_list(self,input_branch_list):
        self.branch_list = json.dumps(input_branch_list)

    def get_branch_list(self):
        jsonDec = json.decoder.JSONDecoder()
        return jsonDec.decode(self.branch_list)

    def __unicode__ (self):
        return self.gitRepositoryURL

#new model for git branch
class GitBranch(models.Model):
    git_repository_url = models.CharField(max_length=300)
    branch_name = models.CharField(max_length=50)
    num_files = models.IntegerField(default=0)
    num_commits = models.IntegerField(default=0)
    status = models.IntegerField(default=0)

    def __unicode__ (self):
           return unicode(self.git_repository_url) + ":" + unicode(self.branch_name)

#new model for git repository
class GitRepo(models.Model):
    git_repository_url = models.CharField(max_length=300)
    status = models.IntegerField(default=0)
    branches = models.ManyToManyField(GitBranch)

    def __unicode__ (self):
        return unicode(self.git_repository_url)

class UserGitStore(models.Model):
    git_store = models.ForeignKey(GitStore, null=True, blank=True)
    git_repo = models.ForeignKey(GitRepo, null=True, blank=True)
    name = models.CharField(max_length=100)
    repo_description = models.CharField(max_length=1000)

    def __unicode__ (self):
        return unicode(self.git_store) + self.name

class SourceControlUser(models.Model):
    user = models.OneToOneField(User)
    ownedRepos = models.ManyToManyField(UserGitStore)

class CodeAuthor(models.Model):
    name = models.CharField(max_length=100)
    num_commits = models.IntegerField(default=0)
    repository = models.ForeignKey(GitStore, null=True, blank=True)
    git_branch = models.ForeignKey(GitBranch, null=True, blank=True)
    additions = models.IntegerField(default=0)
    deletions = models.IntegerField(default=0)

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
    repository = models.ForeignKey(GitStore, null=True, blank=True)
    git_branch = models.ForeignKey(GitBranch, null=True, blank=True)
    author = models.ForeignKey(CodeAuthor)
    patches = models.ManyToManyField(Patch, null=True, blank=True)
    commit_time = models.DateTimeField()
    num_patches = models.IntegerField(default = 0)

    def num_files_change(self):
        return self.num_patches

    def __unicode__ (self):
        return unicode(self.git_branch) + unicode(self.author)
