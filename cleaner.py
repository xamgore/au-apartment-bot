import re

import bleach


def remove_unallowed_tags(text):
    allowed_tags = ['b', 'strong', 'i', 'em', 'code', 'pre', 'br']
    allowed_attrs = {'a': ['href']}

    s = re.sub('</div>\s*<div>', '</div><br><div>', text)
    return bleach.clean(s, allowed_tags, allowed_attrs, strip=True).replace('<br>', '\n')


def unicode_unescape(text):
    return re.sub(r'\\[uU]0*([a-z0-9]{4,})', r'&#x\1;', text)
