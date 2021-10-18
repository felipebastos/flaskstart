"""Copyright 2021 Felipe Bastos Nunes

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
from jinja2 import Environment, PackageLoader, select_autoescape, Template

env = Environment(
    loader=PackageLoader('flaskstarter', 'templates'),
    autoescape=select_autoescape('pyt', 'htmlt', 'tomlt')
)

def get_template(name : str) -> Template:
    """Retrieves and return the specified template.

    Args:
        name (str): Template's name

    Returns:
        Template: A Jinja2 Template object.
    """
    return env.get_template(name)
