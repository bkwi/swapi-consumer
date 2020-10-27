from django.urls import path

from swexplorer import views


urlpatterns = [
    path('', views.CollectionsList.as_view(), name='collections-list'),
    path('collections/<int:collection_id>', views.CollectionDetails.as_view(), name='collection-details'),

    path('api/collections', views.CollectionsListAPI.as_view()),
    path('api/collection-data/<int:collection_id>/page/<int:page>', views.CollectionData.as_view()),
    path('api/collection-data/<int:collection_id>/value-count', views.ValueCount.as_view())
]
