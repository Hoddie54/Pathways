from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.db.models import Sum
from .models import DisplayStage, Firm, PathwayPoint, UserPathwayPoint
from .forms import RatingsForm


class Pathway_Detail_View(TemplateView):
    template_name = 'pathway_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        pk = kwargs['pk']
        firm = Firm.objects.get(pk=pk)
        stages = DisplayStage.objects.filter(firm=firm)
        pathwayPoints = PathwayPoint.objects.filter(displayStage__firm=firm)


        fullStageData = []
        for stage in stages:
            total_stages = len(PathwayPoint.objects.filter(displayStage=stage))
            total_score_self_rated = UserPathwayPoint.objects.filter(user=self.request.user, pathwayPoint__displayStage=stage).aggregate(Sum('rating'))
            if(total_score_self_rated['rating__sum'] is None):
                score = 0
            else:
                score = round(100 * total_score_self_rated['rating__sum'] / (total_stages * 5))
            fullStageData = fullStageData + [(stage, score)]

        fullPathwayPointData = []
        for point in pathwayPoints:
            if UserPathwayPoint.objects.filter(user=self.request.user, pathwayPoint=point).exists():
                rating = UserPathwayPoint.objects.get(user=self.request.user, pathwayPoint=point)
            else:
                rating = 0
            fullPathwayPointData = fullPathwayPointData + [(point, rating)]

        context['firm'] = firm
        context['stages'] = fullStageData
        context['pathwayPoints'] = fullPathwayPointData

        return context

    def save_ratings(request):
        form = RatingsForm(request.POST)
        print(form.data)
        if form.is_valid():
            pk = form.cleaned_data["firm_id"]
            new_scores = form.cleaned_data['ratings'].split(",")
            for score in new_scores:
                try:
                    point = score.split(".")[0]
                    this_score = score.split(".")[1]
                    new_data = UserPathwayPoint.objects.get_or_create(
                       pathwayPoint=PathwayPoint.objects.get(id=point),
                       user=request.user,
                    )

                    new_data[0].rating = int(this_score)
                    new_data[0].save()
                except Exception as e:
                    print(e)
            return redirect('pathway_detail', pk=pk)