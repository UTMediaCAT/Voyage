import sys
from django import forms
from django.db import models
from django.core import validators
from django.utils.six.moves.urllib.parse import urlsplit, urlunsplit

class URLProtocolField(models.CharField):
    default_validators = [validators.URLValidator()]

    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 2000)
        super(URLProtocolField, self).__init__(verbose_name, name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(URLProtocolField, self).deconstruct()
        if kwargs.get("max_length") == 200:
            del kwargs['max_length']
        return name, path, args, kwargs

    def to_python(self, value):

        def split_url(url):
            """
            Returns a list of url parts via ``urlparse.urlsplit`` (or raises a
            ``ValidationError`` exception for certain).
            """
            try:
                return list(urlsplit(url))
            except ValueError:
                # urlparse.urlsplit can raise a ValueError with some
                # misformatted URLs.
                raise ValidationError(self.error_messages['invalid'], code='invalid')

        if value == None:
            value = ""

        if (type(value) is str):
            value = super(URLProtocolField, self).to_python(value.lower())
        else:
            value = super(URLProtocolField, self).to_python(value.geturl().lower())


        if value:
            if (type(value) is not str):
                value = value.geturl()
            url_fields = split_url(value)
            if not url_fields[0]:
                # If no URL scheme given, assume http://
                url_fields[0] = 'http'
            if not url_fields[1]:
                # Assume that if no domain is provided, that the path segment
                # contains the domain.
                url_fields[1] = url_fields[2]
                url_fields[2] = ''
                # Rebuild the url_fields list, since the domain segment may now
                # contain the path too.
                url_fields = split_url(urlunsplit(url_fields))
            value = urlunsplit(url_fields)
        return value

    def formfield(self, **kwargs):
        # As with CharField, this will cause URL validation to be performed
        # twice.
        defaults = {
            'form_class': forms.URLField,
        }
        defaults.update(kwargs)
        return super(URLProtocolField, self).formfield(**defaults)
