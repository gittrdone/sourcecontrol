from django.db import models

from sourceControlApp.models import SourceControlUser, UserGitStore

# Create your models here.
class Query(models.Model):
    name = models.CharField(max_length=256)
    query_command = models.CharField(max_length=1024)
    user = models.ForeignKey(SourceControlUser)

    CHART_TYPE_CHOICES = (
        ('pie', 'Pie'),
        ('bar', 'Bar'),
        ('line', 'Line')
    )

    chart_type = models.CharField(max_length=4, choices=CHART_TYPE_CHOICES, default='pie')

    def auto_chart_type(self):
        # XXX hacky version for now
        if "users" in self.query_command:
            return "pie"
        else:
            return "bar"

    def __unicode__(self):
        return unicode(self.name) + u' ' + unicode(self.query_command)

class Report(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=1024)
    queries = models.ManyToManyField(Query)
    repo = models.ForeignKey(UserGitStore)
    user = models.ForeignKey(SourceControlUser)

    def __unicode__(self):
        return unicode(self.user.user.username) + u' ' + unicode(self.name)
