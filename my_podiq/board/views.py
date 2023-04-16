from django.shortcuts import render, redirect
from .models import Articles
from .forms import ArticlesForm


def board_home(request):
    news = Articles.objects.all()
    return render(request, 'board/board_home.html', {'news': news})


def create(request):
    error=''
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error='Форма запонена неправильно'

    form = ArticlesForm()

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'board/create.html',data)
