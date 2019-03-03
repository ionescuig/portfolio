"""projects URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from django.urls import path
from .views import createproject, DetailProjectView, UpdateProjectView, ListProjectView

urlpatterns = [
    path('', ListProjectView.as_view(), name='project_list'),
    path('detail-project/<slug:slug>', DetailProjectView.as_view(), name='project_detail'),
    path('update-project/<slug:slug>', UpdateProjectView.as_view(), name='project_update'),
    path('create-project/', createproject, name='project_create'),
]
