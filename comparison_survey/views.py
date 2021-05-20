from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .forms import ComparisonSurveyForm, RateObjectForm
from .models import ComparisonSurvey, RateObject


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
        return context


# FOR AUTHORIZED USERS ONLY

def RetrieveCreatorComparisonSurveys(request, template='comparison_survey/dashboard.page.html'):
    """Returns all surveys created by exact user (user id retrieved from request.user) - dashboard.page.html"""
    try:
        creatorSurveys = ComparisonSurvey.objects.filter(author=request.user.id)
        context = {
            'mySurveys': creatorSurveys,
            'total': creatorSurveys.count()
        }
    except ComparisonSurvey.DoesNotExist:
        raise Http404('No surveys found for this creator')
    return render(request, template, context=context)


def RetrieveComparisonSurveyOfCreatorById(request, pk, template='comparison_survey/csurvey.creator.single.html'):
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
        return HttpResponseRedirect(self.get_success_url())


class EditCSurvey(UpdateView):
    model = ComparisonSurvey
    form_class = ComparisonSurveyForm
    pk_url_kwarg = 'cs_pk'
    template_name = 'comparison_survey/csurvey.edit.page.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect(f'my-survey', self.object.id)


def DeleteCSurvey(request, id, template='comparison_survey/survey.edit.page.html'):
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

def CreateRateObject(request, survey_id, template='comparison_survey/csurvey.creator.single.html'):
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
        return redirect('my-survey', survey.pk)
    return render(request, template, {'create_ro_form': form})


def DeleteRateObject(request, ro_pk, template='comparison_survey/csurvey.creator.single.html'):
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
        return redirect('my-survey', survey.pk)
    return render(request, template, context={'create_ro_form': form})


def RateCSurvey(request, cs_pk):
    if request.method == 'POST':
        if request.POST.get("mark"):
            print(type(request.POST.get("mark")))

            csurvey = ComparisonSurvey.objects.get(pk=cs_pk)

            if csurvey.rating == 0.0:
                csurvey.rating = float(request.POST.get("mark"))
                csurvey.save()
            else:
                csurvey.rating = (csurvey.rating + float(request.POST.get("mark"))) / 2
                csurvey.save()
            return redirect('comparison-survey-by-id', pk=cs_pk)
        else:
            return redirect('comparison-survey-home')

# passSurvey

# retrieve statistics for comparison survey

# retrieve rateObjects rating
