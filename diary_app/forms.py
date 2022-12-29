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
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.entry_type = kwargs.pop('pk')            
        super(EntryForm, self).__init__(*args, **kwargs)
        
        if self.entry_type is not None:
            self.fields['entry_type'].queryset = EntryType.objects.filter(pk=self.entry_type)
        else:    
            self.fields['entry_type'].queryset = EntryType.objects.filter(user=self.user)

    class Meta:
        model = Entry
        fields = ['entry_type', 'length']

    @staticmethod
    def get_initial(pk):
        if pk is not None:
            entry_type = EntryType.objects.get(pk=pk)
            initial = {
                'entry_type': entry_type,
                'length': 0
            }
        else: 
            initial = {
                'length': 0
            }
        return initial