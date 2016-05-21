from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from derisk_app.models import *
from derisk_app.forms import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required()
def overview(request):
    params = {}
    params['test'] = request.user
    return render(request, 'overview.html',params)

class ProjectListView(LoginRequiredMixin,ListView):
    model = Project
    template_name = 'project-list.html'
    context_object_name = 'projects'

class ProjectUpdate(LoginRequiredMixin,UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project-edit.html'
    success_url = '/projects/'