from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from pathway.models import Industry

class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('full_name', 'email')


class MyUserCreationForm2(UserCreationForm):
    university = forms.CharField()
    year = forms.ChoiceField(choices=[('1','First year'),('2', 'Second year'),('3', 'Third year'), ('4', 'Fourth year'),('5', '5th year or higher')]
                             ,widget=forms.Select(attrs={
            'style': 'color: #1d8cf8'
        }))
    university_society_position = forms.ChoiceField(
        choices=[('NA or Other','NA or other'),('President', 'President'), ('Treasurer', 'Treasurer'),
                 ('Secretary', 'Secretary'), ('Careers officer', 'Careers officer'),
                 ]
        , widget=forms.Select(attrs={
            'style': 'color: #1d8cf8'
        }))
    industry = forms.ModelMultipleChoiceField(queryset=Industry.objects.all())

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('university', 'year', 'university_society', 'university_society_position','number', 'industry')

    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm2, self).__init__(*args, **kwargs)
        del self.fields['password1']
        del self.fields['password2']



class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('email', 'number', 'university')






