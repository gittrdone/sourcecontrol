from celery import task
from sourceControlApp.repo_mgmt import update_repos

# This file is designed to hold periodic Celery tasks.

@task
def reprocess_repos():
    """
    Celery task to update all repositories.
    """
    update_repos()