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
    add("y", lambda w, i: i > 0 and (i + 2) in _silent_e_positions(w)
        and _nxt(w, i, 1) not in _VOWEL_LETTERS_Y, ["AY"])   # type, strype
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
        if len(core) >= 3 and any(_sonority(a) < _sonority(b)
                                  for a, b in zip(core, core[1:])):
            illegal.append({
                "cluster": [strip_stress(p) for p in core],
                "position": "coda",
                "syllable": idx,
                "note": "coda {0} is three or more consonants and does not fall in "
                        "sonority; English licenses neither".format(_fmt(core)),
            })
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
    if n == 0:
        return {"pattern": "", "primary_syllable": 0, "shape": "no syllables"}
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


# ===========================================================================
# 4. Orthography
# ===========================================================================

RARE_LETTERS = ("j", "k", "q", "x", "z")

# Phonemes that are *common in English*. The "rare letters, common sounds"
# principle (PRD §3.3) is about paying no articulatory cost for orthographic
# distinctiveness, so the bar is English frequency, not cross-linguistic
# frequency — /ɜr/ is hard for a Spanish speaker but trivially common in
# English, and Flickr is not penalised here for it.
#
# Excluded as genuinely low-frequency in English: /ʒ/ (measure, ~0.1%),
# /ɔɪ/ (boy, ~0.2%), /ʊ/ (book, ~0.5%), /ð/ and /θ/ (frequent in function
# words but marginal as a name's sound, and the source of the international
# problem the same rubric flags separately).
RARE_ENGLISH_PHONEMES = frozenset(["ZH", "OY", "UH", "TH", "DH"])
COMMON_PHONEMES = frozenset(p for p in PHONEMES if p not in RARE_ENGLISH_PHONEMES)


def _softener_at(letters: str, i: int, glen: int) -> bool:
    nxt = letters[i + glen:i + glen + 1]
    return nxt in ("e", "i", "y")


# (grapheme, condition(letters, index) or None, [readings], note)
AMBIGUOUS_TABLE: List[Tuple[str, object, List[str], str]] = [
    ("ough", None, ["/uː/ through", "/oʊ/ though", "/ʌf/ rough", "/ɒf/ cough", "/aʊ/ bough"],
     "the worst grapheme in English: five common readings"),
    ("augh", None, ["/ɔː/ caught", "/æf/ laugh"], "two common readings"),
    ("eigh", None, ["/eɪ/ eight", "/aɪ/ height"], "two common readings"),
    ("ea", None, ["/iː/ bead", "/ɛ/ bread", "/eɪ/ break"], "three common readings"),
    ("ie", None, ["/iː/ piece", "/aɪ/ pie", "/ɛ/ friend"], "three common readings"),
    ("ei", None, ["/iː/ receive", "/eɪ/ vein", "/aɪ/ height"], "three common readings"),
    ("oo", None, ["/uː/ food", "/ʊ/ book", "/ʌ/ blood"], "three common readings"),
    ("ou", None, ["/aʊ/ out", "/uː/ soup", "/ʌ/ tough", "/ɔː/ four"], "four common readings"),
    ("ow", None, ["/aʊ/ cow", "/oʊ/ low"], "two common readings, not predictable from position"),
    ("ai", None, ["/eɪ/ rain", "/ɛ/ said"], "two readings"),
    ("ay", None, ["/eɪ/ day", "/ɛ/ says"], "two readings"),
    ("au", None, ["/ɔː/ caught", "/æ/ laugh"], "two readings"),
    ("ch", None, ["/tʃ/ church", "/k/ chorus", "/ʃ/ machine"], "three common readings"),
    ("gh", None, ["/ɡ/ ghost", "/f/ laugh", "silent (night)"], "three readings including silence"),
    ("ph", None, ["/f/ phone", "/p-h/ shepherd"], "usually /f/, but a coined name invites doubt"),
    ("ti", lambda s, i: s[i + 2:i + 3] in ("o", "a"), ["/ʃ/ nation", "/t-i/ tie"],
     "<ti> before a vowel is usually /ʃ/, which is not obvious"),
    ("ci", lambda s, i: s[i + 2:i + 3] in ("o", "a"), ["/ʃ/ special", "/s-i/ city"],
     "<ci> before a vowel is usually /ʃ/"),
    ("si", lambda s, i: s[i + 2:i + 3] in ("o", "a"), ["/ʒ/ vision", "/ʃ/ mansion"],
     "<si> before a vowel is /ʒ/ or /ʃ/"),
    ("kn", lambda s, i: i == 0, ["/n/ knee (silent k)"], "silent initial letter"),
    ("gn", lambda s, i: i == 0, ["/n/ gnome (silent g)"], "silent initial letter"),
    ("wr", lambda s, i: i == 0, ["/r/ wrist (silent w)"], "silent initial letter"),
    ("ps", lambda s, i: i == 0, ["/s/ psalm (silent p)"], "silent initial letter"),
    ("mb", lambda s, i: i + 2 == len(s), ["/m/ climb (silent b)"], "silent final letter"),
    ("mn", lambda s, i: i + 2 == len(s), ["/m/ column (silent n)"], "silent final letter"),
    ("c", lambda s, i: _softener_at(s, i, 1), ["/s/ cent", "/k/ Celt"],
     "<c> before e/i/y is normally soft, but the hard reading survives in names"),
    ("g", lambda s, i: _softener_at(s, i, 1), ["/dʒ/ gem", "/ɡ/ get"],
     "<g> before e/i/y is genuinely unpredictable: gem vs get, giant vs gift"),
    ("x", None, ["/ks/ box", "/z/ Xerox", "/ɡz/ exam"],
     "three readings; initial <x> is /z/, medial is /ks/"),
    ("q", lambda s, i: s[i + 1:i + 2] != "u", ["no settled English reading"],
     "<q> not followed by <u> has no conventional English value"),
    ("y", lambda s, i: 0 < i, ["/aɪ/ my", "/i/ happy", "/ɪ/ gym", "/j/ canyon"],
     "<y> away from word-initial position has four readings"),
]


