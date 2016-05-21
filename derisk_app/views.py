from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from derisk_app.models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required()
def overview(request):
    params = {}
    params['username'] = request.user.username
    return render(request, 'overview.html',params)

class ProjectListView(LoginRequiredMixin,ListView):
    model = Project
    template_name = 'project-list.html'
    context_object_name = 'projects'