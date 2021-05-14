from django.shortcuts import render, get_object_or_404, redirect

from .models import *


def getAll(request, template='poll/home.page.html'):
    dataset = Poll.objects.order_by('-createdAt')
    votedPolls = PollVote.objects.all()
    userID = int(request.user.id)

    passedPolls = set()

    for vote in votedPolls:
        if vote.user_id.id == userID:
            passedPolls.add(vote.poll_id.id)

    numOfPollsPassed = len(passedPolls)

    return render(request, template, {
        'dataset': dataset,
        'userID': userID,
        'passedPolls': passedPolls,
        'numOfPollsPassed': numOfPollsPassed
    })


def getByID(request, id, template='poll/poll.page.html'):
    poll = get_object_or_404(Poll, pk=id)
    pollQuestions = PollQuestion.objects.filter(poll_id=id).order_by('id')
    PollAnswers = []
    numOfQuestions = 0
    for pollQuestion in pollQuestions:
        numOfQuestions += 1
        PollAnswers.append(list(PollAnswer.objects.filter(poll_id=id, question_id=pollQuestion.id).order_by('id')))

    res = []

    for answer in PollAnswers:
        for val in answer:
            res.append(val)

    context = {
        'poll': poll,
        'pollQuestions': pollQuestions,
        'pollAnswers': res,
        'numOfQuestions': numOfQuestions
    }

    return render(request, template, context)


def createPoll(request, template='poll/create.page.html'):
    """Using js we need to insert additional hidden input field numOfQuestions in the form"""
    context = {
        'error': '',
        'categories': ''
    }

    if request.method != 'POST':
        categorySet = Category.objects.all()
        context['categories'] = categorySet
        return render(request, template, context)

    poll = Poll(host_id_id=int(request.user.id), category_id_id=int(request.POST.get('category_id')))

    poll.title = request.POST.get('title')
    poll.imageURL = request.POST.get('imageURL')
    poll.description = request.POST.get('description')
    poll.createdAt = timezone.now()
    poll.save()

    tempPoll = get_object_or_404(Poll, title=poll.title,
                                 description=poll.description,
                                 host_id_id=poll.host_id_id, category_id_id=poll.category_id_id)

    numOfQuestions = int(request.POST.get('total_questions_counter'))
    numOfAnswers = int(request.POST.get('total_answers_counter'))

    if not numOfQuestions > 0:
        context['error'] = "you didn't create any question"
        return render(request, template, context)

    for i in range(numOfQuestions):
        question = request.POST.get(f'question{i + 1}')
        q = PollQuestion(poll_id_id=tempPoll.id, content=question)
        q.save()
        tempPollQuestion = get_object_or_404(PollQuestion, poll_id_id=tempPoll.id, content=question)

        for j in range(numOfAnswers):
            if request.POST.get(f'answer{j + 1}_question{i + 1}') is not None:
                answer_option = request.POST.get(f'answer{j + 1}_question{i + 1}')
                a = PollAnswer(poll_id_id=tempPoll.id, question_id_id=tempPollQuestion.id, content=answer_option)
                a.save()

    return redirect('poll-home')


def votePoll(request, template='poll/poll.page.html'):
    # if request.method != 'POST':
    #     getByID(request, id, template)
    numOfQuestions = int(request.POST.get('numOfQuestions'))
    passedAt = timezone.now()

    poll_id = int(request.POST.get('poll_id'))
    questionStartingID = int(request.POST.get('questionStartingID1'))
    for i in range(numOfQuestions):
        print(request.POST.get(f'answer_for_question{questionStartingID}'))
        pollVote = PollVote()
        pollVote.poll_id_id = poll_id
        pollVote.user_id_id = int(request.user.id)
        pollVote.answer_id_id = int(request.POST.get(f'answer_for_question{questionStartingID}'))
        pollVote.passedAt = passedAt
        pollVote.save()
        questionStartingID += 1

    return redirect('poll-home')


def ratePoll(request):
    print("I am here!")
    print("I am here!")
    print("I am here!")
    print("I am here!")
    print("I am here!")
    poll_id = int(request.POST.get('poll_id'))
    rate = int(request.POST.get('rate'))
    poll = get_object_or_404(Poll, pk=poll_id)
    poll.rating = float(rate)
    print(poll.rating)
    poll.save()

    return redirect('poll-home')
