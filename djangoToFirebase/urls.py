from django.urls import path
from . import views
from .views import ViewPdf
urlpatterns = [
    path('see_data', views.test, name='test'),
    path('update_data', views.updateToFirebase),
    path('pdf/', ViewPdf.as_view())
]