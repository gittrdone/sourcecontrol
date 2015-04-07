from reporting.models import Report


# Generates data for header nav options when logged in
def repo_nav_options(request):
    user = request.user
    if request.user.is_authenticated() and hasattr(request.user, 'sourcecontroluser'):
        repos = user.sourcecontroluser.ownedRepos.all()
        repos_to_display = []
        default_branch_ids = []
        default_branch_files = []
        for repo in repos:
            if repo.git_repo and repo.git_repo.status == 3:
                repos_to_display.append(repo)
                default_branch_files.append(repo.git_repo.default_branch.num_files)
                default_branch_ids.append(repo.git_repo.default_branch.pk)
        return {'repo_nav_options':zip(repos_to_display, default_branch_ids, default_branch_files)}
    else:
        return {'repo_nav_options':None}


# Generates header nav options for reports
def repo_nav_options_reports(request):
    user = request.user
    if request.user.is_authenticated() and hasattr(request.user, 'sourcecontroluser'):
        repos = user.sourcecontroluser.ownedRepos.filter(git_repo__status=3).values('report__name', 'report__pk', 'name', 'pk')
        return {'repo_nav_options_reports': repos}
    else:
        return {'repo_nav_options_reports': None}