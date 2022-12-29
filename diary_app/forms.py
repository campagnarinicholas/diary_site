from django import forms
from .models import EntryType, Entry

class EntryTypeForm(forms.ModelForm):
    """
    Form for creating EntryTypes
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(EntryTypeForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.user = self.user
        return super(EntryTypeForm, self).save(*args, **kwargs)

    class Meta:
        model = EntryType
        # Don't show the user on the form
        exclude = ('user',)

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['entry_type', 'length']