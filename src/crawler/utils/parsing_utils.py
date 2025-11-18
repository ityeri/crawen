import mimetypes


def guess_extension(type: str) -> str | None:
    ext = mimetypes.guess_extension(type)

    if ext is None and type.startswith('application/'):
        return mimetypes.guess_extension('text/' + type.removeprefix('application/'))

    else:
        return ext

def is_text_content_type(content_type: str) -> bool:
    if not content_type:
        return False
    return content_type.startswith("text/") or \
           content_type in ("application/json", "application/xml", "application/javascript")

def parse_urls_from_tag_attr(key: str, value: str) -> list[str]:
    if isinstance(value, list):
        return value
    else:
        if key.lower() == 'srcset':
            return [part.split()[0] for part in value.split(", ")]
        else:
            return [value]