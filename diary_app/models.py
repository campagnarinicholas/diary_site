from django.db import models
from django.contrib.auth.models import User

class EntryType(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField('date created', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Entry(models.Model):
    started_at = models.DateTimeField('started at', auto_now_add=True)
    length = models.IntegerField(default=0)
    entry_type = models.ForeignKey(EntryType, on_delete=models.CASCADE)

    def get_entry_type_url(self):
        link = '<a href="{% url "diary_app:entry_type" ' + self.entry_type_id  + ' %}" class="btn btn-danger">' + self.entry_type.name + '</a>'
        return link