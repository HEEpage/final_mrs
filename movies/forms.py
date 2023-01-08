from django import forms

class mvSesarchForm(forms.Form):
    search_word = forms.CharField(label='Search Word')