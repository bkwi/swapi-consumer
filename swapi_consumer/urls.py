from django.urls import path

from swexplorer import views


urlpatterns = [
    path('', views.Collections.as_view(), name='collections'),

    path('api/fetch-collections', views.FetchCollection.as_view()),
]
