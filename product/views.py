from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Estate, Feedback, Category, Favourite, FeedbackResponse
from .forms import FeedbackForm, FeedbackResponseForm
from django.contrib import messages
from .forms import ContactForm
from .filters import EstateFilter
from django.core.paginator import Paginator

def index(request):
    parent_categories = Category.objects.filter(parent_category__isnull=True)
    estates = Estate.objects.filter(is_active=True)[:8]
    liked_estates_ids = []

    if request.user.is_authenticated:
        liked_estates_ids = Favourite.objects.filter(user=request.user).values_list('estate_id', flat=True)

    for estate in estates:
        estate.is_favourite = estate.id in liked_estates_ids

    return render(request, 'main/index.html', {
        'parent_categories': parent_categories,
        'estates': estates,
        'liked_estates_ids': liked_estates_ids,
    })

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = Category.objects.filter(parent_category=category)
    estates = Estate.objects.filter(category=category)

    if request.user.is_authenticated:
        liked_estates_ids = Favourite.objects.filter(user=request.user).values_list('estate_id', flat=True)
    else:
        liked_estates_ids = []

    for estate in estates:
        estate.is_favourite = estate.id in liked_estates_ids

    return render(request, 'main/category_detail.html', {
        'category': category,
        'subcategories': subcategories,
        'estates': estates,
    })

def detail(request, id):
    estate = get_object_or_404(Estate, id=id)
    mail_cover = estate.image_set.filter(is_main=True).first()
    images = estate.image_set.filter(is_main=False)
    feedbacks = Feedback.objects.filter(estate=estate).order_by('-created_at')
    related_estates = Estate.objects.filter(
        category=estate.category
    ).exclude(
        id=estate.id
    ).order_by('-created_at')[:3]

    if request.user.is_authenticated:
        liked_estates_ids = Favourite.objects.filter(user=request.user).values_list('estate_id', flat=True)
    else:
        liked_estates_ids = []

    if request.method == 'POST':
        if 'feedback_submit' in request.POST and request.user.is_authenticated:
            form = FeedbackForm(request.POST)
            if form.is_valid():
                feedback = form.save(commit=False)
                feedback.user = request.user
                feedback.estate = estate
                feedback.save()
                messages.success(request, 'Ваш отзыв отправлен!')
                return redirect('detail', id=estate.id)

        elif 'response_submit' in request.POST and request.user.is_authenticated:
            response_form = FeedbackResponseForm(request.POST)
            feedback_id = request.POST.get('feedback_id')
            parent_feedback = get_object_or_404(Feedback, id=feedback_id)
            if response_form.is_valid():
                response = response_form.save(commit=False)
                response.user = request.user
                response.feedback = parent_feedback
                response.save()
                messages.success(request, 'Ответ добавлен.')
                return redirect('detail', id=estate.id)

    else:
        form = FeedbackForm()
        response_form = FeedbackResponseForm()

    estate.is_favourite = estate.id in liked_estates_ids

    return render(request, 'main/estate_detail.html', {
        'estate': estate,
        'mail_cover': mail_cover,
        'images': images,
        'feedbacks': feedbacks,
        'related_estates': related_estates,
        'form': form,
        'response_form': response_form,
    })

@login_required
def delete_feedback(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    estate_id = feedback.estate.id

    if request.user == feedback.user or request.user.is_superuser:
        feedback.delete()
        messages.success(request, "Отзыв удалён.")
    else:
        messages.error(request, "Вы не можете удалить этот отзыв.")

    return redirect('detail', id=estate_id)

@login_required
def delete_response(request, pk):
    response = get_object_or_404(FeedbackResponse, pk=pk)
    if request.user == response.user or request.user.is_superuser:
        response.delete()
        messages.success(request, "Ответ удалён.")
    else:
        messages.error(request, "У вас нет прав для удаления.")
    return redirect('detail', id=response.feedback.estate.id)

def estate_list_filtered(request, filter_type):
    if filter_type == 'rent':
        estates = Estate.objects.filter(category__title__icontains='аренда')
    elif filter_type == 'sale':
        estates = Estate.objects.filter(category__title__icontains='продажа')
    elif filter_type == 'popular':
        estates = Estate.objects.filter(is_popular=True)
    elif filter_type == 'new':
        estates = Estate.objects.filter(is_new=True)
    else:
        estates = Estate.objects.all()

    if request.user.is_authenticated:
        liked_estates_ids = Favourite.objects.filter(user=request.user).values_list('estate_id', flat=True)
    else:
        liked_estates_ids = []

    for estate in estates:
        estate.is_favourite = estate.id in liked_estates_ids

    return render(request, 'main/estate_list.html', {
        'estates': estates,
        'filter': filter_type
    })

@login_required
def user_estate_like(request, id):
    estate = get_object_or_404(Estate, id=id)
    like = Favourite.objects.filter(user=request.user, estate=estate).first()

    if like:
        like.delete()
    else:
        Favourite.objects.create(user=request.user, estate=estate)

    return redirect(request.META.get('HTTP_REFERER', 'index'))

@login_required
def favourite_list(request):
    favourite_estates = Estate.objects.filter(favourite__user=request.user)

    for estate in favourite_estates:
        estate.is_favourite = True

    return render(request, 'main/favourite_list.html', {'favourite_estates': favourite_estates})

@login_required
def toggle_favourite(request, id):
    estate = get_object_or_404(Estate, id=id)
    user = request.user

    favourite = Favourite.objects.filter(user=user, estate=estate).first()
    if favourite:
        favourite.delete()
    else:
        Favourite.objects.create(user=user, estate=estate)

    return redirect(request.META.get('HTTP_REFERER', 'index'))

def contact_view(request):
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Ваше сообщение отправлено! Мы свяжемся с вами.')
            return redirect('contact')

    return render(request, 'main/contact.html', {'form': form})

def about_view(request):
    team = [
        {'name': 'Аяна', 'role': 'Руководитель проекта', 'description': 'Организует работу команды и управляет проектом недвижимости.'},
        {'name': 'Билал', 'role': 'Бэкенд-разработчик', 'description': 'Разрабатывает серверную часть сайта: логика, базы данных, API.'},
        {'name': 'Лейла', 'role': 'Фронтенд-разработчик', 'description': 'Создаёт внешний вид сайта, работает с HTML/CSS и формами.'},
        {'name': 'Ситора', 'role': 'Контент-менеджер', 'description': 'Следит за контентом объявлений и текстами сайта.'},
        {'name': 'Байэль', 'role': 'UX/UI-дизайнер', 'description': 'Проектирует удобный интерфейс и стиль сайта.'},
    ]
    return render(request, 'main/about.html', {'team': team})

def estate_list_view(request):
    estates = EstateFilter(request.GET, queryset=Estate.objects.filter(is_active=True))
    paginator = Paginator(estates.qs, 3)
    page_number = request.GET.get('page')
    page_obj= paginator.get_page(page_number)

    return render(request, 'main/estate_list.html', {'estates': estates, 'page_obj': page_obj})