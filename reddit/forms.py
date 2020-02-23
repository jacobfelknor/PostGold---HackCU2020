from django import forms


class RedditSearch(forms.Form):
    q = forms.CharField(label="Ex: lifeofnorman")
