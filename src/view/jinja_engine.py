from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader('src/view/templates'))

def render_template(template_name):
    template = env.get_template(template_name)
    return template.render()

def render_template_messages(template_name, server_response):
    template = env.get_template(template_name)
    return template.render(server_response=server_response)