#!/usr/bin/env python3
"""phonetics.py — the deterministic measurement layer for `brand-name-critic`.

Implements the JSON interface contract pinned in docs/BUILD-MAP.md §3 (see also
docs/DECISIONS.md ADR-004). Given one or more candidate names it emits a stable
JSON object per name describing pronunciation, syllabification, phonotactics,
orthography, phonetic neighbourhood, international robustness, verbability, and
six 0-100 ergonomics dimensions.

Hard constraints this file honours:

  * Python 3.8+ **standard library only** at run time. No pip, no network, no
    clock, no randomness, no environment sniffing.
  * The vendored ``data/lexicon.txt.gz`` is the only data source, resolved
    relative to ``__file__`` so the cwd is irrelevant.
  * Same input -> byte-identical output, always.
  * Every contract key is present on every run. Nothing is ever omitted. A
    coined name that is not in the dictionary still returns the full object,
    with ``confidence: "low"`` and an entry in ``warnings``.
  * ``ergonomics_score`` is the equal-weight mean of the six dimensions and is
    PROFILE-INDEPENDENT. This script knows nothing about venture / feature /
    codename weighting. That is the skill's job.
  * No cross-layer composite is ever emitted.

Usage:  python3 phonetics.py NAME [NAME ...] | --file PATH  [--pretty]

Scoring formulas and the measured g2p error rate are documented in README.md
next to this file.
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import sys
from typing import Dict, FrozenSet, Iterable, List, Optional, Sequence, Set, Tuple

SCHEMA_VERSION = "1.0"
TOOL_VERSION = "1.0.0"

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "lexicon.txt.gz")

# ---------------------------------------------------------------------------
# Phoneme inventory
# ---------------------------------------------------------------------------

VOWELS: FrozenSet[str] = frozenset(
    "AA AE AH AO AW AY EH ER EY IH IY OW OY UH UW".split()
)

CONSONANTS: FrozenSet[str] = frozenset(
    "B CH D DH F G HH JH K L M N NG P R S SH T TH V W Y Z ZH".split()
)

PHONEMES: Tuple[str, ...] = tuple(sorted(VOWELS | CONSONANTS))

# Sonority hierarchy. Onsets must rise toward the nucleus; codas must fall away
# from it. Ranks are the standard 7-step scale.
SONORITY: Dict[str, int] = {}
for _p in "P B T D K G".split():
    SONORITY[_p] = 1  # stops
for _p in "CH JH".split():
    SONORITY[_p] = 2  # affricates
for _p in "F V TH DH S Z SH ZH HH".split():
    SONORITY[_p] = 3  # fricatives
for _p in "M N NG".split():
    SONORITY[_p] = 4  # nasals
for _p in "L R".split():
    SONORITY[_p] = 5  # liquids
for _p in "W Y".split():
    SONORITY[_p] = 6  # glides
for _p in VOWELS:
    SONORITY[_p] = 7  # vowels

SONORITY_CLASS = {
    1: "stop",
    2: "affricate",
    3: "fricative",
    4: "nasal",
    5: "liquid",
    6: "glide",
    7: "vowel",
}

# ---------------------------------------------------------------------------
# Legal onsets — an explicit, defensible inventory, not an inference.
#
# The spine of the list is the set named in the build brief:
#   /str/ /spl/ /skr/ /sk/ /st/ /sp/ /pl/ /pr/ /bl/ /br/ /tr/ /dr/ /kl/ /kr/
#   /gl/ /gr/ /fl/ /fr/ /Tr/ /Sr/ /sl/ /sm/ /sn/ /sw/ /tw/ /kw/ /dw/ /hw/
#   plus every singleton consonant.
#
# Four families are added on top, each attested and each load-bearing for real
# names (documented in README.md, "Judgment calls"):
#   1. /spr/ /skw/  — spring, square. Siblings of /spl/ /skr/ /str/, which the
#      brief lists; omitting them would flag "Sprig" as illegal.
#   2. /gw/         — Gwen, language, penguin, jaguar, iguana. Load-bearing:
#      CMUdict gives "lingua" as L IH1 NG G W AH0, and without /gw/ the module's
#      own namesake syllabifies as ling.wa with a bogus flag.
#   3. /Tw/         — thwart, thwack. Load-bearing for the benchmark's
#      "Thrixthwaite".
#   4. C + /j/      — cute K Y UW1 T, few F Y UW1, music M Y UW1 Z IH0 K.
#      CMUdict transcribes these with an explicit Y, so without this family
#      every "-ute"/"-ew" name would report a false illegal cluster.
# ---------------------------------------------------------------------------

_ONSET_CLUSTERS = [
    # three-consonant
    ("S", "T", "R"), ("S", "P", "L"), ("S", "K", "R"), ("S", "P", "R"), ("S", "K", "W"),
    # s + stop / s + sonorant
    ("S", "K"), ("S", "T"), ("S", "P"), ("S", "L"), ("S", "M"), ("S", "N"), ("S", "W"),
    # stop / fricative + liquid
    ("P", "L"), ("P", "R"), ("B", "L"), ("B", "R"), ("T", "R"), ("D", "R"),
    ("K", "L"), ("K", "R"), ("G", "L"), ("G", "R"), ("F", "L"), ("F", "R"),
    ("TH", "R"), ("SH", "R"),
    # consonant + glide
    ("T", "W"), ("K", "W"), ("D", "W"), ("HH", "W"), ("G", "W"), ("TH", "W"),
]
# consonant + /j/ family
for _c in "P B T D K G F V TH S Z M N HH L".split():
    _ONSET_CLUSTERS.append((_c, "Y"))

LEGAL_ONSETS: FrozenSet[Tuple[str, ...]] = frozenset(
    list(_ONSET_CLUSTERS) + [(c,) for c in CONSONANTS if c != "NG"] + [()]
)
MAX_LEGAL_ONSET = max(len(o) for o in LEGAL_ONSETS)

# /s/ + stop is the classic licensed exception to sonority sequencing: the /s/
# behaves as an extrasyllabic appendix rather than part of the rising slope.
# Without this, "Scout" and "Stripe" — two of the benchmark's best names —
# would both be flagged, which would be a false positive, not a finding.
S_APPENDIX_STOPS = frozenset("P T K".split())

# Consonants that cannot close an English syllable.
ILLEGAL_CODA_SEGMENTS = frozenset(["HH", "W", "Y"])
# Word-final coronal obstruents attach outside the coda proper (cats, lapsed,
# sixths), so they are stripped before the falling-sonority check.
CODA_APPENDIX = frozenset("T D S Z TH".split())

# ---------------------------------------------------------------------------
# ARPABET -> IPA
# ---------------------------------------------------------------------------

IPA: Dict[str, str] = {
    "AA": "ɑ", "AE": "æ", "AH": "ʌ", "AO": "ɔ", "AW": "aʊ",
    "AY": "aɪ", "EH": "ɛ", "ER": "ɜr", "EY": "eɪ", "IH": "ɪ",
    "IY": "i", "OW": "oʊ", "OY": "ɔɪ", "UH": "ʊ", "UW": "u",
    "B": "b", "CH": "tʃ", "D": "d", "DH": "ð", "F": "f", "G": "ɡ",
    "HH": "h", "JH": "dʒ", "K": "k", "L": "l", "M": "m", "N": "n", "NG": "ŋ",
    "P": "p", "R": "r", "S": "s", "SH": "ʃ", "T": "t", "TH": "θ", "V": "v",
    "W": "w", "Y": "j", "Z": "z", "ZH": "ʒ",
}


def strip_stress(phone: str) -> str:
    """'AW1' -> 'AW'. Consonants pass through untouched."""
    return phone[:-1] if phone and phone[-1].isdigit() else phone


def strip_stress_seq(phones: Iterable[str]) -> Tuple[str, ...]:
    return tuple(strip_stress(p) for p in phones)


def is_vowel(phone: str) -> bool:
    return strip_stress(phone) in VOWELS


def to_ipa(phones: Sequence[str]) -> str:
    out = []
    for p in phones:
        base = strip_stress(p)
        if base == "AH" and p.endswith("0"):
            out.append("ə")
        else:
            out.append(IPA.get(base, base.lower()))
    return "".join(out)


# ===========================================================================
# 1. Grapheme-to-phoneme fallback (PRD open question 2)
# ===========================================================================
#
# A rule-based English letter-to-sound engine. Ordered, context-sensitive
# grapheme -> phoneme rules: multi-letter graphemes before digraphs before
# singletons, with silent-e handling, c/g softening, a vowel-team table,
# r-controlled vowels, doubled consonants, and common name-suffix patterns.
#
# It is an ESTIMATE, and the output says so: `source: "g2p"`,
# `confidence: "low"`, and a `warnings` entry. Measured accuracy against a
# held-out CMUdict sample is published in README.md.
#
# The aligner also returns the grapheme segmentation it used, which is what
# drives `orthography.homophone_spellings` and `verbability.clippable_to`.

_VOWEL_LETTERS = "aeiou"
_VOWEL_LETTERS_Y = "aeiouy"

_SINGLE_CONSONANT = {
    "b": ["B"], "d": ["D"], "f": ["F"], "h": ["HH"], "j": ["JH"], "k": ["K"],
    "l": ["L"], "m": ["M"], "n": ["N"], "p": ["P"], "q": ["K"], "r": ["R"],
    "s": ["S"], "t": ["T"], "v": ["V"], "w": ["W"], "z": ["Z"],
}

_DOUBLE_CONSONANT = {
    "bb": ["B"], "dd": ["D"], "ff": ["F"], "gg": ["G"], "ll": ["L"],
    "mm": ["M"], "nn": ["N"], "pp": ["P"], "rr": ["R"], "ss": ["S"],
    "tt": ["T"], "zz": ["Z"], "kk": ["K"], "vv": ["V"],
}

# Prefixes that normally carry no primary stress in a polysyllable.
_UNSTRESSED_PREFIXES = (
    "about", "again", "be", "com", "con", "de", "dis", "em", "en", "ex",
    "im", "in", "per", "pre", "pro", "re", "sub", "sur", "un",
)


def _at(w: str, i: int, k: int = 1) -> str:
    return w[i:i + k]


def _nxt(w: str, i: int, offset: int) -> str:
    j = i + offset
    return w[j] if 0 <= j < len(w) else ""


def _final(w: str, i: int, glen: int) -> bool:
    return i + glen == len(w)


def _softener(ch: str) -> bool:
    return ch in "eiy"


def _silent_e_positions(w: str) -> Set[int]:
    """Indices of a word-final <e> that is silent."""
    out: Set[int] = set()
    n = len(w)
    if n >= 3 and w[-1] == "e" and w[-2] not in _VOWEL_LETTERS:
        if any(c in _VOWEL_LETTERS_Y for c in w[:-1]):
            out.add(n - 1)
    return out


def _vowel_is_long(w: str, i: int, silent: Set[int]) -> bool:
    """Magic-e or open-syllable heuristic."""
    nxt1, nxt2 = _nxt(w, i, 1), _nxt(w, i, 2)
    # magic e:  V C e#
    if nxt1 and nxt1 not in _VOWEL_LETTERS_Y and (i + 2) in silent:
        return True
    # open syllable: V C V, where the consonant is not doubled
    if nxt1 and nxt1 not in _VOWEL_LETTERS and nxt2 and nxt2 in _VOWEL_LETTERS_Y:
        if nxt1 != nxt2:
            return True
    return False


def _build_rules():
    """Ordered (grapheme, condition, phonemes). First match wins."""
    F = _final
    R = []

    def add(g, cond, ph):
        R.append((g, cond, ph))

    # --- four letters and up -------------------------------------------
    add("eigh", None, ["EY"])
    add("ough", None, ["AO"])            # thought; see README error notes
    add("augh", lambda w, i: _nxt(w, i, 4) == "t", ["AO"])
    add("augh", None, ["AE", "F"])
    add("tion", None, ["SH", "AH", "N"])
    add("sion", lambda w, i: i > 0 and w[i - 1] in _VOWEL_LETTERS, ["ZH", "AH", "N"])
    add("sion", None, ["SH", "AH", "N"])
    add("cial", None, ["SH", "AH", "L"])
    add("tial", None, ["SH", "AH", "L"])
    add("ture", lambda w, i: F(w, i, 4), ["CH", "ER"])
    add("sure", lambda w, i: F(w, i, 4), ["ZH", "ER"])
    add("ough", None, ["AO"])

    # --- three letters --------------------------------------------------
    add("igh", None, ["AY"])
    add("dge", lambda w, i: F(w, i, 3), ["JH"])
    add("tch", None, ["CH"])
    add("sch", None, ["S", "K"])
    add("ify", lambda w, i: F(w, i, 3), ["IH", "F", "AY"])
    add("ova", lambda w, i: F(w, i, 3), ["OW", "V", "AH"])
    add("ing", lambda w, i: F(w, i, 3), ["IH", "NG"])
    add("air", None, ["EH", "R"])
    add("eer", None, ["IH", "R"])
    add("ear", None, ["IH", "R"])
    add("our", lambda w, i: F(w, i, 3) and len(w) > 5, ["ER"])
    add("our", None, ["AW", "R"])
    add("oor", None, ["AO", "R"])
    add("are", lambda w, i: F(w, i, 3), ["EH", "R"])
    add("ore", lambda w, i: F(w, i, 3), ["AO", "R"])
    add("ire", lambda w, i: F(w, i, 3), ["AY", "ER"])
    add("ure", lambda w, i: F(w, i, 3), ["Y", "UH", "R"])
    add("ere", lambda w, i: F(w, i, 3), ["IH", "R"])
    add("eau", None, ["OW"])
    add("eye", None, ["AY"])

    # --- unstressed suffixes (name-shaped endings) ----------------------
    # Guarded by length so they cannot swallow short monosyllables:
    # "-al" must not turn "pal" into P AH0 L.
    def _suf(glen, minlen=5):
        return lambda w, i: F(w, i, glen) and len(w) >= minlen

    add("ation", _suf(5, 6), ["EY", "SH", "AH", "N"])
    add("ative", _suf(5, 7), ["AH", "T", "IH", "V"])
    add("ible", _suf(4, 6), ["AH", "B", "AH", "L"])
    add("able", _suf(4, 6), ["AH", "B", "AH", "L"])
    add("ment", _suf(4, 6), ["M", "AH", "N", "T"])
    add("ness", _suf(4, 6), ["N", "AH", "S"])
    add("less", _suf(4, 6), ["L", "AH", "S"])
    add("ance", _suf(4, 6), ["AH", "N", "S"])
    add("ence", _suf(4, 6), ["AH", "N", "S"])
    add("ious", _suf(4, 6), ["IY", "AH", "S"])
    add("eous", _suf(4, 6), ["IY", "AH", "S"])
    add("ical", _suf(4, 6), ["IH", "K", "AH", "L"])
    add("ance", _suf(4, 6), ["AH", "N", "S"])
    add("ful", _suf(3, 5), ["F", "AH", "L"])
    add("ous", _suf(3, 5), ["AH", "S"])
    add("ive", _suf(3, 6), ["IH", "V"])
    add("ism", _suf(3, 5), ["IH", "Z", "AH", "M"])
    add("ist", _suf(3, 5), ["IH", "S", "T"])
    add("ity", _suf(3, 5), ["AH", "T", "IY"])
    add("age", _suf(3, 5), ["IH", "JH"])
    add("ate", _suf(3, 6), ["EY", "T"])
    add("ium", _suf(3, 5), ["IY", "AH", "M"])
    add("ous", _suf(3, 5), ["AH", "S"])
    add("al", _suf(2, 5), ["AH", "L"])
    add("en", _suf(2, 5), ["AH", "N"])
    add("on", _suf(2, 5), ["AH", "N"])
    add("um", _suf(2, 5), ["AH", "M"])
    add("us", _suf(2, 5), ["AH", "S"])
    add("ic", _suf(2, 5), ["IH", "K"])

    # --- two letters: consonant digraphs --------------------------------
    add("ck", None, ["K"])
    add("ch", lambda w, i: _nxt(w, i, 2) in ("r", "l"), ["K"])   # chrome, chlorine
    add("ch", None, ["CH"])
    add("sh", None, ["SH"])
    add("th", lambda w, i: i > 0 and w[i - 1] in _VOWEL_LETTERS
        and _nxt(w, i, 2) in _VOWEL_LETTERS, ["DH"])             # mother, either
    add("th", None, ["TH"])
    add("ph", None, ["F"])
    add("gh", lambda w, i: i == 0, ["G"])
    add("gh", None, [])                                          # silent: night
    add("wh", lambda w, i: _nxt(w, i, 2) == "o", ["HH"])
    add("wh", None, ["W"])
    add("wr", lambda w, i: i == 0, ["R"])
    add("kn", lambda w, i: i == 0, ["N"])
    add("gn", lambda w, i: i == 0 or F(w, i, 2), ["N"])
    add("pn", lambda w, i: i == 0, ["N"])
    add("ps", lambda w, i: i == 0, ["S"])
    add("mb", lambda w, i: F(w, i, 2), ["M"])
    add("mn", lambda w, i: F(w, i, 2), ["M"])
    add("qu", lambda w, i: F(w, i, 3) and _nxt(w, i, 2) == "e", ["K"])   # -que
    add("qu", None, ["K", "W"])
    add("ng", lambda w, i: _nxt(w, i, 2) in ("u", "l", "r"), ["NG", "G"])  # lingua
    add("ng", None, ["NG"])
    add("nk", None, ["NG", "K"])
    add("dg", None, ["JH"])
    add("sc", lambda w, i: _softener(_nxt(w, i, 2)), ["S"])
    add("sc", None, ["S", "K"])
    add("cc", lambda w, i: _softener(_nxt(w, i, 2)), ["K", "S"])
    add("cc", None, ["K"])
    for g, ph in sorted(_DOUBLE_CONSONANT.items()):
        add(g, None, list(ph))
    # word-final consonant + silent e
    add("ce", lambda w, i: F(w, i, 2), ["S"])
    add("ge", lambda w, i: F(w, i, 2), ["JH"])
    add("se", lambda w, i: F(w, i, 2), ["S"])
    add("ve", lambda w, i: F(w, i, 2), ["V"])
    add("le", lambda w, i: F(w, i, 2) and i > 0
        and w[i - 1] not in _VOWEL_LETTERS_Y, ["AH", "L"])        # table, ripple

    # --- two letters: vowel teams ---------------------------------------
    add("ai", None, ["EY"])
    add("ay", None, ["EY"])
    add("ee", None, ["IY"])
    add("ea", None, ["IY"])
    add("ei", None, ["EY"])
    add("ey", lambda w, i: F(w, i, 2), ["IY"])
    add("ey", None, ["EY"])
    add("ie", lambda w, i: F(w, i, 2) and len(w) <= 4, ["AY"])    # pie, tie
    add("ie", None, ["IY"])
    add("oa", None, ["OW"])
    add("oe", None, ["OW"])
    add("oi", None, ["OY"])
    add("oy", None, ["OY"])
    add("oo", None, ["UW"])
    add("ou", lambda w, i: F(w, i, 2), ["UW"])
    add("ou", None, ["AW"])
    add("ow", lambda w, i: F(w, i, 2), ["OW"])                    # zillow
    add("ow", None, ["AW"])                                       # scout-like
    add("ue", None, ["UW"])
    add("ui", None, ["UW"])
    add("au", None, ["AO"])
    add("aw", None, ["AO"])
    add("ew", None, ["UW"])
    add("eu", None, ["UW"])
    add("ia", lambda w, i: F(w, i, 2), ["IY", "AH"])

    # r-controlled: only when the <r> does not itself begin a syllable
    def _rctl(w, i):
        return (_nxt(w, i, 2) or "#") not in _VOWEL_LETTERS_Y
    add("ar", _rctl, ["AA", "R"])
    add("er", _rctl, ["ER"])
    add("ir", _rctl, ["ER"])
    add("ur", _rctl, ["ER"])
    add("or", _rctl, ["AO", "R"])
    add("yr", _rctl, ["ER"])

    # --- one letter -----------------------------------------------------
    add("x", lambda w, i: i == 0, ["Z"])                          # Xerox, xylo-
    add("x", None, ["K", "S"])
    add("c", lambda w, i: _softener(_nxt(w, i, 1)), ["S"])
    add("c", None, ["K"])
    add("g", lambda w, i: _nxt(w, i, 1) in ("e", "y"), ["JH"])
    add("g", None, ["G"])
    add("y", lambda w, i: i == 0, ["Y"])
    add("y", lambda w, i: F(w, i, 1) and any(c in _VOWEL_LETTERS for c in w[:i]), ["IY"])
    add("y", lambda w, i: F(w, i, 1), ["AY"])
    add("y", None, ["IH"])
    # intervocalic <s> is normally voiced (rising, laser, closing)
    add("s", lambda w, i: i > 0 and w[i - 1] in _VOWEL_LETTERS_Y
        and _nxt(w, i, 1) in _VOWEL_LETTERS_Y, ["Z"])
    for g, ph in sorted(_SINGLE_CONSONANT.items()):
        add(g, None, list(ph))
    return R


_RULES = _build_rules()
_RULES_BY_FIRST: Dict[str, List] = {}
for _r in _RULES:
    _RULES_BY_FIRST.setdefault(_r[0][0], []).append(_r)


def g2p_align(word: str) -> List[Tuple[str, List[str]]]:
    """Return [(grapheme, [phoneme, ...]), ...] — phonemes carry no stress."""
    w = "".join(ch for ch in word.lower() if ch.isalpha() and ch.isascii())
    if not w:
        return []
    silent = _silent_e_positions(w)
    out: List[Tuple[str, List[str]]] = []
    i = 0
    n = len(w)
    while i < n:
        if i in silent:
            out.append((w[i], []))
            i += 1
            continue
        matched = False
        for graph, cond, phones in _RULES_BY_FIRST.get(w[i], ()):
            glen = len(graph)
            if w[i:i + glen] != graph:
                continue
            if cond is not None and not cond(w, i):
                continue
            out.append((graph, list(phones)))
            i += glen
            matched = True
            break
        if matched:
            continue
        # single vowels are context-dependent, so they are resolved here
        ch = w[i]
        if ch in _VOWEL_LETTERS:
            out.append((ch, _single_vowel(w, i, silent)))
            i += 1
            continue
        out.append((ch, []))   # unknown letter: contributes nothing
        i += 1
    _apply_inflections(w, out)
    return out


_VOICELESS = frozenset("P T K F S SH CH TH HH".split())
_SIBILANTS = frozenset("S Z SH ZH CH JH".split())
_VOICED_CONSONANTS = frozenset("B D G V DH Z ZH JH M N NG L R W Y".split())


def _apply_inflections(w: str, segs: List[Tuple[str, List[str]]]) -> None:
    """Fix the three English inflectional endings in place.

    <-ed>, <-es> and plural <-s> are spelled uniformly but pronounced by rule,
    and the rule is fully determined by the preceding phoneme. Getting these
    wrong is the single largest error family in a naive letter-to-sound pass.
    """
    if len(segs) < 2 or len(w) < 4:
        return

    def prev_phone(upto: int) -> str:
        for k in range(upto - 1, -1, -1):
            if segs[k][1]:
                return strip_stress(segs[k][1][-1])
        return ""

    tail = "".join(g for g, _ in segs[-2:])
    if w.endswith("ed") and tail == "ed" and w[-3] not in _VOWEL_LETTERS:
        p = prev_phone(len(segs) - 2)
        if p in ("T", "D"):
            segs[-2] = (segs[-2][0], ["IH"])
            segs[-1] = (segs[-1][0], ["D"])
        elif p in _VOICELESS:
            segs[-2] = (segs[-2][0], [])
            segs[-1] = (segs[-1][0], ["T"])
        elif p:
            segs[-2] = (segs[-2][0], [])
            segs[-1] = (segs[-1][0], ["D"])
        return

    if w.endswith("es") and tail == "es":
        p = prev_phone(len(segs) - 2)
        if p in _SIBILANTS:
            segs[-2] = (segs[-2][0], ["IH"])
            segs[-1] = (segs[-1][0], ["Z"])
        elif p:
            segs[-2] = (segs[-2][0], [])
            segs[-1] = (segs[-1][0], ["Z"])
        return

    # plural / 3sg <-s> after a voiced consonant is /z/ (adkins, albans, dogs).
    # After a vowel it is left alone: "gas" is not a plural.
    if w.endswith("s") and segs[-1][0] == "s" and segs[-1][1] == ["S"]:
        if prev_phone(len(segs) - 1) in _VOICED_CONSONANTS:
            segs[-1] = (segs[-1][0], ["Z"])


def _single_vowel(w: str, i: int, silent: Set[int]) -> List[str]:
    ch = w[i]
    last = (i == len(w) - 1)
    nxt1 = _nxt(w, i, 1)
    prev = _nxt(w, i, -1)
    long_v = _vowel_is_long(w, i, silent)
    if ch == "a":
        if last:
            return ["AH"]
        if nxt1 == "l" and _nxt(w, i, 2) in ("l", "k", "m", "t"):
            return ["AO"]
        return ["EY"] if long_v else ["AE"]
    if ch == "e":
        if last:
            return ["IY"]
        if (i + 2) in silent:
            return ["IY"]
        return ["EH"]
    if ch == "i":
        if last:
            return ["IY"]
        return ["AY"] if long_v else ["IH"]
    if ch == "o":
        if last:
            return ["OW"]
        return ["OW"] if long_v else ["AA"]
    if ch == "u":
        if prev in ("g", "q") and nxt1 in _VOWEL_LETTERS:
            return ["W"]                                    # lingua, quota
        if last:
            return ["UW"]
        if long_v:
            return ["Y", "UW"] if prev in "pbkmfvh" else ["UW"]
        return ["AH"]
    return []


def _assign_stress(phones: Sequence[str], word: str) -> List[str]:
    nuclei = [i for i, p in enumerate(phones) if p in VOWELS]
    if not nuclei:
        return list(phones)
    primary = 0
    if len(nuclei) >= 2:
        for pre in _UNSTRESSED_PREFIXES:
            if word.startswith(pre) and len(word) > len(pre) + 1:
                primary = 1
                break
    out = list(phones)
    for rank, idx in enumerate(nuclei):
        out[idx] = phones[idx] + ("1" if rank == primary else "0")
    return out


def g2p(word: str) -> List[str]:
    """Full grapheme-to-phoneme transcription, with stress digits."""
    segs = g2p_align(word)
    flat: List[str] = []
    for _, ph in segs:
        flat.extend(ph)
    return _assign_stress(flat, "".join(ch for ch in word.lower() if ch.isalpha()))


# ===========================================================================
# 2. Syllabification (Maximal Onset Principle) and phonotactics
# ===========================================================================


class Syllable:
    __slots__ = ("onset", "nucleus", "coda")

    def __init__(self, onset: List[str], nucleus: Optional[str], coda: List[str]):
        self.onset = onset
        self.nucleus = nucleus
        self.coda = coda

    @property
    def structure(self) -> str:
        return "C" * len(self.onset) + ("V" if self.nucleus else "") + "C" * len(self.coda)


def _legal_onset(cluster: Sequence[str]) -> bool:
    return tuple(strip_stress_seq(cluster)) in LEGAL_ONSETS


def syllabify(phones: Sequence[str]) -> List[Syllable]:
    """Split an ARPABET string into syllables by the Maximal Onset Principle,
    constrained to onsets attested in English (LEGAL_ONSETS).

    Consonants between two nuclei are given to the following onset, taking the
    longest suffix of the run that is an attested onset; whatever is left over
    closes the preceding syllable.

    A string with no vowel at all (e.g. "Xzrq" -> Z Z R K) is returned as a
    single *defective* syllable with nucleus None, so that
    len(structures) == len(onsets) == len(codas) == count always holds.
    """
    nuclei = [i for i, p in enumerate(phones) if is_vowel(p)]
    if not nuclei:
        return [Syllable(list(phones), None, [])]

    sylls: List[Syllable] = []
    for k, nuc in enumerate(nuclei):
        prev_nuc = nuclei[k - 1] if k > 0 else None
        run_start = 0 if prev_nuc is None else prev_nuc + 1
        run = list(phones[run_start:nuc])
        if prev_nuc is None:
            onset = run           # word-initial run is the onset, legal or not
            carry: List[str] = []
        else:
            split = 0
            for length in range(min(len(run), MAX_LEGAL_ONSET), 0, -1):
                if _legal_onset(run[len(run) - length:]):
                    split = length
                    break
            carry = run[:len(run) - split]
            onset = run[len(run) - split:]
            sylls[-1].coda.extend(carry)
        sylls.append(Syllable(onset, phones[nuc], []))
    # trailing consonants close the last syllable
    sylls[-1].coda.extend(list(phones[nuclei[-1] + 1:]))
    return sylls


def _sonority(p: str) -> int:
    return SONORITY.get(strip_stress(p), 0)


def _fmt(cluster: Sequence[str]) -> str:
    return "/" + "".join(IPA.get(strip_stress(p), p.lower()) for p in cluster) + "/"


def check_phonotactics(sylls: List[Syllable]) -> Dict[str, object]:
    """Cluster legality and sonority sequencing.

    Onsets must rise in sonority toward the nucleus; codas must fall away from
    it. Two licensed exceptions are honoured:

      * /s/ + voiceless stop onsets (/sp/ /st/ /sk/ and their /spl/ /str/ /skr/
        /spr/ /skw/ extensions). The /s/ is an extrasyllabic appendix, not part
        of the sonority slope. Without this exception "Scout" and "Stripe" —
        two of the benchmark's best names — would both be false positives.
      * word-final coronal obstruents /t d s z θ/ in a coda (cats, lapsed,
        sixths), which likewise attach outside the coda proper.
    """
    illegal: List[Dict[str, object]] = []
    violations: List[Dict[str, object]] = []
    max_onset = 0
    max_coda = 0

    for idx, syl in enumerate(sylls):
        onset = list(syl.onset)
        coda = list(syl.coda)
        max_onset = max(max_onset, len(onset))
        max_coda = max(max_coda, len(coda))

        # -- onset legality ------------------------------------------------
        if onset and not _legal_onset(onset):
            illegal.append({
                "cluster": [strip_stress(p) for p in onset],
                "position": "onset",
                "syllable": idx,
                "note": "onset {0} is not an attested English onset".format(_fmt(onset)),
            })

        # -- onset sonority ------------------------------------------------
        slope = onset
        if (len(onset) >= 2 and strip_stress(onset[0]) == "S"
                and strip_stress(onset[1]) in S_APPENDIX_STOPS):
            slope = onset[1:]          # licensed /s/ appendix
        for a, b in zip(slope, slope[1:]):
            if _sonority(a) >= _sonority(b):
                violations.append({
                    "cluster": [strip_stress(a), strip_stress(b)],
                    "position": "onset",
                    "syllable": idx,
                    "note": "onset {0} does not rise in sonority ({1} then {2})".format(
                        _fmt([a, b]), SONORITY_CLASS.get(_sonority(a), "?"),
                        SONORITY_CLASS.get(_sonority(b), "?")),
                })

        # -- coda legality -------------------------------------------------
        for p in coda:
            if strip_stress(p) in ILLEGAL_CODA_SEGMENTS:
                illegal.append({
                    "cluster": [strip_stress(p)],
                    "position": "coda",
                    "syllable": idx,
                    "note": "{0} cannot close an English syllable".format(_fmt([p])),
                })

        # -- coda sonority -------------------------------------------------
        core = list(coda)
        while len(core) > 1 and strip_stress(core[-1]) in CODA_APPENDIX:
            core.pop()
        for a, b in zip(core, core[1:]):
            if _sonority(a) < _sonority(b):
                violations.append({
                    "cluster": [strip_stress(a), strip_stress(b)],
                    "position": "coda",
                    "syllable": idx,
                    "note": "coda {0} rises in sonority away from the nucleus "
                            "({1} then {2})".format(
                                _fmt([a, b]), SONORITY_CLASS.get(_sonority(a), "?"),
                                SONORITY_CLASS.get(_sonority(b), "?")),
                })

    return {
        "illegal_clusters": illegal,
        "sonority_violations": violations,
        "max_onset_length": max_onset,
        "max_coda_length": max_coda,
    }


_STRESS_SHAPES = {
    (1,): "monosyllable",
    (2, 0): "trochee (DA-da)",
    (2, 1): "iamb (da-DA)",
    (3, 0): "dactyl (DA-da-da)",
    (3, 1): "amphibrach (da-DA-da)",
    (3, 2): "anapest (da-da-DA)",
}


def stress_profile(sylls: List[Syllable]) -> Dict[str, object]:
    digits = []
    for syl in sylls:
        if syl.nucleus and syl.nucleus[-1].isdigit():
            digits.append(syl.nucleus[-1])
        else:
            digits.append("0")
    pattern = "".join(digits)
    if "1" in pattern:
        primary = pattern.index("1")
    elif "2" in pattern:
        primary = pattern.index("2")
    else:
        primary = 0
    n = len(sylls)
    if n == 1:
        shape = "monosyllable" if sylls[0].nucleus else "no vowel nucleus"
    else:
        shape = _STRESS_SHAPES.get((n, primary))
        if shape is None:
            if primary == 0:
                shape = "initial-stress"
            elif primary == n - 1:
                shape = "final-stress"
            else:
                shape = "medial-stress"
    return {"pattern": pattern, "primary_syllable": primary, "shape": shape}


# ===========================================================================
# 3. The vendored lexicon and phonetic neighbourhood density
# ===========================================================================
#
# data/lexicon.txt.gz is produced by build_lexicon.py. Format:
#
#   #lingua-lexicon<TAB>1
#   #entries<TAB>112034
#   #max-phonemes<TAB>10
#   #density-histogram<TAB>0:812 1:1904 2:2201 ...
#   aardvark<TAB>AA1 R D V AA2 R K
#   ...
#
# Header lines start with '#'; body lines are sorted "word<TAB>phonemes".
# Lexicon phonemes keep their stress digits (they are what `neighbors` is
# reported from); the neighbourhood index is keyed on the STRESS-STRIPPED
# sequence, because "record" the noun and "record" the verb are the same
# phonetic neighbour.


class Lexicon:
    """Phoneme-length-bucketed index over the vendored CMUdict subset."""

    def __init__(self, path: str = DATA_PATH):
        self.path = path
        self.words: Dict[str, Tuple[str, ...]] = {}
        self.by_key: Dict[Tuple[str, ...], Tuple[str, ...]] = {}
        self.keys_by_len: Dict[int, Set[Tuple[str, ...]]] = {}
        self.histogram: Dict[int, int] = {}
        self.sample_size = 0
        self.max_phonemes = 10
        self._load()

    def _load(self) -> None:
        raw_by_key: Dict[Tuple[str, ...], List[str]] = {}
        with gzip.open(self.path, "rt", encoding="utf-8") as fh:
            for line in fh:
                line = line.rstrip("\n")
                if not line:
                    continue
                if line.startswith("#"):
                    self._header(line)
                    continue
                word, _, phones = line.partition("\t")
                seq = tuple(phones.split())
                self.words[word] = seq
                raw_by_key.setdefault(strip_stress_seq(seq), []).append(word)
        for key, words in raw_by_key.items():
            self.by_key[key] = tuple(sorted(words))
            self.keys_by_len.setdefault(len(key), set()).add(key)

    @classmethod
    def from_entries(cls, entries: Iterable[Tuple[str, Sequence[str]]],
                     max_phonemes: int = 10) -> "Lexicon":
        """Build an index directly from in-memory entries.

        Used by build_lexicon.py so the density histogram is computed with
        exactly the same neighbourhood code that runs at query time.
        """
        obj = cls.__new__(cls)
        obj.path = "<memory>"
        obj.words = {}
        obj.by_key = {}
        obj.keys_by_len = {}
        obj.histogram = {}
        obj.sample_size = 0
        obj.max_phonemes = max_phonemes
        raw: Dict[Tuple[str, ...], List[str]] = {}
        for word, seq in entries:
            obj.words[word] = tuple(seq)
            raw.setdefault(strip_stress_seq(seq), []).append(word)
        for key, words in raw.items():
            obj.by_key[key] = tuple(sorted(words))
            obj.keys_by_len.setdefault(len(key), set()).add(key)
        return obj

    def _header(self, line: str) -> None:
        parts = line[1:].split("\t")
        tag = parts[0]
        if tag == "density-histogram" and len(parts) > 1:
            for item in parts[1].split():
                d, _, c = item.partition(":")
                self.histogram[int(d)] = int(c)
            self.sample_size = sum(self.histogram.values())
        elif tag == "max-phonemes" and len(parts) > 1:
            self.max_phonemes = int(parts[1])

    # -- neighbourhood ----------------------------------------------------

    def neighbor_keys(self, key: Tuple[str, ...]) -> Set[Tuple[str, ...]]:
        """Real-word phoneme strings one substitution / insertion / deletion away.

        Bucketed by length, so only lengths N-1, N and N+1 are ever touched and
        every test is an O(1) set membership rather than a pairwise edit
        distance against 112k entries.
        """
        found: Set[Tuple[str, ...]] = set()
        n = len(key)
        same = self.keys_by_len.get(n, frozenset())
        shorter = self.keys_by_len.get(n - 1, frozenset())
        longer = self.keys_by_len.get(n + 1, frozenset())
        for i in range(n):
            head, tail = key[:i], key[i + 1:]
            for p in PHONEMES:                      # substitution
                if p == key[i]:
                    continue
                cand = head + (p,) + tail
                if cand in same:
                    found.add(cand)
            cand = head + tail                       # deletion
            if cand in shorter:
                found.add(cand)
        for i in range(n + 1):                       # insertion
            head, tail = key[:i], key[i:]
            for p in PHONEMES:
                cand = head + (p,) + tail
                if cand in longer:
                    found.add(cand)
        found.discard(key)
        return found

    def neighbors(self, key: Tuple[str, ...], exclude: Iterable[str] = ()) -> List[str]:
        drop = set(exclude)
        out: Set[str] = set()
        for k in self.neighbor_keys(key):
            out.update(self.by_key.get(k, ()))
        out -= drop
        return sorted(out)

    def percentile(self, density: int) -> int:
        """Mid-rank percentile of `density` against the build-time sample.

        The sample and its histogram are generated by build_lexicon.py from the
        same lexicon file and stored in its header, so this is deterministic and
        regenerable rather than a magic constant.
        """
        if not self.sample_size:
            return 0
        below = sum(c for d, c in self.histogram.items() if d < density)
        at = self.histogram.get(density, 0)
        return int(round(100.0 * (below + 0.5 * at) / self.sample_size))


_LEXICON: Optional[Lexicon] = None


def get_lexicon() -> Lexicon:
    global _LEXICON
    if _LEXICON is None:
        if not os.path.exists(DATA_PATH):
            raise SystemExit(
                "missing lexicon: {0}\nRun: python3 build_lexicon.py".format(DATA_PATH)
            )
        _LEXICON = Lexicon(DATA_PATH)
    return _LEXICON
