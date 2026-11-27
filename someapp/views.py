from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Application, Status
from .forms import RegisterForm, ApplicationForm, ReviewForm

def is_admin(user):
    return user.is_authenticated and user.username == 'Admin26'

# ---------- Регистрация ----------
def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Регистрация прошла успешно! Войдите в систему.')
        return redirect('login')
    return render(request, 'core/register.html', {'form': form})

# ---------- Вход ----------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('cabinet')
        messages.error(request, 'Неверный логин или пароль.')
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# ---------- Личный кабинет ----------
@login_required
def cabinet_view(request):
    apps = request.user.applications.all()
    paginator = Paginator(apps, 5)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'core/cabinet.html', {
        'applications': page,
        'can_review_ids': [a.id for a in apps if a.status == Status.DONE and not hasattr(a, 'review')],
    })

# ---------- Создание заявки ----------
@login_required
def application_create(request):
    form = ApplicationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        app = form.save(commit=False)
        app.user = request.user
        app.status = Status.NEW
        app.save()
        messages.success(request, 'Заявка успешно создана и отправлена на согласование.')
        return redirect('cabinet')
    return render(request, 'core/application_form.html', {'form': form})

# ---------- Отзыв ----------
@login_required
def review_create(request, app_id):
    application = get_object_or_404(Application, pk=app_id, user=request.user)
    if application.status != Status.DONE:
        messages.error(request, 'Оставить отзыв можно только после завершения обучения.')
        return redirect('cabinet')
    if hasattr(application, 'review'):
        messages.info(request, 'Вы уже оставили отзыв.')
        return redirect('cabinet')

    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.application = application
        review.save()
        messages.success(request, 'Спасибо за отзыв!')
        return redirect('cabinet')
    return render(request, 'core/review_form.html', {'form': form, 'app': application})

# ---------- Админ-панель ----------
@user_passes_test(is_admin, login_url='login')
def admin_panel(request):
    q = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '')
    sort = request.GET.get('sort', '-created_at')

    apps = Application.objects.select_related('user', 'user__profile').all()
    if q:
        apps = apps.filter(
            Q(user__username__icontains=q) |
            Q(user__profile__full_name__icontains=q)
        )
    if status_filter:
        apps = apps.filter(status=status_filter)
    if sort in ('created_at', '-created_at', 'start_date', '-start_date'):
        apps = apps.order_by(sort)

    paginator = Paginator(apps, 10)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'core/admin_panel.html', {
        'applications': page,
        'statuses': Status.choices,
        'q': q,
        'status_filter': status_filter,
        'sort': sort,
    })

@user_passes_test(is_admin, login_url='login')
def admin_change_status(request, app_id):
    if request.method != 'POST':
        return redirect('admin_panel')
    application = get_object_or_404(Application, pk=app_id)
    new_status = request.POST.get('status')
    if new_status in dict(Status.choices):
        application.status = new_status
        application.save()
        messages.success(request, f'Статус заявки #{application.pk} обновлен.')
    return redirect('admin_panel')