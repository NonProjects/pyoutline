import click

from getpass import getpass
from traceback import format_exception
from sys import exit, argv as sys_argv
from subprocess import Popen
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
    '--offset', '-o', type=int, default=1,
    help='Key file offset. We will start from this Key'
)
@click.option(
    '--random-port', '-r', is_flag=True,
    help='Will set random listener port, otherwise 25250'
)
@click.option(
    '--port', '-p', type=click.IntRange(49152,65535),
    help='Listener proxy port'
)
def client(outline_key, random_port, port, offset):
    """Will start Outline Proxy from Key / file with Keys"""

    keys = Path(outline_key)

    if keys.exists():
        keys = open(keys).read().strip().split('\n')
        keys = [key.strip() for key in keys]
    else:
        keys = [outline_key]
    
    if offset < 1 or offset > len(keys):
        click.echo(red('Invalid offset specified!'))

    enter, next_ = blue('ENTER'), blue('NEXT')
    ctrld, previ = magenta('CTRL+D'), magenta('PREVIOUS')
    ctrlc, exit_ = cyan('CTRL+C'), cyan('EXIT')
    
    if len(keys) > 1:
        click.echo(
            f"""\n@ Press {enter}  to select {next_} Key\n"""
            f"""@ Press {ctrld} to select {previ} Key\n"""
            f"""@ Press {ctrlc} to close connection and {exit_}"""
        )
    else:
        click.echo(f"\n@ Press {ctrlc} to close connection and {exit_}")

    current_key_position = 0 if not offset else offset - 1

    while True:
        if current_key_position + 1 > len(keys):
            current_key_position -= 1

        key_num = current_key_position + 1
        key = keys[current_key_position]

        click.echo(yellow(f'\r\nTrying [#{key_num}] ({key[:32]}...)'))
        try:
            ok = OutlineKey(key)

            if not ok.is_alive:
                click.echo(red(f'Outline Key [#{key_num}] is offline or not valid.\n'))
                continue
            else:
                click.echo(green(f'Outline Key [#{key_num}] is OK! Connecting...\n'))

            ss = ok.shadowsocks(random_port=random_port, port=port)
            try:
                ss_process = Popen(ss.replace('"','').split(' '))
                if len(keys) == 1:
                    ss_process.wait()
                    exit()
                else:
                    getpass(prompt=''); ss_process.terminate()
                    print('\x1b[1A', end='') # This will move cursor up
                    current_key_position += 1; continue
            except EOFError:
                if current_key_position > 0:
                    current_key_position -= 1

                ss_process.terminate()
                continue

        except ValueError:
            click.echo(red('Invalid Key specified!'))
        except FileNotFoundError:
            ss = ss.replace('ss-local', 'sslocal')
            call(ss.replace('"','').split(' '))
        except Exception as e:
            click.echo(red(e))
            exit(1)
    
if __name__ == '__main__':
    safe_cli()
