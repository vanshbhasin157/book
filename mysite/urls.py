"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from books import views as book_views
from django.contrib.auth import views as auth
from chatting import views as chat_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_book/', book_views.book_view, name='add_book'),
    path('success/', book_views.success, name='success'),
    path('', book_views.display, name='display'),
    path('search/', book_views.search, name='search'),
    path('details/<int:pk>/', book_views.details, name='details'),
    path('login/', book_views.Login, name ='login'), 
    path('logout/', auth.LogoutView.as_view(template_name ='books/logout.html'), name ='logout'), 
    path('register/', book_views.register, name ='register'),
    path('profile/', book_views.profile, name = 'profile'),
    path('profile/password/', book_views.change_password, name='change_password'),
    path('profile/edit/', book_views.edit, name='edit'),
    path('chat/', chat_view.baatein, name='baat'), 
    path('login_api/', book_views.login_api, name='login_api'), 
    path('details_api/', book_views.detail_api, name='details_api'), 
    path('book_view_api/', book_views.book_view_api, name='book_view_api'), 
    path('profile_api/', book_views.profile_api, name='profile_api'), 
    path('display_api/', book_views.display_api, name='display_api'), 
    path('search_api/', book_views.search_api, name='search_api'),
    path('<int:var>/msgs/', chat_view.msg_view, name='msg_view'), 
    path('msgs/', chat_view.msg_list, name='msg_list'),
    





]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)