import click

from traceback import format_exception
from sys import exit, argv as sys_argv
from subprocess import call
from pathlib import Path

from tools import get_free_port, OutlineKey

COLORS = [
    'red','cyan','blue','green',
    'white','yellow','magenta',
    'bright_black','bright_red'
]
for color in COLORS:
    # No problem with using exec function here
    exec(f'{color} = lambda t: click.style(t, fg="{color}", bold=True)')

@click.group()
def cli():
   pass

def safe_cli():
    try:
        cli()
    except Exception as e:
        e = ''.join(format_exception(
            etype = None, 
            value = e, 
            tb = e.__traceback__
        ))
        click.echo(red(e))
        exit(1)

@cli.command()
@click.option(
    '--outline-key', '-k', required=True, prompt=True,
    help='Outline VPN access Key (ss://...), can be path to file with keys'
)
@click.option(
    '--random-port', '-r', is_flag=True,
    help='Will set random listener port, otherwise 53735'
)
@click.option(
    '--port', '-p', type=click.IntRange(49152,65535),
    help='Listener proxy port'
)
def to_shadowsocks(outline_key, random_port, port):
    """Will transform Outline Proxy Key/file with Keys to ShadowSocks"""

    keys = Path(outline_key)

    if keys.exists():
        keys = open(keys).read().strip().split('\n')
        keys = [key.strip() for key in keys]
    else:
        keys = [outline_key]
    
    for key in keys:
        try:
            ok = OutlineKey(key)
            ss = ok.shadowsocks(random_port=random_port, port=port)
            click.echo(bright_black(ss + '\n'))
        except ValueError:
            click.echo(red('Invalid Key specified!'))

@cli.command()
@click.option(
    '--outline-key', '-k', required=True, prompt=True,
    help='Outline VPN access Key (ss://...), can be path to file with keys'
)
@click.option(
    '--random-port', '-r', is_flag=True,
    help='Will set random listener port, otherwise 25250'
)
@click.option(
    '--port', '-p', type=click.IntRange(49152,65535),
    help='Listener proxy port'
)
def client(outline_key, random_port, port):
    """Will start Outline Proxy from Key / file with Keys"""

    keys = Path(outline_key)

    if keys.exists():
        keys = open(keys).read().strip().split('\n')
        keys = [key.strip() for key in keys]
    else:
        keys = [outline_key]
    
    for key in keys:
        click.echo(yellow(f'Trying {key[:32]}...'))

        try:
            ok = OutlineKey(key)

            if not ok.is_alive:
                click.echo(red(f'{key[:32]}... is offline or not valid.\n'))
                continue
            else:
                click.echo(green(f'{key[:32]}... is OK! Connecting...\n'))

            ss = ok.shadowsocks(random_port=random_port, port=port)
            call(ss.replace('"','').split(' '))

        except ValueError:
            click.echo(red('Invalid Key specified!'))
        except FileNotFoundError:
            ss = ss.replace('ss-local', 'sslocal')
            call(ss.replace('"','').split(' '))
        except Exception as e:
            click.echo(red(e))
            exit(1)
    
    if len(keys) > 1:
        click.echo(red('No working keys found.'))

    exit(1)

if __name__ == '__main__':
    safe_cli()
