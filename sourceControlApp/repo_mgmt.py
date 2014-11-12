import os
import re
import subprocess
from datetime import tzinfo, timedelta, datetime

import requests
from celery import task
from pygit2 import clone_repository, GitError
from django.core.exceptions import ObjectDoesNotExist
import random

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
    os.system("rm -rf " + repo_path + "*")

    try:
        repo = clone_repository(url=repo_object.gitRepositoryURL, path=repo_path, checkout_branch=repo_object.branch_name)
    except GitError:
        return -1 # Error flag

    # Remove old data
    Commit.objects.filter(repository=repo_object).delete()
    CodeAuthor.objects.filter(repository=repo_object).delete()

    process_repo(repo, repo_object, repo_path)
    repo_object.save()

def get_repo_data_from_url(url, name, description, user, check_all_branches=False):
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

    if check_all_branches:
        download_and_process_repo_all_branches.apply_async((url, user,))
    else:
        download_and_process_repo.apply_async((url,))

    return repo_entry

@task
def download_and_process_repo(url):
    repo_object = GitStore.objects.get(gitRepositoryURL = url)
    repo_object.status = 1 # Cloning
    repo_object.save()

    path = repo_path + url[-5:] # XXX FIX ME

    try:
        os.system("rm -rf " + path)
        repo = clone_repository(url=url, path=path)
    except GitError:
        repo_object.status = -1
        repo_object.save()
        os.system("rm -rf " + path)
        return

    repo_object.status = 2 # Processing
    repo_object.save()

    process_repo(repo, repo_object, path)

    repo_object.status = 3 # Done!
    repo_object.save()

    os.system("rm -rf " + path)
    return repo_object

@task
def download_and_process_repo_all_branches(url, user):
    repo_object = GitStore.objects.all().filter(gitRepositoryURL = url)[0]
    repo_object.status = 1 # Cloning
    repo_object.save()

    this_path = repo_path + str(random.randrange(0,10000))
    try:
        os.system("rm -rf " + this_path)
        repo = clone_repository(url=url, path=this_path)
    except GitError:
        repo_object.status = -1
        repo_object.save()
        #print("GitError:" + GitError)
        os.system("rm -rf " + this_path)
        return

    repo_object.status = 2 # Processing
    repo_object.save()

    process_repo(repo, repo_object, this_path)

    repo_object.status = 3 # fetching other branches
    repo_object.save()

    default_branch = repo.listall_branches()[0]
    branches = repo.listall_branches(2)
    for branch in branches:
        if branch[0:7] == 'origin/':
            if branch[7:]!=default_branch:
                new_branch = branch[7:]
                download_and_process_repo_branches(url, user, new_branch)

    repo_object.status = 3 # Done!
    repo_object.save()

    os.system("rm -rf " + this_path)
    return repo_object


@task
def download_and_process_repo_branches(url, user, branch_name):
    repo_object_default = GitStore.objects.all().filter(gitRepositoryURL = url)[0]
    print(repo_object_default)
    repo_entry_default = UserGitStore.objects.all().filter(git_store = repo_object_default)[0]
    repo_object = GitStore(gitRepositoryURL = url, branch_name = branch_name)
    repo_object.save()
    repo_name = repo_entry_default.name + "(branch: "+branch_name+")"
    repo_desc = repo_entry_default.repo_description
    repo_entry = UserGitStore(git_store = repo_object, name = repo_name, repo_description = repo_desc)
    #repo_entry = UserGitStore(git_store = repo_object, name = 'repo_name', repo_description = 'repo_desc')
    repo_entry.save()
    user.ownedRepos.add(repo_entry)
    repo_object.status = 1 # Cloning
    repo_object.save()

    this_path = repo_path + branch_name + str(random.randrange(0,10000))
    os.system("rm -rf " + this_path)
    try:
        repo = clone_repository(url=url, path=this_path, checkout_branch=branch_name)
    except GitError:
        repo_object.status = -1
        repo_object.save()
        #print("GitError:" + GitError)
        os.system("rm -rf " + this_path)
        return

    repo_object.status = 2 # Processing
    repo_object.save()

    process_repo(repo, repo_object, this_path)

    repo_object.status = 3 # Done!
    repo_object.save()

    os.system("rm -rf " + this_path)
    return repo_object

def process_repo(repo, repo_object, path):
    """
    Updates a single repo by recloning the repo
    and updating the information in the database
    :param repo: The pygit2 repo to pull information from
    :param repo_object: The model to store information in
    :return:
    """
    repo_object.numCommits = count_commits(repo)
    repo_object.numFiles = count_files(path)
    repo_object.branch_name = repo.listall_branches()[0]
    repo_object.set_branch_list(repo.listall_branches(2))

    repo_object.save()

    # Count commits per author
    count_commits_per_author(repo, repo_object)

def count_commits(repo):
    """
    :param repo: A pygit2 repo to process
    :return: The number of commits in the given repo
    """
    return len(list(repo.walk(repo.head.target)))

def count_files(path):
    """
    :return: a count of the files in the repo
    """
    try:
        num_files = subprocess.check_output('cd ' + path + ' && git ls-files | wc -l', shell = True)
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

        #count additions and deletions
        p = commit.parents
        additions = 0
        deletions = 0
        if len(p) > 0:
            diff = commit.tree.diff_to_tree(p[0].tree)
        else:
            diff = commit.tree.diff_to_tree()
        for patch in diff:
            #Note that the comparison is backward,
            #So addition should become deletions and vice versa
            additions += patch.deletions
            deletions += patch.additions

        author_names = re.findall("^Author: .*", commit.message, re.MULTILINE)
        if author_names:
            for name in author_names:
                code_author = CodeAuthor.objects.get_or_create(repository=repo_db_object, name=name)[0]
                print "Adding", name
                code_author.num_commits += 1
                code_author.additions += additions
                code_author.deletions += deletions
                code_author.save()
        else:
            code_author = CodeAuthor.objects.get_or_create(repository=repo_db_object, name=commit.author.name)[0]
            code_author.num_commits += 1
            code_author.additions += additions
            code_author.deletions += deletions
            code_author.save()

        tz = VariableNonDstTZ(commit.author.offset)
        time=datetime.fromtimestamp(commit.author.time, tz=tz)
        commit_db_object = Commit.objects.get_or_create(repository=repo_db_object,author=code_author,commit_time=time)[0]
        commit_db_object.save()


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
