from django.shortcuts import render,redirect
from . import models
from django.contrib.admin.forms import AuthenticationForm

def vote(request):
    candidates = models.Candidate.objects.all()
    context = {'candidates': candidates }
    return render(request, 'poll/vote.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            return redirect('vote')
    else:  
        form = AuthenticationForm()
    return render(request, 'poll/login.html/', {'form':form})

def addVote(request, pk):
    if request.method == 'POST':
        candidate = models.Candidate.objects.get(pk=pk)
        candidate.count += 1
        candidate.save()
    else:
        pass
    return render(request, 'poll/login.html')

    