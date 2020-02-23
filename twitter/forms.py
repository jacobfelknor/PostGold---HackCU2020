from django import forms


class TwitterSearch(forms.Form):
    q = forms.CharField(label="Ex: elonmusk")
