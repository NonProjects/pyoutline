# PyOutline: CLI app to start Outline VPN keys

With **PyOutline** you can easily run [ShadowSocks proxy](https://en.wikipedia.org/wiki/Shadowsocks) from the [**Outline keys**](https://getoutline.me/access-keys/).

## Installation

**PIP** ([PyPI](https://pypi.org/project/pyoutline/))
```
pip install pyoutline
```
**With clone from GitHub**
```
git clone https://github.com/NonProjects/pyoutline
pip install ./pyoutline
```
## Requirements

You will need ShadowSocks. Install it via PIP:
```
pip install https://github.com/shadowsocks/shadowsocks/archive/5ff694b2c2978b432918dea6ac104706b25cbf48.zip
```
You can also install it via your packet manager if you're on Linux:
```
apt install shadowsocks-libev # Debian 11
```
## Usage

The "*How to use*" is pretty simple:
```
pyoutline client -k "ss://YWVzLTI1Ni1nY206Y2RCSURWNDJEQ3duZklO@ak1344.free.www.outline.network:8118"
```
If you want to transform Outline Key into the ss-local string:
```
pyoutline to-ss -k "ss://YWVzLTI1Ni1nY206Y2RCSURWNDJEQ3duZklO@ak1344.free.www.outline.network:8118"
# ^ ss-local -s "ak1344.free.www.outline.network" -p 8118 -k "cdBIDV42DCwnfIN" -m "aes-256-gcm" -l 53735
```
Set your own port or ask system to set the free one
```
pyoutline client -p 50000 # Set port 50000, script will ask you for Key
pyoutline client -r # Get a random port, script will ask you for Key
```
You can also specify keys from the file. First working Key will be used:
```
pyoutline client -k /home/user/outline_keys.txt
```
The insides of the file with keys should be placed like this:
```
ss://YWVzLTI1Ni1nY206Y2RCSURWNDJEQ3duZklO@ak1344.free.www.outline.network:8118
ss://YWVzLTI1Ni1nY206VEV6amZBWXEySWp0dW9T@ak1343.free.www.outline.network:6679
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpHIXlCd1BXSDNWYW8=@ak1338.free.www.outline.network:810
```
