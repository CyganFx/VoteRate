from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect

from .models import *


def getAll(request, template='poll/home.page.html'):
    dataset = Poll.objects.order_by('-createdAt')
    votedPolls = PollVote.objects.all()
    ratedPolls = UserPollRatings.objects.filter(user_id=int(request.user.id))
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
        'ratedPolls': ratedPolls,
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


def votePoll(request):
    if request.method != 'POST':
        getAll(request)
    numOfQuestions = int(request.POST.get('numOfQuestions'))
    passedAt = timezone.now()

    poll_id = int(request.POST.get('poll_id'))
    questionStartingID = int(request.POST.get('questionStartingID1'))
    for i in range(numOfQuestions):
        pollVote = PollVote()
        pollVote.poll_id_id = poll_id
        pollVote.user_id_id = int(request.user.id)
        pollVote.answer_id_id = int(request.POST.get(f'answer_for_question{questionStartingID}'))
        pollVote.passedAt = passedAt
        pollVote.save()
        questionStartingID += 1

    poll = Poll.objects.get(pk=poll_id)
    poll.passedCounter += 1
    poll.save()

    # stats:
    user = User.objects.get(pk=int(request.user.id))

    try:
        pollStats = PollStats.objects.get(poll_id_id=poll_id)
    except PollStats.DoesNotExist:
        pollStats = PollStats(poll_id_id=poll_id)

    pollStats.passedCounter += 1
    pollStats.poll_id_id = poll_id
    if user.profile.gender == 'man':
        pollStats.manNum += 1
        pollStats.manPercentage = (pollStats.manNum * 100) / pollStats.passedCounter
        pollStats.womenPercentage = (pollStats.womenNum * 100) / pollStats.passedCounter
    else:
        pollStats.womenNum += 1
        pollStats.womenPercentage = (pollStats.womenNum * 100) / pollStats.passedCounter
        pollStats.manPercentage = (pollStats.manNum * 100) / pollStats.passedCounter

    if user.profile.country == 'kz':
        pollStats.countryNumKZ += 1
        pollStats.countryKZPercentage = (pollStats.countryNumKZ * 100) / pollStats.passedCounter
        pollStats.countryUSAPercentage = (pollStats.countryNumUSA * 100) / pollStats.passedCounter

    if user.profile.country == 'usa':
        pollStats.countryNumUSA += 1
        pollStats.countryUSAPercentage = (pollStats.countryNumUSA * 100) / pollStats.passedCounter
        pollStats.countryKZPercentage = (pollStats.countryNumKZ * 100) / pollStats.passedCounter

    if user.profile.higher_education == 'yes':
        pollStats.higher_education_num += 1
        pollStats.higher_education_percentage = (pollStats.higher_education_num * 100) / pollStats.passedCounter
    else:
        pollStats.higher_education_percentage = (pollStats.higher_education_num * 100) / pollStats.passedCounter

    current_date = datetime.now()
    current_year = current_date.year
    pollStats.averageAge = (pollStats.averageAge + (
            current_year - user.profile.birth_date.year)) / pollStats.passedCounter
    pollStats.save()
    return redirect('poll-home')


def ratePoll(request):
    poll_id = int(request.POST.get('poll_id'))
    rate = int(request.POST.get('rate'))
    poll = get_object_or_404(Poll, pk=poll_id)

    try:
        userRating = UserPollRatings.objects.get(user_id_id=int(request.user.id), poll_id_id=poll_id)
        userRating.rating = rate
    except UserPollRatings.DoesNotExist:
        userRating = UserPollRatings(user_id_id=int(request.user.id), poll_id_id=poll_id, rating=rate)
        userRating.save()
        poll.rateCounter += 1

    ratings = UserPollRatings.objects.filter(poll_id_id=poll_id).only('rating')
    ratingsSum = 0.0
    for r in ratings:
        ratingsSum += float(r.rating)

    poll.rating = float(ratingsSum / poll.rateCounter)
    poll.save()

    pollStats = PollStats.objects.get(poll_id_id=poll_id)
    pollStats.rateCounter += 1
    pollStats.save()

    return redirect('poll-home')


def pollStats(request, id, template='poll/statistics.page.html'):
    poll = get_object_or_404(Poll, pk=id)
    pollQuestions = PollQuestion.objects.filter(poll_id=id).order_by('id')
    PollAnswers = []
    numOfQuestions = 0
    for pollQuestion in pollQuestions:
        numOfQuestions += 1
        PollAnswers.append(list(PollAnswer.objects.filter(poll_id=id, question_id=pollQuestion.id).order_by('id')))

    res = []
    answersCounterforSpecificQuestion = 0
    for answer in PollAnswers:
        for val in answer:
            pollVotesTemp = PollVote.objects.filter(poll_id_id=id, answer_id_id=val.id)
            for vote in pollVotesTemp:
                answersCounterforSpecificQuestion += 1

            val.votedNum = answersCounterforSpecificQuestion

            res.append(val)
            answersCounterforSpecificQuestion = 0

    pollStats = PollStats.objects.get(poll_id_id=id)

    context = {
        'poll': poll,
        'pollQuestions': pollQuestions,
        'pollAnswers': res,
        'numOfQuestions': numOfQuestions,
        'pollStats': pollStats
    }

    return render(request, template, context)
