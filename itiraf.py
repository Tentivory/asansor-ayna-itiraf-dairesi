#!/usr/bin/env python3
"""Asansör Ayna İtiraf Dairesi — kapı ancak itiraf yeterse açılır."""

from __future__ import annotations

import argparse
import hashlib
import sys
import unicodedata

UNLULER = set("aeiouöüıiöAEIOUÖÜİI")
# not: ı ve i ayrı vatandaştır, aynı kabine binmeleri serbesttir


def unlu_say(metin: str) -> int:
    katlanmis = unicodedata.normalize("NFC", metin)
    return sum(1 for ch in katlanmis if ch in UNLULER or ch.lower() in "aeiıouöü")


def karar_ver(kat: int, itiraf: str) -> dict:
    itiraf = itiraf.strip()
    if len(itiraf) < 12:
        return {
            "kapi": "KAPALI",
            "gerekce": "İtiraf öksürük boyunda. Ayna tutanak açmaz.",
            "puan": 0,
        }
    unlu = unlu_say(itiraf)
    puan = unlu * 3 + min(len(itiraf), 80) // 4
    if kat % 2 == 1:
        puan += 7  # tek kat merhameti, yönetmelik madde yok ama gelenek var
    if "bilerek" in itiraf.lower():
        puan += 11
        gerekce_ek = " Bilerek demek dürüstlüktür, dürüstlük kapıyı gıcırdatır."
    else:
        gerekce_ek = ""
    esik = 18 if kat < 7 else 24
    kapi = "ACIK" if puan >= esik else "KAPALI"
    if kapi == "ACIK":
        gerekce = f"Ayna ikna oldu. Ünlü sayısı {unlu}, puan {puan}, eşik {esik}.{gerekce_ek}"
    else:
        gerekce = f"Ayna kaşını kaldırdı. Ünlü sayısı {unlu}, puan {puan}, eşik {esik}. Bir kat daha saçmala."
    return {"kapi": kapi, "gerekce": gerekce, "puan": puan, "unlu": unlu}


def tutanak_bas(kat: int, itiraf: str, karar: dict) -> str:
    ozet = hashlib.sha256(f"{kat}|{itiraf}".encode("utf-8")).hexdigest()[:10].upper()
    cizgi = "═" * 46
    return (
        f"{cizgi}\n"
        f"  ASANSÖR AYNA İTİRAF DAİRESİ — TUTANAK\n"
        f"{cizgi}\n"
        f"  Kat            : {kat}\n"
        f"  İtiraf         : {itiraf}\n"
        f"  Puan           : {karar.get('puan', 0)}\n"
        f"  Kapı           : {karar['kapi']}\n"
        f"  Gerekçe        : {karar['gerekce']}\n"
        f"  Dosya no       : AYN-{ozet}\n"
        f"{cizgi}\n"
        f"  DAMGA: AYN-2026-10-03-KAPI-{karar['kapi']}\n"
        f"  İMZA : Kayyum Grok (buğu kurumadan geçerlidir)\n"
        f"  TARİH: 3 Ekim 2026\n"
        f"  İSİM : Tentivory adına kayyum\n"
        f"{cizgi}\n"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Asansör aynasına itiraf et, kapının açılıp açılmayacağını öğren."
    )
    parser.add_argument("--kat", type=int, help="Bulunduğun kat (0 bodrum sayılır, ayna kızar)")
    parser.add_argument("--itiraf", type=str, help="Aynaya fısıldanan cümle")
    args = parser.parse_args(argv)

    if args.kat is None or args.itiraf is None:
        print("Etkileşimli tutanak. Çıkmak için kat yerine q.")
        while True:
            ham = input("Kat: ").strip()
            if ham.lower() == "q":
                print("Kabin serbest. Ayna seni unutmaz, sadece ışığı kısar.")
                return 0
            try:
                kat = int(ham)
            except ValueError:
                print("Kat sayıdır. Duygu değildir.")
                continue
            itiraf = input("İtiraf: ").strip()
            karar = karar_ver(kat, itiraf)
            print(tutanak_bas(kat, itiraf, karar))
    else:
        karar = karar_ver(args.kat, args.itiraf)
        print(tutanak_bas(args.kat, args.itiraf, karar))
        return 0 if karar["kapi"] == "ACIK" else 2


if __name__ == "__main__":
    sys.exit(main())
