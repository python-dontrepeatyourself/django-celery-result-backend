from django import forms

class SendEmailForm(forms.Form):
    email = forms.EmailField()