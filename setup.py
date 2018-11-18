from setuptools import setup, find_packages

setup(
    name = "yaml_tools_project",
    version = "0.1",
    packages = find_packages(),
    author = "Petros Makris",
    install_requires = [
        'cherrypy==18.0.1',
        'jinja2==2.10',
        'requests==2.20.1',
        'mysql-connector==2.1.6',
        'simplejson==3.16.0',

        # https://google-auth.readthedocs.io/en/latest/index.html
        'google-auth==1.6.1'
    ],

    entry_points = {
        'console_scripts': [
            'serve = social.app:app',
            'users = social.users:app',
        ]
    }
)

