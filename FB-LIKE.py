#!/usr/bin/env python3
try:
    import requests, re, time, os, base64, json
    from rich import print as printf
    from rich.panel import Panel
    from rich.console import Console
    from requests.exceptions import RequestException
except (Exception) as e:
    exit(f"{type(e).__name__} : {str(e).capitalize()}!")
 
COOKIES, SUKSES, GAGAL = {
    "NAME": None
}, [], []
 
class KIRIMKAN:
 
    def __init__(self) -> None:
        pass
 
    def VALIDASI_COOKIES(self, cookies):
        with requests.Session() as r:
            r.headers.update({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Site': 'none',
                'Accept-Language': 'en-US,en;q=0.9',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                'Host': 'tanglike.biz',
            })
            response = r.get('https://tanglike.biz/index.php')
            r.headers.update({
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer': 'https://tanglike.biz/index.php',
                'Sec-Fetch-Site': 'same-origin',
                'Accept': '*/*',
                'Cookie': '; '.join([str(x) + '=' + str(y) for x, y in r.cookies.get_dict().items()]),
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Origin': 'https://tanglike.biz',
            })
            if 'EAAAAU' in str(cookies):
                data = {
                    'access_token': cookies,
                    'type': True,
                    'cookies': '',
                }
            else:
                data = {
                    'access_token': '',
                    'type': True,
                    'cookies': base64.b64encode(cookies.encode("ascii")).decode("ascii"),
                }
            response2 = r.post('https://tanglike.biz/login.php', data = data)
            if str(response2.text) == '2':
                COOKIES.update({
                    "NAME": '; '.join([str(x) + '=' + str(y) for x, y in r.cookies.get_dict().items()])
                })
                return ("0_0")
            else:
                printf(Panel(f"[italic red]Sepertinya Akun Facebook Anda Terkena Checkpoint Atau Sudah Kedaluwarsa, Silahkan Gunakan Akun Lain Untuk Login!", width=66, style="bold dark_goldenrod", title=">>> [Login Gagal] <<<"))
                time.sleep(6.5)
                self.MAIN()
 
    def PENGIRIMAN_LIKES(self, cookies, id_like):
        with requests.Session() as r:
            r.headers.update({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cookie': '{}'.format(cookies),
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                'Host': 'tanglike.biz',
            })
            response = r.get('https://tanglike.biz/hacklike.php')
            if 'MEMBER ID:' not in str(response.text):
                printf(Panel(f"[italic red]Sepertinya Akun Facebook Anda Terkena Checkpoint Atau Sudah Kedaluwarsa, Silahkan Gunakan Akun Lain Untuk Login!", width=66, style="bold dark_goldenrod", title=">>> [Login Gagal] <<<"))
                time.sleep(6.5)
                self.MASUKAN_COOKIES()
            else:
                self.sitekey = re.search(r"{'sitekey' : '([^']+)'", str(response.text)).group(1)
                r.headers.update({
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Referer': 'https://tanglike.biz/hacklike.php',
                    'Accept': '*/*',
                    'Cookie': '{}'.format(cookies),
                    'Origin': 'https://tanglike.biz',
                })
                self.g_recaptcha_response = BYPASS().RECAPTCHA(self.sitekey)
                data = {
                    'g-recaptcha-response': '{}'.format(self.g_recaptcha_response),
                    'id_like': '{}'.format(id_like),
                    'limit': '100', # Số lượt thích phải ít hơn 100!
                    'tanglike': '',
                }
                response2 = r.post('https://tanglike.biz/hacklike.php', data = data)
                if 'Bạn đã dùng quá giới hạn hôm nay' in str(response2.text):
                    printf(Panel(f"[italic red]Anda Telah Melampaui Batas Hari Ini, Silakan Kembali Lagi Besok Atau Masuk Dengan Akun Lain Untuk Terus Menggunakan Layanan Ini!", width=66, style="bold dark_goldenrod", title=">>> [Limit] <<<"))
                    exit()
                elif 'Thành công - Đăng nhập thêm nick khác để hack nhiều hơn' in str(response2.text):
                    SUKSES.append(f'{str(response2.text)}')
                    printf(Panel(f"""[bold white]Status :[italic green] Thành công, gửi lượt thích![/]
[bold white]Link :[bold yellow] https://web.facebook.com/{id_like}
[bold white]Likes :[bold red] -+ 100""", width=66, style="bold dark_goldenrod", title=">>> [Sukses] <<<"))
                    self.DELAY(900, id_like)
                    return ("0_0")
                elif 'Like Không Thành Công - Vui lòng đợi 15p sau quay lại' in str(response2.text):
                    printf(f"[bold dark_goldenrod]   ──>[bold red] TERKENA LIMIT, SILAHKAN TUNGGU 15 MENIT!     ", end='\r')
                    time.sleep(5.5)
                    self.DELAY(895, id_like)
                    return ("-_-")
                elif 'Vui lòng điền đầy đủ' in str(response2.text):
                    printf(f"[bold dark_goldenrod]   ──>[bold red] COOKIES KAMU SUDAH TIDAK VALID!          ", end='\r')
                    time.sleep(5.5)
                    return ("-_0")
                else:
                    GAGAL.append(f'{str(response2.text)}')
                    printf(f"[bold dark_goldenrod]   ──>[bold red] GAGAL MENGIRIMKAN LIKES!                 ", end='\r')
                    time.sleep(5.5)
                    return ("0_-")
 
    def DELAY(self, times, id_like):
        global SUKSES, GAGAL
        for sleep in range(int(times), 0, -1):
            time.sleep(1.0)
            printf(f"[bold dark_goldenrod]   ──>[bold green] {id_like}[bold white]/[bold yellow]{sleep}[bold white] SUKSES:-[bold green]{len(SUKSES)}[bold white] GAGAL:-[bold red]{len(GAGAL)}    ", end='\r')
        return ("0_0")
 
    def MAIN(self):
        try:
            BANNER()
            printf(Panel('[italic green]FACEBOOK COOKIE !', width = 66, style = 'green', title = '>>> [Facebook Cookies] <<<', subtitle = '╭──────', subtitle_align = 'left'))
            self.cookies = Console().input('[green]   ╰─> ')
            self.VALIDASI_COOKIES(cookies = self.cookies)
            os.system('xdg-open https://id.traodoisub.com/')
            printf(Panel('[italic red]FACEBOOK POST UID ', width = 66, style = 'green', title = '>>> [FACEBOOK POST UID] <<<', subtitle = '╭──────', subtitle_align = 'left'))
            self.id_like = int(Console().input('[green]   ╰─> '))
            printf(Panel('[italic white]FREE UNLIMITED FACEBOOK LIKE', width = 66, style = 'green', title = '>>> [Catatan] <<<'))
            while True:
                try:
                    self.PENGIRIMAN_LIKES(COOKIES['NAME'], self.id_like)
                except (KeyboardInterrupt):
                    printf(f"\r                                                    ", end='\r')
                    time.sleep(2.5)
                    continue
                except (RequestException):
                    printf(f"[bold dark_goldenrod]   ──>[bold red] KONEKSI KAMU BERMASALAH!", end='\r')
                    time.sleep(10.0)
                    continue
                except (Exception) as e:
                    printf(f"[bold dark_goldenrod]   ──>[bold red] {str(e).upper()}!", end='\r')
                    time.sleep(5.0)
                    continue
        except (Exception) as e:
            printf(Panel(f"[italic red]{type(e).__name__} : {str(e).title()}!", width=66, style="bold dark_goldenrod", title=">>> [Error] <<<"))
            exit()
 
