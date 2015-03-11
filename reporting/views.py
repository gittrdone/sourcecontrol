import json
from collections import OrderedDict

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from sourceControlApp.querying.query_runner import process_string
from reporting.models import Report, Query, auto_chart_type
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
    context_instance['branch_id'] = repo.git_repo.branches.all()[0].pk


    return render_to_response("reports.html", context_instance)

# View an individual report
def view_report(request, repo_id, report_id):
    if not request.user.is_authenticated():
        return redirect("index")

    repo = UserGitStore.objects.get(pk=repo_id)
    report = Report.objects.get(user=request.user.sourcecontroluser, repo=repo, pk=report_id)

    context_instance = RequestContext(request)
    context_instance['default_branch_id'] = repo.git_repo.branches.all()[0].pk
    context_instance['repo_id'] = repo_id
    context_instance['report'] = report

    queries = report.queries.all()
    query_data = []
    for query in queries:
        query_result = process_string(query.query_command, repo)

        #MANGLE CHART DATA HERE (based on chart type)
        if query.chart_type == "pie":
            if query.model == "user":
                values = query_result.extra(
                    select={'label':'name', 'data':'num_commits'}).values(
                        'label', 'data')
            elif query.model == "commit":
                vals = OrderedDict()
                for commit in query_result:
                    date = commit.commit_time.date()
                    if date not in vals:
                        vals[date] = 0
                    vals[date] += 1

                values = [{'label': str(k), 'data': v} for k, v in vals.iteritems()]
            elif query.model == "file":
                values = query_result.values_list('file_path', 'num_edit')
                valueslist = [list(i) for i in values]
            elif query.model == "branch":
                values = query_result.values_list('branch_name', 'num_commits')
                valueslist = [list(i) for i in values]
            response = json.dumps(list(values))

        elif query.chart_type == "bar":
            if query.model == "user":
                values = query_result.values_list('name', 'num_commits')
                valueslist = [list(i) for i in values]
            elif query.model == "commit":
                vals = OrderedDict()
                for commit in query_result:
                    date = commit.commit_time.date()
                    if date not in vals:
                        vals[date] = 0
                    vals[date] += 1
                vals = OrderedDict(sorted(vals.items()))
                valueslist = [[str(k), v] for k,v in vals.iteritems()]
            elif query.model == "file":
                values = query_result.values_list('file_path', 'num_edit')
                valueslist = [list(i) for i in values]
            elif query.model == "branch":
                values = query_result.values_list('branch_name', 'num_commits')
                valueslist = [list(i) for i in values]
            response = json.dumps(valueslist)

        elif query.chart_type == "line":
            if query.model == "user":
                values = query_result.values_list('name', 'num_commits')
                valueslist = [list(i) for i in values]
            elif query.model == "commit":
                vals = OrderedDict()
                for commit in query_result:
                    date = commit.commit_time.date()
                    if date not in vals:
                        vals[date] = 0
                    vals[date] += 1
                vals = OrderedDict(sorted(vals.items()))
                valueslist = [[str(k), v] for k,v in vals.iteritems()]
            elif query.model == "file":
                values = query_result.values_list('file_path', 'num_edit')
                valueslist = [list(i) for i in values]
            elif query.model == "branch":
                values = query_result.values_list('branch_name', 'num_commits')
                valueslist = [list(i) for i in values]

            response = json.dumps(valueslist)

        query_data.append({'query': query, 'query_result': query_result, 'response': response})

    context_instance['queries'] = query_data
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

    if query_one_chart_type == "auto":
        query_one_chart_type = auto_chart_type(query_one_query)

    user = request.user
    sourceControlUser = user.sourcecontroluser
    repo = UserGitStore.objects.get(sourcecontroluser=sourceControlUser, pk=repo_id)

    query_one = Query(name=query_one_name, query_command=query_one_query, desc=query_one_desc, user=sourceControlUser, chart_type=query_one_chart_type)
    query_one.save()

    report = Report(user=sourceControlUser, name=report_name, description=report_desc, repo=repo)
    report.save()
    report.queries.add(query_one)

    num_queries = 1
    #count the queries
    for i in range(2,10+1):
        query_name = request.POST['query_' + str(i) + '_name']
        if query_name:
            num_queries = i

    #generate queries
    for i in range(2, num_queries+1):
        query_name = request.POST['query_' + str(i) + '_name']
        query_desc = request.POST['query_' + str(i) + '_desc']
        query_query = request.POST['query_' + str(i)]
        query_chart_type = request.POST['chart_' + str(i) + '_type']
        if query_chart_type == "auto":
            query_chart_type = auto_chart_type(query_query)
        query = Query(name=query_name, desc=query_desc, query_command=query_query, user=sourceControlUser, chart_type=query_chart_type)
        query.save()
        report.queries.add(query)
        report.save()

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

def edit_query(request):
    if not request.user.is_authenticated():
        return redirect("index")

    query_name = request.POST['editName']
    query_desc = request.POST['editDesc']
    query_command = request.POST['editCommand']
    query_id = request.POST['editQuery']

    query = Query.objects.get(user=request.user.sourcecontroluser, pk=query_id)

    query.name = query_name
    query.desc = query_desc
    query.query_command = query_command
    query.save()

    return redirect("view_report", repo_id=request.POST['repoID'], report_id=request.POST['reportID'])


def delete_query(request, repo_id, report_id, query_id):
    if not request.user.is_authenticated():
        return redirect("index")

    query = Query.objects.get(user=request.user.sourcecontroluser, pk=query_id)
    query.delete()

    return redirect("view_report", repo_id=repo_id, report_id=report_id)
