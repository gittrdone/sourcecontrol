from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from sourceControlApp.models import UserGitStore, CodeAuthor, GitBranch
# Create your views here.

def user_repo_detail(request, cid, repo_id, branch_id):
    context_instance = RequestContext(request)
    author = context_instance['author'] = get_object_or_404(CodeAuthor, pk=cid)
    repo = UserGitStore.objects.get(pk=repo_id)
    branch = GitBranch.objects.get(pk=branch_id)

    context_instance['branches'] = repo.git_repo.branches.filter(codeauthor__name=author.name).values(
        'codeauthor__pk', 'pk', 'branch_name')
    context_instance['branch'] = branch
    context_instance['repo_pk'] = repo.pk
    context_instance['lines_per_commit'] = (author.additions - author.deletions)/author.num_commits

    return render_to_response("userDetail.html", context_instance)

