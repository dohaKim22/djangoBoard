from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import BoardForm
from .models import Board

# Create your views here.
def index(request):
    boards = {'boards': Board.objects.all()}
    return render(request, 'list.html', boards)


def post(request):
    if request.method == "POST":
        form = BoardForm(request.POST, request.FILES)
        if form.is_valid():
            board = form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = BoardForm()

    return render(request, 'post.html', {'form': form})


def detail(request, id):
    try:
        board = Board.objects.get(pk=id)
    except Board.DoesNotExist:
        raise Http404("Does not exist!")
    return render(request, 'detail.html', {'board': board})

def edit(request, id):
    try:
        board = Board.objects.get(pk=id)
    except Board.DoesNotExist:
        raise Http404("게시글이 존재하지 않습니다!")

    if request.method == "POST":
        board.author = request.POST['author']
        board.title = request.POST['title']
        board.content = request.POST['content']
        board.save()
        return redirect('detail', id=board.id)
    else:
        return render(request, 'edit.html', {'board': board})

def delete(request, id):
    try:
        board = Board.objects.get(pk=id)
        board.delete()
    except Board.DoesNotExist:
        raise Http404("Does not exist!")
    return redirect('index')