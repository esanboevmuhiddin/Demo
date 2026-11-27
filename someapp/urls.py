from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('cabinet/', views.cabinet_view, name='cabinet'),
    path('application/new/', views.application_create, name='application_create'),
    path('application/<int:app_id>/review/', views.review_create, name='review_create'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/<int:app_id>/status/', views.admin_change_status, name='admin_change_status'),
]