from django.urls import path, include
from . import views
from .views import send_test_email_view
from django.contrib import admin
from django.contrib.auth import views as auth_views



app_name = "users"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('test-email/', send_test_email_view, name='test_email'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_done.html'), name='password_reset_complete'),
]



# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include("quotes.urls")),
#     path('users/', include("users.urls")),
# ]



