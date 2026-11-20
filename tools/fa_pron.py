#!/usr/bin/env python3
"""American English word → Persian-letter reading (خوانش), from CMUdict (American).
Conventions (kept identical across the course):
  short a /æ/ → َ (اَ) · /ɑ, ʌ/ → ا (آ) · schwa → ِ (اِ), word-final schwa in longer words → ا
  /ɛ/ → ِ · /eɪ/ → ِی · /ɪ, i/ → ی · /oʊ, u, ʊ/ → و · /aɪ/ → ای · /aʊ/ → او · /ɔɪ/ → وی
  /ɔ/ → ا, but before r → ُ (for → فُر) · r is always written (rhotic American r)
  th /θ/ → ث · th /ð/ → د · flap t between vowels before an unstressed vowel → د (water → وادِر)
Manual overrides in content/pron.txt always win."""
import re
try:
    import cmudict
    _D = cmudict.dict()
except Exception:  # pragma: no cover
    _D = {}

CONS = {"B": "ب", "CH": "چ", "D": "د", "DH": "د", "F": "ف", "G": "گ", "HH": "ه", "JH": "ج", "K": "ک",
        "L": "ل", "M": "م", "N": "ن", "NG": "نگ", "P": "پ", "R": "ر", "S": "س", "SH": "ش", "T": "ت",
        "TH": "ث", "V": "و", "W": "و", "Y": "ی", "Z": "ز", "ZH": "ژ"}
#        medial, initial, after-vowel
VOW = {"AA": ("ا", "آ", "آ"), "AE": ("َ", "اَ", "ئَ"), "AH1": ("ا", "آ", "آ"), "AH0": ("ِ", "اِ", "ئِ"),
       "AO": ("ا", "آ", "آ"), "AOR": ("ُ", "اُ", "ئُ"), "AW": ("او", "آو", "آو"), "AY": ("ای", "آی", "آی"),
       "EH": ("ِ", "اِ", "ئِ"), "ER": ("ِر", "اِر", "ئِر"), "EY": ("ِی", "اِی", "ئِی"), "IH": ("ی", "ای", "ئی"),
       "IY": ("ی", "ای", "ئی"), "OW": ("و", "او", "ئو"), "OY": ("وی", "اوی", "ئوی"), "UH": ("و", "او", "ئو"),
       "UW": ("و", "او", "ئو")}


def is_vowel(ph):
    return ph[-1].isdigit()


def from_phones(phones):
    out = []
    nsyl = sum(1 for p in phones if is_vowel(p))
    for i, ph in enumerate(phones):
        prev = phones[i - 1] if i else None
        nxt = phones[i + 1] if i + 1 < len(phones) else None
        if is_vowel(ph):
            base, stress = ph[:-1], ph[-1]
            key = base
            if base == "AH":
                key = "AH1" if stress in "12" else "AH0"
            if base == "AO" and nxt == "R":
                key = "AOR"
            med, ini, hia = VOW[key]
            if key == "AH0" and nxt is None and nsyl > 1:
                med = hia = "ا"
            if prev is None:
                out.append(ini)
            elif is_vowel(prev) and not prev.startswith("ER"):
                out.append(hia)
            else:
                out.append(med)
        else:
            if ph == "T" and prev and (is_vowel(prev) or prev == "R") and nxt and is_vowel(nxt) and nxt[-1] == "0":
                out.append("د")
                continue
            if ph == "R" and prev and prev.startswith("ER"):
                continue
            if ph == "NG" and nxt in ("K", "G"):
                out.append("ن")
                continue
            out.append(CONS[ph])
    return "".join(out)


def word(w):
    """Return reading or None if unknown."""
    w = w.replace("’", "'").lower()
    if "-" in w:
        parts = [word(p) for p in w.split("-")]
        return None if None in parts else "-".join(parts)
    prons = _D.get(w)
    if not prons:
        return None
    return from_phones(prons[0])


if __name__ == "__main__":
    import sys
    for w in sys.argv[1:]:
        print(w, word(w))
