from django.contrib import messages
from django.shortcuts import render


def index(request):
    return render(request, 'docs/index.html')


def dev_tools(request):
    """
    Public overview of site components.
    """
    return render(request, 'docs/dev_tools.html')
