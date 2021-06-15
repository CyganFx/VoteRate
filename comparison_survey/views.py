import random

from django.db.models import Count
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from voterate_django.utils import render_to_pdf
from .forms import ComparisonSurveyForm, RateObjectForm, ComplaintForm
from .models import ComparisonSurvey, RateObject, ComparisonSurveyResult, Complaint, Category, PassedSurvey


# #### Comparison Survey views (CRUD) ####

# FOR ANY USER

class ComparisonSurveyAll(ListView):
    """Returns all comparison surveys - csurvey.index.page.html"""
    model = ComparisonSurvey
    template_name = 'comparison_survey/csurvey.index.page.html'
    paginate_by = 12
    queryset = ComparisonSurvey.objects.all().order_by('-views')
    context_object_name = 'cSurveys'

    def get_context_data(self, *args, **kwargs):
        context = super(ComparisonSurveyAll, self).get_context_data(*args, **kwargs)
        context['total'] = ComparisonSurvey.objects.all().count()
        context['category_list'] = Category.objects.all()
        return context


class CSurveysByCategory(ListView):
    """Returns list of comparison surveys filtered by exact category"""
    template_name = 'comparison_survey/csurvey.index.page.html'
    context_object_name = 'cSurveys'

    def get_queryset(self):
        return ComparisonSurvey.objects.filter(category=self.kwargs['category_id'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['total'] = self.get_queryset().count()
        context['category_item'] = Category.objects.get(pk=self.kwargs['category_id'])
        context['category_list'] = Category.objects.all()
        return context


class ComparisonSurveyDetail(DetailView):
    """Returns exact comparison survey by id - csurvey.single.page.html"""
    model = ComparisonSurvey
    template_name = 'comparison_survey/csurvey.single.page.html'
    context_object_name = 'survey'

    def get_context_data(self, *args, **kwargs):
        context = super(ComparisonSurveyDetail, self).get_context_data(*args, **kwargs)
        context['rateObjects'] = RateObject.objects.all().filter(survey_id=self.object.id)
        cs_object = self.get_object()
        cs_object.views += 1
        cs_object.save()

        if PassedSurvey.objects.filter(user=self.request.user, survey=self.get_object()).count() > 0:
            context['passedSurvey'] = PassedSurvey.objects.get(user=self.request.user, survey=self.get_object())
        return context


# FOR AUTHORIZED USERS ONLY

def retrieve_creator_comparison_surveys(request, template='comparison_survey/dashboard.page.html'):
    """Returns all surveys created by exact user (user id retrieved from request.user) - dashboard.page.html"""
    try:
        creatorSurveys = ComparisonSurvey.objects.filter(author=request.user.id).order_by('category__title')
        viewsAll = ComparisonSurvey.objects.values('views')
        totalViews = 0
        for v in viewsAll:
            totalViews = totalViews + v['views']
        context = {
            'mySurveys': creatorSurveys,
            'total': creatorSurveys.count(),
            'totalViews': totalViews,
        }
    except ComparisonSurvey.DoesNotExist:
        raise Http404('No surveys found for this creator')
    return render(request, template, context=context)


def retrieve_comparison_survey_of_creator_by_id(request, pk, template='comparison_survey/csurvey.creator.single.html'):
    """Returns exact comparison survey by id - csurvey.creator.single.html"""
    try:
        survey = ComparisonSurvey.objects.get(id=pk, author=request.user)
        rateObjects = RateObject.objects.filter(survey_id=pk)
        context = {
            'survey': survey,
            'rateObjects': rateObjects,
            'total_ro': rateObjects.count(),
            'create_ro_form': RateObjectForm
        }
    except ComparisonSurvey.DoesNotExist:
        raise Http404('No comparison survey found made by you')

    return render(request, template, context=context)


class CreateCSurvey(CreateView):
    """Used to create comparison survey and redirect user after creation to the user's surveys dashboard - survey.edit.page.html"""
    model = ComparisonSurvey
    form_class = ComparisonSurveyForm
    template_name = 'comparison_survey/csurvey.new.page.html'
    success_url = '../my_surveys/all'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        messages.success(self.request, "New Comparison survey created")  # this would be displayed on dashboard
        return HttpResponseRedirect(self.get_success_url())


class EditCSurvey(UpdateView):
    model = ComparisonSurvey
    form_class = ComparisonSurveyForm
    pk_url_kwarg = 'cs_pk'
    template_name = 'comparison_survey/csurvey.edit.page.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        messages.success(self.request,
                         f"Comparison survey - {self.object.topic} successfully updated")  # this would be displayed on creator.single cs page
        return redirect(f'my-survey', self.object.id)


def delete_csurvey(request, id, template='comparison_survey/survey.edit.page.html'):
    """Used to delete comparison survey record - survey.edit.page.html, csurvey.single.page.html"""
    try:
        data = get_object_or_404(ComparisonSurvey, id=id)
    except Exception:
        raise Http404('Does Not Exist')

    if request.method == 'POST':
        data.delete()

        return redirect('my-surveys-all')
    return render(request, template)

# #### Rate Objects' views (CRUD) ####

def create_rate_object(request, survey_id, template='comparison_survey/csurvey.creator.single.html'):
    """Used to create Rate Object and redirect user after creation to the comparison survey page that it belongs"""
    # provide data consistency
    survey = get_object_or_404(ComparisonSurvey, pk=survey_id)
    # save the number of top elements
    survey.top_number += 1
    survey.save()

    form = RateObjectForm(request.POST or None)
    if form.is_valid():
        form.instance.survey = survey
        form.save()

        if survey.top_number % 2 != 0:
            messages.warning(request, "Rate objects quantity must be even!")

        return redirect('my-survey', survey.pk)
    return render(request, template, {'create_ro_form': form})


def delete_rate_object(request, ro_pk, template='comparison_survey/csurvey.creator.single.html'):
    """Used to delete rate object record - survey.edit.page.html, csurvey.single.page.html"""
    try:
        rate_obj = get_object_or_404(RateObject, pk=ro_pk)
    except Exception:
        raise Http404('Does Not Exist')

    form = RateObjectForm(request.POST or None)
    if request.method == 'POST':
        survey = get_object_or_404(ComparisonSurvey, pk=rate_obj.survey.pk)
        # reduce the number of top elements
        survey.top_number -= 1
        survey.save()
        rate_obj.delete()
        messages.success(request,
                         f"Rate object - {rate_obj.description} successfully deleted")  # this would be displayed on dashboard
        return redirect('my-survey', survey.pk)
    return render(request, template, context={'create_ro_form': form})


def rate_csurvey(request, survey_id):
    """view used for making rate operation"""
    if request.method == 'POST':
        if request.POST.get("mark"):
            print(type(request.POST.get("mark")))

            csurvey = ComparisonSurvey.objects.get(pk=survey_id)

            if csurvey.rating == 0.0:
                csurvey.rating = float(request.POST.get("mark"))
                csurvey.save()
            else:
                csurvey.rating = (csurvey.rating + float(request.POST.get("mark"))) / 2
                csurvey.save()
            messages.success(request,
                             f"{csurvey.topic}: Thank you for your response")  # this message will be displayed on cs single page
            return redirect('comparison-survey-by-id', pk=survey_id)
        else:
            messages.error(request,
                           "Oops. Some errors were occured during rating")  # this message will be displayed on index page
            return redirect('comparison-survey-home')


def leave_complaint(request, survey_id, template='comparison_survey/csurvey.feedback.page.html'):
    """view used for creating complaint to specific comparison survey"""
    # provide data consistency
    survey = get_object_or_404(ComparisonSurvey, pk=survey_id)
    # save the number of top elements

    form = ComplaintForm(request.POST or None)
    if form.is_valid():
        form.instance.survey = survey
        form.instance.user = request.user
        form.save()
        messages.success(request,
                         f"{survey.topic}: We will definitely consider your complaint")  # this message will be displayed on cs single page
        return redirect('comparison-survey-by-id', survey.pk)
    return render(request, template, {'create_ro_form': form})


def statistics(request, survey_id, template='comparison_survey/csurvey.statistics.page.html'):
    """view for statistics render of comparison survey"""
    try:
        survey = get_object_or_404(ComparisonSurvey, id=survey_id)

        labels = []
        data = []

        results_raw = ComparisonSurveyResult.objects.filter(survey__pk=survey_id) \
            .values('rate_object__description', 'rate_object__media') \
            .annotate(total=Count('respondent')).order_by('-total')
        peoplePassed = PassedSurvey.objects.values('user').filter(survey=survey).count()
        totalChoices = 0
        for cs in results_raw:
            totalChoices = totalChoices + cs['total']
        for cs in results_raw:
            labels.append(f'{cs["rate_object__description"]} - {round(cs["total"] / totalChoices * 100, 1)} %')
            data.append(round(cs['total'] / totalChoices * 100, 1))
        context = {
            'survey': survey,
            'results': results_raw,
            'peoplePassed': peoplePassed,
            'totalChoices': totalChoices,
            'labels': labels,
            'data': data,
        }
    except ComparisonSurveyResult.DoesNotExist:
        raise Http404('No comparison survey results found')
    return render(request, template, context=context)


def feedback_actions(request, survey_id, template='comparison_survey/csurvey.feedback.page.html'):
    try:
        survey = get_object_or_404(ComparisonSurvey, id=survey_id)
        context = {
            'survey': survey,
            'complaint_form': ComplaintForm,
        }
    except ComparisonSurveyResult.DoesNotExist:
        raise Http404('No comparison survey found')
    return render(request, template, context=context)


class ComplaintAll(ListView):
    """Returns all complaints list - csurvey.moderator.page.html"""
    model = Complaint
    template_name = 'comparison_survey/csurvey.moderator.page.html'
    queryset = Complaint.objects \
        .values('survey_id', 'survey__topic') \
        .annotate(total=Count('reason')).order_by('total')
    context_object_name = 'complaints'


def complaints_for_csurvey(request, survey_id, template='comparison_survey/csurvey.complaint.page.html'):
    """Returns complaints for specific comparison survey"""
    try:
        survey = ComparisonSurvey.objects.get(id=survey_id)
        complaints = Complaint.objects.filter(survey=survey_id)
        context = {
            'survey': survey,
            'complaints': complaints,
        }
    except ComparisonSurvey.DoesNotExist:
        raise Http404('No comparison survey found')

    return render(request, template, context=context)


def csurvey_pass_view(request, pk, template='comparison_survey/csurvey.pass.page.html'):
    """View for passing survey where temporary data saved on session. View where tracked user's survey pass"""
    if request.method == 'POST':
        print(request.POST.get('choice'))
        if request.POST.get('choice'):
            ro = RateObject.objects.get(pk=request.POST.get('choice'))
            cs = ComparisonSurvey.objects.get(pk=pk)
            # recording user choice
            newRecord = ComparisonSurveyResult.objects.create(respondent=request.user, survey=cs,
                                                              rate_object=ro)
        return redirect('comparison-survey-pass', pk=pk)
    else:
        survey = ComparisonSurvey.objects.get(id=pk)
        context = {
            'survey': survey
        }

        # returns set of rate objects if they were stored in session or adds new set of ro
        rateObjectsIDsList = list(
            request.session.get('rateObjects', RateObject.objects.filter(survey_id=pk).values_list('pk', flat=True)))

        # check if user completed survey or not
        if len(rateObjectsIDsList) != survey.top_number and request.session.get('completed'):
            del request.session['rateObjects']
            del request.session['completed']

        print(f'rate object left = {rateObjectsIDsList}')

        # survey pass termination point
        if len(rateObjectsIDsList) - 1 <= 0:
            request.session['completed'] = True

            # record to user's completed surveys list
            if PassedSurvey.objects.filter(user=request.user, survey=survey).count() > 0:
                # update time of completion if user completed it before
                passedSurvey = PassedSurvey.objects.get(user=request.user, survey=survey.id)
                passedSurvey.last_passed_date = timezone.now()
                passedSurvey.save()
            else:
                # record it if user passes it first time
                _ = PassedSurvey.objects.create(user=request.user, survey=survey)
            return redirect('comparison-survey-statistics', survey.id)
        # taking couple of random ro from set of ro
        coupleIDs = random.sample(rateObjectsIDsList, k=2)
        couple = []
        # safe deletion of choice couples in order to keep track of survey pass AND getting objects of ro from db
        for choice in coupleIDs:
            rateObjectsIDsList.remove(choice)
            couple.append(RateObject.objects.get(pk=choice))
        # recording current user survey variants (ro) to session
        request.session['rateObjects'] = rateObjectsIDsList
        context['couple'] = couple
        return render(request, template, context=context)


def generate_pdf(request, survey_id, template='comparison_survey/csurvey.statistics.pdf.html'):
    """view for exporting statistics render as pdf file"""
    survey = get_object_or_404(ComparisonSurvey, id=survey_id)
    results_raw = ComparisonSurveyResult.objects.filter(survey__pk=survey_id) \
        .values('rate_object__description', 'rate_object__media') \
        .annotate(total=Count('respondent')).order_by('-total')
    peoplePassed = PassedSurvey.objects.values('user').filter(survey=survey).count()
    totalChoices = 0
    for cs in results_raw:
        totalChoices = totalChoices + cs['total']
    context = {
        'survey': survey,
        'results': results_raw,
        'peoplePassed': peoplePassed,
        'totalChoices': totalChoices,
    }
    pdf = render_to_pdf(template, context)
    return pdf
