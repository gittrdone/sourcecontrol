from celery import task
from sourceControlApp.repo_mgmt import update_repos

@task
def reprocess_repos():
    update_repos()