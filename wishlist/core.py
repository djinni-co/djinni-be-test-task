import functools

from django import http
from django.template import loader, engines, backends
from django.template.backends.utils import csrf_input_lazy, csrf_token_lazy


# this one won't render context argh
def render_macro_nice(request, template_name, macro_name, **ctx):
    tmpl = loader.get_template(template_name)
    mod = tmpl.template.module
    macro = getattr(mod, macro_name)

    reqctx = {
        "request": request,
        "csrf_input": csrf_input_lazy(request),
        "csrf_token": csrf_token_lazy(request),
    }
    for context_processor in tmpl.backend.template_context_processors:
        reqctx.update(context_processor(request))

    markup = macro(**ctx)
    return http.HttpResponse(markup)


@functools.cache
def macro_t(template_name, macro_name):
    jinja = next(e for e in engines.all()
                 if isinstance(e, backends.jinja2.Jinja2))
    return jinja.env.from_string(
        '{%% from "%s" import card with context %%}{{ %s(**ctx) }}'
        % (template_name, macro_name))


def render_macro(request, template_name, macro_name, **ctx):
    jinja = next(e for e in engines.all()
                 if isinstance(e, backends.jinja2.Jinja2))
    reqctx = {
        "ctx": ctx,
        "request": request,
        "csrf_input": csrf_input_lazy(request),
        "csrf_token": csrf_token_lazy(request),
    }
    for context_processor in jinja.template_context_processors:
        reqctx.update(context_processor(request))

    t = macro_t(template_name, macro_name)
    markup = t.render(reqctx)
    return http.HttpResponse(markup)