def ambiguous_graphemes(letters: str) -> List[Dict[str, object]]:
    """Spellings with more than one common English reading.

    Driven by AMBIGUOUS_TABLE above — an explicit, arguable inventory, not a
    heuristic. Occurrences of the same grapheme collapse into one entry with a
    list of positions, so a word is not penalised twice for the same problem.
    """
    found: Dict[str, Dict[str, object]] = {}
    order: List[str] = []
    n = len(letters)
    i = 0
    while i < n:
        for graph, cond, readings, note in AMBIGUOUS_TABLE:
            g = len(graph)
            if letters[i:i + g] != graph:
                continue
            if cond is not None and not cond(letters, i):
                continue
            if graph not in found:
                found[graph] = {"grapheme": graph, "positions": [], "readings": list(readings),
                                "note": note}
                order.append(graph)
            found[graph]["positions"].append(i)  # type: ignore[index]
            i += g - 1
            break
        i += 1
    return [found[g] for g in order]


# Phoneme -> alternate spellings. Used to generate plausible misspellings of a
# name heard once. Keys are the phoneme sequence of one grapheme segment, so
# multi-phoneme graphemes like <x> = /ks/ are covered.
SPELLINGS: Dict[str, List[str]] = {
    "AA": ["o", "a", "ah", "au"],
    "AE": ["a", "ah"],
    "AH": ["a", "u", "o", "e", "ah"],
    "AO": ["aw", "au", "o"],
    "AW": ["ou", "ow"],
    "AY": ["i", "y", "ie"],
    "EH": ["e", "ea", "ai"],
    "ER": ["er", "ur", "ir", "or", "ar", "yr"],
    "EY": ["a", "ai", "ay", "ei", "ey"],
    "IH": ["i", "y", "e"],
    "IY": ["ee", "ea", "e", "ie", "y", "i"],
    "OW": ["o", "oa", "ow", "oe"],
    "OY": ["oi", "oy"],
    "UH": ["oo", "u"],
    "UW": ["oo", "u", "ue", "ew", "ou"],
    "B": ["b", "bb"], "CH": ["ch", "tch"], "D": ["d", "dd"],
    "DH": ["th"], "F": ["f", "ph", "ff"], "G": ["g", "gg", "gh"],
    "HH": ["h", "wh"], "JH": ["j", "g", "dg", "ge"],
    "K": ["k", "c", "ck"], "L": ["l", "ll"],
    "M": ["m", "mm"], "N": ["n", "nn"],
    "NG": ["ng", "n"], "P": ["p", "pp"], "R": ["r", "rr"],
    "S": ["s", "ss", "c", "sc", "ce"], "SH": ["sh", "ti", "ci", "ch"],
    "T": ["t", "tt"], "TH": ["th"], "V": ["v", "vv"],
    "W": ["w", "wh"], "Y": ["y", "i"], "Z": ["z", "s", "zz", "x"],
    "ZH": ["si", "ge", "s"],
    "K S": ["x", "cks", "ks"],
    "NG G": ["ng", "ngu"],
    "K W": ["qu", "kw", "cw"],
    "Y UW": ["u", "ew", "ue", "eu"],
}

_GEMINATES = frozenset(["bb", "cc", "dd", "ff", "gg", "kk", "ll", "mm", "nn",
                        "pp", "rr", "ss", "tt", "vv", "zz"])
_FINAL_GEMINATES = frozenset(["ss", "ll", "ff", "zz"])


