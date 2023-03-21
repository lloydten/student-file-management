"""student_file_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from systemManagement import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authorize', views.authorize,name='authorize'),
    path('',views.index,name='index'),
    path('home',views.home,name="home"),
    path('delete_file',views.delete_file,name='delete_file'),
    path('upload_file',views.upload_view,name="upload_file"),
    path('download_file',views.download_file,name="download_file"),
    path('images',views.images,name="images"),
    path('videos',views.videos,name="videos"),
    path('audio',views.audio,name="audio"),
    path('pdfs',views.pdfs,name="pdfs"),
    path('text_files',views.text_files,name="text_files"),
    path('code_files',views.code_files,name="code_files"),
    path('search',views.search,name="search"),
    path('home/<str:code>',views.home,name="home"),
]