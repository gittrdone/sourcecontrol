from django.shortcuts import render, render_to_response
from repoManager.models import GitStore
import os
import subprocess
from django.http import HttpResponse
from django.template import RequestContext

# Create your views here.
def index(request):
    return render(request, 'gitRepoDemo.html', { 'repo_list': GitStore.objects.all() })

def count_files(request):
    context_instance = RequestContext(request)
    repo_url = request.GET['repo']
    os.system('mkdir repo')
    os.system('git clone '+repo_url+' repo')
    num_files = subprocess.check_output('cd repo && git ls-files | wc -l',shell = True)
    os.system('rm -rf repo')
    GitStore.objects.get_or_create(gitRepositoryURL = repo_url, numFiles = num_files) #PROBLEMATIC LINE
    context_instance["repo_url"]=repo_url
    context_instance["count"]=num_files
    context_instance["repo_list"]=GitStore.objects.all()
    return render_to_response("gitRepoDemo.html", context_instance)
