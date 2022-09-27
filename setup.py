from setuptools import setup

# github.com/shadowsocks/shadowsocks commit from master. For safety.
ss_commit = '5ff694b2c2978b432918dea6ac104706b25cbf48'
ss_archive = f'https://github.com/shadowsocks/shadowsocks/archive/{ss_commit}.zip'

setup(
    name="pyoutline",
    version='0.3',
    license='MIT',
    description = 'A simple CLI app to start Outline Proxy',
    long_description = open('README.md').read(),
    long_description_content_type='text/markdown',
    author = 'NonProjects',
    author_email = 'thenonproton@pm.me',
    url = 'https://github.com/NonProjects/pyoutline',
    download_url = 'https://github.com/NonProjects/pyoutline/archive/refs/tags/v0.3.tar.gz',
    py_modules=['pyoutline', 'pyoutline_tools'],
    install_requires=[
        'click', f'shadowsocks @ {ss_archive}'
    ],
    entry_points='''
        [console_scripts]
        pyoutline=pyoutline:safe_cli
    ''',
)
