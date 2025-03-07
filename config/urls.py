"""
URL configuration for gigwork_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from gigwork import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'gigs', views.GigViewSet)
router.register(r'postings', views.PostingViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('gigwork/api/', include(router.urls)),
    #path('test/<int:param>/', views.test),
    #path('users/<str:field>/<str:value>/', views.UserViewSet.get_users_by_field),
    #path('gigs/<str:field>/<str:str>/', views.GigViewSet.get_gigs_by_field),
    #path('postings/<str:field>/<str:str>/', views.PostingViewSet.get_postings_by_field),
    ]
