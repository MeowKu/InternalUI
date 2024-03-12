
import os, sys, ast, json, time, random, base64, subprocess, requests, shutil, uuid, threading
from itertools import cycle
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from __future__ import print_function

import time
import datetime
from colorclass import Color, Windows
from terminaltables import SingleTable
import argparse
import requests
import sys
import signal

import PySimpleGUI as sg

import os, sys, time, random, asyncio, json , logging, base64; from datetime import datetime; from typing import Dict, Tuple

try:
    import psutil; from aiohttp import ClientSession; from tasksio import TaskPool; from rich.table import Table; from rich.console import Console; from rich.highlighter import ReprHighlighter
except ImportError:
    os.system("pip install aiohttp")
    os.system("pip install tasksio")
    os.system("pip install psutil")
    os.system("pip install rich")
    import psutil; from tasksio import TaskPool; from aiohttp import ClientSession; from rich.table import Table; from rich.console import Console; from rich.highlighter import ReprHighlighter


mode = sys.argv[1]
thread_count = 100

token_list = "token.txt"
use_proxies = ""
proxy_type = ""
proxy_list = ""
proxy_auth = ""
proxy_user = ""
proxy_pass = ""
endpointname = ""

if endpointname == "stable":
    endpoint = ""
else:
    endpoint = endpointname + "."


executor = ThreadPoolExecutor(max_workers=int(thread_count))
tokenlist = open("tokens/"+token_list).read().splitlines()

def select_random_proxy():
    proxylist = open(proxy_list).read().splitlines()
    return random.choice(proxylist)

def setup_request(token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36'
    }
    if use_proxies == 1:
        proxy_origin = select_random_proxy()
        if proxy_auth == 1:
            proxies = {
                'http': f'{proxy_type}://{proxy_user}:{proxy_pass}@{proxy_origin}',
                'https': f'{proxy_type}://{proxy_user}:{proxy_pass}@{proxy_origin}'
            }
        else:
            proxies = {
                'http': f'{proxy_type}://{proxy_origin}',
                'https': f'{proxy_type}://{proxy_origin}'
            }
    else:
        proxies = {
            "http": None,
            "https": None,
        }
    return headers, proxies

def request_new_proxy():
    proxy_origin = select_random_proxy()
    if proxy_auth == 1:
        proxies = {
            'http': f'{proxy_type}://{proxy_user}:{proxy_pass}@{proxy_origin}',
            'https': f'{proxy_type}://{proxy_user}:{proxy_pass}@{proxy_origin}'
        }
    else:
        proxies = {
            'http': f'{proxy_type}://{proxy_origin}',
            'https': f'{proxy_type}://{proxy_origin}'
        }
    return proxies

def asciigen(length):
    asc = ''
    for x in range(int(length)):
        num = random.randrange(13000)
        asc = asc + chr(num)
    return asc

def get_mime(data):
    if data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
        return 'image/png'
    elif data[6:10] in (b'JFIF', b'Exif'):
        return 'image/jpeg'
    elif data.startswith((b'\x47\x49\x46\x38\x37\x61', b'\x47\x49\x46\x38\x39\x61')):
        return 'image/gif'
    elif data.startswith(b'RIFF') and data[8:12] == b'WEBP':
        return 'image/webp'

def bytes_to_base64_data(data):
    fmt = 'data:{mime};base64,{data}'
    mime = get_mime(data)
    b64 = base64.b64encode(data).decode('ascii')
    return fmt.format(mime=mime, data=b64)

def write_error(token, message, code):
    print(f"Token {token[:24]}... Error: {message} (Code {code})")

#
    


parser = argparse.ArgumentParser(description="MINING POOL HUB Information Gatherer 2018 Orhan Gazi Hafif WTFPL Licence")
parser.add_argument('-a', metavar='api_key', required=True, help='API KEY from \'Edit Account\' page.\n')
parser.add_argument('-i', metavar='id', help='USER ID from \'Edit Account\' page\n')
parser.add_argument('-c', metavar='crypto_currency', default='BTC', help='Which exchange currency to display total in'
                                                                         ' (default BTC).\n')
parser.add_argument('-f', metavar='fiat_currency', help=' Not needed, extra column for displaying other fiat currency '
                                                        'total.\n')
parser.add_argument('-n', metavar='non_stop', help=' Not needed, if equals \'YES\', run the application continuously, '
                                                   'default, in every 2 minutes.\n')
parser.add_argument('-d', metavar='dashboard_coin', help='For displaying that coin\'s dashboard info, name must be same'
                                                         ' at website, for example, for zcash.miningpoolhub.org, it '
                                                         'must be zcash.\n')
parser.add_argument('-d2', metavar='dashboard_coin2', help='For displaying that coin\'s dashboard info, name must be same'
                                                         ' at website, for example, for zcash.miningpoolhub.org, it '
                                                         'must be zcash.\n')
parser.add_argument('-d3', metavar='dashboard_coin3', help='For displaying that coin\'s dashboard info, name must be same'
                                                         ' at website, for example, for zcash.miningpoolhub.org, it '
                                                         'must be zcash.\n')
parser.add_argument('-d4', metavar='dashboard_coin4', help='For displaying that coin\'s dashboard info, name must be same'
                                                         ' at website, for example, for zcash.miningpoolhub.org, it '
                                                         'must be zcash.\n')
parser.add_argument('-r', metavar='reload_time', default='120', help='Reload time in seconds. Must be between 10 and '
                                                                     '1800, (default 120)')
args = parser.parse_args()

def handler(signum, frame):
    print (Color('\n{autogreen}Bye bye!{/autogreen}'))
    exit()

signal.signal(signal.SIGINT, handler)

