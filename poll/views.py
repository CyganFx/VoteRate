from django.shortcuts import render, get_object_or_404, redirect

from .forms import *
from .models import *


def getAll(request, template='poll/home.page.html'):
    dataset = Poll.objects.order_by('-createdAt')
    return render(request, template, {'dataset': dataset})


def getByID(request, id, template='poll/poll.page.html'):
    poll = get_object_or_404(Poll, pk=id)
    pollQuestions = PollQuestion.objects.filter(poll_id=id).order_by('id')
    tempPollAnswers = []
    for pollQuestion in pollQuestions:
        tempPollAnswers.append(list(PollAnswer.objects.filter(poll_id=id, question_id=pollQuestion.id).order_by('id')))

    pollAnswers = []

    for answer in tempPollAnswers:
        pollAnswers.append(answer)

    res = []

    for answer in pollAnswers:
        for val in answer:
            res.append(val)

    context = {
        'poll': poll,
        'pollQuestions': pollQuestions,
        'pollAnswers': res,
    }

    return render(request, template, context)


def createPoll(request, template='poll/create.page.html'):
    """Using js we need to insert additional hidden input field numOfQuestions in the form"""
    context = {
        'form': '',
        'error': ''
    }
    if request.method != 'POST':
        context['form'] = PollForm()
        return render(request, template, context)

    pollForm = PollForm(request.POST)
    numOfQuestions = request.POST.get('numOfQuestions')

    if not pollForm.is_valid():
        context['error'] = "form is not valid"
        return render(request, template, context)
    if not numOfQuestions > 0:
        context['error'] = "problems with js or you didn't create any question"
        return render(request, template, context)

    pollForm.host_id = request.user.id
    pollForm.createdAt = timezone.now()
    poll = pollForm.save()

    for i in range(numOfQuestions):
        question = request.POST.get(f'question{i}')
        q = PollQuestion(poll_id=poll.id, content=question)
        pollQuestion = q.save()

        answer_option = request.POST.get(f'answer{i}')
        a = PollAnswer(poll_id=poll.id, question_id=pollQuestion.id, content=answer_option)
        a.save()

    return redirect('poll-home')
