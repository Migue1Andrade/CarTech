from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages

from carros.models import Car
from chat.models import Chat


def home(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        return redirect(reverse('carros:plp') + '?search=' + search)
    return render(request, 'core/home.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "As senhas não coincidem.")
            return render(request, 'core/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Este nome de usuário já está em uso.")
            return render(request, 'core/signup.html')

        user = User.objects.create_user(username=username, password=password1)
        login(request, user)
        return redirect('home')

    return render(request, 'core/signup.html')


@login_required
def my_ads(request):
    cars = Car.objects.filter(created_by=request.user)
    return render(request, 'core/my_ads.html', {'cars': cars})


@login_required
def delete_ad(request, pk):
    car = get_object_or_404(Car, pk=pk, created_by=request.user)
    try:
        car.delete()
        messages.success(request, 'Anúncio deletado com sucesso.')
    except Exception as e:
        messages.error(request, f'Ocorreu um erro ao deletar o anúncio: {str(e)}')
    return redirect('my_ads')


@login_required
def my_chats(request):
    chats = Chat.objects.filter(Q(buyer=request.user) | Q(seller=request.user))
    return render(request, 'core/chats.html', {'chats': chats})
