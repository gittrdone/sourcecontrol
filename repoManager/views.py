from django.shortcuts import render, render_to_response
from repoManager.models import GitStore
import os
import subprocess
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.models import User

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

def logon(request):
    return render(request, 'login.html', { "failed": False })

def do_logon(request):
    username = request.POST["user_name"]
    password = request.POST["password"]

    auth_result = authenticate(username=username, password=password)
    if auth_result is not None:
        login(request, auth_result)
        page_result = redirect("index")
    else:
        context_instance = RequestContext(request)
        context_instance["failed"] = True
        page_result = render_to_response("login.html", context_instance)

    return page_result

def signup(request):
    return render(request, 'signup.html', { })

def do_signup(request):

    #create a user
    user_name = request.POST["user_name"]
    email = request.POST["email"]
    password = request.POST["password"]
    user = User.objects.create_user(user_name, email, password)
    user.save()

    auth_result = authenticate(username = user_name, password = password)
    login(request, auth_result)
    return redirect('index')

def do_logout(request):
    logout(request)
    return redirect('index')