from apps.store import models


def seasons_context(request):
    if 'admin' in request.path:
        return dict()

    seasons = models.Season.objects.all().order_by('pk')

    return dict(seasons=seasons)
