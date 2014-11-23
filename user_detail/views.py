from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from sourceControlApp.models import GitStore, CodeAuthor
from django.core import serializers
# Create your views here.

def user_repo_detail(request, cid):
    context_instance = RequestContext(request)
    author = context_instance['author'] = get_object_or_404(CodeAuthor, pk=cid)
    # context_instance['json_commits'] = serializers.serialize("json", author.commit_set.all())

    return render_to_response("userDetail.html", context_instance)



