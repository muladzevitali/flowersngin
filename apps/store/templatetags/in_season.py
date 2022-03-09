from django import template

register = template.Library()


@register.filter(name='in_season')
def in_season(things, season):
    return things.filter(season=season)