def _spellable(tok: str) -> bool:
    """Orthographic plausibility gate for a generated misspelling.

    English spelling conventions that no misspeller violates: a word does not
    begin with a geminate or with <ck>, a geminate sits between a vowel and
    whatever follows, <q> is followed by <u>, and no letter appears three times
    running.
    """
    if len(tok) < 2:
        return False
    if tok[:2] in _GEMINATES or tok[:2] == "ck":
        return False
    if tok[-2:] in _GEMINATES and tok[-2:] not in _FINAL_GEMINATES:
        return False
    for i in range(1, len(tok) - 1):
        if tok[i] == tok[i + 1] and tok[i:i + 2] in _GEMINATES:
            if tok[i - 1] not in "aeiouy":
                return False
    for i in range(len(tok) - 2):
        if tok[i] == tok[i + 1] == tok[i + 2]:
            return False
    for i, ch in enumerate(tok):
        if ch == "q" and tok[i + 1:i + 2] != "u":
            return False
    return True

MAX_HOMOPHONES = 8


def homophone_spellings(tokens: Sequence[str]) -> List[str]:
    """Plausible misspellings someone would produce hearing the name once.

    Method: segment the spelling into graphemes with the g2p aligner, then for
    each segment substitute the alternate spellings SPELLINGS lists for that
    segment's phonemes. A candidate is kept only if the g2p engine reads it back
    as the *same* phoneme string as the name itself — so "Linguo" is rejected
    (it reads /lɪŋɡwoʊ/) while "Lyngua" is kept. That verification step is what
    stops the list filling with letter salad; its accuracy is bounded by the
    g2p engine's, which is documented in README.md.
    """
    target = tuple(strip_stress_seq(sum((g2p(t) for t in tokens), [])))
    if not target:
        return []
    seg_lists = [g2p_align(t) for t in tokens]
    candidates: Set[str] = set()

    for ti, segs in enumerate(seg_lists):
        for si, (graph, phones) in enumerate(segs):
            if not phones:
                continue
            for alt in SPELLINGS.get(" ".join(phones), ()):
                if alt == graph:
                    continue
                new_tok = "".join(
                    alt if k == si else g for k, (g, _) in enumerate(segs)
                )
                if new_tok == tokens[ti] or not _spellable(new_tok):
                    continue
                cand = list(tokens)
                cand[ti] = new_tok
                candidates.add(" ".join(cand))

    keep: List[str] = []
    original = " ".join(tokens)
    for cand in sorted(candidates):
        if cand == original:
            continue
        toks = cand.split(" ")
        read = tuple(strip_stress_seq(sum((g2p(t) for t in toks), [])))
        if read == target:
            keep.append(cand)
    return keep[:MAX_HOMOPHONES]


def rare_letter_common_sound(letters: str, phones: Sequence[str],
                             phonotactics: Dict[str, object],
                             has_nucleus: bool) -> Optional[bool]:
    """The `rare letters, common sounds` test (PRD §3.3).

    None  — no rare letter in the spelling; the test does not apply.
    True  — a rare letter (z q x j k) sits on top of sounds that are all common
            in English, in a phonotactically legal word. This is the Barton
            sweet spot: Xerox, Zillow, Kodak, Coke.
    False — the rare letter buys distinctiveness by spending articulation: a
            phoneme outside the common English set, or a cluster English does
            not license, or no vowel at all. This is Xzrq.
    """
    present = [c for c in RARE_LETTERS if c in letters]
    if not present:
        return None
    if not has_nucleus:
        return False
    if phonotactics["illegal_clusters"] or phonotactics["sonority_violations"]:
        return False
    for p in phones:
        if strip_stress(p) not in COMMON_PHONEMES:
            return False
    return True


# ===========================================================================
# 5. International robustness
# ===========================================================================
#
# Phonemes absent from, or hard in, major world languages. Weights reflect how
# widely the difficulty is shared, and drive the low/medium/high band.

HARD_PHONEMES: Dict[str, Dict[str, object]] = {
    "TH": {"label": "/θ/", "weight": 2,
           "languages": ["French", "German", "Spanish (most dialects)", "Italian",
                         "Portuguese", "Russian", "Mandarin", "Japanese", "Korean", "Hindi"],
           "note": "rare outside English; usually substituted with /t/, /s/ or /f/"},
    "DH": {"label": "/ð/", "weight": 2,
           "languages": ["French", "German", "Italian", "Portuguese", "Russian",
                         "Mandarin", "Japanese", "Korean", "Hindi"],
           "note": "rare outside English; usually substituted with /d/ or /z/"},
    "AE": {"label": "/æ/", "weight": 1,
           "languages": ["Spanish", "Italian", "Portuguese", "Russian", "Mandarin", "Japanese"],
           "note": "merges with /a/ or /ɛ/ for most non-English speakers"},
    "ER": {"label": "/ɜr/", "weight": 1,
           "languages": ["French", "German", "Spanish", "Italian", "Japanese", "Korean"],
           "note": "the English r-coloured vowel has no close equivalent in most languages"},
    "ZH": {"label": "/ʒ/", "weight": 2,
           "languages": ["Spanish", "German", "Mandarin", "Japanese", "Korean", "Hindi"],
           "note": "absent from many inventories; substituted with /ʃ/, /z/ or /dʒ/"},
    "OY": {"label": "/ɔɪ/", "weight": 1,
           "languages": ["Mandarin", "Japanese", "Korean"],
           "note": "a marginal diphthong outside European languages"},
}

