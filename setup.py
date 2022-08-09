from setuptools import setup

setup(
    name="pyoutline",
    version='0.2',
    license='MIT',
    description = 'A simple CLI app to start Outline Proxy',
    long_description = open('README.md').read(),
    long_description_content_type='text/markdown',
    author = 'NonProjects',
    author_email = 'thenonproton@pm.me',
    url = 'https://github.com/NonProjects/pyoutline',
    download_url = 'https://github.com/NonProjects/pyoutline/archive/refs/tags/v0.2.tar.gz',
    py_modules=['pyoutline', 'tools'],
    install_requires=['click'],
    entry_points='''
        [console_scripts]
        pyoutline=pyoutline:safe_cli
    ''',
)
