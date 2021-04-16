from django.shortcuts import render

posts = [
    {
        'author': 'CoreyMS',
        'title': 'Blog Post 1',
        'date_posted': 'August 27'
    },
    {
        'author': 'asd2',
        'title': 'Blog Post 2',
        'date_posted': 'August 28'
    }
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'comparison_survey/home.page.html')
