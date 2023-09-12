from django import template

register = template.Library()


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()


@register.filter
def get_item(dictionary, keyword):
    if type(dictionary) == dict:
        return dictionary.get(keyword)


@register.filter
def ru_plural(value, variants):
    variants = variants.split(",")
    if not value and value != 0:
        return variants[0]
    value = abs(int(value))
    if value % 10 == 1 and value % 100 != 11:
        variant = 0
    elif 2 <= value % 10 <= 4 and (value % 100 < 10 or value % 100 >= 20):
        variant = 1
    else:
        variant = 2
    return variants[variant]
