from django.contrib import admin
from sourceControlApp.models import GitStore, CodeAuthor, Commit, UserGitStore, GitRepo, GitBranch

class GitStoreAdmin(admin.ModelAdmin):
    list_display = ["gitRepositoryURL", "numFiles"]

class UserGitStoreAdmin(admin.ModelAdmin):
    list_display = ["git_store","name", "repo_description"]

class CodeAuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "repository", "num_commits", "additions", "deletions"]

class CommitAdmin(admin.ModelAdmin):
    list_display = ["git_branch", "author"]

class GitRepoAdmin(admin.ModelAdmin):
    list_display = ["git_repository_url"]

class GitBranchAdmin(admin.ModelAdmin):
    list_display = ["git_repository_url","branch_name", "num_files", "num_commits", "status"]

# Register your models here.
admin.site.register(GitStore, GitStoreAdmin)
admin.site.register(UserGitStore, UserGitStoreAdmin)
admin.site.register(CodeAuthor, CodeAuthorAdmin)
admin.site.register(Commit, CommitAdmin)
admin.site.register(GitRepo, GitRepoAdmin)
admin.site.register(GitBranch, GitBranchAdmin)

