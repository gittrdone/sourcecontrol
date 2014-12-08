def repo_nav_options(request):
    user = request.user
    if request.user.is_authenticated():
        repos = user.sourcecontroluser.ownedRepos.all()
        default_branch_ids = []
        default_branch_files = []
        for repo in repos:
            if repo.git_repo.status == 3:
                default_branch_files.append(repo.git_repo.branches.all()[0].num_files)
                default_branch_ids.append(repo.git_repo.branches.all()[0].pk)
            else:
                default_branch_files.append(-1)
                default_branch_ids.append(-1)
        return {'repo_nav_options':zip(repos, default_branch_ids, default_branch_files)}