RL_CONTRAST_LANGUAGES = ["Japanese", "Korean"]
VW_CONTRAST_LANGUAGES = ["Hindi", "German", "Japanese", "Korean"]
INITIAL_NG_LANGUAGES = ["English-adjacent European languages generally",
                        "French", "German", "Spanish", "Italian", "Russian"]


def international_profile(phones: Sequence[str], sylls: List[Syllable]) -> Dict[str, object]:
    base = [strip_stress(p) for p in phones]
    present = set(base)
    hard: List[Dict[str, object]] = []
    languages: Set[str] = set()
    weight = 0

    for ph in ("TH", "DH", "AE", "ER", "ZH", "OY"):
        if ph in present:
            spec = HARD_PHONEMES[ph]
            hard.append({"phoneme": ph, "ipa": spec["label"], "note": spec["note"]})
            languages.update(spec["languages"])  # type: ignore[arg-type]
            weight += int(spec["weight"])  # type: ignore[arg-type]

    # the /r/–/l/ contrast is a problem only when both are present in one word
    rhotic = ("R" in present) or ("ER" in present)
    if rhotic and "L" in present:
        hard.append({"phoneme": "R+L", "ipa": "/r/–/l/",
                     "note": "the name contains both /r/ and /l/; the contrast is not "
                             "phonemic in Japanese or Korean"})
        languages.update(RL_CONTRAST_LANGUAGES)
        weight += 1
    if "V" in present and "W" in present:
        hard.append({"phoneme": "V+W", "ipa": "/v/–/w/",
                     "note": "the name contains both /v/ and /w/; the contrast is absent "
                             "or unstable in Hindi and German"})
        languages.update(VW_CONTRAST_LANGUAGES)
        weight += 1
    if sylls and sylls[0].onset and strip_stress(sylls[0].onset[0]) == "NG":
        hard.append({"phoneme": "NG-initial", "ipa": "/ŋ/ word-initially",
                     "note": "/ŋ/ cannot begin a word in English or in most European languages"})
        languages.update(INITIAL_NG_LANGUAGES)
        weight += 2

    # Structural difficulty counts too: a consonant cluster of three or more,
    # and above all a name with no vowel nucleus, are hard everywhere and
    # especially in CV-syllable languages (Japanese, Mandarin, Korean).
    structural = 0
    if any(len(s_.onset) >= 3 or len(s_.coda) >= 3 for s_ in sylls):
        structural += 1
        languages.update(["Japanese", "Mandarin", "Korean"])
    if sylls and not any(s_.nucleus for s_ in sylls):
        structural += 2
        languages.update(["Japanese", "Mandarin", "Korean"])
    total = weight + structural
    risk = "low" if total == 0 else ("medium" if total <= 2 else "high")
    return {
        "hard_phonemes": hard,
        "affected_languages": sorted(languages),
        "risk": risk,
        "_weight": weight,
    }


# ===========================================================================
# 6. Verbability
# ===========================================================================

_NO_DOUBLE = frozenset("wxy")


def clip_candidates(letters: str) -> List[str]:
    """Shorter forms that stay pronounceable.

    English clipping cuts at the first syllable boundary (Palantir -> Pal,
    Lingua -> Ling), so both the maximal-onset cut and the "closed" variant that
    pulls the next consonant back into the coda are offered. A candidate is kept
    only if it is at least three letters and its own phonotactics are clean.
    """
    segs = g2p_align(letters)
    phones: List[str] = []
    owner: List[int] = []
    for si, (_, ph) in enumerate(segs):
        for x in ph:
            phones.append(x)
            owner.append(si)
    if not phones:
        return []
    stressed = _assign_stress(phones, letters)
    sylls = syllabify(stressed)
    if len(sylls) < 2:
        return []
    cut = len(sylls[0].onset) + (1 if sylls[0].nucleus else 0) + len(sylls[0].coda)
    out: List[str] = []
    for b in (cut, cut + 1):
        if b <= 0 or b >= len(phones):
            continue
        clip = "".join(g for g, _ in segs[:owner[b - 1] + 1])
        if len(clip) < 3 or len(clip) >= len(letters):
            continue
        csyl = syllabify(_assign_stress(phones[:b], clip))
        if not csyl or csyl[0].nucleus is None:
            continue
        pt = check_phonotactics(csyl)
        if pt["illegal_clusters"] or pt["sonority_violations"]:
            continue
        out.append(clip)
    return sorted(set(out))


