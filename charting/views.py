import datetime
from django.http import JsonResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
import pytz
from sourceControlApp.models import GitStore, SourceControlUser, UserGitStore, GitBranch, CodeAuthor


def dates_between_datetimes(start,end):
    """
    this is a generator to generate a list of date values between two dates
    :param start:  start date
    :param end:  end date
    :return:
    """
    while start < end:
        yield start.date()
        start += datetime.timedelta(days=1)
# Create your views here.
def json_pie_data_for_repo(request, repo_id, branch_id):
    r = UserGitStore.objects.get(pk=repo_id)
    b = GitBranch.objects.get(pk=branch_id)

    ## this a lot better to get the correct data without serializing the whole object ;)
    ## the select changes the name as part of the query thus saving time with having to rename dict keys
    values = b.codeauthor_set.extra(
        select={'label':'name', 'data':'num_commits'}
    ).values(
        'label', 'data'
    )
    response = JsonResponse(list(values), safe=False)
    return response

def json_bar_data_for_repo_commits(request, repo_id, branch_id):
    r = UserGitStore.objects.get(pk=repo_id)
    b = GitBranch.objects.get(pk=branch_id)

    ## XXX ow ow ow
    hour_offset_from_utc = 4 #The library defaults to UTC
    last_week = datetime.datetime.today() - datetime.timedelta(days=6) - datetime.timedelta(hours=hour_offset_from_utc) # Beginning of this week
    today = datetime.datetime.now() - datetime.timedelta(hours=hour_offset_from_utc)

    ## here we differ slightly by populating the dict initially with zeroes and appending
    dbd = dates_between_datetimes(last_week, today)
    ## whoa dict comprehensions, next level maneuver
    daily_commit_counts = {i:0 for i in dbd}

    weekly_commits = b.commit_set.filter(commit_time__range=(last_week, today))
    for commit in weekly_commits:
        day_commit = commit.commit_time - datetime.timedelta(hours=hour_offset_from_utc)
        day = day_commit.date()
        ## since the dictionary is already prepopulated with the dates, no need for if else
        daily_commit_counts[day] += 1
        ## also +=1 is a lot cleaner for appending, neat tricks you can do stuff like -=, *=, /= etc

    ## do something for real with it, also lol dicts don't store order
    daily_commit_keys = sorted(daily_commit_counts, key= lambda k: k)
    # flot wants it this way.
    daily_commit_list = [[i.strftime("%a"),daily_commit_counts[i]] for i in daily_commit_keys]

    response = JsonResponse(daily_commit_list, safe=False)
    return response

def json_bar_data_for_user_repo_commits(request, committer_id, start=None, end=None, days=7):
    author=get_object_or_404(CodeAuthor, pk=committer_id)

    if not ( start and end ):
        #utc_end = datetime.datetime.now(pytz.utc)
        #end = utc_end - datetime.timedelta(hours=4)
        #start = end - datetime.timedelta(days=days)
        ## ow ow ow
        hour_offset_from_utc = 4 #The library defaults to UTC
        start = datetime.datetime.today() - datetime.timedelta(days=6) - datetime.timedelta(hours=hour_offset_from_utc) # Beginning of this week
        end = datetime.datetime.now() - datetime.timedelta(hours=hour_offset_from_utc)

    if end and not start:
        start = end - datetime.timedelta(days=days)


    author_commits=author.commit_set.filter(commit_time__range=(start,end))

    # author_commits = author.commit_set.all()
    dbd = dates_between_datetimes(start, end)
    ## whoa dict comprehensions, next level maneuver
    e = {i:0 for i in dbd}
    # e={}
    for i in author_commits:
        if i.commit_time.date() in e:
            e[i.commit_time.date()] += 1
        else:
            e[i.commit_time.date()] = 1

     ## do something for real with it, also lol dicts don't store order
    daily_commit_keys = sorted(e, key= lambda k: k)
    # flot wants it this way.
    daily_commit_list = [[i.strftime("%a"),e[i]] for i in daily_commit_keys]

    return JsonResponse(daily_commit_list, safe=False)


