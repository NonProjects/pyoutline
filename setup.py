from setuptools import setup

setup(
    name="pyoutline",
    version='0.3.1',
    license='MIT',
    description = 'A simple CLI app to run Outline VPN',
    long_description = open('README.md').read(),
    long_description_content_type='text/markdown',
    author = 'NonProjects',
    author_email = 'thenonproton@pm.me',
    url = 'https://github.com/NonProjects/pyoutline',
    download_url = 'https://github.com/NonProjects/pyoutline/archive/refs/tags/v0.3.1.tar.gz',
    py_modules=['pyoutline', 'pyoutline_tools'],
    install_requires=['click'],
    entry_points='''
        [console_scripts]
        pyoutline=pyoutline:safe_cli
    ''',
)
