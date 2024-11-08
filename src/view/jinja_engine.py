from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader('C:/Users/HP/PycharmProjects/Tennis_Match_Scoreboard/src/view/templates'))
# env = Environment(loader=FileSystemLoader('src/view/templates'))

def render_template(template_name):
    template = env.get_template(template_name)
    return template.render()
