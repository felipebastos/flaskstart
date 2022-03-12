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

from flaskstarter.tools.templating import get_template


@click.group()
def manage():
    '''This script manages the {{name}} project.'''


@manage.command()
@click.argument('port', default='5000')
def runserver(port):
    '''Run Flask server on development mode and selected TCP port.'''
    cmd = ''
    if os.name == 'posix':
        cmd = f'export FLASK_APP={{name}}.app; export FLASK_ENV=development; flask run --port={port}'
        subprocess.run(cmd, shell=True)
    elif os.name == 'nt':
        cmd = f'$env:FLASK_APP = "{{name}}.app"; $env:FLASK_ENV = "development"; flask run --port={port}'
        subprocess.run(["powershell", "-Command", cmd])


@manage.command()
@click.argument('name')
def plug_extension(name: str):
    settings = toml.load(os.path.join(
        os.getcwd(), 'instance', 'settings.toml'))
    if f'{{name}}.ext.{name}:init_app' in settings['default']['EXTENSIONS']:
        click.echo('An extension with such a name seems to be already plugged.')
        exit(0)
    # project.ext.database
    with open(os.path.join(os.getcwd(), '{{name}}', 'ext', f'{name}.py'), 'w') as new_extension:
        ext_template = get_template('ext.pyt')
        new_extension.write(ext_template.render())

    settings['default']['EXTENSIONS'].append(
        f'{{name}}.ext.{name}:init_app')
    with open(os.path.join(os.getcwd(), 'instance', 'settings.toml'), 'w') as f:
        f.write(toml.dumps(settings))
    
    click.echo('Extension added and configured. Remember to code it, as it is just a skeleton.')

@manage.command()
@click.argument('name')
@click.option('-t', '--templates', help="sets if the blueprint will use a private templates' directory.", is_flag=True, default=False)
def plug_blueprint(name: str, templates: bool):
    '''Creates blueprint under blueprints directory and adds it to instance's settings.toml.'''
    settings = toml.load(os.path.join(
        os.getcwd(), 'instance', 'settings.toml'))
    if f'{{name}}.blueprints.{name}.{name}:init_app' in settings['default']['EXTENSIONS']:
        click.echo('A blueprint with such a name seems to be already plugged.')
        exit(0)
    os.mkdir(os.path.join(os.getcwd(), '{{name}}', 'blueprints', name))
    if templates:
        tf = os.path.join(
            os.getcwd(), '{{name}}', 'blueprints', name, 'templates', name)
        os.makedirs(tf)
        click.echo(f"Placed this blueprint's templates under {tf}")

    init = open(os.path.join(
        os.getcwd(), '{{name}}', 'blueprints', name, '__init__.py'), 'w')
    init.close()
    with open(os.path.join(os.getcwd(), '{{name}}', 'blueprints', name, f'{name}.py'), 'w') as blueprint:
        bluet = get_template('blueprint.pyt')
        blueprint.write(bluet.render(
            name=name, templates=templates))

    settings = toml.load(os.path.join(
        os.getcwd(), 'instance', 'settings.toml'))
    settings['default']['EXTENSIONS'].append(
        f'{{name}}.blueprints.{name}.{name}:init_app')
    with open(os.path.join(os.getcwd(), 'instance', 'settings.toml'), 'w') as f:
        f.write(toml.dumps(settings))

    click.echo(
        'Blueprint created and registered on instance/settings.toml. Restart your app if running.')


@manage.command()
def plug_database():
    '''Adds a basic set of models to project and let it ready for migrations. At the start it will be set to flask_sqlalchemy as ORM and sqlite as database, as well as use flask_migrate as migration tool.'''
    # setup tasks
    settings = toml.load(os.path.join(
        os.getcwd(), 'instance', 'settings.toml'))
    if '{{name}}.ext.database:init_app' in settings['default']['EXTENSIONS']:
        click.echo('Database seems to be already plugged.')
        exit(0)

    # add and install requirements
    cmd = ''
    if os.name == 'posix':
        cmd = f'pip install flask-sqlalchemy flask-migrate;'
    elif os.name == 'nt':
        cmd = f'pip install flask-sqlalchemy flask-migrate;'
    subprocess.call(cmd, shell=True)
    click.echo("Remember to add flask-sqlalchemy and flask-migrate to the list of dependencies")
    click.pause()
    # project.ext.database
    with open(os.path.join(os.getcwd(), '{{name}}', 'ext', 'database.py'), 'w') as db_module:
        db_template = get_template('database.pyt')
        db_module.write(db_template.render(name='{{name}}'))
    # models.py (basic example)
    with open(os.path.join(os.getcwd(), '{{name}}', 'models.py'), 'w') as models_file:
        mod_template = get_template('models.pyt')
        models_file.write(mod_template.render(project='{{name}}'))
    # settings.toml
    settings = toml.load(os.path.join(
        os.getcwd(), 'instance', 'settings.toml'))
    settings['default']['EXTENSIONS'].append(
        '{{name}}.ext.database:init_app')
    settings['default']['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(
        os.getcwd(), 'instance', 'db.sqlite3')
    with open(os.path.join(os.getcwd(), 'instance', 'settings.toml'), 'w') as f:
        f.write(toml.dumps(settings))

    click.echo('Creating migrations directory')
    cmd = ''
    if os.name == 'posix':
        cmd = f'export FLASK_APP={{name}}.app; export FLASK_ENV=development; flask db init'
        subprocess.run(cmd, shell=True)
    elif os.name == 'nt':
        cmd = f'$env:FLASK_APP = "{{name}}.app"; $env:FLASK_ENV = "development"; flask db init'
        subprocess.run(['powershell', '-Command', cmd])
    
    click.echo("Everything is setted up. Please, before doing migrations, remember your models isn't connected to any entrypoint of your app.")


@manage.command()
@click.argument('message')
def db_migrate(message):
    settings = toml.load(os.path.join(
        os.getcwd(), 'instance', 'settings.toml'))
    if '{{name}}.ext.database:init_app' not in settings['default']['EXTENSIONS']:
        click.echo('No database plugged.')
        exit(0)
    from flask_migrate import migrate
    from {{name}}.app import create_app
    app = create_app()
    with app.app_context():
        migrate(message=message)


@manage.command()
def db_upgrade():
    settings = toml.load(os.path.join(
        os.getcwd(), 'instance', 'settings.toml'))
    if '{{name}}.ext.database:init_app' not in settings['default']['EXTENSIONS']:
        click.echo('No database plugged.')
        exit(0)
    from flask_migrate import upgrade
    from {{name}}.app import create_app
    app = create_app()
    with app.app_context():
        upgrade()


@manage.command()
def db_downgrade():
    settings = toml.load(os.path.join(
        os.getcwd(), 'instance', 'settings.toml'))
    if '{{name}}.ext.database:init_app' not in settings['default']['EXTENSIONS']:
        click.echo('No database plugged.')
        exit(0)
    from flask_migrate import downgrade
    from {{name}}.app import create_app
    app = create_app()
    with app.app_context():
        downgrade()


if __name__ == '__main__':
    manage(prog_name='manage')
