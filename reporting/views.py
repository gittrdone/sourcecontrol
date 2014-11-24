import json

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from sourceControlApp.querying.query_runner import process_string
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
    report = Report.objects.get(user=request.user.sourcecontroluser, repo=repo, pk=report_id)

    context_instance = RequestContext(request)
    context_instance['report'] = report

    # XXX Only does first query for now!!
    context_instance['query_result'] = process_string(report.queries.all()[0].query_command, repo)

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

    user = request.user
    sourceControlUser = user.sourcecontroluser
    repo = UserGitStore.objects.get(sourcecontroluser=sourceControlUser, pk=repo_id)

    query = Query(name=report_query_name, query_command=report_query_query, user=sourceControlUser)
    query.save()

    report = Report(user=sourceControlUser, name=report_name, description=report_desc, repo=repo)
    report.save()
    report.queries.add(query)

    context_instance = RequestContext(request)
    context_instance['reports_list'] = Report.objects.filter(user=sourceControlUser, repo=repo)
    context_instance['repo_name'] = repo.name

    return redirect("reports", repo_id=repo_id)

def edit_report(request):
    if not request.user.is_authenticated():
        return redirect("index")

    report_name = request.POST['editName']
    report_desc = request.POST['editDesc']
    report_id = request.POST['editReport']

    report = Report.objects.get(user=request.user.sourcecontroluser, pk=report_id)

    report.name = report_name
    report.description = report_desc
    report.save()

    return redirect("reports", repo_id=report.repo.pk)

def delete_report(request, repo_id, report_id):
    if not request.user.is_authenticated():
        return redirect("index")

    report = Report.objects.get(user=request.user.sourcecontroluser, pk=report_id)
    report.delete()

    return redirect("reports", repo_id=repo_id)