import json

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from reporting.models import Report, Query
from sourceControlApp.models import UserGitStore

# View existing reports list
def view_reports(request, repo_id):
    if not request.user.is_authenticated():
        return redirect("index")

    repo = UserGitStore.objects.get(pk=repo_id)
    sourceControlUser = request.user.sourcecontroluser

    context_instance = RequestContext(request)
    context_instance['reports_list'] = Report.objects.filter(user=sourceControlUser, repo=repo)
    context_instance['repo_name'] = repo.name
    context_instance['repo_id'] = repo.pk

    return render_to_response("reports.html", context_instance)

# View an individual report
def view_report(request, repo_id, report_id):
    if not request.user.is_authenticated():
        return redirect("index")

    repo = UserGitStore.objects.get(pk=repo_id)

    context_instance = RequestContext(request)
    context_instance['report'] = Report.objects.get(user=request.user, repo=repo, pk=report_id)

    return render_to_response("report.html", context_instance)

# The interface for making a new report
def new_report(request, repo_id):
    if not request.user.is_authenticated():
        return redirect("index")

    context_instance = RequestContext(request)
    context_instance['queries'] = Query.objects.filter(user=request.user)

    return render_to_response("newReport.html", context_instance)

# Endpoint for adding a new report to the DB
def add_report(request, repo_id):
    if not request.user.is_authenticated():
        return redirect("index")

    report_name = request.GET['report_name']
    report_query_name = request.GET['report_query_name']
    report_query_query = request.GET['report_query_query']
    report_desc = request.GET['report_desc']
    #data = json.loads(request.body)

    #queries = data['queries']

    #for query in data['new_queries']:
    #    new_q = Query(user=request.user, name=query['name'], query_command=query['command'])
    #    new_q.save()
    #    queries.append(new_q)


    user = request.user
    sourceControlUser = user.sourcecontroluser
    repo = UserGitStore.objects.get(sourcecontroluser=sourceControlUser, pk=repo_id)

    query = Query(name=report_query_name, query_command=report_query_query, user=sourceControlUser)
    query.save()

    #report = Report(user=request.user, name=data['name'], description=['desc'], repo=repo, queries=queries)
    report = Report(user=sourceControlUser, name=report_name, description=report_desc, repo=repo)
    report.save()
    report.queries.add(query)

    #return redirect("reports")
    context_instance = RequestContext(request)
    context_instance['reports_list'] = Report.objects.filter(user=sourceControlUser, repo=repo)
    context_instance['repo_name'] = repo.name
    return redirect("reports", repo_id=repo_id)

def remove_report(request, report_id):
    if not request.user.is_authenticated():
        return redirect("index")

    report = Report.objects.get(user=request.user, pk=report_id)
    report.delete()

    return redirect("reports")