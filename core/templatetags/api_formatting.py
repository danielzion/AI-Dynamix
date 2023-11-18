# myapp/templatetags/api_formatting.py

from django import template
import json
import re

register = template.Library()


@register.filter(name='format_openai_response')
def format_openai_response(value):
    try:
        # Attempt to load the response as JSON
        data = json.loads(value)

        # If it's a dictionary, format it prettily
        if isinstance(data, dict):
            formatted_json = json.dumps(data, indent=4)
            # Further format if there are code fields in the JSON
            return format_code_fields(formatted_json)

        # Add more conditions here for other data types if necessary
        # ...

    except json.JSONDecodeError:
        # If it's not JSON, handle it as plain text
        # This includes formatting for code enclosed in backticks
        return format_code_fields(value)

    # Default return if none of the above conditions are met
    return value


def format_code_fields(text):
    # Replace triple backticks with HTML code tags
    formatted_text = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', text, flags=re.DOTALL)

    # Replace single line breaks with HTML line breaks for better readability
    formatted_text = formatted_text.replace("\n", "<br>")

    return formatted_text


@register.filter(name='format_code_snippets')
def format_code_snippets(value):
    # Replace triple backticks with HTML code tags for code formatting
    formatted_value = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', value, flags=re.DOTALL)
    return formatted_value
