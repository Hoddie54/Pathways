from django.urls import path
from .views import questions_page, questions_pack_detail_view, \
    question_answer_view, my_answers_search_view, my_answers_question_pack_detail, my_answer_review

urlpatterns = [
    path('', questions_page, name='questions'),
    path('pack/<int:pk>', questions_pack_detail_view, name='questions_pack_detail_view'),
    path('question/<int:pk>', question_answer_view, name='question_answer_view'),
    path('answers/', my_answers_search_view, name='my_answers_search_view'),
    path('answers/pack/<int:pk>', my_answers_question_pack_detail, name='my_answers_question_pack_detail'),
    path('answers/question/<int:pk>', my_answer_review, name='my_answer_review'),
]