import os
import shutil

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Create static directory
static_dir = 'static_site'
create_dir(static_dir)

# Copy index.html
shutil.copy2('index.html', static_dir)

# Copy static files
static_src = 'src/control_room/static'
static_dest = os.path.join(static_dir, 'static')
shutil.copytree(static_src, static_dest)

# Copy templates
templates_src = 'src/control_room/templates'
templates_dest = os.path.join(static_dir, 'templates')
shutil.copytree(templates_src, templates_dest)

print("Static site generated in 'static_site' directory")
