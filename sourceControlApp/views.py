from datetime import date, datetime, timedelta
from json import dumps
from django.shortcuts import render, render_to_response
from sourceControlApp.models import GitStore, SourceControlUser, UserGitStore
from sourceControlApp.repo_mgmt import get_repo_data_from_url, canonicalize_repo_url
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core import serializers
from .forms import UpdateUserGitStoreForm

# Create your views here.
def index(request):
    if request.user.is_authenticated():
        user = request.user
        repos = user.sourcecontroluser.ownedRepos.all()
        #form = UpdateUserGitStoreForm()
    else:
        repos = []
        #have it throw an error saying to log in

    if request.user.is_authenticated():
        return render(request, 'repoList.html', { 'repo_list': repos })
    else:
        return render(request, 'index.html', {})

def add_repo(request):
    context_instance = RequestContext(request)
    repo_url = request.GET['repo']
    repo_name = request.GET['name']
    repo_description = request.GET['desc']

    if request.user.is_authenticated():
        user = request.user
        sourceControlUser = user.sourcecontroluser

        try:
            existing_store = GitStore.objects.filter(gitRepositoryURL=canonicalize_repo_url(repo_url))[0]
        except:
            existing_store = None

        if existing_store != None and len(sourceControlUser.ownedRepos.filter(git_store=existing_store)) > 0:
            error = True
        else:
            repo = get_repo_data_from_url(repo_url, repo_name, repo_description, sourceControlUser)
            error = (repo == -1) # Check for error flag

        if error:
            context_instance["git_error"] = True
            context_instance["git_error_name"] = repo_name
            context_instance["git_error_description"] = repo_description
        else:
            sourceControlUser.ownedRepos.add(repo)

        # Store object and render page
        context_instance["repo_url"] = repo_url
        context_instance["repo_list"] = sourceControlUser.ownedRepos.all()
        return render_to_response("repoList.html", context_instance)
    else:
        # XXX Throw error
        return render_to_response("repoList.html", {})

def repo_detail(request):
    repo_id = request.GET['repo']

    repo = UserGitStore.objects.get(pk=repo_id)

    context_instance = RequestContext(request)
    context_instance['repo'] = repo
    context_instance['repo_pk'] = repo.pk
    context_instance['authors'] = repo.git_store.codeauthor_set.all().order_by('-num_commits')
    context_instance['json_authors'] = serializers.serialize("json", repo.git_store.codeauthor_set.all())

    hour_offset_from_utc = 4 #The library defaults to UTC
    last_week = datetime.today() - timedelta(days=6) - timedelta(hours=hour_offset_from_utc) # Beginning of this week
    today = datetime.now() - timedelta(hours=hour_offset_from_utc)

    daily_commit_counts = {}
    weekly_commits = repo.git_store.commit_set.filter(commit_time__range=(last_week, today))
    for commit in weekly_commits:
        day_commit = commit.commit_time - timedelta(hours=hour_offset_from_utc)
        day = day_commit.day
        if day in daily_commit_counts:
            daily_commit_counts[day] = daily_commit_counts[day] + 1
        else:
            daily_commit_counts[day] = 0

    context_instance['week_commits'] = dumps(daily_commit_counts)
    return render_to_response("repoDetail.html", context_instance)

def repo_status(request, repo_id):
    user_repo = UserGitStore.objects.get(pk=repo_id)
    repo = user_repo.git_store

    ret = {}
    ret['status'] = repo.status
    if repo.status == 3:
        ret['numFiles'] = repo.numFiles
        ret['numCommits'] = repo.numCommits

    return HttpResponse(dumps(ret), content_type="application/json")


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

def edit_repo(request):
    context_instance = RequestContext(request)
    repo_url = request.POST['editRepo']
    repo_name = request.POST['editName']
    repo_description = request.POST['editDesc']

    if request.user.is_authenticated():
        user = request.user
        sourceControlUser = user.sourcecontroluser

        try:
            existing_storee = GitStore.objects.get(gitRepositoryURL=canonicalize_repo_url(repo_url))
            existing_store = sourceControlUser.ownedRepos.get(git_store = existing_storee)
        except:
            existing_store = None

        #otherwise we are good to go on editing
        existing_store.name = repo_name
        existing_store.repo_description = repo_description
        existing_store.save()

        # Re-serve the page
        context_instance["repo_list"] = sourceControlUser.ownedRepos.all()
        return render_to_response("repoList.html", context_instance)
    else:
        # XXX Throw error
        return render_to_response("repoList.html", {})

def delete_repo(request):
    context_instance = RequestContext(request)
    repo_url = request.POST['editRepo']

    if request.user.is_authenticated():
        user = request.user
        sourceControlUser = user.sourcecontroluser

        try:
            existing_storee = GitStore.objects.get(gitRepositoryURL=canonicalize_repo_url(repo_url))
            existing_store = sourceControlUser.ownedRepos.get(git_store = existing_storee)
        except:
            existing_store = None

        #otherwise we are good to go on deleting
        UserGitStore.delete(existing_store)

        # Store object and render page
        context_instance["repo_url"] = repo_url
        context_instance["repo_list"] = sourceControlUser.ownedRepos.all()
        return render_to_response("repoList.html", context_instance)
    else:
        # XXX Throw error
        return render_to_response("repoList.html", {})