def BANNER():
    print("""
\x1b[38;5;82m╔━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╗
\x1b[38;5;82m┃\x1b[38;5;82m____ _  _    ____ _ ___  ___  _ _  _ ┃\x1b[38;5;84mFACEBOOK  \x1b[38;5;84m: \033[33;1mSK.SIDDIK.KHAN\x1b[38;5;82m  ┃
\x1b[38;5;82m┃\x1b[38;5;83m[__  |_/     [__  | |  \ |  \ | |_/  ┃\x1b[38;5;84mTOOL OWNER\x1b[38;5;84m: \x1b[38;5;82mSK.SIDDIK.KHAN\x1b[38;5;82m  ┃
\x1b[38;5;82m┃\x1b[38;5;84m___] | \_    ___] | |__/ |__/ | | \_ ┃\x1b[38;5;84mGITHUB \x1b[38;5;84m   : \033[35;1mSK-SIDDIK-143 \x1b[38;5;82m  ┃
\x1b[38;5;82m┣━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
\x1b[38;5;82m┃ \x1b[38;5;82mVERSION : \x1b[38;5;84m3.3    \x1b[38;5;82m\x1b[38;5;82m┃ \x1b[38;5;82mWP \x1b[38;5;84m: \x1b[38;5;82m01831773688\x1b[38;5;82m ┃  \x1b[38;5;84mTOOL\x1b[38;5;82m: \033[31;1mFACEBOOK-AUTO-LIKE \x1b[38;5;82m ┃
\x1b[38;5;82m╚━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╝""") 
 
class BYPASS:
 
    def __init__(self) -> None:
        pass
 
    def RECAPTCHA(self, sitekey): # Register here <https://multibot.in/dashboard/signup.php> and change the key!
        self.key = ("MgXbGJwcfBkrdZRUoHYT8Nl7FuStvQOI")
        response = requests.get(f'http://api.multibot.in/in.php?key={self.key}&method=userrecaptcha&googlekey={sitekey}&pageurl=https://tanglike.biz/hacklike.php')
        if 'ERROR_ZERO_BLANCE' in str(response.text):
            printf(Panel('[italic red]AFTER NOT WORK TOOL CHANGES YOUR KEY !', width = 66, style = 'green', title = '>>> [Saldo Habis] <<<'))
            exit()
        self.status, self.id = str(response.text).split('|')[0], str(response.text).split('|')[1]
        if 'OK' in str(response.text):
            while True:
                response2 = requests.get(f'http://api.multibot.in/res.php?key={self.key}&id={self.id}')
                if 'OK|' in str(response2.text):
                    return (str(response2.text).split('|')[1])
                elif 'CAPCHA_NOT_READY' in str(response2.text):
                    printf(f"[bold dark_goldenrod]   ──>[bold green] WAITING FOR SANDING !     ", end='\r')
                    time.sleep(2.5)
                    for sleep in range(60, 0, -1):
                        time.sleep(1.0)
                        printf(f'''[green]   ──>[bold white] WAIT[bold green] {sleep}[bold white] Second ...                  ''', end = '\r')
                    continue
                else:
                    self.RECAPTCHA(sitekey)
        else:
            printf('[green]   ──>[bold red] successful !          ', end = '\r')
            time.sleep(7.5)
            self.RECAPTCHA(sitekey)
 
if __name__ == '__main__':
    os.system('git pull')
    KIRIMKAN().MAIN()
    