from django import forms

from .models import AccountDiary
from store.models import Store


class AccountDiaryForm(forms.ModelForm):
    store = forms.ModelChoiceField(queryset=Store.objects.all(), required=False)

    class Meta:
        model = AccountDiary
        fields = ['title', 'date', 'type', 'store', 'account_tag', 'amount', 'is_public', 'description']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['store'].required = False
        self.fields['description'].required = False

    def clean(self):
        cleaned_data = super().clean()
        type = cleaned_data.get('type')

        if type == 'IN':
            cleaned_data['is_public'] = False

        return cleaned_data
