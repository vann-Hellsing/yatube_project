from django import template


register = template.Library()


@register.filter
def uglify(text):
    change_text = []
    for _ in range(len(text)):
        if _ % 2 == 0:
            change_text.append(text[_].lower())
        else:
            change_text.append((text[_].upper()))

    return ''.join(change_text)