def agentive_form(letters: str, syllable_count: int) -> str:
    """Regular English agentive derivation, spelled out so it is auditable.

    -e      -> +r        (Stripe -> striper)
    -y      -> -y +ier   (Notify -> notifier)
    CVC     -> double the final consonant, monosyllables only (Scan -> scanner)
    else    -> +er       (Scout -> scouter, Slack -> slacker)
    """
    w = letters
    if not w:
        return ""
    if w.endswith("e"):
        return w + "r"
    if w.endswith("y") and len(w) > 2 and w[-2] not in "aeiou":
        return w[:-1] + "ier"
    if (syllable_count == 1 and len(w) >= 3
            and w[-1] not in "aeiou" and w[-1] not in _NO_DOUBLE
            and w[-2] in "aeiou" and w[-3] not in "aeiou"):
        return w + w[-1] + "er"
    return w + "er"


# ===========================================================================
# 7. The six dimensions
#
# Every score is 100 minus documented penalties (or a documented base plus
# documented adjustments), clamped to 0-100. There are no free parameters that
# are not written down in README.md alongside their justification.
# ===========================================================================


def _consonant_runs(letters: str) -> List[str]:
    runs: List[str] = []
    cur = ""
    for ch in letters:
        if ch in "aeiouy" or ch == " ":
            if cur:
                runs.append(cur)
            cur = ""
        else:
            cur += ch
    if cur:
        runs.append(cur)
    return runs


def _ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return "{0}{1}".format(n, suffix)


def _clamp(x: float) -> int:
    return int(max(0, min(100, round(x))))


