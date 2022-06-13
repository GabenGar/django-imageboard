import re
import os
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag()
def customize_post_string(post_string, posts_ids, pk=None):
    post_string = escape(post_string)
    post_string = insert_links(post_string, posts_ids, pk)
    post_string = color_quoted_text(post_string)
    return mark_safe(post_string.replace("\n", "<br>"))


@register.filter(name='strippath')  # gets '/filepath/file.extension', returns 'file.extension'
def into_basename(file):
    return os.path.basename(file)


def color_quoted_text(post_string):
    quoted_text = re.findall(r'^\s*&gt;.+', post_string, flags=re.MULTILINE)  # '^\s*&gt;[^&gt;].+'
    if quoted_text:
        for count, index in enumerate(quoted_text):
            span = f"<span style='color:peru'>{quoted_text[count]}</span>"
            post_string = post_string.replace(quoted_text[count], span)
    return post_string


def insert_links(post_string, posts_ids, pk):
    match = re.findall(pattern='&gt;&gt;[0-9]+', string=post_string)
    if match:
        for m in match:
            post_id = m.strip('&gt;&gt;')
            if int(post_id) in posts_ids:
                if pk:  # pk isn't None only when passed from the list of threads page
                    post_string = post_string.replace(m, f"<a class='quote' href='/thread/{pk}/#id{post_id}'>{m}</a>")
                else:
                    post_string = post_string.replace(m, f"<a class='quote' href='#id{post_id}'>{m}</a>")
    return post_string
