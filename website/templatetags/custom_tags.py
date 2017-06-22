from django import template
register = template.Library()


# https://chriskief.com/2013/11/06/conditional-output-of-a-django-block/
# register tag as decorator
@register.tag(name='captureas')
def do_captureas(parser, token):

    try:
        tag_name, args = token.contents.split(None, 1)
        # splitting by None == splitting by spaces
    except ValueError:
        raise template.TemplateSyntaxError("'captureas' node requires variable name.")

    # parser.parse() takes tuple of block tag names to parse until
    # nodelist here is a list of all nodes between the {% captureas %} and
    # {% endcaptureas %} block tags
    nodelist = parser.parse(('endcaptureas',))

    # explicitly call delete b/c parser hasn't yet "consumed" the
    # {% endcaptureas %} tag
    parser.delete_first_token()

    return CaptureasNode(nodelist, args)


class CaptureasNode(template.Node):

    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = output
        return ''
