from django.shortcuts import render
from repoManager.models import GitStore
import os
import subprocess
from django.http import HttpResponse

# Create your views here.
def index(request):
	return render(request, 'gitRepoDemo.html', { 'repo_list': GitStore.objects.all() })

def count_files(request):
	repo_url = request.GET['repo']
	os.system('mkdir repo')
	os.system('git clone '+repo_url+' repo')
	num_files = subprocess.check_output('cd repo && git ls-files | wc -l',shell = True)
	os.system('rm -rf repo')
	GitStore.objects.create(gitRepositoryURL = repo_url, numFiles = num_files) #PROBLEMATIC LINE
	return HttpResponse('the repository url at '+repo_url+' has '+num_files+' files')
