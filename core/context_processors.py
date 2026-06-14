from .utils import get_team_settings


def site_theme(request):
    return {"settings": get_team_settings()}
