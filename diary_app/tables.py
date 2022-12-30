import django_tables2 as tables
from .models import Entry, EntryType
from django_tables2.utils import A  # alias for Accessor

class EntryTable(tables.Table):
    delete = tables.TemplateColumn(template_code='<a href="{% url "diary_app:delete_entry" record.id %}" class="btn btn-danger">Delete</a>')

    class Meta:
        model = Entry
        template_name = "django_tables2/semantic.html"
        exclude = ('id',)
