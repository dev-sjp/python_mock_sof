from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404
from pybo.models import Question


def index(request):

    3 / 0
    # question_list = Question.objects.order_by('-create_date') # - means Descending
    # context = { 'question_list': question_list }

    # page = request.GET.get('page', '1')  # Page  (set default), http://localhost:8000/pybo/?page=1
    # input parameter
    page = request.GET.get('page', '1')  # page
    kw = request.GET.get('kw', '')  # searching word
    so = request.GET.get('so', 'recent')  # order by ...

    # ordering
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')




    # list order by descending
    # question_list = Question.objects.order_by('-create_date')

    # search
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # title search
            Q(content__icontains=kw) |  # content search
            Q(author__username__icontains=kw) |  # question author search
            Q(answer__author__username__icontains=kw)  # answer author search
        ).distinct()


    # paging
    paginator = Paginator(question_list, 10)  # 10 item per 1 list
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so, }  # add page and kw

    return render (request, 'pybo/question_list.html', context)


def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk = question_id)
    context = {'question': question}
    return render (request,'pybo/question_detail.html', context)