def _dimensions(ctx: Dict[str, object]) -> Dict[str, Dict[str, object]]:
    sylls: List[Syllable] = ctx["syllables"]          # type: ignore[assignment]
    pt: Dict[str, object] = ctx["phonotactics"]        # type: ignore[assignment]
    n_syl = len(sylls)
    has_nucleus = bool(ctx["has_nucleus"])
    illegal = pt["illegal_clusters"]
    sonority = pt["sonority_violations"]
    clusters2 = sum(1 for s in sylls if len(s.onset) >= 2) + \
        sum(1 for s in sylls if len(s.coda) >= 2)
    clusters3 = sum(1 for s in sylls if len(s.onset) >= 3) + \
        sum(1 for s in sylls if len(s.coda) >= 3)
    longest_cluster = max([0] + [len(s.onset) for s in sylls] + [len(s.coda) for s in sylls])

    # -- 1. pronounceability ----------------------------------------------
    score = 100.0
    ev: List[str] = []
    syl_pen = {0: 0, 1: 0, 2: 0, 3: 6, 4: 14}.get(n_syl, 22)
    score -= syl_pen
    ev.append("{0} syllable{1}".format(n_syl, "" if n_syl == 1 else "s")
              + ("" if syl_pen == 0 else " (-{0})".format(syl_pen)))
    if not has_nucleus:
        score -= 40
        ev.append("no vowel nucleus — cannot be produced as a syllable (-40)")
    if illegal:
        pen = min(45, 18 * len(illegal))
        score -= pen
        ev.append("{0} illegal cluster{1}: {2} (-{3})".format(
            len(illegal), "" if len(illegal) == 1 else "s",
            ", ".join(sorted({_fmt(c["cluster"]) for c in illegal})), pen))
    else:
        ev.append("all clusters attested in English")
    if sonority:
        pen = min(30, 12 * len(sonority))
        score -= pen
        ev.append("{0} sonority violation{1}: {2} (-{3})".format(
            len(sonority), "" if len(sonority) == 1 else "s",
            ", ".join(sorted({_fmt(c["cluster"]) for c in sonority})), pen))
    else:
        ev.append("no sonority violation")
    if clusters2:
        score -= 4 * clusters2
        ev.append("{0} consonant cluster{1} (-{2})".format(
            clusters2, "" if clusters2 == 1 else "s", 4 * clusters2))
    over = max(0, longest_cluster - 3)
    if over:
        score -= 8 * over
        ev.append("longest cluster is {0} consonants (-{1})".format(longest_cluster, 8 * over))
    pronounceability = {"score": _clamp(score), "evidence": ev}

    # -- 2. spellability ---------------------------------------------------
    amb: List[Dict[str, object]] = ctx["ambiguous"]        # type: ignore[assignment]
    homo: List[str] = ctx["homophones"]                     # type: ignore[assignment]
    rlcs = ctx["rare_letter_common_sound"]
    letters: str = ctx["letters_only"]                      # type: ignore[assignment]
    score = 100.0
    ev = []
    if amb:
        pen = 10 * min(len(amb), 4)
        score -= pen
        ev.append("{0} ambiguous grapheme{1}: {2} (-{3})".format(
            len(amb), "" if len(amb) == 1 else "s",
            ", ".join("<{0}>".format(a["grapheme"]) for a in amb), pen))
    else:
        ev.append("no ambiguous graphemes")
    if homo:
        pen = 6 * min(len(homo), 5)
        score -= pen
        ev.append("{0} plausible misspelling{1} from hearing it once: {2} (-{3})".format(
            len(homo), "" if len(homo) == 1 else "s", ", ".join(homo[:4]), pen))
    else:
        ev.append("no plausible alternate spelling generated")
    if rlcs is False:
        score -= 10
        ev.append("rare letter on a rare or illegal sound (-10)")
    runs = _consonant_runs(letters)
    long_runs = [r for r in runs if len(r) >= 4]
    if long_runs:
        pen = min(16, 8 * len(long_runs))
        score -= pen
        ev.append("consonant letter run{0} <{1}> — hard to reconstruct in writing (-{2})".format(
            "" if len(long_runs) == 1 else "s", ">, <".join(long_runs), pen))
    if not any(c in "aeiouy" for c in letters):
        score -= 25
        ev.append("no vowel letter — cannot be spelled from hearing it (-25)")
    spellability = {"score": _clamp(score), "evidence": ev}

    # -- 3. distinctiveness ------------------------------------------------
    percentile = int(ctx["percentile"])                      # type: ignore[arg-type]
    density = int(ctx["density"])                            # type: ignore[arg-type]
    rare = list(ctx["rare_letters"])                         # type: ignore[arg-type]
    score = 100.0 - 0.6 * percentile
    ev = ["neighbourhood density {0} ({1} percentile of the lexicon)".format(
        density, _ordinal(percentile))]
    if rlcs is True:
        score += 12
        ev.append("rare letters, common sounds: <{0}> on common English phonemes (+12)".format(
            ">, <".join(rare)))
    elif rlcs is False:
        ev.append("rare letters <{0}>, but not on common sounds — no bonus".format(
            ">, <".join(rare)))
    else:
        ev.append("no rare letters (z q x j k)")
    distinctiveness = {"score": _clamp(score), "evidence": ev}

    # -- 4. rhythm & recall -------------------------------------------------
    stress: Dict[str, object] = ctx["stress"]               # type: ignore[assignment]
    ev = []
    if not has_nucleus:
        score = 20.0
        ev.append("no vowel nucleus — there is no rhythm to reproduce")
    else:
        base = {1: 90.0, 2: 100.0, 3: 88.0, 4: 74.0}.get(n_syl, 60.0)
        score = base
        ev.append({1: "monosyllable — maximally reproducible",
                   2: "two syllables — the most reproducible length in English"}.get(
            n_syl, "{0} syllables".format(n_syl)) + " (base {0:.0f})".format(base))
        shape = str(stress["shape"])
        if "1" not in str(stress["pattern"]):
            score -= 10
            ev.append("no primary stress located (-10)")
        else:
            ev.append("stress {0}: {1}".format(stress["pattern"], shape))
        if n_syl == 3 and shape.startswith("dactyl"):
            score += 4
            ev.append("dactylic — the strongest three-syllable pattern (+4)")
    if illegal or sonority:
        pen = min(15, 5 * (len(illegal) + len(sonority)))
        score -= pen
        ev.append("clusters English does not license make it hard to repeat back "
                  "(-{0})".format(pen))
    if len(letters) > 10:
        score -= 6
        ev.append("{0} letters — long for recall (-6)".format(len(letters)))
    rhythm = {"score": _clamp(score), "evidence": ev}

    # -- 5. verbability -----------------------------------------------------
    clips: List[str] = ctx["clips"]                          # type: ignore[assignment]
    ends_vowel = bool(ctx["ends_in_vowel"])
    in_lexicon = bool(ctx["in_lexicon"])
    base = {1: 90.0, 2: 75.0, 3: 55.0}.get(n_syl, 35.0)
    score = base
    ev = ["{0} syllable{1} (base {2:.0f})".format(n_syl, "" if n_syl == 1 else "s", base)]
    if not has_nucleus:
        score -= 50
        ev.append("no vowel nucleus — cannot be inflected (-50)")
    if in_lexicon:
        score += 5
        ev.append("already an English word — inflects without explanation (+5)")
    if clips:
        score += 5
        ev.append("clips to {0} (+5)".format(", ".join(clips)))
    if ends_vowel:
        score -= 5
        ev.append("ends in a vowel — awkward to inflect (-5)")
    if illegal:
        score -= 10
        ev.append("illegal clusters block clean inflection (-10)")
    elif sonority:
        score -= 6
        ev.append("sonority violations make inflected forms awkward (-6)")
    verbability = {"score": _clamp(score), "evidence": ev}

    # -- 6. international robustness ----------------------------------------
    intl: Dict[str, object] = ctx["international"]           # type: ignore[assignment]
    weight = int(intl["_weight"])                            # type: ignore[arg-type]
    hard = intl["hard_phonemes"]
    score = 100.0 - 12 * weight - 4 * clusters2 - 8 * clusters3
    ev = []
    if hard:
        ev.append("hard phonemes: {0} (-{1})".format(
            ", ".join(str(h["ipa"]) for h in hard), 12 * weight))  # type: ignore[index]
    else:
        ev.append("no phonemes outside the cross-linguistically common core")
    if clusters2:
        ev.append("{0} consonant cluster{1} — costly for CV-syllable languages (-{2})".format(
            clusters2, "" if clusters2 == 1 else "s", 4 * clusters2 + 8 * clusters3))
    if longest_cluster > 2:
        score -= 6 * (longest_cluster - 2)
        ev.append("longest cluster {0} consonants (-{1})".format(
            longest_cluster, 6 * (longest_cluster - 2)))
    if not has_nucleus:
        score -= 20
        ev.append("no vowel nucleus (-20)")
    if len(letters) > 10:
        score -= 6
        ev.append("{0} letters (-6)".format(len(letters)))
    international = {"score": _clamp(score), "evidence": ev}

    return {
        "pronounceability": pronounceability,
        "spellability": spellability,
        "distinctiveness": distinctiveness,
        "rhythm_recall": rhythm,
        "verbability": verbability,
        "international_robustness": international,
    }


