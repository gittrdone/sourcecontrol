import os
import re
import subprocess
from datetime import tzinfo, timedelta, datetime

import requests
from celery import task
from pygit2 import clone_repository, GitError
from django.core.exceptions import ObjectDoesNotExist
import random

from sourceControlApp.models import UserGitStore, GitStore, CodeAuthor, Commit, GitRepo, GitBranch

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
    for repo in GitBranch.objects.all():
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
        repo = clone_repository(url=repo_object.git_repository_url, path=repo_path, checkout_branch=repo_object.branch_name)
    except GitError:
        return -1 # Error flag

    process_repo(repo, repo_object, repo_path)
    repo_object.save()

def get_repo_data_from_url(url, name, description, user):
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

    # try:
    #     repo_object = GitStore.objects.get(gitRepositoryURL = url)
    #     repo_entry = UserGitStore(git_store=repo_object, name=name, repo_description=description)
    #     repo_entry.save()
    #     return repo_entry
    # except ObjectDoesNotExist:
    #     repo_object = GitStore(gitRepositoryURL = url)
    #     repo_object.save()
    #     repo_entry = UserGitStore(git_store=repo_object, name=name, repo_description=description)
    #     repo_entry.save()
    # if not is_valid_repo(url):
    #     return -1

    try:
        repo_object_old = GitStore.objects.get(gitRepositoryURL = url)
        repo_object = GitRepo.objects.get(git_repository_url = url)
        repo_entry = UserGitStore(git_repo=repo_object, name=name, repo_description=description)
        repo_entry.save()
        return repo_entry
    except:
        repo_object = GitRepo(git_repository_url = url)
        repo_object.save()
        repo_entry = UserGitStore(git_repo=repo_object, name=name, repo_description=description)
        repo_entry.save()
    if not is_valid_repo(url):
        return -1

    download_and_process_repo(repo_object)

    return repo_entry

@task
def download_and_process_repo(repo_object, branch_name=None):
    """
    more robust way to process repo
    :param repo_object: The pygit2 repo to pull information from
    :return:
    """
    url = repo_object.git_repository_url

    # XXX this should generate unique path
    this_path = repo_path + str(random.randrange(0,10000))

    try:
        os.system("rm -rf " + this_path)
        repo = clone_repository(url=url, path=this_path, checkout_branch=branch_name)
    except GitError:
        repo_object.status = -1
        repo_object.save()
        #print("GitError:" + GitError)
        os.system("rm -rf " + this_path)
        return

    branch_db_object = GitBranch(git_repository_url = url)
    branch_db_object.status = 1 #initialized properly
    branch_db_object.save()
    repo_object.branches.add(branch_db_object)
    repo_object.status = 2 # Processing
    repo_object.save()

    process_repo(repo, branch_db_object, this_path)

    repo_object.status = 3 # Checking other repos
    repo_object.save()

    if branch_name is None:
        default_branch = repo.listall_branches()[0]
        branch_list = [branch.replace('origin/', '') for branch in repo.listall_branches(2)]
        for branch in branch_list:
            if branch !=default_branch:
                download_and_process_repo(repo_object, branch)
    repo_object.status = 3 # Done
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
    repo_object.num_commits = count_commits(repo)
    repo_object.num_files = count_files(path)
    repo_object.branch_name = repo.listall_branches()[0]

    # Count commits per author
    count_commits_per_author_branch(repo, repo_object)
    repo_object.status = 3 # Done
    repo_object.save()

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

def count_commits_per_author_branch(repo, branch_db_object):
    """
    Stores a count of all commits associated with author
    :param repo: The pygit2 repo to process
    :param repo_db_object: The model to update
    """

    try:
        latest_commit = Commit.objects.filter(git_branch=branch_db_object).latest('commit_time')
    except ObjectDoesNotExist:
        latest_commit = None

    for commit in repo.walk(repo.head.target):
        tz = VariableNonDstTZ(commit.author.offset)
        time=datetime.fromtimestamp(commit.author.time, tz=tz)

        if (latest_commit is not None and time <= latest_commit.commit_time):
            continue

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

        author_names = re.findall("^Author: ([^<>]*) <(.*)>", commit.message, re.MULTILINE)
        if author_names:
            for name in author_names:
                code_author = CodeAuthor.objects.get_or_create(git_branch=branch_db_object, name=name[0])[0]
                code_author.num_commits += 1
                code_author.additions += additions
                code_author.deletions += deletions
                code_author.save()
        else:
            code_author = CodeAuthor.objects.get_or_create(git_branch=branch_db_object, name=commit.author.name)[0]
            code_author.num_commits += 1
            code_author.additions += additions
            code_author.deletions += deletions
            code_author.save()


        commit_db_object = Commit.objects.get_or_create(git_branch=branch_db_object,author=code_author,commit_time=time)[0]
        commit_db_object.save()

def count_commits_per_author(repo, repo_db_object):
    """
    Stores a count of all commits associated with author
    :param repo: The pygit2 repo to process
    :param repo_db_object: The model to update
    """

    try:
        latest_commit = Commit.objects.filter(repository=repo_db_object).latest('commit_time')
    except ObjectDoesNotExist:
        latest_commit = None

    for commit in repo.walk(repo.head.target):
        tz = VariableNonDstTZ(commit.author.offset)
        time=datetime.fromtimestamp(commit.author.time, tz=tz)

        if (latest_commit is not None and time <= latest_commit.commit_time):
            continue

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

        author_names = re.findall("^Author: ([^<>]*) <(.*)>", commit.message, re.MULTILINE)
        if author_names:
            for name in author_names:
                code_author = CodeAuthor.objects.get_or_create(repository=repo_db_object, name=name[0])[0]
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
