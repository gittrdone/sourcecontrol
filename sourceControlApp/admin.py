from django.contrib import admin
from sourceControlApp.models import GitStore, CodeAuthor, Commit

class GitStoreAdmin(admin.ModelAdmin):
    list_display = ["gitRepositoryURL", "numFiles", "repoName"]

class CodeAuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "repository", "num_commits"]

class CommitAdmin(admin.ModelAdmin):
    list_display = ["repository", "author", "num_patches"]

# Register your models here.
admin.site.register(GitStore, GitStoreAdmin)
admin.site.register(CodeAuthor, CodeAuthorAdmin)
admin.site.register(Commit, CommitAdmin)