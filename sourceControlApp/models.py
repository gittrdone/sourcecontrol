from django.db import models
from django.contrib.auth.models import User


class GitBranch(models.Model):
    """
    New model for git branch
    Commit objects point back to this
    """
    git_repository_url = models.CharField(max_length=300)
    branch_name = models.CharField(max_length=50)
    num_files = models.IntegerField(default=0)
    num_commits = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    is_default = models.IntegerField(default=0)

    def __unicode__ (self):
        return unicode(self.git_repository_url) + ":" + unicode(self.branch_name)


class GitRepo(models.Model):
    """
    New model for git repository
    Contains information related to a whole repository, including
    branches and jenkins associations
    """
    git_repository_url = models.CharField(max_length=300)
    status = models.IntegerField(default=0)
    branches = models.ManyToManyField(GitBranch)
    num_commits = models.IntegerField(default=0)

    # Might be moved somewhere else in the future?
    jenkins_url = models.CharField(max_length=300, null=True, blank=True)
    jenkins_job_name = models.CharField(max_length=100, null=True, blank=True)

    @property
    def default_branch(self):
        for branch in self.branches.all():
            if branch.is_default == 1:
                return branch
        return self.branches.all()[0]  # This is for legacy support only

    @property
    def get_branch_list(self):
        branch_list = [br.branch_name for br in self.branches.all()]
        return branch_list

    def get_branch_by_branch_name(self, branch_name):
        for branch in self.branches:
            if branch.branch_name == branch_name:
                return branch
        return None

    def __unicode__ (self):
        return unicode(self.git_repository_url)


class UserGitStore(models.Model):
    """
    User data associated with git repository entry
    """
    git_repo = models.ForeignKey(GitRepo, null=True, blank=True)
    name = models.CharField(max_length=100)
    repo_description = models.CharField(max_length=1000)

    def __unicode__ (self):
        return unicode(self.git_repo) + self.name


class SourceControlUser(models.Model):
    """
    Actual user model. Holds references to owned repositories
    """
    user = models.OneToOneField(User)
    ownedRepos = models.ManyToManyField(UserGitStore)


class CodeAuthor(models.Model):
    """
    Author of code as recorded in git history
    """
    name = models.CharField(max_length=100)
    num_commits = models.IntegerField(default=0)
    git_branch = models.ForeignKey(GitBranch, null=True, blank=True)
    additions = models.IntegerField(default=0)
    deletions = models.IntegerField(default=0)
    # The total number of broken builds by THIS CodeAuthor
    # Note: this CodeAuthor might not be the one who start the breaking sequence
    num_break_build = models.IntegerField(default=0)
    # The total number of builds that fix by THIS CodeAuthor
    # Note: this CodeAuthor is the one that stop the breaking sequence
    num_fix_build = models.IntegerField(default=0)
    # The total number of builds by THIS CodeAuthor
    num_build = models.IntegerField(default=0)

    def __unicode__ (self):
        return unicode(self.git_branch) + self.name


# Patch to a file as included in a commit. Has number
# of additions and deletions
class Patch(models.Model):
    filename = models.CharField(max_length=100)
    addition = models.IntegerField(default=0)
    deletion = models.IntegerField(default=0)
    next = models.ForeignKey("Patch", null=True, blank=True)

    def __unicode__(self):
        return unicode(self.repository) + ":" + self.filename


# Reference to a commit. Holds reference to branches, authors,
# and patches that are associated with it
class Commit(models.Model):
    # Try many authors later
    #authors = models.ManyToManyField(CodeAuthor)
    commit_id = models.CharField(max_length=50)
    git_repo = models.ForeignKey(GitRepo, null=True, blank=True)
    branches = models.ManyToManyField(GitBranch)
    author = models.ForeignKey(CodeAuthor)
    patches = models.ManyToManyField(Patch, null=True, blank=True)
    commit_time = models.DateTimeField()
    num_patches = models.IntegerField(default = 0)
    break_build_status = models.IntegerField(default = -1) #0 = no. 1 = yes. -1 = unknown

    def num_files_change(self):
        return self.num_patches

    def __unicode__ (self):
        return unicode(self.git_repo) + unicode(self.author)


# Data related to a file in the repository. Stores total number of additions,
# deletions, and number of edits.
class FileEntry(models.Model):
    file_path = models.CharField(max_length=300)
    git_branch = models.ForeignKey(GitBranch)
    additions = models.IntegerField(default=0)
    deletions = models.IntegerField(default=0)
    num_edit = models.IntegerField(default=0)
    in_current_built = models.BooleanField(default=False)
