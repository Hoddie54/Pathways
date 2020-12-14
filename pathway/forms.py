from django import forms


class RatingsForm(forms.Form):
    ratings = forms.CharField()
    firm_id = forms.CharField()