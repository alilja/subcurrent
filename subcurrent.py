from os import listdir

from yaml import load
from jinja2 import Environment, PackageLoader
from markdown import markdown
from slugify import slugify

jinja_env = Environment(loader=PackageLoader('subcurrent', 'templates'))

with open("config.yaml") as f:
    config = load(f)

for item in listdir("posts"):
    dot_location = item.find(".")
    if dot_location == -1:
        continue
    if item[dot_location:] != ".md":
        continue

    # if it's a special file, get the right template
    special_files = {"index", "404"}
    if item[:dot_location] in special_files:
        template = jinja_env.get_template('%s.html' % item[:dot_location])
    else:
        template = jinja_env.get_template('post.html')

    with open("posts/%s" % item) as f:
        lines = f.readlines()

    title = lines[0].decode("utf8", "ignore").strip('#\n\r ')
    slug = slugify(title)
    body = markdown(unicode(''.join(lines[1:]), "UTF-8"))

    with open("../{0}.html".format(slug), "wb") as output_file:
        output_file.write(template.render(site_name=config["site_name"], title=title, body_text=body))

