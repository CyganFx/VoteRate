from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView
from .forms import ComparisonSurveyForm, RateObjectForm
from .models import ComparisonSurvey, RateObject


# #### Comparison Survey views (CRUD) ####

# FOR ANY USER

class ComparisonSurveyAll(ListView):
    """Returns all comparison surveys - csurvey.index.page.html"""
    model = ComparisonSurvey
    template_name = 'comparison_survey/csurvey.index.page.html'
    paginate_by = 12
    queryset = ComparisonSurvey.objects.all().order_by('-rating')
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
        }
    except ComparisonSurvey.DoesNotExist:
        raise Http404('No surveys found for this creator')
    return render(request, template, context=context)


def RetrieveComparisonSurveyOfCreatorById(request, id, template='comparison_survey/survey.edit.page.html'):
    """Returns exact comparison survey by id - csurvey.single.page.html"""
    try:
        survey = ComparisonSurvey.objects.get(id=id)
        rateObjects = RateObject.objects.filter(survey_id=id)
        context = {
            'survey': survey,
            'rateObjects': rateObjects,
        }
    except ComparisonSurvey.DoesNotExist:
        raise Http404('Data does not exist')

    return render(request, template, context=context)


class CreateComparisonSurvey(CreateView):
    """Used to create comparison survey and redirect user after creation to the user's surveys dashboard - survey.edit.page.html"""
    model = ComparisonSurvey
    form_class = ComparisonSurveyForm
    template_name = 'comparison_survey/survey.new.page.html'
    success_url = '../my_surveys/all'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


def UpdateComparisonSurvey(request, id, template='comparison_survey/survey.edit.page.html'):
    """Used to update comparison survey details - survey.edit.page.html"""
    oldComparisonSurvey = get_object_or_404(ComparisonSurvey, pk=id)
    form = ComparisonSurveyForm(request.POST or None, instance=oldComparisonSurvey)
    if form.is_valid():
        form.save()
        return redirect(f'my-surveys/{id}')
    return render(request, template, {'form': form})


def DeleteComparisonSurvey(request, id, template='comparison_survey/survey.edit.page.html'):
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


def CreateRateObject(request, template='comparison_survey/rateobj.new.page.html'):
    """Used to create Rate Object and redirect user after creation to the comparison survey page that it belongs"""
    form = RateObjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('my-surveys-all')
    return render(request, template, {'form': form})


def DeleteRateObject(request, id, template='comparison_survey/survey.edit.page.html'):
    """Used to delete comparison survey record - survey.edit.page.html, csurvey.single.page.html"""
    try:
        data = get_object_or_404(RateObject, id=id)
    except Exception:
        raise Http404('Does Not Exist')

    if request.method == 'POST':
        data.delete()
        return redirect('my-surveys-all')
    return render(request, template)

# passSurvey

# retrieve statistics for comparison survey

# retrieve rateObjects rating
