from django.db import models

from sourceControlApp.models import SourceControlUser, UserGitStore

def auto_chart_type(query_command):
    # XXX hacky version for now
    if "users" in query_command:
        return "pie"
    else:
        return "bar"

# Create your models here.
class Query(models.Model):
    name = models.CharField(max_length=256)
    desc = models.CharField(max_length=1024, default='')
    query_command = models.CharField(max_length=1024)
    user = models.ForeignKey(SourceControlUser)

    CHART_TYPE_CHOICES = (
        ('pie', 'Pie'),
        ('bar', 'Bar'),
        ('line', 'Line')
    )

    @property
    def model(self):
        #XXX gross
        if "users" in self.query_command:
            return "user"
        elif "commits" in self.query_command:
            return "commit"
        elif "branches" in self.query_command:
            return "branch"
        elif "files" in self.query_command:
            return "file"
        else:
            pass

    chart_type = models.CharField(max_length=4, choices=CHART_TYPE_CHOICES, default='pie')

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
