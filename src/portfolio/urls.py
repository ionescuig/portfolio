"""portfolio URL Configuration

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
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from projects.views import HomeView, AboutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('projects/', include(('projects.urls', 'projects'), namespace='projects')),
    path('about', AboutView.as_view(), name='about'),

    path('articles/', include(('articles.urls', 'articles'), namespace='articles')),
    path('summernote/', include('django_summernote.urls')),
]

# -----------------------------
# --- For local development ---
# -----------------------------
try:
    from .settings.local import DEBUG
except:
    DEBUG = False

if DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
