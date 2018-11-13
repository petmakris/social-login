from setuptools import setup, find_packages

setup(
    name = "yaml_tools_project",
    version = "0.1",
    packages = find_packages(),
    author = "Petros Makris",
    install_requires = [
        'cherrypy==18.0.1',
        'jinja2==2.10',
        'pickledb==0.8.1',
        'requests==2.20.1'
    ],

    entry_points = {
        'console_scripts': [
            'serve = social.app:app',
        ]
    }
)

