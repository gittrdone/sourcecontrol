import os
import subprocess
from pygit2 import Repository, clone_repository

class GitRepo(object):
    def __init__(self, url):
        self.url = url

    def count_files(self):
        repo_url = self.url
        repo_path = 'repo'
        repo = clone_repository(url = repo_url, path = repo_path)
        num_files = subprocess.check_output('cd repo && git ls-files | wc -l', shell = True)
        os.system('rm -rf repo')
        return num_files