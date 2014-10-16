import os
import re
import subprocess
from datetime import datetime
from datetime import tzinfo, timedelta, datetime

import requests
from celery import task
from pygit2 import clone_repository, GitError
from django.core.exceptions import ObjectDoesNotExist

from sourceControlApp.models import UserGitStore, GitStore, CodeAuthor, Commit, Patch

repo_path = 'repo'

class VariableNonDstTZ(tzinfo):

    minute_offset = 0

    def __init__(self, offset):
        self.minute_offset = offset

    def utcoffset(self, date_time):
        return timedelta(minutes = self.minute_offset)

    def dst(self, date_time):
        return timedelta(0)

def update_repos():
    """
    Updates all of the repos in the database with
    updated information.
    """
    for repo in GitStore.objects.all():
        update_repo(repo)

def update_repo(repo_object):
    """
    Updates a single repo by recloning the repo
    and updating the information in the database
    :param repo_object: Existing object to update
    :return: -1 if there is an error
    """
    os.system("rm -rf " + repo_path)

    try:
        repo = clone_repository(url=repo_object.gitRepositoryURL, path=repo_path)
    except GitError:
        return -1 # Error flag

    # Remove old data
    Commit.objects.filter(repository=repo_object).delete()
    CodeAuthor.objects.filter(repository=repo_object).delete()

    process_repo(repo, repo_object)
    repo_object.save()

def get_repo_data_from_url(url, name, description):
    """
    Updates a single repo by recloning the repo
    and updating the information in the database
    :param url: URL of the repository
    :param name: Name to reference the repository by
    :param description: Description of the repo
    :return: A reference the the repo in the database
    """
    os.system("rm -rf " + repo_path)

    if url[:4] != "http":
        print "Only HTTP git URLs supported!"
        return -1

    url = canonicalize_repo_url(url)

    try:
        repo_object = GitStore.objects.get(gitRepositoryURL = url)
        repo_entry = UserGitStore(git_store=repo_object, name=name, repo_description=description)
        repo_entry.save()
        return repo_entry
    except ObjectDoesNotExist:
        repo_object = GitStore(gitRepositoryURL = url)
        repo_object.save()
        repo_entry = UserGitStore(git_store=repo_object, name=name, repo_description=description)
        repo_entry.save()

    if not is_valid_repo(url):
        return -1

    download_and_process_repo.apply_async((url,))

    return repo_entry

@task
def download_and_process_repo(url, branch_name=''):
    if branch_name=='':
        repo_object = GitStore.objects.get(gitRepositoryURL = url)
    else:
        repo_object = GitStore.objects.create(gitRepositoryURL = url, branch_name = branch_name)
    repo_object.status = 1 # Cloning
    repo_object.save()

    try:
        if branch_name != '':
            repo = clone_repository(url=url, path=repo_path+branch_name, checkout_branch=branch_name)
        else:
            repo = clone_repository(url=url, path=repo_path)
    except GitError:
        repo_object.status = -1
        repo_object.save()
        return

    repo_object.status = 2 # Processing
    repo_object.save()

    default_branch = repo.listall_branches()
    if branch_name == '':
        refs = repo.listall_references()
        for ref in refs:
            print(branch_name)
            print(ref[13:])
            if ref[0:20] == 'refs/remotes/origin/':
                if ref[13:]!=default_branch:
                    new_branch = ref[20:]
                    os.system("rm -rf " + repo_path + new_branch)
                    download_and_process_repo(url, new_branch)
                    os.system("rm -rf " + repo_path + new_branch)

    process_repo(repo, repo_object)

    repo_object.status = 3 # Done!
    repo_object.save()

    return repo_object

def process_repo(repo, repo_object):
    """
    Updates a single repo by recloning the repo
    and updating the information in the database
    :param repo: The pygit2 repo to pull information from
    :param repo_object: The model to store information in
    :return:
    """
    repo_object.numCommits = count_commits(repo)
    repo_object.numFiles = count_files()
    repo_object.branch_name = repo.listall_branches()[0]

    repo_object.save()

    # Count commits per author
    count_commits_per_author(repo, repo_object)

def count_commits(repo):
    """
    :param repo: A pygit2 repo to process
    :return: The number of commits in the given repo
    """
    return len(list(repo.walk(repo.head.target)))

def count_files():
    """
    :return: a count of the files in the repo
    """
    try:
        num_files = subprocess.check_output('cd ' + repo_path + ' && git ls-files | wc -l', shell = True)
        return num_files
    except GitError:
        return -1

def count_commits_per_author(repo, repo_db_object):
    """
    Stores a count of all commits associated with author
    :param repo: The pygit2 repo to process
    :param repo_db_object: The model to update
    """
    for commit in repo.walk(repo.head.target):
        code_author = CodeAuthor.objects.get_or_create(repository=repo_db_object, name=commit.author.name)[0]
        code_author.num_commits += 1
        code_author.save()
        tz = VariableNonDstTZ(commit.author.offset)
        time=datetime.fromtimestamp(commit.author.time, tz=tz)
        commit_db_object = Commit.objects.get_or_create(repository=repo_db_object,author=code_author,commit_time=time)[0]
        commit_db_object.save()
        ##This part is taking too much time. But it's working.
        # for entry in commit.tree:
        #     patch = Patch.objects.get_or_create(repository = repo_db_object, filename = entry.name)[0]
        #     patch.save()
        #     commit_db_object.num_patches += 1
        #     commit_db_object.patches.add(patch)
        # commit_db_object.save()

def is_valid_repo(url):
    """
    Checks if the given URL refers to a git repository
    :param url: XXX For now, we assume this is an HTTP(S) url ending WITHOUT .git or /
    :return: a boolean stating whether the URL is a git repository
    """

    # This is the resource git uses to initiate a clone from a repo
    # If it exists, we have a git repo!
    git_data_url = url + ".git/info/refs?service=git-upload-pack"

    # Use git's user agent to fool servers
    resp = requests.get(git_data_url, headers={"User-Agent": "git/1.9.3"})

    # Follow redirects
    while resp.status_code == 301:
        resp = requests.get(resp.headers['location'], headers={"User-Agent": "git/1.9.3"})

    return resp.status_code == 200

def canonicalize_repo_url(url):
    # Remove trailing slash
    if url[-1:] == '/':
        url = url[:-1]

    # Remove trailing .git
    if url[-4:] == '.git':
        url = url[:-4]

    # Use HTTP URL as canonical for now
    return "http" + re.match("https?(.*)", url).group(1)
