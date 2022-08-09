from socket import socket, gaierror
from base64 import urlsafe_b64decode

def get_free_port():
    """This func will return free port"""
    with socket() as s:
        s.bind(('', 0))
        return s.getsockname()[1]

class OutlineKey:
    def __init__(self, key: str):
        self.key = key
        try:
            pass_enc = urlsafe_b64decode(key.split('ss://')[1].split('@')[0])
            self.enc, self.password = pass_enc.decode().split(':')

            server_port = key.split('@')[1].split('#')[0].split(':')
            self.server, self.port = server_port
        except Exception as e:
            raise ValueError(f'Invalid Key! {e}') from None

    def __repr__(self) -> str:
        return f'OutlineKey({self.key}) # at {id(self)}'

    def __str__(self) -> str:
        return (
            f"""Key: {self.key}\nEnc: {self.enc}\nPassword: {self.password}\n"""
            f"""Server: {self.server}\nPort: {self.port}"""
        )
    def shadowsocks(self, random_port: bool=False, port: int=None) -> str:
        port = get_free_port() if random_port else (port if port else 53735)
        return (
            f"""ss-local -s "{self.server}" -p {self.port} -k """
            f"""\"{self.password}" -m "{self.enc}" -l {port}"""
        )
    @property
    def is_alive(self):
        """Will return True if addr:port is accessible"""
        with socket() as s:
            try:
                s.bind((self.server, int(self.port)))
            except gaierror:
                return False
            except OSError:
                return True
            except:
                return False
