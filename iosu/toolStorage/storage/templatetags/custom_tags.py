from django import template

register = template.Library()


@register.filter
def get_tool_count(equipment, tool_id):
    # Access the dynamically generated annotation field for the specific tool
    tool_count_field = f'tool_{tool_id}'
    return getattr(equipment, tool_count_field, 0)
