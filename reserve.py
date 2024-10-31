from aiohttp import web
from sys import platform
import os, hashlib, aiohttp, curses, threading

recieved = 0
transferred = 0
uncached = 0

art = r"""
@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@
#@@######################################@@%
#@%========---------------------=========%@#
#@%==========-=--------------============%@#
#@%========---------------------=========%@#                   Reserve v1
*@%=======*@@@@@@@@=----=@@@@@@@@*=======%@#            Created by jarvisdevil
*@%======-*@-::::*@=----=@*:::::@*=======%@#    https://github.com/jarvisdevlin/Reserve
*@%=======*@-::::*@=--:-=@*:::::@*=======%@#
#@%=======*@-::::*@=----=@*:::::@*=======%@#
*@%======-*@@@@@@@@=---:=@@@@@@@@*=======%@#
*@%=======-------------------------======%@#
*@@==========-----------------===========%@#
*@@=====@@@@@@@@@@@@@@@@@@@@@@@@@@@@=====%@#      Reserve is serving via 0.0.0.0:19997
*@@=====@@========================@@=====%@#
*@@+====@@::::::::::::::::::::::::@@====+@@#
*@@++==+@@=-----------------------@@+==++@@#
*@@+++==@@@@@@@@@@@@@@@@@@@@@@@@@@@@==+++@@#
*@@++++========-------------=========++++@@#
*@@*++++++=======================+++++++*@@*
*@@***++++++++===============+++++++++***@@*
*@@******++++++++++++++++++++++++++******@@#
*@@*********++++++++++++++++++++*********@@#
*@@*****************++++**+**************@@#
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""

def screw_you_curses():
    if platform == "linux" or platform == "linux2":
        os.system('printf "\e[8;45;160t"')
    elif platform == "darwin":
        os.system('printf "\e[8;45;160t"')
    elif platform == "win32":
        os.system('mode con: cols=160 lines=45')
    else:
        print("oof")

def display(stdscr):
    screw_you_curses()
    global art
    lines = art.splitlines()
    
    while True:
        stdscr.clear()

        for i, line in enumerate(lines):
            stdscr.addstr(i, 0, line)

        counter = len(lines)
        stdscr.addstr(counter + 1, 0, f"Data Received: {recieved} bytes")
        stdscr.addstr(counter + 2, 0, f"Data Transferred: {transferred} bytes")
        stdscr.addstr(counter + 3, 0, f"Uncached Responses: {uncached}")

        stdscr.refresh()
        curses.napms(500)

async def req(request):
    global recieved, transferred, uncached

    path = request.path.strip('/')
    data = await request.post()
    recieved += sum(len(k) + len(v) for k, v in data.items())

    os.makedirs(f'./reserve/{path}', exist_ok=True)
    hash = hashlib.sha256(str(data).encode()).hexdigest()
    cache = os.path.join(f'./reserve/{path}', f'{hash}.txt')

    if os.path.exists(cache):
        with open(cache, 'r') as f:
            return web.Response(text=f.read(), status=200)

    async with aiohttp.ClientSession() as session:
        headers = {"User-Agent": "", "Content-Type": "application/x-www-form-urlencoded"}

        async with session.post(f'http://www.boomlings.com/{path}', headers=headers, data=data) as resp:
            r = await resp.text()
            transferred += len(r)
            uncached += 1

            with open(cache, 'w') as f:
                f.write(r)

            return web.Response(text=r, status=resp.status)

def main():
    threading.Thread(target=curses.wrapper, args=(display,), daemon=True).start()
    app = web.Application()
    app.router.add_post('/{tail:.*}', req)
    web.run_app(app, port=19997)

if __name__ == "__main__":
    main()
