import os
import subprocess
from sourceControlApp.models import GitStore, CodeAuthor, Commit, Patch
from pygit2 import clone_repository, GitError
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

repo_path = 'repo'

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

    process_repo(repo, repo_object)

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
