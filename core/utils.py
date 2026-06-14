from .models import TeamSettings


DEFAULT_TEAM_SETTINGS = {
    "team_tag": "W2W",
    "team_name": "War To Win",
    "welcome_text": "Une team mobile ambitieuse, disciplinee et prete pour les prochains defis.",
    "font_choice": TeamSettings.FONT_TECH,
    "background_color": "#050507",
    "background_soft_color": "#0f0a0d",
    "card_color": "#121116",
    "card_soft_color": "#17141c",
    "primary_color": "#ff274b",
    "primary_soft_color": "#ff5c78",
    "accent_color": "#00b16a",
    "text_color": "#ffffff",
    "muted_color": "#a7acba",
}


def get_team_settings():
    settings = TeamSettings.objects.first()

    if settings:
        return settings

    return TeamSettings.objects.create(**DEFAULT_TEAM_SETTINGS)
