from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views



from django.conf import settings
from django.conf.urls.static import static

from personal.views import (
    home_screen_view,    
    temp,
    home_proj,
    dashboard,

)


from account.views import (    
    register_view,
    login_view,
    logout_view,
    cas_view,

)

urlpatterns = [	
       
	path('admin/', admin.site.urls),
 
    path('', login_view, name="login"),
    path('account/', include('account.urls', namespace='account')),
    path('logout/', logout_view, name="logout"),  
    path('register/', register_view, name="register"),
    path('home/', home_screen_view, name='home'),
    path('cas/', cas_view, name="cas"),        
    path('temp/', temp, name='temp'),    
    path('home-proj/', home_proj, name='home-proj'),
    path('dashboard/', dashboard, name='dashboard'),
    
    
    
    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
     name='password_reset_complete'),
     
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
