import os
from datetime import datetime

from django.conf import settings
from django.http import JsonResponse
from django.views.generic import TemplateView, View

from swexplorer import utils


class Collections(TemplateView):
    template_name = 'swexplorer/collections_list.html'


class FetchCollection(View):
    def post(self, request):

        ts = datetime.now().timestamp()
        filepath = f'{settings.DATASET_FOLDER}/dataset_{ts}.csv'
        try:
            utils.fetch_collection(filepath=filepath)
        except Exception:
            if os.path.exists(filepath):
                os.remove(filepath)
            return JsonResponse({'error': 'Failed to fetch dataset'}, status=500)

        return JsonResponse({'datasets': 1})
