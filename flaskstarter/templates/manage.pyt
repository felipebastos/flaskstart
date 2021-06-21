"""manage.py was auto-generated by flaskstarter.

   Flaskstarter is an opensource tool that aims to help
   developers to start and maintain a flask backend project.

   Copyright 2021 Felipe Bastos Nunes

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import click
import os
import subprocess
import toml

from jinja2 import Environment, PackageLoader, select_autoescape


@click.group()
def manage():
    '''This script manages the {{name}} project.'''


@manage.command()
@click.argument('port', default='5000')
def runserver(port):
    '''Run Flask server on development mode and selected TCP port.'''
    cmd = ''
    if os.name == 'posix':
        cmd = f'. .venv/bin/activate; export FLASK_APP={{name}}; export FLASK_ENV=development; flask run --port={port}'
    elif os.name == 'nt':
        cmd = f'call .venv/Scripts/activate; set FLASK_APP={{name}}; set FLASK_ENV=development; flask run --port={port}'
    subprocess.run(cmd, shell=True)


@manage.command()
@click.argument('name')
@click.option('-t', '--templates', help="sets if the blueprint will use a private templates' directory.", is_flag=True)
def create_blueprint(name: str, templates: bool):
    '''Creates blueprint under blueprints directory and adds it to instance's settings.toml.'''
    os.mkdir(os.path.join(os.getcwd(), '{{name}}', 'blueprints', name))
    if templates:
        tf = os.path.join(os.getcwd(), '{{name}}', 'blueprints', name, 'templates', name)
        os.makedirs(tf)
        click.echo(f"Place this blueprint's templates under {tf}")

    env = Environment(
        loader=PackageLoader('flaskstarter', 'templates'),
        autoescape=select_autoescape('pyt', 'htmlt')
    )
    init = open(os.path.join(
        os.getcwd(), '{{name}}', 'blueprints', name, '__init__.py'), 'w')
    init.close()
    with open(os.path.join(os.getcwd(), '{{name}}', 'blueprints', name, f'{name}.py'), 'w') as blueprint:
        bluet = env.get_template('blueprint.pyt')
        blueprint.write(bluet.render(
            name=name, templates=templates))

    settings = toml.load(os.path.join(
        os.getcwd(), 'instance', 'settings.toml'))
    settings['default']['EXTENSIONS'].append(
        f'{{name}}.blueprints.{name}.{name}')
    with open(os.path.join(os.getcwd(), 'instance', 'settings.toml'), 'w') as f:
        f.write(toml.dumps(settings))

    click.echo(
        'Blueprint created and registered on instance/settings.toml. Restart your app if running.')


if __name__ == '__main__':
    manage(prog_name='manage')
