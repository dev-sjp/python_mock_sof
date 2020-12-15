from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from pybo.forms import QuestionForm
from pybo.models import Question


@login_required(login_url='common:login')
def question_create(request):
   # form = QuestionForm()
   if request.method == 'POST':
       form = QuestionForm(request.POST)
       if form.is_valid():
           question = form.save(commit=False)
           question.author = request.user
           question.create_date = timezone.now()
           question.save()
           return redirect('pybo:index')
   else:
       form = QuestionForm()
   context = {'form': form}

   return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    pybo Question Update
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, 'No Permission')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()  # Update Modify Date
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo question delete
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, 'No permission')
        return redirect('pybo:detail', question_id=question.id)

    question.delete()
    return redirect('pybo:index')