# ===========================================================================
# 8. Pronunciation resolution and the top-level analysis
# ===========================================================================

MIN_COMPOUND_PART = 3        # letters
MIN_COMPOUND_PHONEMES = 3    # phonemes
MAX_NEIGHBORS = 12


def decompose(token: str, lex: Lexicon) -> Optional[Tuple[str, str]]:
    """Split a token into two known lexicon words (firefox -> fire + fox).

    Among all valid splits the one with the largest smaller part wins; ties go
    to the leftmost split point. Both parts must be at least three letters AND
    at least three phonemes, so "ox", "low", "an" and similar fragments cannot
    manufacture a decomposition. (Without the phoneme floor, CMUdict's large
    surname inventory reads "Zillow" as "zill" + "low".)
    """
    n = len(token)
    if n < MIN_COMPOUND_PART * 2:
        return None
    best: Optional[Tuple[int, int, Tuple[str, str]]] = None
    for i in range(MIN_COMPOUND_PART, n - MIN_COMPOUND_PART + 1):
        left, right = token[:i], token[i:]
        if left in lex.words and right in lex.words \
                and len(lex.words[left]) >= MIN_COMPOUND_PHONEMES \
                and len(lex.words[right]) >= MIN_COMPOUND_PHONEMES:
            rank = (min(len(left), len(right)), -i)
            if best is None or rank > best[:2]:
                best = (rank[0], rank[1], (left, right))
    return best[2] if best else None


def resolve_token(token: str, lex: Lexicon) -> Tuple[List[str], str, str, List[str]]:
    """-> (phones, source, confidence, warnings)"""
    if token in lex.words:
        return list(lex.words[token]), "cmudict", "high", []
    parts = decompose(token, lex)
    if parts:
        second = [p.replace("1", "2") if p[-1:] == "1" else p for p in lex.words[parts[1]]]
        phones = list(lex.words[parts[0]]) + second
        return (phones, "cmudict-compound", "medium",
                ['"{0}" is not in the dictionary; read as the compound "{1}" + "{2}"'.format(
                    token, parts[0], parts[1])])
    return (g2p(token), "g2p", "low",
            ['"{0}" is not in the dictionary; pronunciation inferred by rule-based g2p '
             '— treat as low confidence'.format(token)])


_SOURCE_RANK = {"cmudict": 0, "cmudict-compound": 1, "g2p": 2}
_CONFIDENCE_RANK = {"high": 0, "medium": 1, "low": 2}


def normalize(name: str) -> Tuple[str, List[str]]:
    """-> (normalized display string, token list)

    Multi-word and hyphenated input is supported: each token is looked up
    separately and the phoneme strings are concatenated, which is also how the
    syllabification is done (syllables never straddle a word boundary).
    """
    cleaned = []
    for ch in name.lower():
        if ch.isalpha() and ch.isascii():
            cleaned.append(ch)
        elif ch.isspace() or ch in "-_/&+.":
            cleaned.append(" ")
    normalized = " ".join("".join(cleaned).split())
    return normalized, [t for t in normalized.split(" ") if t]


