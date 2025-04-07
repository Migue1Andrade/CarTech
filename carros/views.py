from django.shortcuts import render, redirect, get_object_or_404
from carros.models import Car
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def new(request):
    if request.method == 'POST':
        car_model = request.POST.get('car_model')
        brand = request.POST.get('brand')
        year = request.POST.get('year')
        color = request.POST.get('color')
        mileage = request.POST.get('mileage')
        fuel_type = request.POST.get('fuel_type')
        type = request.POST.get('type')
        price_str = request.POST.get('price')
        price = float(price_str.replace('.', '').replace(',', '.'))
        description = request.POST.get('description')
        image = request.FILES.get('image')

        car = Car.objects.create(
            car_model=car_model,
            brand=brand,
            year=year,
            color=color,
            mileage=mileage,
            fuel_type=fuel_type,
            type=type,
            price=price,
            description=description,
            image=image,
            created_by=request.user
        )
        return redirect('home')
    
    return render(request, 'carros/form.html', {
        'title': 'Novo Anúncio'
    })

@login_required
def edit(request, pk):
    car = get_object_or_404(Car, pk=pk, created_by=request.user)

    if request.method == 'POST':
        car.car_model = request.POST.get('car_model')
        car.brand = request.POST.get('brand')
        car.year = request.POST.get('year')
        car.color = request.POST.get('color')
        car.mileage = request.POST.get('mileage')
        car.fuel_type = request.POST.get('fuel_type')
        car.type = request.POST.get('type')
        price_str = request.POST.get('price')
        car.price = float(price_str.replace('.', '').replace(',', '.'))
        car.description = request.POST.get('description')

        if 'image' in request.FILES:
            car.image = request.FILES['image']

        car.save()
        return redirect('carros:pdp', pk=car.id)

    return render(request, 'carros/edit-form.html', {
        'car': car
    })

@login_required
def car_list(request):
    objects = Car.objects.filter(created_by=request.user, is_sold=False)
    return render(request, 'carros/description.html', {'carros': objects})

def plp(request):
    search = request.GET.get('search')
    brand = request.GET.get('brand')
    marca = request.GET.get('marca')
    modelo = request.GET.get('modelo')
    ano = request.GET.get('ano')
    cor = request.GET.get('cor')
    quilometragem = request.GET.get('quilometragem')
    combustivel = request.GET.get('combustivel')
    carroceria = request.GET.get('carroceria')
    preco = request.GET.get('preco')

    cars = Car.objects.filter(is_sold=False)

    if search:
        cars = cars.filter(car_model__icontains=search)
    if brand:
        cars = cars.filter(brand=brand)
    if marca:
        cars = cars.filter(brand__icontains=marca)
    if modelo:
        cars = cars.filter(car_model__icontains=modelo)
    if ano:
        cars = cars.filter(year=ano)
    if cor:
        cars = cars.filter(color__icontains=cor)
    if quilometragem:
        cars = cars.filter(mileage=quilometragem)
    if combustivel:
        cars = cars.filter(fuel_type__icontains=combustivel)
    if carroceria:
        cars = cars.filter(type__icontains=carroceria)
    if preco:
        cars = cars.filter(price=preco)

    context = {
        'cars': cars,
        'Marca': Car.objects.values_list('brand', flat=True).distinct(),
        'Modelo': Car.objects.values_list('car_model', flat=True).distinct(),
        'Ano': Car.objects.values_list('year', flat=True).distinct(),
        'Cor': Car.objects.values_list('color', flat=True).distinct(),
        'Quilometragem': Car.objects.values_list('mileage', flat=True).distinct(),
        'Combustível': Car.objects.values_list('fuel_type', flat=True).distinct(),
        'Tipo de Carroceria': Car.objects.values_list('type', flat=True).distinct(),
        'Preço': Car.objects.values_list('price', flat=True).distinct()
    }

    return render(request, 'carros/paginadelistagem.html', context)

def pdp(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'carros/paginadedescricao.html', {'car': car})

@login_required
def finalize(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if car.created_by == request.user:
        car.is_sold = True
        car.save()
        return HttpResponseRedirect(reverse('carros:pdp', args=[car_id]))
    else:
        return redirect('home')
