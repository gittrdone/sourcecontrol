import datetime
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from sourceControlApp.models import GitStore, SourceControlUser, UserGitStore

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
def json_pie_data_for_repo(request, repo_id):
    r = UserGitStore.objects.get(pk=repo_id)

    ## this a lot better to get the correct data without serializing the whole object ;)
    ## the select changes the name as part of the query thus saving time with having to rename dict keys
    values = r.git_store.codeauthor_set.extra(
        select={'label':'name', 'data':'num_commits'}
    ).values(
        'label', 'data'
    )
    response = JsonResponse(list(values), safe=False)
    return response

def json_bar_data_for_repo_commits(request, repo_id):
    r = UserGitStore.objects.get(pk=repo_id)

    ## ow ow ow
    hour_offset_from_utc = 4 #The library defaults to UTC
    last_week = datetime.datetime.today() - datetime.timedelta(days=6) - datetime.timedelta(hours=hour_offset_from_utc) # Beginning of this week
    today = datetime.datetime.now() - datetime.timedelta(hours=hour_offset_from_utc)

    ## here we differ slightly by populating the dict initially with zeroes and appending
    dbd = dates_between_datetimes(last_week, today)
    ## whoa dict comprehensions, next level maneuver
    daily_commit_counts = {i:0 for i in dbd}

    weekly_commits = r.git_store.commit_set.filter(commit_time__range=(last_week, today))
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
