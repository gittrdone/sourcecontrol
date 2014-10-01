from django.shortcuts import render, render_to_response
from sourceControlApp.models import GitStore, SourceControlUser
from sourceControlApp.repo_mgmt import get_repo_data_from_url
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def index(request):
    if request.user.is_authenticated():
        user = request.user
        repos = user.sourcecontroluser.ownedRepos.all() 
    else:
        repos = []
        #have it throw an error saying to log in
    return render(request, 'repoList.html', { 'repo_list': repos })

def add_repo(request):
    context_instance = RequestContext(request)
    repo_url = request.GET['repo']

    repo = get_repo_data_from_url(repo_url)
    error = (repo == -1) # Check for error flag

    if request.user.is_authenticated():
        user = request.user
        sourceControlUser = user.sourcecontroluser
        if error:
            context_instance["git_error"] = True
        else:
            sourceControlUser.ownedRepos.add(repo)

        # Store object and render page
        context_instance["repo_url"] = repo_url
        context_instance["repo_list"] = sourceControlUser.ownedRepos.all()
        return render_to_response("repoList.html", context_instance)
    else:
        return render_to_response("repoList.html", {})

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
    
    sourceControlUser = SourceControlUser.objects.create(user=user) 
    return redirect('index')

def do_logout(request):
    logout(request)
    return redirect('index')

def load_repo_page(request):
    repo_url = request.repo_url
