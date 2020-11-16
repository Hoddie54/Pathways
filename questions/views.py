from django.shortcuts import render, redirect
from .models import QuestionPack, Stage, FirmQuestionPackConnector, Question, UserAnswer
from pathway.models import Firm
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime#
from math import floor

@login_required
def questions_page(request):

    #Handle the search
    query = request.GET.get('search')
    firm = request.GET.get('firm')
    stage = request.GET.get('stage')

    question_packs = get_question_pack_list(query, firm, stage)

    paginator = Paginator(question_packs, 6)
    page = request.GET.get('page')

    try:
        question_packs_displayed = paginator.page(page)
    except PageNotAnInteger:
        question_packs_displayed = paginator.page(1)
    except EmptyPage:
        question_packs_displayed = paginator.page(paginator.num_pages)

    questions_completed = UserAnswer.objects.filter(
        user=request.user,
        time_finished__isnull=False,
    )

    context = {
        'question_packs': question_packs_displayed,
        'firm_list': Firm.objects.all(),
        'stage_list': Stage.objects.all(),
        'questions_completed': questions_completed.count()
    }
    return render(request, 'questions.html', context)

@login_required
def questions_pack_detail_view(request, pk):

    question_pack = QuestionPack.objects.get(pk=pk)
    my_answers = UserAnswer.objects.filter(
        user=request.user,
        time_finished__isnull=False
                                           )

    context = {
        'question_pack': question_pack,
        'my_answers': my_answers
    }
    return render(request, 'questions_pack_detail_view.html', context)

###TODO - Add user passes test
@login_required
def question_answer_view(request, pk):
    question = Question.objects.get(pk=pk)
    context = {
        'question': question
    }

    print(request.POST)

    if UserAnswer.objects.filter(question=question, user=request.user).count() == 0:
        new_answer = UserAnswer.objects.create(
            question=question,
            user=request.user,
            time_started=datetime.now(),
            my_answer=None,
        )
        new_answer.save()
    else:
        old_answer = UserAnswer.objects.get(question=question, user=request.user)
        answer_from_form = request.POST.get('answer')
        if answer_from_form is not None:
            old_answer.time_finished = datetime.now()
            old_answer.my_answer = answer_from_form
            old_answer.attempt = old_answer.attempt + 1
            old_answer.save()
            return redirect('questions_pack_detail_view', question.question_pack_id)
        elif old_answer.time_finished is not None:
            pass
        else:
            old_answer.time_started = datetime.now()
        old_answer.save()

    return render(request, 'question_answer_view.html', context)

@login_required
def my_answers_search_view(request):
    query = request.GET.get('search')
    firm = request.GET.get('firm')
    stage = request.GET.get('stage')

    question_packs = get_question_pack_list(query, firm, stage)
    question_packs.order_by('questionpack__useranswer__time_finished')

    questions_answered = []


    paginator = Paginator(question_packs, 4)
    page = request.GET.get('page')

    try:
        question_packs_displayed = paginator.page(page)
    except PageNotAnInteger:
        question_packs_displayed = paginator.page(1)
    except EmptyPage:
        question_packs_displayed = paginator.page(paginator.num_pages)

    for thispack in question_packs_displayed:
        completed_questions = UserAnswer.objects.filter(
            user=request.user,
            question__question_pack=thispack,
            time_finished__isnull=False, )
        questions_answered = questions_answered + [completed_questions.count(), ]

    context = {
        'question_packs': question_packs_displayed,
        'firm_list': Firm.objects.all(),
        'stage_list': Stage.objects.all(),
        'questions_answered': questions_answered,
    }
    return render(request, 'my_answers_search_view.html', context)


@login_required
def my_answers_question_pack_detail(request, pk):
    question_pack = QuestionPack.objects.get(pk=pk)
    my_answers = UserAnswer.objects.filter(
        user=request.user,
        time_finished__isnull=False
                                           )

    context = {
        'question_pack': question_pack,
        'my_answers': my_answers
    }
    return render(request, 'my_answers_question_pack_detail.html', context)

def my_answer_review_test(request, pk):
    print(request.user)
    print(UserAnswer.objects.get(pk=pk).time_finished)

    if request.user.id != UserAnswer.objects.get(pk=pk).user.id:

        return False
    if UserAnswer.objects.get(pk=pk).time_finished is None:

        return False
    return True

##TODO-Add permission
@login_required
def my_answer_review(request, pk):

    print(my_answer_review_test(request, pk))
    if(not my_answer_review_test(request, pk)):
        return redirect('error')

    my_answer = UserAnswer.objects.get(pk=pk)
    time_taken = (my_answer.time_finished - my_answer.time_started).total_seconds()
    question = my_answer.question

    context = {
        'my_answer': my_answer,
        'time_taken': str(floor(time_taken/60)) + " minutes " + str(round((time_taken/60 - floor(time_taken/60))*60)) + " seconds",
        'question' : question,
    }

    return render(request, 'my_answer_review.html', context)





def is_this_null_or_zero(value):
    if value is None:
        return True
    elif value == '0':
        return True
    else:
        return False

def get_question_pack_list(query, firm, stage):

    if (is_this_null_or_zero(firm) and is_this_null_or_zero(stage)):
        if query is None:
            query = ''
        question_packs = QuestionPack.objects.filter(name__contains=query)
    else:
        if is_this_null_or_zero(firm):
            firms = QuestionPack.objects.all()
        else:
            firms = QuestionPack.objects.filter(firmquestions__firm_id__in=firm)
        if is_this_null_or_zero(stage):
            stages = QuestionPack.objects.all()
        else:
            stages = QuestionPack.objects.filter(stage_id=stage)

        question_packs = (firms & stages).distinct()

    return question_packs