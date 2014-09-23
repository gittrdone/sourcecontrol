from django.contrib import admin
from repoManager.models import GitStore

class GitStoreAdmin(admin.ModelAdmin):
    list_display = ["gitRepositoryURL", "numFiles"]

# Register your models here.
admin.site.register(GitStore, GitStoreAdmin)