#!/usr/bin/env python3
# spectra_trace.py

import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from phonenumbers.phonenumberutil import NumberParseException
from colorama import Fore, Style, init

# Colorama başlat
init(autoreset=True)

DEFAULT_REGION = "TR"

BANNER = Fore.MAGENTA + r"""
 ____                      _              _______                 
|  _ \                    | |            |__   __|                
| |_) |_ __ __ ___      _| |_ ___ _ __     | | ___  __ _ _ __    
|  _ <| '__/ _` \ \ /\ / / __/ _ \ '__|    | |/ _ \/ _` | '_ \   
| |_) | | | (_| |\ V  V /| ||  __/ |       | |  __/ (_| | |_) |  
|____/|_|  \__,_| \_/\_/  \__\___|_|       |_|\___|\__,_| .__/   
                                                         | |      
                                                         |_|      
"""

def clean_number(s):
    return s.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

def normalize_number(num):
    num = clean_number(num)
    if num.startswith("+"):
        return num
    if num.startswith("0") and len(num) >= 10:
        return "+90" + num[1:]
    return "+90" + num

def trace_once(raw, default_region=DEFAULT_REGION, lang="tr"):
    num = normalize_number(raw)

    try:
        p = phonenumbers.parse(num, None)
    except NumberParseException as e:
        print(Fore.RED + f"[!] Numara çözümlenemedi: {e}")
        return

    print(Fore.CYAN + "\n====== 📱 SORGULAMA SONUCU ======\n")

    print(Fore.YELLOW + f"Girdi       : {Fore.WHITE}{raw}")

    try:
        e164 = phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.E164)
        print(Fore.YELLOW + f"E.164       : {Fore.GREEN}{e164}")
    except:
        print(Fore.YELLOW + "E.164       : " + Fore.RED + "(formatlanamadı)")

    print(Fore.YELLOW + f"Mümkün mü   : {Fore.GREEN if phonenumbers.is_possible_number(p) else Fore.RED}{phonenumbers.is_possible_number(p)}")
    print(Fore.YELLOW + f"Geçerli mi  : {Fore.GREEN if phonenumbers.is_valid_number(p) else Fore.RED}{phonenumbers.is_valid_number(p)}")

    try:
        loc = geocoder.description_for_number(p, lang) or "Bilgi yok"
        print(Fore.YELLOW + f"Konum       : {Fore.WHITE}{loc}")
    except:
        print(Fore.YELLOW + "Konum       : " + Fore.RED + "(bilgi yok)")

    try:
        oper = carrier.name_for_number(p, lang) or "Bilgi yok"
        print(Fore.YELLOW + f"Operatör    : {Fore.GREEN}{oper}")
    except:
        print(Fore.YELLOW + "Operatör    : " + Fore.RED + "(bilgi yok)")

    try:
        tz = timezone.time_zones_for_number(p)
        print(Fore.YELLOW + f"Zaman dilimi: {Fore.WHITE}{tz}")
    except:
        print(Fore.YELLOW + "Zaman dilimi: " + Fore.RED + "(bilgi yok)")

    print(Fore.CYAN + "\n=================================\n")

def main():
    print(BANNER)  # ASCII SANAT BURADA ÇIKIYOR
    print(Fore.MAGENTA + "📞 PhoneTracer — Renkli Mod Aktif!")
    print(Fore.BLUE + "Numarayı uluslararası formatta yaz: " + Fore.WHITE + "(+905321234567)")
    print(Fore.BLUE + "Yerel format da olur: " + Fore.WHITE + "(05321234567)")
    print()

    try:
        raw = input(Fore.GREEN + "Numara gir → ")
    except (KeyboardInterrupt, EOFError):
        print(Fore.RED + "\nÇıkılıyor.")
        return

    if not raw.strip():
        print(Fore.RED + "Boş giriş — çıkılıyor.")
        return

    trace_once(raw)

if __name__ == "__main__":
    main()
  
