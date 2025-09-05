from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('blog/<int:blog_id>/', views.blog_detail_view, name='blog_detail'),
    path('create_blog/', views.create_blog_view ,name='create_blog'),
    path('edit_blog/<int:blog_id>/', views.edit_blog_view, name='edit_blog'),
    path('delete_blog/<int:blog_id>/', views.delete_blog_view, name='delete_blog'),
]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)