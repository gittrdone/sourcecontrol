import json

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from sourceControlApp.querying.query_runner import process_string
from reporting.models import Report, Query
from sourceControlApp.models import UserGitStore
from django.http import JsonResponse

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
    query_result = process_string(report.queries.all()[0].query_command, repo)
    context_instance['query_result'] = query_result

    query_chart_type = report.queries.all()[0].chart_type
    context_instance['query_chart_type'] = query_chart_type

    #MANGLE CHART DATA HERE (based on chart type)
    if query_chart_type == "pie":
        #if query_result.model == "users":
        values = query_result.extra(
            select={'label':'name', 'data':'num_commits'} ).values(
                'label', 'data')

        response = json.dumps(list(values))

    elif query_chart_type == "bar":
    #    if query_result.model == "user":
        values = query_result.values_list('name', 'num_commits')
        valueslist = [list(i) for i in values]

        response = json.dumps(valueslist)

    elif query_chart_type == "line":
        #    if query_result.model == "user":
        values = query_result.values_list('name', 'num_commits')
        valueslist = [list(i) for i in values]

        response = json.dumps(valueslist)

    context_instance['response'] = response
    return render_to_response("report.html", context_instance)

# The interface for making a new report
def new_report(request, repo_id):
    if not request.user.is_authenticated():
        return redirect("index")

    context_instance = RequestContext(request)
    context_instance['queries'] = Query.objects.filter(user=request.user)

    return render_to_response("newReport.html", context_instance)

def addReport(request, repo_id):
    if not request.user.is_authenticated():
        return redirect("index")

    context_instance = RequestContext(request)
    context_instance['repo_id'] = repo_id

    return render_to_response("addReport.html", context_instance)

# Endpoint for adding a new report to the DB
def add_report(request, repo_id):
    if not request.user.is_authenticated():
        return redirect("index")

    report_name = request.POST['report_name']
    report_desc = request.POST['report_desc']
    query_one_name = request.POST['query_1_name']
    query_one_desc = request.POST['query_1_desc']
    query_one_query = request.POST['query_1']
    query_one_chart_type = request.POST['chart_1_type']

    user = request.user
    sourceControlUser = user.sourcecontroluser
    repo = UserGitStore.objects.get(sourcecontroluser=sourceControlUser, pk=repo_id)

    query_one = Query(name=query_one_name, query_command=query_one_query, desc=query_one_desc, user=sourceControlUser, chart_type=query_one_chart_type)
    query_one.save()

    report = Report(user=sourceControlUser, name=report_name, description=report_desc, repo=repo)
    report.save()
    report.queries.add(query_one)

    num_queries = 1;
    #count the queries
    for i in range(2,10):
        query_name = request.POST['query_' + str(i) + '_name']
        if query_name:
            num_queries = i

    #generate queries
    for i in range(2, num_queries):
        query_name = request.POST['query_' + str(i) + '_name']
        query_desc = request.POST['query_' + str(i) + '_desc']
        query_query = request.POST['query_' + str(i)]
        query_chart_type = request.POST['chart_' + str(i) + '_type']
        query = Query(name=query_name, desc=query_desc, query_command=query_query, user=sourceControlUser, chart_type=query_chart_type)
        query.save()
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