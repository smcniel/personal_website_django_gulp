# Custom subclassing of sorl-thumbnail
import os
import re
from sorl.thumbnail.base import ThumbnailBackend
from django.template.defaultfilters import slugify
from django.conf import settings


class SEOThumbnailBackend(ThumbnailBackend):
    """
    Custom backend for SEO friendly thumbnail
    Code from http://blog.yawd.eu/2012/seo-friendly-image-names-sorl-thumbnail-and-django/
    """
    def _get_thumbnail_filename(self, source, geometry_string, options):
        # Computes the destination filename
        split_path = re.sub(r'^%s%s?' % (source.storage.path(''), os.sep), '', source.name).split(os.sep)
        split_path.insert(-1, geometry_string)

        # attempt to slugify the filename to make it SEO-friendly
        split_name = split_path[-1].split('.')
        try:
            split_path[-1] = '%s.%s' % (slugify('.'.join(split_name[:-1])), split_name[-1])
        except:
            # on fail keep the original filename
            pass

        path = os.sep.join(split_path)

        # if the path already starts with THUMBNAIL_PREFIX do not concatenate
        # the PREFIX
        if not path.startswith(settings.THUMBNAIL_PREFIX):
            return '%s%s' % (settings.THUMBNAIL_PREFIX, path)
        return path
