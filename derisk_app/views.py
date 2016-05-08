from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required()
def overview(request):
    params = {}
    params['username'] = request.user.username
    return render(request, 'overview.html',params)