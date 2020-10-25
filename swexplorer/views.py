import os
import uuid

from django.conf import settings
from django.http import JsonResponse
from django.views.generic import TemplateView, View

from swexplorer import utils
from swexplorer.models import Collection


class CollectionsList(TemplateView):
    template_name = 'swexplorer/collections_list.html'


class CollectionsListAPI(View):
    def get(self, request):
        response = {
            'collections': [
                {
                    'id': c.id,
                    'created_at': c.created_at.strftime('%c')
                } for c in Collection.objects.all()
            ]
        }
        return JsonResponse(response)

    def post(self, request):
        filename = uuid.uuid4().hex
        filepath = f'{settings.DATASET_FOLDER}/{filename}.csv'

        try:
            total_items = utils.fetch_collection(filepath=filepath)
        except Exception:
            if os.path.exists(filepath):
                os.remove(filepath)
            return JsonResponse({'error': 'Failed to fetch dataset'}, status=500)

        c = Collection.objects.create(filename=filename, total_items=total_items)
        return JsonResponse({
            'id': c.id,
            'created_at': c.created_at.strftime('%c')
        })


class CollectionDetails(TemplateView):
    template_name = 'swexplorer/collection_details.html'


class CollectionData(View):
    def get(self, request, collection_id, page):
        collection = Collection.objects.get(id=collection_id)
        filepath = f'{settings.DATASET_FOLDER}/{collection.filename}.csv'
        headers, rows, next_page = utils.load_more(filepath, page, total_items=collection.total_items)
        return JsonResponse({
            'headers': headers,
            'rows': rows,
            'next_page': next_page
        })