def analyze(name: str, lex: Optional[Lexicon] = None) -> Dict[str, object]:
    """Measure one candidate name. Returns the full contract object."""
    if lex is None:
        lex = get_lexicon()
    normalized, tokens = normalize(name)
    warnings: List[str] = []

    if not tokens:
        warnings.append("input contains no alphabetic characters; nothing to measure")

    phones: List[str] = []
    token_phones: List[List[str]] = []
    sylls: List[Syllable] = []
    source, confidence = "cmudict", "high"
    for tok in tokens:
        tp, tsrc, tconf, twarn = resolve_token(tok, lex)
        warnings.extend(twarn)
        token_phones.append(tp)
        phones.extend(tp)
        sylls.extend(syllabify(tp))
        if _SOURCE_RANK[tsrc] > _SOURCE_RANK[source]:
            source = tsrc
        if _CONFIDENCE_RANK[tconf] > _CONFIDENCE_RANK[confidence]:
            confidence = tconf
    if not tokens:
        source, confidence = "g2p", "low"

    has_nucleus = any(s.nucleus is not None for s in sylls)
    if sylls and not has_nucleus:
        warnings.append("no vowel nucleus: the name has no syllable an English "
                        "speaker can produce")

    phonotactics = check_phonotactics(sylls)
    stress = stress_profile(sylls)
    letters_only = normalized.replace(" ", "")

    # -- neighbourhood -----------------------------------------------------
    key = strip_stress_seq(phones)
    if key:
        neighbor_words = lex.neighbors(key, exclude=set(tokens) | {letters_only})
    else:
        neighbor_words = []
    density = len(neighbor_words)
    percentile = lex.percentile(density)
    coverage = "complete" if len(key) <= lex.max_phonemes - 1 else "truncated"
    if coverage == "truncated":
        warnings.append(
            "{0} phonemes exceeds the lexicon's {1}-phoneme cutoff, so neighbours one "
            "insertion longer are not represented; density is a lower bound".format(
                len(key), lex.max_phonemes))

    # -- orthography -------------------------------------------------------
    amb = ambiguous_graphemes(letters_only)
    homo = homophone_spellings(tokens) if tokens else []
    rare_present = [c for c in RARE_LETTERS if c in letters_only]
    rlcs = rare_letter_common_sound(letters_only, phones, phonotactics, has_nucleus)

    intl = international_profile(phones, sylls)

    clips = clip_candidates(letters_only) if len(tokens) == 1 else []
    ends_vowel = bool(phones) and is_vowel(phones[-1])

    ctx = {
        "syllables": sylls,
        "phonotactics": phonotactics,
        "has_nucleus": has_nucleus,
        "ambiguous": amb,
        "homophones": homo,
        "rare_letter_common_sound": rlcs,
        "rare_letters": rare_present,
        "letters_only": letters_only,
        "percentile": percentile,
        "density": density,
        "stress": stress,
        "clips": clips,
        "ends_in_vowel": ends_vowel,
        "in_lexicon": all(t in lex.words for t in tokens) if tokens else False,
        "international": intl,
    }
    dims = _dimensions(ctx)
    ergonomics = int(round(sum(d["score"] for d in dims.values()) / float(len(dims))))

    return {
        "schema_version": SCHEMA_VERSION,
        "input": name,
        "normalized": normalized,
        "pronunciation": {
            "source": source,
            "confidence": confidence,
            "arpabet": list(phones),
            "ipa": " ".join(to_ipa(tp) for tp in token_phones),
        },
        "syllables": {
            "count": len(sylls),
            "structures": [s.structure for s in sylls],
            "onsets": [[strip_stress(p) for p in s.onset] for s in sylls],
            "codas": [[strip_stress(p) for p in s.coda] for s in sylls],
        },
        "stress": stress,
        "phonotactics": phonotactics,
        "orthography": {
            "letters": len(letters_only),
            "rare_letters": rare_present,
            "rare_letter_common_sound": rlcs,
            "ambiguous_graphemes": amb,
            "homophone_spellings": homo,
        },
        "neighborhood": {
            "density": density,
            "neighbors": neighbor_words[:MAX_NEIGHBORS],
            "percentile": percentile,
            "coverage": coverage,
        },
        "international": {
            "hard_phonemes": intl["hard_phonemes"],
            "affected_languages": intl["affected_languages"],
            "risk": intl["risk"],
        },
        "verbability": {
            "syllable_count": len(sylls),
            "ends_in_vowel": ends_vowel,
            "clippable_to": clips,
            "verb_form": "to {0}".format(normalized) if normalized else "",
            "agentive": agentive_form(letters_only, len(sylls)),
        },
        "dimensions": dims,
        "ergonomics_score": ergonomics,
        "warnings": warnings,
    }


# ===========================================================================
# 9. CLI
# ===========================================================================

def read_name_file(path: str) -> List[str]:
    names: List[str] = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.split("#", 1)[0].strip()
            if line:
                names.append(line)
    return names


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        prog="phonetics.py",
        description="Deterministic phonetic measurement for brand-name-critic. "
                    "Emits one JSON object per name (a JSON array for more than one).")
    ap.add_argument("names", nargs="*", help="candidate names")
    ap.add_argument("--file", help="read names from PATH, one per line; '#' starts a comment")
    ap.add_argument("--pretty", action="store_true", help="indent the JSON output")
    ap.add_argument("--version", action="version",
                    version="phonetics.py {0} (schema {1})".format(TOOL_VERSION, SCHEMA_VERSION))
    args = ap.parse_args(argv)

    names = list(args.names)
    if args.file:
        names.extend(read_name_file(args.file))
    if not names:
        ap.error("no names given; pass names as arguments or use --file")

    lex = get_lexicon()
    results = [analyze(n, lex) for n in names]
    payload: object = results[0] if len(results) == 1 else results
    kwargs = {"ensure_ascii": False, "sort_keys": False}
    if args.pretty:
        kwargs["indent"] = 2
    else:
        kwargs["separators"] = (",", ":")
    sys.stdout.write(json.dumps(payload, **kwargs))  # type: ignore[arg-type]
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
