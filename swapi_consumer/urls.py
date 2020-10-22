from django.urls import path

from swexplorer import views


urlpatterns = [
    path('', views.CollectionsList.as_view(), name='collections-list'),

    path('api/collections', views.CollectionsAPI.as_view()),
]
