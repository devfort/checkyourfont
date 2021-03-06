from collections import namedtuple
from django.conf import settings
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        kwargs['baseurl'] = 'http://checkyourfont.com/'
        return super(Home, self).get_context_data(**kwargs)

    def render_to_response(self, context, **response_kwargs):
        response = super(Home, self).render_to_response(context, **response_kwargs)
        if not settings.DEBUG:
            response['Cache-Control'] = "max-age=86400"
        return response


class Font(TemplateView):
    template_name = 'font.html'

    def get_context_data(self, **kwargs):
        def int_(other):
            try:
                return int(other)
            except ValueError:
                return None

        def param_(kv):
            bits = kv.split('=', 2)
            ret = [ bits[0].replace('+', ' ') ]
            if len(bits) > 1:
                ret.append(bits[1].replace('+', ' '))
            else:
                ret.append(True)
            return ret

        SIZE = namedtuple('SIZE', ('pixels', 'is_key'))
        SOURCE = namedtuple('SOURCE', ('url', 'format', 'google', 'args'))

        class WebFont(object):
            def __init__(self, name, config):
                self.name = name
                # config is a string, worry about this later
                self.config = config

            def google(self):
                return self.config.startswith('google/')

            def sizes(self):
                return self.config[7:]

            def sources(self):
                return [
                    SOURCE(url=self.config, format='woff'),
                ]

        bits = self.kwargs['params'].split(';')
        font, params = bits[0].replace('+', ' '), bits[1:]
        kwargs['font'] = font
        kwargs['webfonts'] = {}
        sizes = None
        key_sizes = None
        min_size = None
        max_size = None
        for name, value in (param_(p) for p in params):
            if name == 'sizes':
                sizes = filter(
                    lambda x: x is not None,
                    map(int_, value.split(','))
                )
            elif name == 'sizes.max':
                max_size = int_(value)
            elif name == 'sizes.min':
                min_size = int_(value)
            elif name == 'sizes.key':
                key_sizes = filter(
                    lambda x: x is not None,
                    map(int_, value.split(','))
                )
            elif name.startswith('font.'):
                font = name[5:]
                kwargs['webfonts'][font] = WebFont(font, value)
            elif name == 'text':
                kwargs['text'] = """Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."""

        if sizes is None:
            if min_size is None:
                min_size = 10
            if max_size is None:
                max_size = 24
            sizes = range(min_size, max_size+1)

        if key_sizes is None:
            # FIXME guess smarter
            key_sizes = [ 12, 14, 18, 24 ]
        key_sizes = set(key_sizes)

        sizes_ = []
        for size in sizes:
            sizes_.append(SIZE(pixels=size, is_key=size in key_sizes))

        kwargs['sizes'] = sizes_

        return super(Font, self).get_context_data(**kwargs)

    def render_to_response(self, context, **response_kwargs):
        response = super(Font, self).render_to_response(context, **response_kwargs)
        if not settings.DEBUG:
            response['Cache-Control'] = "max-age=86400"
        return response
