from django.contrib import messages
from django.shortcuts import render


def index(request):
    return render(request, 'docs/index.html')


def dev_tools(request):
    """
    Public overview of the site components.
    """
    return render(request, 'docs/dev_tools.html')


def terms_of_use(request):
    return render(request, 'docs/terms_of_use.html')
