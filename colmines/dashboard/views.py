from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction, IntegrityError


def index(request):
    context = {
        
    }
    return render(request, 'dashboard/index.html', context)
