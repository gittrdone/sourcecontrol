from datetime import datetime, timedelta
from json import dumps
from django.shortcuts import render, render_to_response, get_object_or_404
from sourceControlApp.models import GitRepo, SourceControlUser, UserGitStore, GitBranch
from sourceControlApp.repo_mgmt import get_repo_data_from_url, canonicalize_repo_url, update_jenkins_info
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core import serializers


def index(request):
    """
    Renders the main page of SourceControl.
    If the user is logged in, she gets a repo list.
    :param request:
    :return:
    """
    if not request.user.is_authenticated():
        return render(request, 'index.html', {})

    user = request.user
    repos = user.sourcecontroluser.ownedRepos.all()
    default_branch_ids = []
    default_branch_files = []
    for repo in repos:
        if repo.git_repo.status == 3:
            default_branch_files.append(repo.git_repo.default_branch.num_files)
            default_branch_ids.append(repo.git_repo.default_branch.pk)
        else:
            default_branch_files.append(-1)
            default_branch_ids.append(-1)

    context_instance = RequestContext(request)
    context_instance["repo_list"] = zip(repos, default_branch_ids, default_branch_files)

    return render_to_response('repoList.html', context_instance)


def add_repo(request):
    """
    Adds a repos to a user's list of repos
    :param request:
    :return:
    """
    if not request.user.is_authenticated():
        return redirect("index")

    repo_url = request.GET['repo']
    repo_name = request.GET['name']
    repo_description = request.GET['desc']
    try:
        repo_jenkins_url = request.GET['jenkinsUrl']
        repo_jenkins_job_name = request.GET['jenkinsJobName']
    except:
        repo_jenkins_url = ""
        repo_jenkins_job_name = ""

    doEmail = True
    try:
        email_to = request.GET['emailTo']
    except:
        email_to = ""

    user = request.user
    source_control_user = user.sourcecontroluser

    try:
        existing_store = GitRepo.objects.filter(git_repository_url=canonicalize_repo_url(repo_url))[0]
    except:
        existing_store = None

    if existing_store is not None and len(source_control_user.ownedRepos.filter(git_repo=existing_store)) > 0:
        error = True
        already_own = True
    else:
        repo = get_repo_data_from_url(repo_url, repo_name, repo_description,
                                      source_control_user, email_address=email_to)
        error = (repo == -1)  # Check for error flag
        already_own = False

    if error:
        if already_own:
            messages.error(request, "You already have this repository in your account!")
        else:
            messages.error(request, "Not a valid repository!")
    else:
        source_control_user.ownedRepos.add(repo)
        update_jenkins_info(repo.git_repo, repo_jenkins_url, repo_jenkins_job_name)

    return redirect("index")


def repo_detail(request, repo_id, branch_id):
    """
    Renders the main page of SourceControl.
    If the user is logged in, she gets a repo list.
    :param request:
    :return:
    """
    repo = UserGitStore.objects.get(pk=repo_id)
    branch = GitBranch.objects.get(pk=branch_id)

    context_instance = RequestContext(request)
    context_instance['repo'] = repo
    context_instance['repo_pk'] = repo.pk
    context_instance['authors'] = branch.codeauthor_set.all().order_by('-num_commits')
    context_instance['json_authors'] = serializers.serialize("json", branch.codeauthor_set.all())
    context_instance['branches'] = repo.git_repo.branches.all()
    context_instance['branch'] = branch

    hour_offset_from_utc = 4  # The library defaults to UTC
    last_week = datetime.today() - timedelta(days=6) - timedelta(hours=hour_offset_from_utc) # Beginning of this week
    today = datetime.now() - timedelta(hours=hour_offset_from_utc)

    daily_commit_counts = {}
    weekly_commits = branch.commit_set.filter(commit_time__range=(last_week, today))
    for commit in weekly_commits:
        day_commit = commit.commit_time - timedelta(hours=hour_offset_from_utc)
        day = day_commit.day
        if day in daily_commit_counts:
            daily_commit_counts[day] += 1
        else:
            daily_commit_counts[day] = 0

    context_instance['week_commits'] = dumps(daily_commit_counts)
    return render_to_response("repoDetail.html", context_instance)