class MphInfo:
    def __init__(self, api_key, id, currency, fiat_currency, dcoin, d2coin, d3coin, d4coin, reload_time):
        Windows.enable(auto_colors=True, reset_atexit=True)  # For just Windows
        self.key_            = api_key
        self.id_             = id
        self.cur_            = currency
        self.fcur_           = fiat_currency
        self.coin_           = dcoin
        self.coin2_          = d2coin
        self.coin3_          = d3coin
        self.coin4_          = d4coin
        self.reload_time_    = int(reload_time)
        self.crypto_symbols_ = {}

        self.btc_ = 0.0 # 1 BTC in USD

        if self.reload_time_ > 1800 or int(reload_time) < 15:
            print('reload_time argument must be between 10 and 1800. For more info, run $ python3 display.py --help' )
            exit()


        self.setSymbols()

        #print(Color('{autoyellow}benafleck{/autoyellow}')) # lol ;)

        self.time_str_ = 'Hello world, What time is it?'

        self.dot_count_ = 0

        self.other_cur = False
        if args.f != None:
            self.other_cur = True

        self.dashb_    = False
        self.dashb2_    = False
        self.dashb3_    = False
        self.dashb4_    = False
        if args.d != None:
            self.dashb_ = True
        if args.d2 != None:
            self.dashb2_ = True
        if args.d3 != None:
            self.dashb3_ = True
        if args.d4 != None:
            self.dashb4_ = True

        self.balances_table_data_ = []
        self.balances_table_     = SingleTable([])

        if self.dashb_:
            self.dashb_table_data_ = []
            self.dashb_table_      = SingleTable([])

        if self.dashb2_:
            self.dashb2_table_data_ = []
            self.dashb2_table_      = SingleTable([])

        if self.dashb3_:
            self.dashb3_table_data_ = []
            self.dashb3_table_      = SingleTable([])

        if self.dashb4_:
            self.dashb4_table_data_ = []
            self.dashb4_table_      = SingleTable([])

        self.printDotInfo('Getting values and converting to currencies')
        self.getStats()
        self.printTables()

        if args.n == 'YES':
            self.displayNonStop()
        else:
            exit()

    def displayNonStop(self):
        while True:
            time.sleep(self.reload_time_)
            self.clearLastLine()
            self.printDotInfo(str(Color(self.time_str_)))
            self.getStats()
            self.printTables()

    def clearScreen(self):
        print("\033[H\033[J")

    def clearLastLine(self):
        sys.stdout.write("\033[F")  # back to previous line
        #sys.stdout.write("\033[K")  # Clear to the end of line

    def strI0(self, value): # returns integer's str or '0.0'
        try:
            return str(int(value))
        except:
            return '0'

    def strF0(self, value, perc=None): # returns float's str or '0.0'
        try:
            if perc == None:
                return str(float(value))
            else:
                return str(perc % float(value))
        except:
            return '0.0'

    def printTables(self):
        self.clearScreen()
        self.makeTables()
        print(self.balances_table_.table)
        if self.dashb_:
            print(self.dashb_table_.table)
        if self.dashb2_:
            print(self.dashb2_table_.table)
        if self.dashb3_:
            print(self.dashb3_table_.table)
        if self.dashb4_:
            print(self.dashb4_table_.table)

        self.time_str_  = ' {autocyan}BTC{/autocyan} ${autogreen}' + str("%.2f" % self.btc_)  + '{/autogreen}'

        self.time_str_ += time.strftime(' Last update: {autoyellow}%d/%m/%Y{/autoyellow} {autocyan}%H:%M:%S {/autocyan}',
                                       datetime.datetime.now().timetuple())
        print(Color(self.time_str_))

    def makeTables(self):
        self.balances_table_ = SingleTable(self.balances_table_data_)
        self.balances_table_.inner_heading_row_border = False
        self.balances_table_.inner_row_border = True
        self.balances_table_.justify_columns = {0: 'center', 1: 'center', 2: 'center', 3: 'center'}

        if self.dashb_:
            self.dashb_table_ = self.makeDashbTable(self.dashb_table_data_)

        if self.dashb2_:
            self.dashb2_table_ = self.makeDashbTable(self.dashb2_table_data_)

        if self.dashb3_:
            self.dashb3_table_ = self.makeDashbTable(self.dashb3_table_data_)

        if self.dashb4_:
            self.dashb4_table_ = self.makeDashbTable(self.dashb3_table_data_)

    def makeDashbTable(self, data):
        table = SingleTable(data)
        table.inner_heading_row_border = False
        table.inner_row_border = True
        table.justify_columns = {0: 'center', 1: 'center'}
        return table

    def getMphJsonDict(self, method, coin=None, id=None):
        url = "https://{}miningpoolhub.com/index.php?page=api&action={}&api_key={}&id={}"

        if coin == None and id == None:
            url=url.format("", method, self.key_, "")

        elif coin != None and id != None:
            url=url.format(coin + '.', method, self.key_, id)

        response = requests.get(url, timeout=10)
        json_dict = {}
        try:
            json_dict = response.json()

        except ValueError:
            print()
            print()
            print(Color('{autored}Website didn\'t response with a valid json:{/autored}'))
            print(response.content)
            exit()

        return json_dict

    def getValueInOtherCurrency(self, curency, amount, other_currency, use_dot=None):
        url = "https://min-api.cryptocompare.com/data/price?fsym={}&tsyms={}"
        if curency.upper() == other_currency.upper(): # No need to convert
            return amount
        url = url.format(curency.upper(), other_currency.upper())
        response = requests.get(url, timeout=10)
        json_dict = response.json()
        price = json_dict[other_currency.upper()]
        value = float(price) * float(amount)
        if use_dot != None:
            self.printDotInfo()
        return value

    def printDotInfo(self, info=None):
        """ ⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏ """
        if info == None:
            if self.dot_count_ == 0:
                self.writeAndFlushAndCount('\b\b\b ⠙ \b ', True)
            elif self.dot_count_ == 1:
                self.writeAndFlushAndCount('\b\b\b ⠹ \b ', True)
            elif self.dot_count_ == 2:
                self.writeAndFlushAndCount('\b\b\b ⠹ \b ', True)
            elif self.dot_count_ == 3:
                self.writeAndFlushAndCount('\b\b\b ⠸ \b ', True)
            elif self.dot_count_ == 4:
                self.writeAndFlushAndCount('\b\b\b ⠼ \b ', True)
            elif self.dot_count_ == 5:
                self.writeAndFlushAndCount('\b\b\b ⠴ \b ', True)
            elif self.dot_count_ == 6:
                self.writeAndFlushAndCount('\b\b\b ⠦ \b ', True)
            elif self.dot_count_ == 7:
                self.writeAndFlushAndCount('\b\b\b ⠧ \b ', True)
            elif self.dot_count_ == 8:
                self.writeAndFlushAndCount('\b\b\b ⠇ \b ', True)
            elif self.dot_count_ == 9:
                self.writeAndFlushAndCount('\b\b\b ⠏ \b ', True)
            else:
                self.writeAndFlushAndCount('\b\b\b ⠋ \b ')
        else:
            sys.stdout.write(info + ' ⠋ \b ')

    def writeAndFlushAndCount(self, str, plus_one = False):
        if plus_one:
            sys.stdout.write(str)
            sys.stdout.flush()
            self.dot_count_ += 1
        else:
            sys.stdout.write(str)
            sys.stdout.flush()
            self.dot_count_ = 0


    def getStats(self):
        sign = ""
        if self.other_cur:
            if self.fcur_ == 'USD':
                self.other_cur = False
            if self.fcur_ == 'TRY':
                sign = '₺'
            elif self.fcur_ == 'EUR':
                sign = '€'
            elif self.fcur_ == 'AZN':
                sign = '₼'
            elif self.fcur_ == 'GBP':
                sign = '£'
            elif self.fcur_ == 'CNY' or self.fcur_ == 'JPY' :
                sign = '¥'
            elif self.fcur_ == 'AUD':
                sign = '$'
            elif self.fcur_ == 'ALL':
                sign = 'L'
            else:
                sign = self.fcur_

        if self.cur_ == 'BTC':
            fave_crypto_sign = 'Ƀ'
        elif self.cur_ == 'ETH':
            fave_crypto_sign = '⧫'
        else:
            fave_crypto_sign = self.cur_

        balances_dict = {}
        balances_dict  = self.getMphJsonDict("getuserallbalances")

        coins = {}
        total_fave_crypto = 0.0

        for coin in balances_dict["getuserallbalances"]["data"]:
            symbol = self.crypto_symbols_[coin["coin"]]
            balance = sum([
                coin["confirmed"],
                coin["unconfirmed"]
             ])
            balance_ex = sum([
                coin["ae_confirmed"],
                coin["ae_unconfirmed"],
                coin["exchange"]
             ])
            coins[symbol + "_balance"] = balance
            coins[symbol + "_exchange"] = balance_ex
            coin_total_balance = balance + balance_ex

            total_fave_crypto += self.getValueInOtherCurrency(symbol, coin_total_balance, self.cur_, True)
            coins[symbol + "_fiat_usd"] = self.getValueInOtherCurrency(symbol, balance, 'USD', True)
            if self.other_cur:
                coins[symbol + "_fiat_my_cur"] = self.getValueInOtherCurrency(symbol, balance, self.fcur_, True)


        total_usd = self.getValueInOtherCurrency(self.cur_, total_fave_crypto, 'USD', True)

        self.balances_table_data_ = []

        title =[
            Color('{autoyellow}Total Balance{/autoyellow}\n'+ fave_crypto_sign +'{autocyan}'
                  + str("%.6f" % total_fave_crypto) + '{/autocyan}'),
            Color('{autoyellow}Confirmed+{/autoyellow}\n{autoyellow}Unconfirmed{/autoyellow}'),
            Color('{autoyellow}Exchange+{/autoyellow}\n{autoyellow}AE_All{/autoyellow}'),
            Color('{autoyellow}Total{/autoyellow}\n${autocyan}' + str("%.2f" % total_usd) + '{/autocyan}'),
        ]

        if self.other_cur:
            total_fiat = self.getValueInOtherCurrency(self.cur_, total_fave_crypto, self.fcur_, True)
            title.append(Color('{autoyellow}Total{/autoyellow}\n' + sign + '{autocyan}'
                               + str("%.2f" % total_fiat) + '{/autocyan}'))

        self.balances_table_data_.append(title)

        for coin in balances_dict["getuserallbalances"]["data"]:
            symbol = self.crypto_symbols_[coin["coin"]]

            coin_line = [
                Color('{autocyan}' + coin["coin"].title() + '{/autocyan}'),
                Color( str("%.9f" % coins[symbol + '_balance'])),
                Color('{autored}' + str("%.6f" % coins[symbol + '_exchange']) + '{/autored}'),
                Color('${autogreen}' + str("%.2f" % coins[symbol + '_fiat_usd']) + '{/autogreen}'),
            ]

            if self.other_cur:
                coin_line.append(Color(sign + '{autogreen}'
                                       + str("%.2f" % coins[symbol + '_fiat_my_cur']) + '{/autogreen}'))

            self.balances_table_data_.append(coin_line)


        if self.dashb_:
            self.dashb_table_data_ = self.getDashbStats(self.coin_, sign)

        if self.dashb2_:
            self.dashb2_table_data_ = self.getDashbStats(self.coin2_, sign)

        if self.dashb3_:
            self.dashb3_table_data_ = self.getDashbStats(self.coin3_, sign)

        if self.dashb4_:
            self.dashb4_table_data_ = self.getDashbStats(self.coin4_, sign)

    def getDashbStats(self, coin, fave_sign):
        worker_dict    = self.getMphJsonDict("getuserworkers", coin, self.id_)
        dashboard_dict = self.getMphJsonDict("getdashboarddata", coin, self.id_)

        dashb_str = ''
        symbol       = self.crypto_symbols_[coin]
        last24       = float(dashboard_dict["getdashboarddata"]["data"]["recent_credits_24hours"]["amount"])
        last24_usd   = self.getValueInOtherCurrency(symbol, last24, 'USD', True)
        usd_val_coin = self.getValueInOtherCurrency(symbol,      1, 'USD', True)
        last24_btc   = self.getValueInOtherCurrency(symbol, last24, 'BTC', True)
        self.btc_    = self.getValueInOtherCurrency( 'BTC',      1, 'USD', True)
        dashb_str   += Color('{autoyellow}Last 24h {/autoyellow} {autocyan}' + str("%.8f" % last24)
                             + '{/autocyan} ' + symbol + '\n')
        dashb_str   += Color('{autoyellow}Est. 30d:{/autoyellow}\n'
                           + 'Ƀ{autocyan}'  + str("%.8f" % (30 * last24_btc)) + '{/autocyan}\n'
                           + '${autogreen}' + str("%.2f" % (30 * last24_usd)) + '{/autogreen}')

        if self.other_cur:
            last24_fiat = self.getValueInOtherCurrency(symbol, last24, self.fcur_, True)
            dashb_str+= Color('\n' + fave_sign + '{autogreen}' + str("%.2f" % (30 * last24_fiat)) + '{/autogreen}')

        table = []
        total_hashrate = 0.0
        workers_str = ''
        for worker in worker_dict["getuserworkers"]["data"]:
            workers_str += Color('{autoyellow}' + worker["username"] + '{/autoyellow} {autocyan}'
                                 + str("%.3f" % float(self.strF0(worker["hashrate"]))) + '{/autocyan} KH/s\n')
            total_hashrate += float(self.strF0(worker["hashrate"]))

        workers_str += Color('\n{autoyellow}TOTAL{/autoyellow} {autocyan}' + str("%.3f" % total_hashrate)
                             + '{/autocyan} KH/s\n')

        workers_str += Color('{autocyan}' + symbol + '{/autocyan} ${autogreen}'
                             + str("%.2f" % usd_val_coin) + '{/autogreen}')

        dashboard_info = [workers_str, dashb_str]
        table.append(dashboard_info)
        return table

    def setSymbols(self):
        self.crypto_symbols_ = {
            "adzcoin": "ADZ",
            "auroracoin": "AUR",
            "bitcoin": "BTC",
            "bitcoin-cash": "BCH",
            "bitcoin-gold": "BTG",
            "dash": "DSH",
            "digibyte": "DGB",
            "digibyte-groestl": "DGB",
            "digibyte-skein": "DGB",
            "digibyte-qubit": "DGB",
            "electroneum" : "ETN",
            "ethereum": "ETH",
            "ethereum-classic": "ETC",
            "expanse": "EXP",
            "feathercoin": "FTC",
            "gamecredits": "GAME",
            "geocoin": "GEO",
            "globalboosty": "BSTY",
            "groestlcoin": "GRS",
            "litecoin": "LTC",
            "maxcoin": "MAX",
            "monacoin": "MONA",
            "monero": "XMR",
            "musicoin": "MUSIC",
            "myriadcoin": "XMY",
            "myriadcoin-skein": "XMY",
            "myriadcoin-groestl": "XMY",
            "myriadcoin-yescrypt": "XMY",
            "sexcoin": "SXC",
            "siacoin": "SC",
            "startcoin": "START",
            "verge-scrypt": "XVG",
            "vertcoin": "VTC",
            "zcash": "ZEC",
            "zclassic": "ZCL",
            "zcoin": "XZC",
            "zencash": "ZEN"
        }

