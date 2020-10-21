from django.http import JsonResponse
from django.views.generic import TemplateView, View

from swexplorer import utils


class Collections(TemplateView):
    template_name = 'swexplorer/collections_list.html'


class FetchCollection(View):
    def post(self, request):

        utils.fetch_collection()
        return JsonResponse({'people': 1})
