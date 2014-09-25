import os
import subprocess

class GitRepo(object):
    def __init__(self, url):
        self.url = url

    def count_files(self):
        os.system('mkdir repo')
        os.system('git clone ' + self.url + ' repo')
        num_files = subprocess.check_output('cd repo && git ls-files | wc -l', shell = True)
        os.system('rm -rf repo')
        return num_files