def main():
    m = MphInfo(args.a, args.i, args.c, args.f, args.d, args.d2, args.d3, args.d4, args.r)
#


logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;9m[\x1b[0m%(asctime)s\x1b[38;5;9m]\x1b[0m %(message)s\x1b[0m",
    datefmt="%H:%M:%S"
)


class Discord(object):

    def __init__(self):
        if os.name == 'nt':
            self.clear = lambda: os.system("cls")
        else:
            self.clear = lambda: os.system("clear")

        self.clear()
        self.tokens = []
        self.blacklisted_users = []
        self.users = []

        self.guild_name = None
        self.guild_id = None
        self.channel_id = None
        self.invite = None
        self.g = "\033[92m"
        self.red = "\x1b[38;5;9m"
        self.rst = "\x1b[0m"
        self.success = f"{self.g}[+]{self.rst} "
        self.err = f"{self.red}[{self.rst}!{self.red}]{self.rst} "
        self.opbracket = f"{self.red}({self.rst}"
        self.opbracket2 = f"{self.g}[{self.rst}"
        self.closebrckt = f"{self.red}){self.rst}"
        self.closebrckt2 = f"{self.g}]{self.rst}"
        self.question = "\x1b[38;5;9m[\x1b[0m?\x1b[38;5;9m]\x1b[0m "
        self.arrow = f" {self.red}->{self.rst} "
        with open("data/useragents.txt", encoding="utf-8") as f:
            self.useragents = [i.strip() for i in f]

        try:
            with open("data/tokens.json", "r") as file:
                tkns = json.load(file)
                if len(tkns) == 0:
                    logging.info(f"{self.err} Please insert your tokens {self.opbracket}tokens.json{self.closebrckt}")
                    sys.exit()
                for tkn in tkns:
                    self.tokens.append(tkn)

        except Exception:
            logging.info(f"{self.err} Please insert your tokens correctly in {self.opbracket}tokens.json{self.closebrckt}")
            sys.exit()
        try:
            with open("data/message.json", "r") as file:
                data = json.load(file)
            msg = data['content']
        except Exception:
            logging.info(
                f"{self.err} Please insert your message correctly in {self.opbracket}message.json{self.closebrckt}\nRead the wiki if you need examples")
            sys.exit()
        try:
            with open("data/config.json", "r") as file:
                config = json.load(file)
                for user in config["blacklisted_users"]:
                    self.blacklisted_users.append(str(user))
                self.send_embed = config["send_embed"]
                self.send_message = config["send_normal_message"]
                self.captcha_api_key = config["captcha_api_key"]
                self.captcha_submit_url = config["captcha_submit_url"]
                self.captcha_get_url = config["captcha_get_url"]
                self.discord_hcaptcha_id = "4c672d35-0701-42b2-88c3-78380b0db560"
                self.discord_captcha_referer = "https://discord.com/channels/@me"
                not_counter = 0
                if not self.send_embed:
                    not_counter += 1
                    self.embd = ""
                else:
                    logging.info(f"{self.g}[+]{self.rst} You can build your embed link at {self.red}https://embed.rauf.wtf/{self.rst},\nyou could also host your own html file so the url becomes shorter")
                    self.embd = input(f"{self.question}Embed Link{self.arrow}")
                    self.hide = input(f"{self.question}Should the Embed link be hidden? (This will increase the message lenght by 1k characters, but the link will be invisible)\n(y/n){self.arrow}")
                    if self.hide.lower() == "y":
                        self.embd = f"\n ||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||__ {self.embd}"
                    else:
                        self.embd = f"\n{self.embd}"
                if not self.send_message:
                    not_counter += 1
                    msg = ""
                if not_counter == 2:
                    logging.info(f"{self.err} You can\'t set send message and send embed to false {self.opbracket}config.json{self.closebrckt}.\nIf you do this you would try to send an empty message\nRead the wiki if you need help")
                    sys.exit()
        except Exception:
            logging.info(
                f"{self.err} Please insert the configuration stuff correctly {self.opbracket}config.json{self.closebrckt}.\nRead the wiki if you need help")
            sys.exit()
        with open("data/proxies.txt", encoding="utf-8") as f:
            self.proxies = [i.strip() for i in f]

        logging.info(
            f"{self.g}[+]{self.rst} Successfully loaded {self.red}%s{self.rst} token(s)\n" % (len(self.tokens)))
        self.mode = input(f"{self.question}Use Proxies? {self.opbracket}y/n{self.closebrckt}{self.arrow}")
        if self.mode.lower() == "y":
            self.use_proxies = True
            self.proxy_typee = input(f"{self.opbracket2}1{self.closebrckt2} http   | {self.opbracket2}2{self.closebrckt2} https\n{self.opbracket2}3{self.closebrckt2} socks4 | {self.opbracket2}4{self.closebrckt2} socks5\n{self.question}Proxy type{self.arrow}")
            if self.proxy_typee == "1":
                self.proxy_type = "http"
            elif self.proxy_typee == "2":
                self.proxy_type = "https"
            elif self.proxy_typee == "3":
                self.proxy_type = "socks4"
            elif self.proxy_typee == "4":
                self.proxy_type = "socks5"
            else: self.use_proxies = False
        else:
            self.use_proxies = False

        self.message = msg
        self.embed = self.embd
        try:
            self.delay = float(input(f"{self.question}Delay{self.arrow}"))
        except Exception:
            self.delay = 5
        try:
            self.ratelimit_delay = float(input(f"{self.question}Rate limit Delay{self.arrow}"))
        except Exception:
            self.ratelimit_delay = 300
        self.total_tokens = len(self.tokens)
        self.invalid_tokens_start = 0
        self.locked_tokens_start = 0
        self.locked_tokens_total = 0
        self.invalid_tokens_total = 0
        self.valid_tokens_start = 0
        self.valid_tokens_end = 0
        self.total_rate_limits = 0
        self.total_server_joins_success = 0
        self.total_server_joins_locked = 0
        self.total_server_joins_invalid = 0
        self.total_dms_success = 0
        self.total_dms_fail = 0
        self.invalid_token_dm = 0
        self.locked_token_dm = 0
        self.total_server_leave_success = 0
        self.total_server_leave_locked = 0
        self.total_server_leave_invalid = 0

        print()

    def stop(self):
        process = psutil.Process(os.getpid())
        process.terminate()

    def nonce(self):
        date = datetime.now()
        unixts = time.mktime(date.timetuple())
        return str((int(unixts) * 1000 - 1420070400000) * 4194304)

    # need to overwrite the whole json when updating, luckily the database won't be enormous
    def overwrite_json(self, content):
        self.json_db = open(f"data/token_profiles.json", "w")
        self.clean_json = json.dumps(content, indent=4, separators=(",", ": "))
        self.json_db.write(self.clean_json)
        self.json_db.close()
    def find_index_in_db(self, data_to_search, token_to_find):
        token_to_find = str(token_to_find)
        for i in range(len(data_to_search)):
            if data_to_search[i]["token"] == token_to_find:
                # token already exists in json file
                return int(i), "none"

        # in this case, the token isnt in the json file yet
        # so we automatically create him
        data_to_search.append({
            "token": str(token_to_find),
            "dcfduid": "none",
            "sdcfduid": "none",
            "fingerprint": "none",
            "super_property": "none",
            "user_agent": "none"
            # will overwrite all the "none" with needed things later
        })
        # now that the token profile is created, re-check and return int

        for i in range(len(data_to_search)):
            if data_to_search[i]["token"] == token_to_find:
                return i, data_to_search

    async def setup(self, token):
        if not os.path.exists("data/token_profiles.json"):
            creating_file = open(f"data/token_profiles.json", "w")
            creating_file.write("""{\n\t"tokens": []
}""")
            creating_file.close()

        token_profiles = open("data/token_profiles.json")
        json_content = json.load(token_profiles)
        token_index, new_data = self.find_index_in_db(json_content["tokens"], token)
        if new_data != "none":
            json_content["tokens"] = new_data
        json_token_content = json_content["tokens"][token_index]

        if json_token_content["dcfduid"] == "none":
            async with ClientSession() as client:
                async with client.get("https://discord.com/app") as response:
                    cookies = str(response.cookies)
                    dcfduid = cookies.split("dcfduid=")[1].split(";")[0]
                    sdcfduid = cookies.split("sdcfduid=")[1].split(";")[0]
                async with client.get("https://discordapp.com/api/v9/experiments") as finger:
                    jsonn = await finger.json()
                    fingerprint = jsonn["fingerprint"]
                # logging.info(f"{self.success}Obtained dcfduid cookie: {dcfduid}")
                # logging.info(f"{self.success}Obtained sdcfduid cookie: {sdcfduid}")
                # logging.info(f"{self.success}Obtained fingerprint: {fingerprint}")
                useragent = random.choice(self.useragents)
                if "Windows" in useragent:
                    device = "Windows"
                elif "Macintosh" in useragent:
                    device = "Mac OS X"
                elif "Linux" in useragent:
                    device = "Ubuntu"
                elif "iPad" in useragent:
                    device = "iPadOS"
                elif "iPhone" in useragent:
                    device = "iOS"
                elif "Android" in useragent:
                    device = "Android 11"
                elif "X11" in useragent:
                    device = "Unix"
                elif "iPod" in useragent:
                    device = "iOS"
                elif "PlayStation" in useragent:
                    device = "Orbis OS"
                else:
                    device = "hoeOS"

                decoded_superproperty = '{"os":"%s","browser":"Discord Client","release_channel":"stable","client_version":"0.0.264","os_version":"15.6.0","os_arch":"x64","system_locale":"en-US","client_build_number":108924,"client_event_source":null}' % (
                    device)
                message_bytes = decoded_superproperty.encode('ascii')
                base64_bytes = base64.b64encode(message_bytes)
                x_super_property = base64_bytes.decode('ascii')
                if json_token_content["dcfduid"] == "none":
                    json_token_content["dcfduid"] = dcfduid
                if json_token_content["sdcfduid"] == "none":
                    json_token_content["sdcfduid"] = sdcfduid
                if json_token_content["fingerprint"] == "none":
                    json_token_content["fingerprint"] = fingerprint
                if json_token_content["super_property"] == "none":
                    json_token_content["super_property"] = x_super_property
                if json_token_content["user_agent"] == "none":
                    json_token_content["user_agent"] = useragent
                json_content["tokens"][token_index] = json_token_content
                self.overwrite_json(json_content)

    async def headers(self, token):
        token_profiles = open("data/token_profiles.json")
        json_content = json.load(token_profiles)
        token_index, new_data = self.find_index_in_db(json_content["tokens"], token)
        if new_data != "none":
            json_content["tokens"] = new_data
        json_token_content = json_content["tokens"][token_index]
        useragent = json_token_content["user_agent"]
        x_super_property = json_token_content["super_property"]
        dcfduid = json_token_content["dcfduid"]
        sdcfduid = json_token_content["sdcfduid"]
        fingerprint = json_token_content["fingerprint"]

        return {
            "Authorization": token,
            "accept": "*/*",
            "accept-language": "en-US",
            "connection": "keep-alive",
            "cookie": "__dcfduid=%s; __sdcfduid=%s; locale=en-US" % (dcfduid, sdcfduid),
            "DNT": "1",
            "origin": "https://discord.com",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "referer": "https://discord.com/channels/@me",
            "TE": "Trailers",
            "User-Agent": useragent,
            "x-debug-options": "bugReporterEnabled",
            "x-fingerprint": fingerprint,
            "X-Super-Properties": x_super_property
        }
    async def submit_cap_key(self, proxy):
        url = self.captcha_submit_url
        querystring = {
            "key": self.captcha_api_key,
            "method": "hcaptcha",
            "sitekey": self.discord_hcaptcha_id,
            "pageurl": self.discord_captcha_referer
        }
        headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
        async with ClientSession(headers=headers) as mass_dm_brrr:
            async with mass_dm_brrr.post(url, params=querystring, proxy=proxy) as response:
                text = await response.text()
                return text.split("|", 1)[1]

    async def get_discord_captcha(self, captcha_key_response, proxy):
        params = {"key": self.captcha_api_key, "action": "get", "id": captcha_key_response}
        async with ClientSession() as mass_dm_brrr:
            async with mass_dm_brrr.get(self.captcha_get_url, params=params, proxy=proxy) as response:
                text = await response.text()
                return text.split("|", 1)

    async def getCaptcha(self, proxy):
        captcha_step_one = await self.submit_cap_key(proxy)
        logging.info(f"Captcha step one = {captcha_step_one}")
        looping = True
        while looping:
            logging.info('Sleeping 10 seconds')
            await asyncio.sleep(10)
            captcha_step_two = await self.get_discord_captcha(captcha_step_one, proxy)
            try:
                if len(captcha_step_two[1]) > 60:
                    logging.info("Captcha done")
                    return captcha_step_two[1]
            except IndexError:
                logging.info("Captcha Not Found!")

    async def login(self, token: str, proxy: str):
        try:
            headers = await self.headers(token)
            async with ClientSession(headers=headers) as mass_dm_brrr:
                async with mass_dm_brrr.get("https://discord.com/api/v9/users/@me/library", proxy=proxy) as response:
                    try:
                        json = await response.json()
                        jsoncode = json["code"]
                        code = f"{self.opbracket}{jsoncode}{self.closebrckt} | "
                    except:
                        code = ""
                    if response.status == 200:
                        logging.info(
                            f"{self.success}Successfully logged in {code}{self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.valid_tokens_start += 1
                    if response.status == 401:
                        logging.info(f"{self.err}Invalid account {code}{self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.invalid_tokens_start += 1
                        self.tokens.remove(token)
                    if response.status == 403:
                        logging.info(f"{self.err}Locked account {code}{self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.locked_tokens_start += 1
                        self.tokens.remove(token)
                    if response.status == 429:
                        logging.info(f"{self.err}Rate limited {code}{self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        time.sleep(self.ratelimit_delay)
                        self.total_rate_limits += 1
                        await self.login(token, proxy)
        except Exception:
            await self.login(token, proxy)

    async def join(self, token: str, proxy: str):
        try:
            headers = await self.headers(token)
            async with ClientSession(headers=headers) as hoemotion:
                async with hoemotion.post("https://discord.com/api/v9/invites/%s" % (self.invite), json={}, proxy=proxy) as response:
                    json = await response.json()
                    if response.status == 200:
                        self.guild_name = json["guild"]["name"]
                        self.guild_id = json["guild"]["id"]
                        self.channel_id = json["channel"]["id"]
                        logging.info(f"{self.success}Successfully joined %s {self.opbracket}%s{self.closebrckt}" % (
                        self.guild_name[:20], token[:59]))
                        self.total_server_joins_success += 1
                    elif response.status == 401:
                        logging.info(f"{self.err}Invalid account {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.tokens.remove(token)
                        self.total_server_joins_invalid += 1
                    elif response.status == 403:
                        logging.info(f"{self.err}Locked account {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.total_server_joins_locked += 1
                        self.tokens.remove(token)
                    elif response.status == 429:
                        logging.info(f"{self.err}Rate limited {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.total_rate_limits += 1
                        time.sleep(self.ratelimit_delay)
                        await self.join(token, proxy)
                    elif response.status == 404:
                        logging.info(f"{self.err}Server-Invite is invalid or has expired :/")
                        self.stop()
                    elif response.status == 400:
                        logging.info(f"Bad Request, trying to join with hcaptcha..\n({json})")
                        captcha_key = await self.getCaptcha(proxy)
                        async with ClientSession(headers=headers) as hcap_join:
                            async with hcap_join.post("https://discord.com/api/v9/invites/%s" % (self.invite), json={"captcha_key": captcha_key}, proxy=proxy) as response:
                                if response.status == 200:
                                    self.guild_name = json["guild"]["name"]
                                    self.guild_id = json["guild"]["id"]
                                    self.channel_id = json["channel"]["id"]
                                    logging.info(
                                        f"{self.success}Successfully joined %s by using hcap bypass {self.opbracket}%s{self.closebrckt}" % (
                                            self.guild_name[:20], token[:59]))
                                    self.total_server_joins_success += 1
                                elif response.status == 401:
                                    logging.info(
                                        f"{self.err}Invalid account {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                                    self.tokens.remove(token)
                                    self.total_server_joins_invalid += 1
                                elif response.status == 403:
                                    logging.info(
                                        f"{self.err}Locked account {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                                    self.total_server_joins_locked += 1
                                    self.tokens.remove(token)
                                elif response.status == 429:
                                    logging.info(
                                        f"{self.err}Rate limited {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                                    self.total_rate_limits += 1
                                    time.sleep(self.ratelimit_delay)
                                    await self.join(token, proxy)
                                elif response.status == 404:
                                    logging.info(f"{self.err}Server-Invite is invalid or has expired :/")
                                    self.stop()
                                else:
                                    self.tokens.remove(token)

                    else:
                        self.tokens.remove(token)
        except Exception:
            await self.join(token, proxy)

    async def create_dm(self, token: str, user: str, proxy: str):
        try:
            headers = await self.headers(token)
            async with ClientSession(headers=headers) as chupapi_munanyo:
                async with chupapi_munanyo.post("https://discord.com/api/v9/users/@me/channels",
                                                json={"recipients": [user]}, proxy=proxy) as response:
                    json = await response.json()
                    if response.status == 200:
                        logging.info(
                            f"{self.success}Successfully created direct message with %s {self.opbracket}%s{self.closebrckt}" % (
                            json["recipients"][0]["username"], token[:59]))
                        return json["id"]
                    elif response.status == 401:
                        logging.info(f"{self.err}Invalid account {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.invalid_tokens_total += 1
                        self.tokens.remove(token)
                        return False
                    elif response.status == 403:
                        logging.info(
                            f"{self.err}Can\'t message user {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.tokens.remove(token)
                    elif response.status == 429:
                        logging.info(f"{self.err}Rate limited {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.total_rate_limits += 1
                        time.sleep(self.ratelimit_delay)
                        return await self.create_dm(token, user, proxy)
                    elif response.status == 400:
                        logging.info(
                            f"{self.err}Can\'t create DM with yourself! {self.opbracket}%s{self.closebrckt}" % (
                            token[:59]))
                    elif response.status == 404:
                        logging.info(
                            f"{self.err}User doesn\'t exist! {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                    else:
                        return False
        except Exception:
            return await self.create_dm(token, user, proxy)

    async def direct_message(self, token: str, channel: str, user, proxy: str):
        embed = self.embed
        message = self.get_user_in_message(user)
        headers = await self.headers(token)
        async with ClientSession(headers=headers) as virgin:
            async with virgin.post("https://discord.com/api/v9/channels/%s/messages" % (channel),
                                   json={"content": f"{message}{embed}", "nonce": self.nonce(),
                                         "tts": False}, proxy=proxy) as response:
                json = await response.json()
                if response.status == 200:
                    logging.info(f"{self.success}Successfully sent message {self.opbracket}%s{self.red}){self.rst}" % (
                    token[:59]))
                    self.total_dms_success += 1
                elif response.status == 401:
                    logging.info(f"{self.err}Invalid account {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                    self.tokens.remove(token)
                    self.invalid_tokens_total += 1
                    self.invalid_token_dm += 1
                    return False
                elif response.status == 403 and json["code"] == 40003:
                    logging.info(f"{self.err}Rate limited {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                    time.sleep(self.ratelimit_delay)
                    self.total_rate_limits += 1
                    await self.direct_message(token, channel, user, proxy)
                elif response.status == 403 and json["code"] == 50007:
                    logging.info(f"{self.err}User has direct messages disabled {self.opbracket}%s{self.closebrckt}" % (
                    token[:59]))
                    self.total_dms_fail += 1
                elif response.status == 403 and json["code"] == 40002:
                    logging.info(f"{self.err}Locked {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                    self.locked_token_dm += 1
                    self.locked_tokens_total += 1
                    self.tokens.remove(token)
                    return False
                elif response.status == 429:
                    logging.info(f"{self.err}Rate limited {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                    time.sleep(self.ratelimit_delay)
                    self.total_rate_limits += 1
                    await self.direct_message(token, channel, user, proxy)
                elif response.status == 400:
                    self.total_dms_fail += 1
                    code = json["code"]
                    logging.info(f"{self.err}Can\'t DM this User! {self.opbracket}{code}{self.closebrckt} | {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                elif response.status == 404:
                    logging.info(f"{self.err}User doesn\'t exist! {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                else:
                    return False

    def get_user_in_message(self, user: str = None):
        mssage = self.message
        message = mssage.replace("<user>", f"<@{user}>")
        return message



    async def send(self, token: str, user: str, proxy: str):
        channel = await self.create_dm(token, user, proxy)
        if channel == False:
            return await self.send(random.choice(self.tokens), user, proxy)
        response = await self.direct_message(token, channel, user, proxy)
        if response == False:
            return await self.send(random.choice(self.tokens), user, proxy)

    async def leave(self, token: str, proxy: str):
        try:
            headers = await self.headers(token)
            async with ClientSession(headers=headers) as client:
                async with client.delete(f"https://discord.com/api/v9/users/@me/guilds/{self.guild_id}",
                                         json={"lurking": False}, proxy=proxy) as response:
                    json = await response.json()
                    message = json["message"]
                    code = json["code"]
                    if response.status == 200:
                        logging.info(
                            f"{self.success}Successfully left the Guild {self.opbracket}%s{self.closebrckt}" % (
                            token[:59]))
                        self.total_server_leave_success += 1
                    elif response.status == 204:
                        logging.info(
                            f"{self.success}Successfully left the Guild {self.opbracket}%s{self.closebrckt}" % (
                            token[:59]))
                        self.total_server_leave_success += 1
                    elif response.status == 404:
                        logging.info(
                            f"{self.success}Successfully left the Guild {self.opbracket}%s{self.closebrckt}" % (
                            token[:59]))
                        self.total_server_leave_success += 1
                    elif response.status == 403:
                        self.total_server_leave_locked += 1
                        logging.info(f"{self.err}{message} | {code} {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                    elif response.status == 401:
                        self.total_server_leave_invalid += 1
                        self.locked_tokens_total += 1
                        logging.info(f"{self.err}{message} | {code} {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                    elif response.status == 429:
                        self.total_rate_limits += 1
                        logging.info(f"{self.err}{message} | {code} {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        time.sleep(self.ratelimit_delay)
                        await self.leave(token, proxy)
                    else:
                        logging.info(
                            f"{self.err}{response.status} | {message} | {code} | {self.opbracket}%s{self.closebrckt}" % (
                            token[:59]))

        except Exception:
            await self.leave(token, proxy)

    async def start(self, first_start):
        if len(self.tokens) == 0:
            logging.info("No tokens loaded.")
            time.sleep(5)
            sys.exit()

        def table():

            table = Table(
                title=f"Total Users Scraped: {len(self.users)}",
                caption="github.com/hoemotion",
                caption_justify="right",
                caption_style="bright_yellow"
            )

            table.add_column("Tokens", header_style="bright_cyan", style="blue", no_wrap=True)
            table.add_column("Login Details", header_style="bright_magenta", style="magenta", justify="center")
            table.add_column("Join Details", justify="center", header_style="light_green", style="bright_green")
            table.add_column("DM Users", justify="center", header_style="magenta", style="blue")
            table.add_column("Leave Details", justify="center", header_style="bright_cyan", style="bright_green")

            table.add_row(
                f"[Total] Tokens: {self.total_tokens}",
                f"[Login] Valid Tokens: {self.valid_tokens_start}",
                f"[Join] Valid Tokens: {self.total_server_joins_success}",
                f"[DM] Total DMed: {self.total_dms_success}\n[DM] Total Failed: {self.total_dms_fail}",
                f"[Leave] Tokens Left Successfully: {self.total_server_leave_success}",
                style="on black",
                end_section=True,
            )
            table.add_row(
                f"[Total] Tokens Invalid: {self.invalid_tokens_total}",
                f"[Login] Tokens Invalid: {self.invalid_tokens_start}",
                f"[Join] Tokens Invalid: {self.total_server_joins_invalid}",
                f"[DM] Tokens Invalid: {self.invalid_token_dm}",
                f"[Leave] Tokens Invalid: {self.total_server_leave_invalid}",
                style="on black",
                end_section=True,
            )
            table.add_row(
                f"[Total] Tokens Locked: {self.locked_tokens_total}",
                f"[Login] Tokens Locked: {self.locked_tokens_start}",
                f"[Join] Tokens Locked: {self.total_server_joins_locked}",
                f"[DM] Tokens Locked: {self.locked_token_dm}",
                f"[Leave] Tokens Locked: {self.total_server_leave_locked}",
                style="on black",
                end_section=True,
            )

            def header(text: str) -> None:
                console.print()
                console.rule(highlight(text))
                console.print()

            console = Console()
            highlight = ReprHighlighter()

            table.width = None
            table.expand = False
            table.row_styles = ["dim", "none"]
            table.show_lines = True
            table.leading = 0
            header("MassDM analytics")
            console.print(table, justify="center")
            return

        if first_start == "true":
            print()
            logging.info(
                "Setting up the token_profiles.json file..\nThis might take a while depending on the amount of your tokens.")
            print()

            async with TaskPool(1_000) as pool:
                for token in self.tokens:
                    if len(self.tokens) != 0:
                        await pool.put(self.setup(token))
                    else:
                        self.stop()

            if len(self.tokens) == 0:
                self.stop()

        async def check_tokens():
            async with TaskPool(1_000) as pool:
                for token in self.tokens:
                    if len(self.tokens) != 0:
                        if self.use_proxies:
                            proxy = "%s://%s" % (self.proxy_type, random.choice(self.proxies))
                        else:
                            proxy = None
                        await pool.put(self.login(token, proxy))
                    else:
                        self.stop()

            if len(self.tokens) == 0:
                self.stop()
            return "success"

        async def join_server():
            self.invite = input(f"{self.question}Invite{self.arrow}discord.gg/").replace("/", "").replace("discord.com",
                                                                                                          "").replace(
                "discord.gg", "").replace("invite", "").replace("https:", "").replace("http:", "").replace(
                "discordapp.com", "")
            print()
            logging.info("Joining server.")
            print()

            async with TaskPool(1_000) as pool:
                for token in self.tokens:
                    if len(self.tokens) != 0:
                        if self.use_proxies:
                            proxy = "%s://%s" % (self.proxy_type, random.choice(self.proxies))
                        else:
                            proxy = None
                        await pool.put(self.join(token, proxy))
                        if self.delay != 0: await asyncio.sleep(self.delay)
                    else:
                        self.stop()

            if len(self.tokens) == 0:
                self.stop()
            return "success"

        async def scrape_users():
            self.guild_id = input(f"{self.question}Enter Guild ID{self.arrow}")
            self.channel_id = input(f"{self.question}Enter Channel ID{self.arrow}")
            self.invite = input(f"{self.question}Invite{self.arrow}discord.gg/").replace("/", "").replace("discord.com",
                                                                                                          "").replace(
                "discord.gg", "").replace("invite", "").replace("https:", "").replace("http:", "").replace(
                "discordapp.com", "")
            try:
                headers = await self.headers(self.tokens[0])
                async with ClientSession(headers=headers) as hoemotion:
                    async with hoemotion.get("https://discord.com/api/v9/invites/%s?with_counts=true&with_expiration=true" % (self.invite), json={}) as response:
                        json = await response.json()
                        if response.status == 200:
                            self.guild_name = json["guild"]["name"]
                        else:
                            self.tokens.remove(token)
                            self.guild_name = "Unknown Guild"
            except:
                self.guild_name = "Unknown Guild"


            print()
            logging.info("Scraping Users from %s...\nPlease be patient" % self.guild_name)
            print()

            print()
            logging.info(f"Successfully scraped {self.red}%s{self.rst} members" % (len(self.users)))
            print()

            if len(self.tokens) == 0: self.stop()
            return "success"

        async def mass_dm():
            with open("data/users.txt", encoding="utf-8") as f:
                self.users = [i.strip() for i in f]
            logging.info("Sending messages to %s users." % (len(self.users)))
            async with TaskPool(1_000) as pool:
                for user in self.users:
                    if len(self.tokens) != 0:
                        if str(user) not in self.blacklisted_users:
                            if self.use_proxies:
                                proxy = "%s://%s" % (self.proxy_type, random.choice(self.proxies))
                            else:
                                proxy = None
                            await pool.put(self.send(random.choice(self.tokens), user, proxy))
                            if self.delay != 0: await asyncio.sleep(self.delay)
                        else:
                            logging.info(f"{self.err}Blacklisted User: {self.red}%s{self.rst}" % (user))
                    else:
                        table()
                        self.stop()
                return "success"

        async def leave_guild():
            self.guild_id = input(f"{self.question} Enter Guild ID{self.arrow}")

            logging.info("Leaving %s" % self.guild_id)
            print()
            async with TaskPool(1_000) as pool:
                if len(self.tokens) != 0:
                    for token in self.tokens:
                        if self.use_proxies:
                            proxy = "%s://%s" % (self.proxy_type, random.choice(self.proxies))
                        else:
                            proxy = None
                        await pool.put(self.leave(token, proxy))
                        if self.delay != 0:
                            await asyncio.sleep(self.delay)
                    logging.info("All Tasks are done")
                    table()
                    self.stop()
                else:
                    table()
                    self.stop()
            return "success"
        print(f"""
{self.opbracket2}1{self.closebrckt2} Join Server
{self.opbracket2}2{self.closebrckt2} Leave Server
{self.opbracket2}3{self.closebrckt2} Scrape Users
{self.opbracket2}4{self.closebrckt2} Mass DM
{self.opbracket2}5{self.closebrckt2} Check tokens
{self.opbracket2}6{self.closebrckt2} Exit""")
        list = ["1", "2", "3", "4", "5", "6"]
        choose = input(f"{self.question} Please Enter your option{self.arrow}")
        while choose not in list:
            choose = input(f"{self.question} Please Enter your option{self.arrow}")
        if choose == "1":
            lol = await join_server()
            if lol == "success":
                return await self.start(first_start="false")
        elif choose == "2":
            lol = await leave_guild()
            if lol == "success":
                return await self.start(first_start="false")
        elif choose == "3":
            lol = await scrape_users()
            if lol == "success":
                return await self.start(first_start="false")
        elif choose == "4":
            lol = await mass_dm()
            if lol == "success":
                return await self.start(first_start="false")
        elif choose == "5":
            lol = await check_tokens()
            if lol == "success":
                return await self.start(first_start="false")
        elif choose == "6":
            logging.info("Byee!")
            table()
            self.stop()

#

def center(var:str, space:int=None): # From Pycenter
    if not space:
        space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines())/2)])) / 2
    
    return "\n".join((' ' * int(space)) + var for var in var.splitlines())

class Console():        
    def printer(self, color, status, code):
        threading.Lock().acquire()
        print(f"{color} {status} > discord.gift/{code}")
    
    def proxies_count(self):
        proxies_list = 0
        with open('config/proxies.txt', 'r') as file:
            proxies = [line.strip() for line in file]
        
        for _ in proxies:
            proxies_list += 1
        
        return int(proxies_list)


class Worker():              
    def random_proxy(self):
        with open('config/proxies.txt', 'r') as f:
            proxies = [line.strip() for line in f]
        
        return random.choice(proxies)

    def config(self, args, args2=False):
        with open('config/config.json', 'r') as conf:
            data = json.load(conf)
        
        if args2:
            return data[args][args2]
        else:
            return data[args]
    
    def run(self):
        self.code = "".join(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890") for _ in range(16))
        try:
            req = requests.get(f'https://discordapp.com/api/v6/entitlements/gift-codes/{self.code}?with_application=false&with_subscription_plan=true', proxies={'http': self.config("proxies")+'://'+self.random_proxy(),'https': self.config("proxies")+'://'+self.random_proxy()}, timeout=1)
            
            if req.status_code == 200:
                Console().printer(" Valid ", self.code)
                open('results/hit.txt', 'a+').write(self.code+"\n")
                try:
                    requests.post(Worker().config("webhook", "url"), json={"content": f"||@here|| **__New Valid Nitro !!__**\n\nhttps://discord.gift/{self.code}", "username": Worker().config("webhook", "username"), "avatar_url": Worker().config("webhook", "avatar")})
                except:
                    pass
            elif req.status_code == 404:
                Console().printer("Invalid", self.code)
            elif req.status_code == 429:
                # rate = (int(req.json()['retry_after']) / 1000) + 1
                Console().printer("RTlimit", self.code)
                # time.sleep(rate)
            else:
                Console().printer(" Retry ", self.code)
                  
        except KeyboardInterrupt:
            Console().ui()
            threading.Lock().acquire()
            print(f"Stopped > Nitro Gen Stopped by Keyboard Interrupt.")
            os.system('pause >nul')
            exit()
        except:
            # Console().printer(Fore.LIGHTRED_EX, "Invalid", self.code)
            Console().printer(" Retry ", self.code)

if mode == "checker":
    verifiedtokens = []
    unverifiedtokens = []
    invalidtokens = []
    phonelocked = []
    printqueue = []
    printed = []
    def checkv2(token):
        headers, proxies = setup_request(token)
        request = requests.Session()
        while True:
            try:
                src = request.get('https://'+endpoint+'discord.com/api/v8/users/@me', headers=headers, proxies=proxies, timeout=10)
            except Exception:
                if use_proxies == 1:
                    proxies = request_new_proxy()
                else:
                    break
            else:
                break
        if src.status_code == 401:
            invalidtokens.append(token)
            printqueue.append(f"[INVALID]: {token}")
        else:
            response = json.loads(src.content.decode())
            while True:
                try:
                    src = request.get('https://'+endpoint+'discord.com/api/v8/applications/trending/global', headers=headers, proxies=proxies, timeout=10)
                except Exception:
                    if use_proxies == 1:
                        proxies = request_new_proxy()
                    else:
                        break
                else:
                    break
            if src.status_code == 403:
                if response["verified"]:
                    printqueue.append(f"[PHONE LOCKED (VERIFIED)]: {token}")
                    phonelocked.append(token)
                else:
                    printqueue.append(f"[PHONE LOCKED (UNVERIFIED)]: {token}")
                    phonelocked.append(token)
            else:
                if response["verified"]:
                    if response["phone"] is not None:
                        printqueue.append(f"[VERIFIED (E & P)]: {token}")
                    else:
                        printqueue.append(f"[VERIFIED (E)]: {token}")
                    verifiedtokens.append(token)
                else:
                    if response["phone"] is not None:
                        printqueue.append(f"[VERIFIED (P)]: {token}")
                        verifiedtokens.append(token)
                    else:
                        printqueue.append(f"[UNVERIFIED]: {token}")
                        unverifiedtokens.append(token)
    layout = [
        [sg.Output(size=(100,30))],
        [sg.Button('Save Working',size=(10,1)), sg.RButton('Stop Checking',size=(15,1))]
    ]
    for token in tokenlist:
        executor.submit(checkv2, token)
    window = sg.Window(f'Token Checker [{len(verifiedtokens)} Verified] [{len(unverifiedtokens)} Unverified] [{len(phonelocked)} Phone Locked] [{len(invalidtokens)} Invalid]', layout, keep_on_top=True)
    while True:
        event, values = window.Read(timeout=10)
        if event == sg.TIMEOUT_KEY:
            for token in printqueue:
                if token in printed:
                    continue
                else:
                    print(token)
                    printed.append(token)
            window.TKroot.title(f'Token Checker [{len(verifiedtokens)} Verified] [{len(unverifiedtokens)} Unverified] [{len(phonelocked)} Phone Locked] [{len(invalidtokens)} Invalid]')
        elif event is None:
            break
        elif event == "Save Working":
            try:
                if not os.path.isdir("tokens/old"):
                    os.mkdir("tokens/old")
                shutil.copyfile("tokens/"+token_list, f'tokens/old/{token_list.replace(".txt","")}old{random.randint(1,999)}.txt')
            except Exception:
                pass
            time.sleep(0.1)
            with open ("tokens/"+token_list,"w+") as handle:
                for token in verifiedtokens:
                    handle.write(f"{token}\n")
                for token in unverifiedtokens:
                    handle.write(f"{token}\n")
                sg.PopupOK('Saved', title="Saved tokens", keep_on_top=True)
        elif event == "Stop Checking":
            executor.shutdown(wait=False)
    window.Close()

elif mode == "Crypto":
    main()

elif mode == "Mass":
    client = Discord()
    asyncio.get_event_loop().run_until_complete(client.start(first_start="true"))

elif mode == "NitroGen":
    Console().ui()
    print(" "+ str(Console().proxies_count()) + " Total proxies loaded...\n\n")
    DNG = Worker()
    
    while True:
        if threading.active_count() <= int(Worker().config("thread")):  
            threading.Thread(target=DNG.run(), args=()).start()

elif mode == 'TokenGen':
    print("Token Generator")
    def getCookies(self) -> list:
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Referer': 'https://discord.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        }

        response = self.session.get('https://discord.com/api/v9/experiments', headers=headers)
        return response.cookies, response.json().get("fingerprint")
    

    def register(self) -> bool:
        try:
            xcookies, fingerprint = self.getCookies()
            cookies = {
                '__dcfduid': xcookies.get('__dcfduid'),
                '__sdcfduid': xcookies.get('__sdcfduid'),
                '__cfruid': xcookies.get('__cfruid'),
                'locale': 'en-US',
            }
            # CapMonster API
            captchaService = ""
            key = ""
            capKey = ""

            payload = {
                "consent": True,
                "fingerprint": fingerprint,
                "username": "vastdabest",
                "captcha_key": capKey,
                "invite": "vast"
            }
            from json import dumps
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
                'content-length': str(len(dumps(payload))),
                'Content-Type': 'application/json',
                'Origin': 'https://discord.com',
                'Referer': 'https://discord.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-GPC': '1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 12.5; XBOX Build/NHG47K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/117.0.0.0 Safari/537.36',
                'X-Fingerprint': fingerprint,
            }

            response = self.session.post('https://discord.com/api/v9/auth/register', headers=headers, cookies=cookies, json=payload)
            if "token" not in response.text:
                if "retry_after" in response.text:
                    return False
                return False

            token = response.json().get('token')

            headers.pop('content-length')
            headers.pop('X-Fingerprint')
            headers['Authorization'] = token
            status = requests.get('https://discord.com/api/v9/users/@me/library', headers=headers)
            if status.status_code != 200:
                with open("./locked.txt", "a+") as f:
                    f.write(f"{token}\n")
                return False
            
            with open("./unlocked.txt", "a+") as f:
                f.write(f"{token}\n")

                
            return True
        except Exception as e:
            pass