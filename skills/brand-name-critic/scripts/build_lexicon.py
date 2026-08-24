#!/usr/bin/env python3
"""build_lexicon.py — reproducible generator for the vendored lexicon.

This is a BUILD-TIME script. It is the only place the `cmudict` pip package is
imported. `phonetics.py` never imports it and never touches the network; at run
time the vendored `data/lexicon.txt.gz` is the sole data source.

    pip install cmudict
    python3 build_lexicon.py                 # rebuild data/lexicon.txt.gz
    python3 build_lexicon.py --measure-g2p   # measure the g2p fallback only

Filtering rules
---------------
1. Keys must be lowercase a-z only. This drops apostrophes ("'bout"), hyphens,
   periods (abbreviations) and digits.
2. CMUdict's `(2)`/`(3)` alternate-pronunciation duplicate keys are dropped; the
   first pronunciation for each word is kept. (`cmudict.dict()` already groups
   alternates under one key as a list, so "keep the first" is `prons[0]`.)
3. Entries with more than MAX_PHONEMES (10) phonemes are dropped.

Why the <=10 phoneme cutoff
---------------------------
Neighbourhood density counts real words one phoneme edit away. A one-edit
neighbour of an N-phoneme name has N-1, N, or N+1 phonemes and nothing else, so
the index only ever needs those three length buckets. With a cutoff of 10, every
name of up to **9 phonemes** has complete neighbourhood coverage: its N+1 bucket
is fully represented. A name of 10 or more phonemes would need an 11+ bucket that
was filtered out, so those names report `"coverage": "truncated"` rather than
quietly under-counting. The cutoff exists because the tail past 10 phonemes is
almost entirely long inflected forms and technical vocabulary that no brand name
is a neighbour of, and dropping it takes the file from ~1MB to ~700KB.

Determinism
-----------
Output is sorted and written with `mtime=0` in the gzip header, so two rebuilds
from the same CMUdict release are byte-identical.
"""

from __future__ import annotations

import argparse
import gzip
import os
import random
import re
import sys
from typing import Dict, List, Sequence, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "data", "lexicon.txt.gz")

MAX_PHONEMES = 10
FORMAT_VERSION = 1

# Density histogram: every SAMPLE_STRIDE-th word of the sorted lexicon. A stride
# rather than a random draw, so no seed is involved and the sample is a stable
# function of the lexicon itself.
SAMPLE_TARGET = 8000

# g2p measurement: a seeded random sample. Seeded, so the published number is
# reproducible; random, so it is not biased toward the front of the alphabet.
G2P_SAMPLE_SEED = 20260824
G2P_SAMPLE_SIZE = 2500

WORD_RE = re.compile(r"^[a-z]+$")

sys.path.insert(0, HERE)
import phonetics  # noqa: E402  (local, standard-library-only module)


# ---------------------------------------------------------------------------
# 1. Extract and filter
# ---------------------------------------------------------------------------

def load_cmudict() -> List[Tuple[str, Tuple[str, ...]]]:
    try:
        import cmudict  # type: ignore
    except ImportError:
        raise SystemExit(
            "cmudict is not installed. This is a BUILD-time dependency only:\n"
            "    pip install cmudict"
        )
    raw = cmudict.dict()
    total = len(raw)
    kept: List[Tuple[str, Tuple[str, ...]]] = []
    dropped_shape = 0
    dropped_length = 0
    for word in sorted(raw):
        if not WORD_RE.match(word):
            dropped_shape += 1
            continue
        pron = tuple(raw[word][0])          # first pronunciation wins
        if len(pron) > MAX_PHONEMES:
            dropped_length += 1
            continue
        kept.append((word, pron))
    print("cmudict entries (alternates already grouped): {0}".format(total))
    print("  dropped, not lowercase a-z only:            {0}".format(dropped_shape))
    print("  dropped, more than {0} phonemes:             {1}".format(
        MAX_PHONEMES, dropped_length))
    print("  kept:                                       {0}".format(len(kept)))
    return kept


# ---------------------------------------------------------------------------
# 2. Density histogram
# ---------------------------------------------------------------------------

