from django.urls import path
from .views import login_view, register, meus_produtos, detalhes_produto, logout_view, CustomPasswordResetCompleteView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', login_view, name='login'),
    path('register/', register, name='register'),
    path('meus_produtos/', meus_produtos, name='meus_produtos'),
    path('produtos/<int:produto_id>/', detalhes_produto, name='detalhes_produto'),
    path('logout/', logout_view, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset_form'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

]
