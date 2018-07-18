import re

import bleach


def remove_unallowed_tags(text):
    allowed_tags = ['b', 'strong', 'i', 'em', 'code', 'pre', 'br']
    allowed_attrs = {'a': ['href']}

    s = re.sub('</div>\s*<div>', '</div><br><div>', text)
    return bleach.clean(s, allowed_tags, allowed_attrs, strip=True).replace('<br>', '\n')


def unicode_unescape(text):
    to_xml = lambda x: f'&#x{x.group(1).lstrip("0")};'
    return re.sub(r'\\[uU]([a-z0-9]{8}|[a-z0-9]{4})', to_xml, text)
