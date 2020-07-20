from django.conf import settings
from django.contrib import admin
from django.urls import path,include,reverse_lazy
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/',include('account.urls')),
    path('chat/',include('chat.urls')),
    path('',include('django.contrib.auth.urls')),
    # path('login/',auth_views.LoginView.as_view(),name='login'),
    # path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    # path('password-reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    # path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    # path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    # path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
