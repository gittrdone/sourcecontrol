import os
import subprocess
from sourceControlApp.models import GitStore, CodeAuthor
from sourceControlApp.models import Commit, Patch
from pygit2 import clone_repository, GitError
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

repo_path = 'repo'

def get_repo_data_from_url(url, name, description):
    os.system("rm -rf " + repo_path)

    try:
        repo_object = GitStore.objects.get(gitRepositoryURL = url)
        return repo_object
    except ObjectDoesNotExist:
        repo_object = GitStore()

    try:
        repo = clone_repository(url=url, path=repo_path)
    except GitError:
        return -1 # Error flag

    repo_object.repoDescription = description
    repo_object.repoName = name
    repo_object.gitRepositoryURL = url
    repo_object.numCommits = count_commits(repo)
    repo_object.numFiles = count_files()

    repo_object.save()

    # Count commits per author
    count_commits_per_author(repo, repo_object)

    return repo_object

def count_commits(repo):
    return len(list(repo.walk(repo.head.target)))

def count_files():
    try:
        num_files = subprocess.check_output('cd ' + repo_path + ' && git ls-files | wc -l', shell = True)
        return num_files
    except GitError:
        return -1

def count_commits_per_author(repo, repo_db_object):
    for commit in repo.walk(repo.head.target):
        code_author = CodeAuthor.objects.get_or_create(repository=repo_db_object, name=commit.author.name)[0]
        code_author.num_commits += 1
        code_author.save()
        time=datetime.fromtimestamp(commit.author.time)
        commit_db_object = Commit.objects.get_or_create(repository=repo_db_object,author=code_author,commit_time=time)[0]
        commit_db_object.save()
        ##This part is taking too much time. But it's working.
        # for entry in commit.tree:
        #     patch = Patch.objects.get_or_create(repository = repo_db_object, filename = entry.name)[0]
        #     patch.save()
        #     commit_db_object.num_patches += 1
        #     commit_db_object.patches.add(patch)
        # commit_db_object.save()
