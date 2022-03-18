from django.urls import path, include
from .views import *

urlpatterns = [
    path('admin/', include('app.admin.urls')),
    path('', include('app.client.urls')),

    path('login/', LoginView.as_view()),

]

