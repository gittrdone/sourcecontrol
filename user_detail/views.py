from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from sourceControlApp.models import GitStore, CodeAuthor
# Create your views here.

def user_repo_detail(request, cid):
    context_instance = RequestContext(request)
    context_instance['author'] = get_object_or_404(CodeAuthor, pk=cid)
    return render_to_response("userDetail.html", context_instance)



