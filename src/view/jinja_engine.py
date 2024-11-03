from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader('C:/Users/HP/PycharmProjects/Tennis_Match_Scoreboard/src/view/templates'))

def render_template(template_name):
    template = env.get_template(template_name)
    return template.render()

# print(render_template('start.html').encode('utf-8'))
#
# import os
#
# template_folder = r'src/view/templates'
# print(os.listdir(template_folder))  # Выводит список файлов в указанной директории
#
# # print(os.getcwd())
# #
# # template_folder ='C:/Users/HP/PycharmProjects/Tennis_Match_Scoreboard/src/view'
# # os.getcwd()
# # print(os.listdir(template_folder))  # Выводит список файлов в указанной директории
