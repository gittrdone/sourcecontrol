from django.contrib import admin
from reporting.models import Query, Report


class QueryAdmin(admin.ModelAdmin):
    list_display = ["name", "query_command", "user", "chart_type"]


class ReportAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "repo", "user"]

admin.site.register(Query, QueryAdmin)
admin.site.register(Report, ReportAdmin)
