from django import template

register = template.Library()


@register.filter
def get_products_count(equipment, product_id):
    # Access the dynamically generated annotation field for the specific product
    product_count_field = f'product_{product_id}'
    return getattr(equipment, product_count_field, 0)
