from django.shortcuts import render
from django.views.generic import TemplateView
from .models import UserFirm
from .forms import OrderingForm
from pathway.models import DisplayStage
from accounts.models import LoginEvent
from django.shortcuts import redirect
from django.contrib.auth.mixins import  LoginRequiredMixin
from django.db import transaction


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        firm_list = UserFirm.objects.filter(user_id=self.request.user).order_by('order')
        context['firm_list'] = firm_list
        context['stage_list'] = DisplayStage.objects.all()
        context['streak'] = self.request.user.streak

        return context

    def save_firm_ordering(request):
        form = OrderingForm(request.POST)

        if form.is_valid():
            ordered_ids = form.cleaned_data["ordering"].split(',')
            new_stages = form.cleaned_data["stage"].split(',')
            with transaction.atomic():
                current_order=1
                for counter, id in enumerate(ordered_ids):

                    firm = UserFirm.objects.get(id=id, user=request.user)
                    print(firm.firm.name + " " + new_stages[counter] + " " + str(request.user))
                    firm.order = current_order
                    firm.stage = DisplayStage.objects.get(id=new_stages[counter])
                    firm.save()
                    current_order +=1
            return redirect('dashboard')