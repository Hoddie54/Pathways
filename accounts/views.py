from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from .forms import MyUserCreationForm, MyUserCreationForm2
from pathway.models import Firm, DisplayStage
from tracker.models import UserIndustry, UserFirm
from formtools.wizard.views import SessionWizardView

FORMS = [('step1', MyUserCreationForm),
         ('step2', MyUserCreationForm2),]

TEMPLATES = {'step1': 'registration/signup1.html',
             'step2': 'registration/signup2.html'}

class SignUpView(SessionWizardView):
    #form_class = MyUserCreationForm
    #success_url = reverse_lazy('login')
    #template_name = 'registration/signup1.html'

    def done(self, form_list, form_dict, **kwargs):

        form_data = [form.cleaned_data for form in form_list]
        new_user = get_user_model().objects.create_user(
            email=form_data[0]['email'],
            full_name=form_data[0]['full_name'],
            password=form_data[0]['password2'],
            number=form_data[1]['number'],
            university=form_data[1]['university'],
            university_society=form_data[1]['university_society'],
            university_society_position=form_data[1]['university_society_position'],
        )
        print(form_data[1]['industry'])
        new_user.save()
        for CurrentIndustry in form_data[1]['industry']:
            new_user_industry = UserIndustry.objects.create(
                user=new_user,
                industry=CurrentIndustry,
            )
            new_user_industry.save()

        for firm in Firm.objects.all():
            new_user_firm = UserFirm.objects.create(
                user=new_user,
                firm=firm,
                stage=firm.displaystage_set.first()
            )
            new_user_firm.save()

        return HttpResponseRedirect(reverse_lazy('login'))

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]


