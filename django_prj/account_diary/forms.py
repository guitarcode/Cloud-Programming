from django import forms

from .models import AccountDiary


class AccountDiaryForm(forms.ModelForm):
    class Meta:
        model = AccountDiary
        fields = ['title', 'date', 'store', 'type', 'account_tag', 'amount', 'is_public', 'description']

        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
