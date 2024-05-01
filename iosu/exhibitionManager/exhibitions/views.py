from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db.models import Count, Max, Value, CharField, Sum, Case, When, IntegerField, F

from .forms import LoginForm, CompanyForm, ExhibitionForm
from .models import Products, Company, ParticipationExhibition, ExhibitionPlace, Exhibition, RentExhibitionPlace


def index(request):
    company_name = None
    exhibition_name = None
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        company_form = CompanyForm(request.POST)
        exhibition_form = ExhibitionForm(request.POST)
        if request.POST.get('username'):
            username = request.POST.get('username').lower()
            password = request.POST.get('password')
            try:
                user = authenticate(request, username=username, password=password)
            except User.DoesNotExist:
                messages.add_message(request, messages.ERROR, 'Неверный логин или пароль')
            else:
                if user:
                    login(request, user)
                    return redirect('index')
                else:
                    messages.add_message(request, messages.ERROR, 'Неверный логин или пароль')
        if company_form.is_valid():
            company_name = company_form.cleaned_data['company_name']
        if exhibition_form.is_valid():
            exhibition_name = exhibition_form.cleaned_data['exhibition_name']
    else:
        login_form = LoginForm()
        company_form = CompanyForm()
        exhibition_form = ExhibitionForm()

    exhibition_places = ExhibitionPlace.objects.filter(exhibition__name=exhibition_name).prefetch_related(
        'rentexhibitionplace_set', 'rentexhibitionplace_set__participation__company', 'rentexhibitionplace_set__participation__advertisement_set'
    ).select_related('exhibition').order_by('number')

    exhibition = Exhibition.objects.filter(name=exhibition_name).prefetch_related(
        'participationexhibition_set__company'
    ).first()

    # Запросы

    max_rent_number = ParticipationExhibition.objects.annotate(
        rent_count=Count('rentexhibitionplace')
    ).aggregate(
        max_count=Max('rent_count')
    )['max_count']
    companies_with_max_rent = ParticipationExhibition.objects.annotate(
        rent_count=Count('rentexhibitionplace')
    ).filter(rent_count=max_rent_number, rent_count__gt=0)

    num_products_per_company = Company.objects.annotate(
        num_of_products=Count('products')
    ).order_by('pk').all()

    products_of_company = Products.objects.filter(company__name=company_name).all() if company_name else None

    products = Products.objects.all()
    product_annotations = {}
    for product in products:
        product_annotations[f'product_{product.pk}'] = Sum(
            Case(
                When(
                    products=product,
                    then=F('products__amount')
                ),
                default=0,
                output_field=IntegerField()
            )
        )
    products_per_companies = Company.objects.annotate(
        **product_annotations
    )

    companies_union_products = Company.objects.annotate(
        type_name=Value('Предприятие', output_field=CharField())
    ).values('name', 'type_name').union(
        Products.objects.annotate(
            type_name=Value('Продукция', output_field=CharField())
        ).values('name', 'type_name'),
        all=True,
    )

    context = {
        'login_form': login_form,
        'company_form': company_form,
        'company_name': company_name,
        'exhibition_form': exhibition_form,
        'exhibition_places': exhibition_places,
        'exhibition': exhibition,
        # Запросы
        'max_rent_number': max_rent_number,
        'companies_with_max_rent': companies_with_max_rent,
        'num_products_per_company': num_products_per_company,
        'products_of_company': products_of_company,
        'products': products,
        'products_per_companies': products_per_companies,
        'companies_union_products': companies_union_products,
    }
    return render(request, 'index.html', context)


def print_document(request, rent_id: int):
    from random import randint
    rent = RentExhibitionPlace.objects.get(pk=rent_id)
    context = {
        'number': randint(11111, 99999),
        'rent': rent,
    }
    return render(request, 'document.html', context)