def density_histogram(entries: Sequence[Tuple[str, Tuple[str, ...]]]) -> Dict[int, int]:
    lex = phonetics.Lexicon.from_entries(entries, MAX_PHONEMES)
    stride = max(1, len(entries) // SAMPLE_TARGET)
    hist: Dict[int, int] = {}
    n = 0
    for i in range(0, len(entries), stride):
        word, pron = entries[i]
        key = phonetics.strip_stress_seq(pron)
        density = len(lex.neighbors(key, exclude={word}))
        hist[density] = hist.get(density, 0) + 1
        n += 1
        if n % 1000 == 0:
            print("  sampled {0} words...".format(n), file=sys.stderr)
    print("density sample: {0} words (stride {1}), densities {2}-{3}".format(
        n, stride, min(hist), max(hist)))
    return hist


# ---------------------------------------------------------------------------
# 3. Emit
# ---------------------------------------------------------------------------

def write_lexicon(entries: Sequence[Tuple[str, Tuple[str, ...]]],
                  hist: Dict[int, int], path: str = OUT_PATH) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    hist_str = " ".join("{0}:{1}".format(d, hist[d]) for d in sorted(hist))
    lines = [
        "#lingua-lexicon\t{0}".format(FORMAT_VERSION),
        "#entries\t{0}".format(len(entries)),
        "#max-phonemes\t{0}".format(MAX_PHONEMES),
        "#density-sample\t{0}".format(sum(hist.values())),
        "#density-histogram\t{0}".format(hist_str),
    ]
    lines.extend("{0}\t{1}".format(w, " ".join(p)) for w, p in entries)
    payload = ("\n".join(lines) + "\n").encode("utf-8")
    # mtime=0 and a fixed compresslevel make the artifact byte-stable.
    with open(path, "wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw,
                           compresslevel=9, mtime=0) as gz:
            gz.write(payload)
    size = os.path.getsize(path)
    print("wrote {0}  ({1} entries, {2:.1f} KB gzipped)".format(
        path, len(entries), size / 1024.0))


# ---------------------------------------------------------------------------
# 4. g2p accuracy measurement (PRD open question 2)
# ---------------------------------------------------------------------------

def _levenshtein(a: Sequence[str], b: Sequence[str]) -> int:
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def _score(sample: Sequence[Tuple[str, Tuple[str, ...]]]) -> Dict[str, float]:
    exact = 0
    edits = 0
    ref_len = 0
    for word, ref in sample:
        hyp = list(phonetics.strip_stress_seq(phonetics.g2p(word)))
        r = list(phonetics.strip_stress_seq(ref))
        if hyp == r:
            exact += 1
        edits += _levenshtein(r, hyp)
        ref_len += len(r)
    n = max(1, len(sample))
    return {"n": len(sample),
            "exact": 100.0 * exact / n,
            "per_phoneme": 100.0 * (1.0 - edits / float(max(1, ref_len)))}


def measure_g2p(entries: Sequence[Tuple[str, Tuple[str, ...]]]) -> Dict[str, float]:
    """Hold out a seeded random sample and score the rule-based g2p on it."""
    rng = random.Random(G2P_SAMPLE_SEED)
    pool = list(entries)
    sample = rng.sample(pool, min(G2P_SAMPLE_SIZE, len(pool)))
    sample.sort()

    exact_nostress = 0
    exact_stress = 0
    total_ref = 0
    total_edits = 0
    len_exact = 0
    for word, ref in sample:
        hyp = phonetics.g2p(word)
        ref_ns = list(phonetics.strip_stress_seq(ref))
        hyp_ns = list(phonetics.strip_stress_seq(hyp))
        if hyp_ns == ref_ns:
            exact_nostress += 1
        if list(hyp) == list(ref):
            exact_stress += 1
        if len(hyp_ns) == len(ref_ns):
            len_exact += 1
        total_edits += _levenshtein(ref_ns, hyp_ns)
        total_ref += len(ref_ns)

    n = len(sample)
    per = total_edits / float(total_ref)
    short = _score([x for x in sample if len(x[0]) <= 6])
    medium = _score([x for x in sample if 7 <= len(x[0]) <= 9])
    long_ = _score([x for x in sample if len(x[0]) >= 10])
    return {
        "short_n": short["n"], "short_exact": short["exact"],
        "short_per_phoneme": short["per_phoneme"],
        "medium_n": medium["n"], "medium_exact": medium["exact"],
        "medium_per_phoneme": medium["per_phoneme"],
        "long_n": long_["n"], "long_exact": long_["exact"],
        "long_per_phoneme": long_["per_phoneme"],
        "sample_size": n,
        "seed": G2P_SAMPLE_SEED,
        "exact_match_no_stress": 100.0 * exact_nostress / n,
        "exact_match_with_stress": 100.0 * exact_stress / n,
        "phoneme_error_rate": 100.0 * per,
        "per_phoneme_accuracy": 100.0 * (1.0 - per),
        "length_match": 100.0 * len_exact / n,
    }


def print_measurement(m: Dict[str, float]) -> None:
    print("")
    print("g2p accuracy — held-out CMUdict sample")
    print("  sample size ..................... {0:.0f} words (seed {1:.0f})".format(
        m["sample_size"], m["seed"]))
    print("  exact phoneme-string match ...... {0:.1f}%  (stress ignored)".format(
        m["exact_match_no_stress"]))
    print("  exact phoneme-string match ...... {0:.1f}%  (stress included)".format(
        m["exact_match_with_stress"]))
    print("  per-phoneme accuracy ............ {0:.1f}%  (1 - phoneme error rate)".format(
        m["per_phoneme_accuracy"]))
    print("  phoneme error rate .............. {0:.1f}%".format(m["phoneme_error_rate"]))
    print("  correct phoneme count ........... {0:.1f}%".format(m["length_match"]))
    print("")
    print("  by word length (brand names live in the first row)")
    print("    <=6 letters  n={0:<5.0f} exact {1:5.1f}%   per-phoneme {2:5.1f}%".format(
        m["short_n"], m["short_exact"], m["short_per_phoneme"]))
    print("    7-9 letters  n={0:<5.0f} exact {1:5.1f}%   per-phoneme {2:5.1f}%".format(
        m["medium_n"], m["medium_exact"], m["medium_per_phoneme"]))
    print("    10+ letters  n={0:<5.0f} exact {1:5.1f}%   per-phoneme {2:5.1f}%".format(
        m["long_n"], m["long_exact"], m["long_per_phoneme"]))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=OUT_PATH, help="output path")
    ap.add_argument("--measure-g2p", action="store_true",
                    help="only measure g2p accuracy; do not rebuild the lexicon")
    ap.add_argument("--skip-measure", action="store_true",
                    help="rebuild the lexicon without the g2p measurement pass")
    args = ap.parse_args(argv)

    entries = load_cmudict()
    if args.measure_g2p:
        print_measurement(measure_g2p(entries))
        return 0
    hist = density_histogram(entries)
    write_lexicon(entries, hist, args.out)
    if not args.skip_measure:
        print_measurement(measure_g2p(entries))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
