from django.contrib import admin
from sourceControlApp.models import GitStore

class GitStoreAdmin(admin.ModelAdmin):
    list_display = ["gitRepositoryURL", "numFiles"]

# Register your models here.
admin.site.register(GitStore, GitStoreAdmin)