def repo_status(request, repo_id):
    """
    Returns status of the current repo in terms of its cloning and processing
    :param request:
    :param repo_id: The repo to check
    :return: A json object containing the status
    """

    user_repo = UserGitStore.objects.get(pk=repo_id)
    repo = user_repo.git_repo

    ret = {'status': repo.status}
    if repo.status == 3:
        ret['numFiles'] = repo.default_branch.num_files
        ret['numCommits'] = repo.num_commits
        ret['branchId'] = repo.default_branch.pk

    return HttpResponse(dumps(ret), content_type="application/json")


def do_logon(request):
    """
    Logs a user in and redirects them to the main page (which will now be a repo list)
    If it fails, we'll reload the page with an error
    :param request:
    :return:
    """
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


def do_signup(request):
    """
    Create and register a new user
    Or fail and tell them why
    :param request:
    :return:
    """
    # Create a user
    user_name = request.POST["user_name"]

    # Check if user object with same name already exists
    if User.objects.filter(username=user_name):
        return render(request, 'signup.html', {'fail': True})

    else:
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.create_user(user_name, email, password)
        user.save()

        auth_result = authenticate(username = user_name, password = password)
        login(request, auth_result)

        # Create the actual user
        SourceControlUser.objects.create(user=user)
        return redirect('index')


def do_logout(request):
    """
    Logs the user out and redirects them to the main page,
    which will now be the landing page
    :param request:
    :return:
    """
    logout(request)
    return redirect('index')


def edit_repo(request):
    """
    Edits a user's repository details, such as name and description
    :param request:
    :return:
    """
    if not request.user.is_authenticated():
        return redirect("index")

    repo_url = request.POST['editRepo']
    repo_name = request.POST['editName']
    repo_description = request.POST['editDesc']

    user = request.user
    source_control_user = user.sourcecontroluser

    try:
        existing_store_repo = GitRepo.objects.get(git_repository_url=canonicalize_repo_url(repo_url))
        existing_store = source_control_user.ownedRepos.get(git_repo=existing_store_repo)
    except:
        existing_store = None

    if existing_store is None:
        # Handle error
        pass
    else:
        # Otherwise we are good to go on editing
        existing_store.name = repo_name
        existing_store.repo_description = repo_description
        existing_store.save()

    # Re-serve the page
    return redirect("index")


def delete_repo(request, id):
    """
    Deletes a repository from a user's list
    :param request:
    :param id:
    :return:
    """
    if not request.user.is_authenticated():
        return redirect("index")

    # XXX Check ownership
    o = get_object_or_404(UserGitStore, pk=id)
    o.delete()

    return redirect("index")


def edit_user_settings(request):
    """
    Modify user settings
    :param request:
    :return:
    """
    if not request.user.is_authenticated():
        return redirect("index")

    user = request.user
    user_name = request.POST["edit_name"]
    email = request.POST["edit_email"]
    user.username = user_name
    user.email = email
    user.save()
    return redirect("index")


# Static pages:
def logon(request):
    """
    Logon page
    :param request:
    :return:
    """
    return render(request, 'login.html', {"failed": False})


def signup(request):
    """
    Sign up page
    :param request:
    :return:
    """
    return render(request, 'signup.html', {})


def queryhelp(request):
    """
    Query help page
    :param request:
    :return:
    """
    context_instance = RequestContext(request)
    return render_to_response("queryhelp.html", context_instance)


def queryref(request):
    """
    Query reference page
    :param request:
    :return:
    """
    context_instance = RequestContext(request)
    return render_to_response("queryReference.html", context_instance)


def queryexamples(request):
    """
    Query examples page
    :param request:
    :return:
    """
    context_instance = RequestContext(request)
    return render_to_response("queryExamples.html", context_instance)