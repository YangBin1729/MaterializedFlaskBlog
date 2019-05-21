from .models import Tag


def generate_tags(tagname):
    tag = Tag.query.filter_by(name=tagname).first()
    if not tag:
        tag = Tag(name=tagname)
    return tag
