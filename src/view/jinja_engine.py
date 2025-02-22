from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('src/view/templates'))

def render_template(template_name, **kwargs):
    template = env.get_template(template_name)
    return template.render(kwargs)