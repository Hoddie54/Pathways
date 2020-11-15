from django.shortcuts import render
from .models import QuestionPack, Stage, FirmQuestionPackConnector
from pathway.models import Firm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def questions_page(request):

    #Handle the search
    query = request.GET.get('search')
    firm = request.GET.get('firm')
    stage = request.GET.get('stage')

    if(firm is None and stage is None):
        if query is None:
            query = ''
        question_packs = QuestionPack.objects.filter(name__contains=query)
    else:
        if firm is None:
            firms = QuestionPack.objects.all()
        else:
            firms = QuestionPack.objects.filter(firmquestions__firm_id__in=firm)
        if stage is None:
            stages = QuestionPack.objects.all()
        else:
            stages = QuestionPack.objects.filter(stage_id=stage)

        question_packs = (firms & stages).distinct()
        print(question_packs)

    paginator = Paginator(question_packs, 6)
    page = request.GET.get('page')

    try:
        question_packs_displayed = paginator.page(page)
    except PageNotAnInteger:
        question_packs_displayed = paginator.page(1)
    except EmptyPage:
        question_packs_displayed = paginator.page(paginator.num_pages)

    context = {
        'question_packs': question_packs_displayed,
        'firm_list': Firm.objects.all(),
        'stage_list': Stage.objects.all(),
    }
    return render(request, 'questions.html', context)


def questions_pack_detail_view(request, pk):

    question_pack = QuestionPack.objects.get(pk=pk)

    context = {
        'question_pack': question_pack
    }
    return render(request, 'questions_pack_detail_view.html', context)