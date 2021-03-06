from django.contrib import admin
from sourceControlApp.models import CodeAuthor, Commit, UserGitStore, GitRepo, GitBranch, FileEntry


class UserGitStoreAdmin(admin.ModelAdmin):
    list_display = ["git_repo","name", "repo_description"]


class CodeAuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "git_branch", "num_commits", "additions", "deletions", "num_break_build"]


class CommitAdmin(admin.ModelAdmin):
    list_display = ["git_repo", "author", "commit_id"]


class GitRepoAdmin(admin.ModelAdmin):
    list_display = ["git_repository_url", "num_commits"]


class GitBranchAdmin(admin.ModelAdmin):
    list_display = ["git_repository_url","branch_name", "num_files", "num_commits", "status"]


class FileEntryAdmin(admin.ModelAdmin):
    list_display = ["file_path","git_branch", "num_edit", "in_current_built"]

# Register the models
admin.site.register(UserGitStore, UserGitStoreAdmin)
admin.site.register(CodeAuthor, CodeAuthorAdmin)
admin.site.register(Commit, CommitAdmin)
admin.site.register(GitRepo, GitRepoAdmin)
admin.site.register(GitBranch, GitBranchAdmin)
admin.site.register(FileEntry, FileEntryAdmin)

