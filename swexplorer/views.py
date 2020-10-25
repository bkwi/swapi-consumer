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
            utils.fetch_collection(filepath=filepath)
        except Exception:
            if os.path.exists(filepath):
                os.remove(filepath)
            return JsonResponse({'error': 'Failed to fetch dataset'}, status=500)

        c = Collection.objects.create(filename=filename)
        return JsonResponse({
            'id': c.id,
            'created_at': c.created_at.strftime('%c')
        })


class CollectionDetails(TemplateView):
    template_name = 'swexplorer/collection_details.html'


class CollectionData(View):
    def get(self, request, collection_id):
        filename = Collection.objects.get(id=collection_id).filename
        filepath = f'{settings.DATASET_FOLDER}/{filename}.csv'
        headers, rows = utils.load_more(filepath)
        return JsonResponse({
            'headers': headers,
            'rows': rows
        })
