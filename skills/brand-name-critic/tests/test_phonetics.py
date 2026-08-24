#!/usr/bin/env python3
"""Tests for phonetics.py — plain unittest, no pytest, no third-party imports.

    cd skills/brand-name-critic
    python3 -m unittest discover -s tests -v
"""

import json
import os
import subprocess
import sys
import time
import unittest

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(TESTS_DIR)
SCRIPTS_DIR = os.path.join(SKILL_DIR, "scripts")
SCRIPT = os.path.join(SCRIPTS_DIR, "phonetics.py")
BENCHMARK = os.path.join(TESTS_DIR, "benchmark.txt")

sys.path.insert(0, SCRIPTS_DIR)
import phonetics  # noqa: E402


def run_cli(*args):
    proc = subprocess.run([sys.executable, SCRIPT] + list(args),
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise AssertionError(proc.stderr.decode("utf-8"))
    return proc.stdout


class Base(unittest.TestCase):
    """Shared, analysed once: the lexicon load is the expensive part."""

    lex = None
    results = None

    @classmethod
    def setUpClass(cls):
        if Base.lex is None:
            Base.lex = phonetics.get_lexicon()
            names = phonetics.read_name_file(BENCHMARK)
            Base.results = {n: phonetics.analyze(n, Base.lex) for n in names}
        cls.lex = Base.lex
        cls.results = Base.results

    def r(self, name):
        return self.results[name]


# ---------------------------------------------------------------------------

class TestBenchmarkFile(Base):

    def test_benchmark_has_twenty_names(self):
        self.assertEqual(len(phonetics.read_name_file(BENCHMARK)), 20)

    def test_prd_names_present(self):
        names = set(phonetics.read_name_file(BENCHMARK))
        for expected in ("Scout", "Stripe", "Notion", "Xerox", "Kodak", "Zillow",
                         "Flickr", "Palantir", "Slack", "Figma", "Lingua", "Xzrq"):
            self.assertIn(expected, names)


class TestDeterminism(Base):

    def test_two_cli_runs_are_byte_identical(self):
        a = run_cli("--file", BENCHMARK)
        b = run_cli("--file", BENCHMARK)
        self.assertEqual(a, b)

    def test_pretty_runs_are_byte_identical(self):
        a = run_cli("--file", BENCHMARK, "--pretty")
        b = run_cli("--file", BENCHMARK, "--pretty")
        self.assertEqual(a, b)

    def test_in_process_matches_cli(self):
        cli = json.loads(run_cli("Scout").decode("utf-8"))
        self.assertEqual(cli, phonetics.analyze("Scout", self.lex))

    def test_batch_order_is_input_order(self):
        out = json.loads(run_cli("Xzrq", "Scout", "Lingua").decode("utf-8"))
        self.assertEqual([o["input"] for o in out], ["Xzrq", "Scout", "Lingua"])


class TestSchema(Base):
    """Every key in the BUILD-MAP §3 contract, correct type, never omitted."""

    DIMENSIONS = ("pronounceability", "spellability", "distinctiveness",
                  "rhythm_recall", "verbability", "international_robustness")

    def check(self, obj, name):
        def has(container, key, types, path):
            self.assertIn(key, container, "{0}: missing {1}".format(name, path))
            self.assertIsInstance(container[key], types,
                                  "{0}: {1} has type {2}".format(
                                      name, path, type(container[key]).__name__))
            return container[key]

        has(obj, "schema_version", str, "schema_version")
        self.assertEqual(obj["schema_version"], "1.0")
        has(obj, "input", str, "input")
        has(obj, "normalized", str, "normalized")

        p = has(obj, "pronunciation", dict, "pronunciation")
        self.assertIn(has(p, "source", str, "pronunciation.source"),
                      ("cmudict", "g2p", "cmudict-compound"))
        self.assertIn(has(p, "confidence", str, "pronunciation.confidence"),
                      ("high", "medium", "low"))
        for ph in has(p, "arpabet", list, "pronunciation.arpabet"):
            self.assertIsInstance(ph, str)
        has(p, "ipa", str, "pronunciation.ipa")

        s = has(obj, "syllables", dict, "syllables")
        count = has(s, "count", int, "syllables.count")
        for key in ("structures", "onsets", "codas"):
            val = has(s, key, list, "syllables." + key)
            self.assertEqual(len(val), count,
                             "{0}: syllables.{1} length != count".format(name, key))
        for st in s["structures"]:
            self.assertIsInstance(st, str)
            self.assertEqual(set(st) - set("CV"), set())
        for group in s["onsets"] + s["codas"]:
            self.assertIsInstance(group, list)
            for ph in group:
                self.assertIsInstance(ph, str)

        st = has(obj, "stress", dict, "stress")
        has(st, "pattern", str, "stress.pattern")
        has(st, "primary_syllable", int, "stress.primary_syllable")
        has(st, "shape", str, "stress.shape")

        pt = has(obj, "phonotactics", dict, "phonotactics")
        for key in ("illegal_clusters", "sonority_violations"):
            for item in has(pt, key, list, "phonotactics." + key):
                self.assertIsInstance(item, dict)
                for f in ("cluster", "position", "syllable", "note"):
                    self.assertIn(f, item)
        has(pt, "max_onset_length", int, "phonotactics.max_onset_length")
        has(pt, "max_coda_length", int, "phonotactics.max_coda_length")

        o = has(obj, "orthography", dict, "orthography")
        has(o, "letters", int, "orthography.letters")
        has(o, "rare_letters", list, "orthography.rare_letters")
        self.assertIn("rare_letter_common_sound", o)
        self.assertIn(o["rare_letter_common_sound"], (True, False, None))
        for item in has(o, "ambiguous_graphemes", list, "orthography.ambiguous_graphemes"):
            self.assertIsInstance(item, dict)
            for f in ("grapheme", "positions", "readings", "note"):
                self.assertIn(f, item)
        for item in has(o, "homophone_spellings", list, "orthography.homophone_spellings"):
            self.assertIsInstance(item, str)

        n = has(obj, "neighborhood", dict, "neighborhood")
        has(n, "density", int, "neighborhood.density")
        neighbors = has(n, "neighbors", list, "neighborhood.neighbors")
        self.assertLessEqual(len(neighbors), 12)
        self.assertEqual(neighbors, sorted(neighbors))
        pct = has(n, "percentile", int, "neighborhood.percentile")
        self.assertTrue(0 <= pct <= 100)
        self.assertIn(has(n, "coverage", str, "neighborhood.coverage"),
                      ("complete", "truncated"))

        i = has(obj, "international", dict, "international")
        has(i, "hard_phonemes", list, "international.hard_phonemes")
        has(i, "affected_languages", list, "international.affected_languages")
        self.assertIn(has(i, "risk", str, "international.risk"), ("low", "medium", "high"))
        self.assertNotIn("_weight", i, "internal weight leaked into the contract")

        v = has(obj, "verbability", dict, "verbability")
        has(v, "syllable_count", int, "verbability.syllable_count")
        has(v, "ends_in_vowel", bool, "verbability.ends_in_vowel")
        has(v, "clippable_to", list, "verbability.clippable_to")
        has(v, "verb_form", str, "verbability.verb_form")
        has(v, "agentive", str, "verbability.agentive")

        d = has(obj, "dimensions", dict, "dimensions")
        self.assertEqual(set(d), set(self.DIMENSIONS))
        for key in self.DIMENSIONS:
            dim = d[key]
            self.assertIsInstance(dim, dict)
            score = dim["score"]
            self.assertIsInstance(score, int)
            self.assertTrue(0 <= score <= 100, "{0}: {1} = {2}".format(name, key, score))
            self.assertIsInstance(dim["evidence"], list)
            self.assertTrue(dim["evidence"], "{0}: {1} has no evidence".format(name, key))
            for e in dim["evidence"]:
                self.assertIsInstance(e, str)

        erg = has(obj, "ergonomics_score", int, "ergonomics_score")
        self.assertTrue(0 <= erg <= 100)
        for w in has(obj, "warnings", list, "warnings"):
            self.assertIsInstance(w, str)

    def test_every_benchmark_name_matches_the_contract(self):
        for name, obj in self.results.items():
            with self.subTest(name=name):
                self.check(obj, name)

    def test_coined_g2p_names_also_match_the_contract(self):
        for name in ("Zephyrq", "Blivvox", "Qwintara", "Xzrq", "Vzzt"):
            with self.subTest(name=name):
                self.check(phonetics.analyze(name, self.lex), name)

    def test_ergonomics_is_the_equal_weight_mean_of_the_six(self):
        for name, obj in self.results.items():
            scores = [d["score"] for d in obj["dimensions"].values()]
            self.assertEqual(len(scores), 6)
            self.assertEqual(obj["ergonomics_score"],
                             int(round(sum(scores) / 6.0)), name)

    def test_no_cross_layer_composite_is_emitted(self):
        blob = json.dumps(self.r("Scout"))
        for forbidden in ("brandability", "practicality", "overall", "verdict",
                          "recommendation"):
            self.assertNotIn(forbidden, blob)

    def test_json_round_trips(self):
        for name, obj in self.results.items():
            self.assertEqual(json.loads(json.dumps(obj)), obj, name)


class TestKnownPronunciations(Base):

    def test_scout(self):
        r = self.r("Scout")
        self.assertEqual(r["pronunciation"]["arpabet"], ["S", "K", "AW1", "T"])
        self.assertEqual(r["pronunciation"]["source"], "cmudict")
        self.assertEqual(r["pronunciation"]["confidence"], "high")
        self.assertEqual(r["syllables"]["count"], 1)
        self.assertEqual(r["syllables"]["structures"], ["CCVC"])
        self.assertEqual(r["syllables"]["onsets"], [["S", "K"]])
        self.assertEqual(r["syllables"]["codas"], [["T"]])
        self.assertEqual(r["stress"]["shape"], "monosyllable")

    def test_stripe(self):
        r = self.r("Stripe")
        self.assertEqual(r["pronunciation"]["arpabet"], ["S", "T", "R", "AY1", "P"])
        self.assertEqual(r["syllables"]["count"], 1)
        self.assertEqual(r["syllables"]["onsets"], [["S", "T", "R"]])

    def test_lingua_is_two_syllables_trochaic(self):
        r = self.r("Lingua")
        self.assertEqual(r["syllables"]["count"], 2)
        self.assertEqual(r["stress"]["pattern"], "10")
        self.assertTrue(r["stress"]["shape"].startswith("trochee"))
        self.assertEqual(r["phonotactics"]["illegal_clusters"], [])
        self.assertEqual(r["phonotactics"]["sonority_violations"], [])
        self.assertEqual(r["orthography"]["ambiguous_graphemes"], [])

    def test_ipa_is_produced(self):
        self.assertEqual(self.r("Scout")["pronunciation"]["ipa"], "skaʊt")


class TestPhonotactics(Base):
    """The /s/+stop onset exception, and the rules it must not disable."""

    def test_sk_and_st_onsets_do_not_fire_a_sonority_violation(self):
        for name in ("Scout", "Stripe"):
            with self.subTest(name=name):
                r = self.r(name)
                self.assertEqual(r["phonotactics"]["sonority_violations"], [],
                                 "/s/+stop must be the licensed exception")
                self.assertEqual(r["phonotactics"]["illegal_clusters"], [])

    def test_s_stop_exception_covers_the_whole_family(self):
        for cluster in (["S", "P"], ["S", "T"], ["S", "K"], ["S", "P", "L"],
                        ["S", "T", "R"], ["S", "K", "R"], ["S", "P", "R"],
                        ["S", "K", "W"]):
            syl = phonetics.Syllable(cluster, "AA1", [])
            pt = phonetics.check_phonotactics([syl])
            with self.subTest(cluster=cluster):
                self.assertEqual(pt["sonority_violations"], [])
                self.assertEqual(pt["illegal_clusters"], [])

    def test_named_legal_onsets_are_all_present(self):
        required = [("S", "T", "R"), ("S", "P", "L"), ("S", "K", "R"), ("S", "K"),
                    ("S", "T"), ("S", "P"), ("P", "L"), ("P", "R"), ("B", "L"),
                    ("B", "R"), ("T", "R"), ("D", "R"), ("K", "L"), ("K", "R"),
                    ("G", "L"), ("G", "R"), ("F", "L"), ("F", "R"), ("TH", "R"),
                    ("SH", "R"), ("S", "L"), ("S", "M"), ("S", "N"), ("S", "W"),
                    ("T", "W"), ("K", "W"), ("D", "W"), ("HH", "W")]
        for onset in required:
            self.assertIn(onset, phonetics.LEGAL_ONSETS, str(onset))
        for c in phonetics.CONSONANTS:
            if c != "NG":
                self.assertIn((c,), phonetics.LEGAL_ONSETS, c)

    def test_thrixthwaite_onsets_are_legal(self):
        r = self.r("Thrixthwaite")
        self.assertEqual(r["phonotactics"]["illegal_clusters"], [],
                         "/thr/ and /thw/ are attested; flagging them is a false positive")

    def test_illegal_onset_is_reported_with_the_offending_cluster(self):
        r = self.r("Xzrq")
        illegal = r["phonotactics"]["illegal_clusters"]
        self.assertTrue(illegal)
        self.assertEqual(illegal[0]["cluster"], ["Z", "Z", "R", "K"])
        self.assertEqual(illegal[0]["position"], "onset")

    def test_sonority_rises_in_onsets_and_falls_in_codas(self):
        rising = phonetics.check_phonotactics(
            [phonetics.Syllable(["R", "K"], "AA1", [])])
        self.assertTrue(rising["sonority_violations"])
        falling = phonetics.check_phonotactics(
            [phonetics.Syllable(["K", "R"], "AA1", ["N", "T"])])
        self.assertEqual(falling["sonority_violations"], [])
        bad_coda = phonetics.check_phonotactics(
            [phonetics.Syllable(["K"], "AA1", ["T", "R"])])
        self.assertTrue(bad_coda["sonority_violations"])

    def test_initial_ng_is_not_a_legal_onset(self):
        self.assertNotIn(("NG",), phonetics.LEGAL_ONSETS)

    def test_no_vowel_still_yields_one_defective_syllable(self):
        r = self.r("Xzrq")
        self.assertEqual(r["syllables"]["count"], 1)
        self.assertEqual(r["syllables"]["structures"], ["CCCC"])
        self.assertEqual(r["stress"]["shape"], "no vowel nucleus")
        self.assertTrue(any("no vowel nucleus" in w for w in r["warnings"]))


class TestRareLetterCommonSound(Base):

    def test_xerox_is_the_sweet_spot(self):
        self.assertIs(self.r("Xerox")["orthography"]["rare_letter_common_sound"], True)

    def test_zillow_is_the_sweet_spot(self):
        self.assertIs(self.r("Zillow")["orthography"]["rare_letter_common_sound"], True)

    def test_xzrq_is_not(self):
        self.assertIs(self.r("Xzrq")["orthography"]["rare_letter_common_sound"], False)

    def test_scout_has_no_rare_letter_so_the_test_does_not_apply(self):
        r = self.r("Scout")
        self.assertIsNone(r["orthography"]["rare_letter_common_sound"])
        self.assertEqual(r["orthography"]["rare_letters"], [])

    def test_rare_letters_are_listed_when_present(self):
        self.assertEqual(self.r("Xerox")["orthography"]["rare_letters"], ["x"])
        self.assertEqual(self.r("Xzrq")["orthography"]["rare_letters"], ["q", "x", "z"])

    def test_the_sweet_spot_pays_off_in_distinctiveness(self):
        xerox = self.r("Xerox")["dimensions"]["distinctiveness"]["score"]
        self.assertTrue(any("rare letters, common sounds" in e
                            for e in self.r("Xerox")["dimensions"]["distinctiveness"]["evidence"]))
        self.assertGreater(xerox, self.r("Cat")["dimensions"]["distinctiveness"]["score"])


class TestOrthography(Base):

    def test_ambiguous_graphemes_come_from_the_table(self):
        self.assertIn("ou", [a["grapheme"] for a in
                             self.r("Scout")["orthography"]["ambiguous_graphemes"]])
        self.assertIn("ti", [a["grapheme"] for a in
                             self.r("Notion")["orthography"]["ambiguous_graphemes"]])
        self.assertIn("x", [a["grapheme"] for a in
                            self.r("Xerox")["orthography"]["ambiguous_graphemes"]])

    def test_repeated_grapheme_is_one_entry_with_two_positions(self):
        entries = self.r("Xerox")["orthography"]["ambiguous_graphemes"]
        x = [a for a in entries if a["grapheme"] == "x"][0]
        self.assertEqual(len(x["positions"]), 2)

    def test_homophones_are_sorted_capped_and_exclude_the_name(self):
        for name, obj in self.results.items():
            homo = obj["orthography"]["homophone_spellings"]
            with self.subTest(name=name):
                self.assertEqual(homo, sorted(homo))
                self.assertLessEqual(len(homo), phonetics.MAX_HOMOPHONES)
                self.assertNotIn(obj["normalized"], homo)

    def test_homophones_read_back_as_the_same_word(self):
        for name in ("Scout", "Xerox", "Lingua"):
            obj = self.r(name)
            target = phonetics.strip_stress_seq(
                sum((phonetics.g2p(t) for t in obj["normalized"].split()), []))
            for cand in obj["orthography"]["homophone_spellings"]:
                read = phonetics.strip_stress_seq(
                    sum((phonetics.g2p(t) for t in cand.split()), []))
                self.assertEqual(read, target, "{0} -> {1}".format(name, cand))

    def test_scout_generates_the_ow_misspelling(self):
        self.assertIn("scowt", self.r("Scout")["orthography"]["homophone_spellings"])


class TestNeighborhood(Base):

    def test_dense_name_beats_sparse_coined_name(self):
        dense = self.r("Cat")["neighborhood"]
        sparse = self.r("Xzrq")["neighborhood"]
        self.assertGreater(dense["density"], sparse["density"])
        self.assertGreater(dense["percentile"], sparse["percentile"])

    def test_dense_name_beats_a_sparse_real_name(self):
        self.assertGreater(self.r("Cat")["neighborhood"]["density"],
                           self.r("Lingua")["neighborhood"]["density"])

    def test_density_is_lower_for_the_distinctive_names(self):
        self.assertLess(self.r("Cat")["dimensions"]["distinctiveness"]["score"],
                        self.r("Lingua")["dimensions"]["distinctiveness"]["score"])

    def test_neighbors_are_real_lexicon_words(self):
        for name, obj in self.results.items():
            for w in obj["neighborhood"]["neighbors"]:
                self.assertIn(w, self.lex.words, "{0}: {1}".format(name, w))

    def test_neighbors_are_one_edit_away(self):
        obj = self.r("Cat")
        key = phonetics.strip_stress_seq(obj["pronunciation"]["arpabet"])
        for w in obj["neighborhood"]["neighbors"]:
            other = phonetics.strip_stress_seq(self.lex.words[w])
            self.assertEqual(_edit_distance(key, other), 1, w)

    def test_coverage_is_complete_for_short_names_truncated_for_long(self):
        self.assertEqual(self.r("Scout")["neighborhood"]["coverage"], "complete")
        long_name = phonetics.analyze("Constantinopolitan", self.lex)
        self.assertEqual(long_name["neighborhood"]["coverage"], "truncated")
        self.assertTrue(any("lower bound" in w for w in long_name["warnings"]))

    def test_percentile_is_monotone_in_density(self):
        last = -1
        for d in range(0, 60):
            p = self.lex.percentile(d)
            self.assertGreaterEqual(p, last)
            last = p


def _edit_distance(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


class TestMultiWord(Base):

    def test_base_camp(self):
        r = self.r("Base Camp")
        self.assertEqual(r["normalized"], "base camp")
        self.assertEqual(r["pronunciation"]["arpabet"],
                         ["B", "EY1", "S", "K", "AE1", "M", "P"])
        self.assertEqual(r["pronunciation"]["source"], "cmudict")
        self.assertEqual(r["syllables"]["count"], 2)
        self.assertEqual(r["orthography"]["letters"], 8)

    def test_syllables_do_not_straddle_the_word_boundary(self):
        r = self.r("Base Camp")
        self.assertEqual(r["syllables"]["onsets"], [["B"], ["K"]])
        self.assertEqual(r["syllables"]["codas"], [["S"], ["M", "P"]])

    def test_hyphen_is_treated_as_a_word_boundary(self):
        hyphen = phonetics.analyze("Base-Camp", self.lex)
        space = self.r("Base Camp")
        self.assertEqual(hyphen["pronunciation"]["arpabet"],
                         space["pronunciation"]["arpabet"])
        self.assertEqual(hyphen["ergonomics_score"], space["ergonomics_score"])

    def test_cli_accepts_a_quoted_multiword_name(self):
        out = json.loads(run_cli("Base Camp").decode("utf-8"))
        self.assertEqual(out["normalized"], "base camp")


class TestFallbacks(Base):

    def test_unknown_name_uses_g2p_and_says_so(self):
        r = self.r("Figma")
        self.assertEqual(r["pronunciation"]["source"], "g2p")
        self.assertEqual(r["pronunciation"]["confidence"], "low")
        self.assertTrue(any("g2p" in w for w in r["warnings"]))

    def test_g2p_still_returns_every_key(self):
        obj = phonetics.analyze("Qwintara", self.lex)
        self.assertEqual(obj["pronunciation"]["source"], "g2p")
        self.assertTrue(obj["pronunciation"]["arpabet"])
        self.assertTrue(obj["dimensions"])
        self.assertTrue(obj["warnings"])

    def test_compound_decomposition_is_tried_before_g2p(self):
        parts = phonetics.decompose("wavebreak", self.lex)
        self.assertEqual(parts, ("wave", "break"))
        obj = phonetics.analyze("Wavebreak", self.lex)
        self.assertEqual(obj["pronunciation"]["source"], "cmudict-compound")
        self.assertEqual(obj["pronunciation"]["confidence"], "medium")
        self.assertTrue(any("compound" in w for w in obj["warnings"]))

    def test_compound_demotes_the_second_element_stress(self):
        obj = phonetics.analyze("Wavebreak", self.lex)
        self.assertEqual(obj["stress"]["pattern"].count("1"), 1)

    def test_short_fragments_cannot_manufacture_a_compound(self):
        self.assertIsNone(phonetics.decompose("zillow", self.lex))
        self.assertEqual(self.r("Zillow")["pronunciation"]["source"], "g2p")

    def test_dictionary_word_wins_over_decomposition(self):
        self.assertEqual(self.r("Firefox")["pronunciation"]["source"], "cmudict")

    def test_g2p_is_pure_and_repeatable(self):
        for word in ("figma", "qwintara", "xzrq", "thrixthwaite"):
            self.assertEqual(phonetics.g2p(word), phonetics.g2p(word))


class TestVerbability(Base):

    def test_monosyllables_do_not_clip(self):
        self.assertEqual(self.r("Scout")["verbability"]["clippable_to"], [])

    def test_polysyllables_clip_at_the_first_syllable(self):
        self.assertIn("ling", self.r("Lingua")["verbability"]["clippable_to"])
        self.assertIn("fig", self.r("Figma")["verbability"]["clippable_to"])
        self.assertIn("pal", self.r("Palantir")["verbability"]["clippable_to"])

    def test_agentive_forms(self):
        self.assertEqual(self.r("Scout")["verbability"]["agentive"], "scouter")
        self.assertEqual(self.r("Stripe")["verbability"]["agentive"], "striper")
        self.assertEqual(self.r("Slack")["verbability"]["agentive"], "slacker")

    def test_ends_in_vowel(self):
        self.assertTrue(self.r("Lingua")["verbability"]["ends_in_vowel"])
        self.assertFalse(self.r("Scout")["verbability"]["ends_in_vowel"])


class TestInternational(Base):

    def test_no_hard_phonemes_is_low_risk(self):
        self.assertEqual(self.r("Scout")["international"]["risk"], "low")
        self.assertEqual(self.r("Scout")["international"]["hard_phonemes"], [])

    def test_theta_is_flagged_with_languages(self):
        r = self.r("Blorbnth")
        self.assertIn("TH", [h["phoneme"] for h in r["international"]["hard_phonemes"]])
        self.assertIn("Japanese", r["international"]["affected_languages"])
        self.assertEqual(r["international"]["risk"], "high")

    def test_r_l_contrast_is_flagged(self):
        r = self.r("Palantir")
        self.assertIn("R+L", [h["phoneme"] for h in r["international"]["hard_phonemes"]])
        self.assertIn("Japanese", r["international"]["affected_languages"])
        self.assertIn("Korean", r["international"]["affected_languages"])
        self.assertNotEqual(r["international"]["risk"], "low")

    def test_initial_ng_is_flagged(self):
        syl = [phonetics.Syllable(["NG"], "AA1", [])]
        prof = phonetics.international_profile(["NG", "AA1"], syl)
        self.assertIn("NG-initial", [h["phoneme"] for h in prof["hard_phonemes"]])

    def test_v_w_contrast_is_flagged(self):
        prof = phonetics.international_profile(
            ["V", "IH1", "W", "AH0"],
            phonetics.syllabify(["V", "IH1", "W", "AH0"]))
        self.assertIn("V+W", [h["phoneme"] for h in prof["hard_phonemes"]])
        self.assertIn("Hindi", prof["affected_languages"])


class TestScoringSanity(Base):
    """PRD §7.2 makes falsifiable claims about two of these names."""

    def test_lingua_is_comfortable(self):
        r = self.r("Lingua")
        self.assertGreaterEqual(r["ergonomics_score"], 85)
        self.assertGreaterEqual(r["dimensions"]["pronounceability"]["score"], 90)
        self.assertGreaterEqual(r["dimensions"]["spellability"]["score"], 90)
        self.assertGreaterEqual(r["dimensions"]["rhythm_recall"]["score"], 90)

    def test_xzrq_is_bad_for_the_right_reasons(self):
        r = self.r("Xzrq")
        self.assertLess(r["ergonomics_score"], 50)
        self.assertLess(r["dimensions"]["pronounceability"]["score"], 30)
        self.assertLess(r["dimensions"]["spellability"]["score"], 40)
        self.assertLess(r["dimensions"]["rhythm_recall"]["score"], 30)
        # ...and NOT for distinctiveness, which is genuinely high
        self.assertGreater(r["dimensions"]["distinctiveness"]["score"], 60)

    def test_the_good_names_all_clear_seventy(self):
        for name in ("Scout", "Stripe", "Notion", "Xerox", "Kodak", "Zillow",
                     "Slack", "Figma", "Lingua", "Cat"):
            self.assertGreaterEqual(self.r(name)["ergonomics_score"], 70, name)

    def test_the_broken_names_all_fall_below_the_good_ones(self):
        worst_good = min(self.r(n)["ergonomics_score"]
                         for n in ("Scout", "Stripe", "Notion", "Xerox", "Kodak",
                                   "Zillow", "Slack", "Figma", "Lingua", "Cat"))
        for name in ("Xzrq", "Vzzt", "Sqwrlyx"):
            self.assertLess(self.r(name)["ergonomics_score"], worst_good, name)

    def test_evidence_is_attached_to_every_score(self):
        for name, obj in self.results.items():
            for key, dim in obj["dimensions"].items():
                self.assertTrue(dim["evidence"], "{0}/{1}".format(name, key))


class TestCLI(Base):

    def test_single_name_is_an_object(self):
        self.assertIsInstance(json.loads(run_cli("Scout").decode("utf-8")), dict)

    def test_several_names_are_an_array(self):
        out = json.loads(run_cli("Scout", "Stripe").decode("utf-8"))
        self.assertIsInstance(out, list)
        self.assertEqual(len(out), 2)

    def test_file_mode_reads_all_twenty(self):
        out = json.loads(run_cli("--file", BENCHMARK).decode("utf-8"))
        self.assertEqual(len(out), 20)

    def test_pretty_is_indented_and_equivalent(self):
        compact = json.loads(run_cli("Scout").decode("utf-8"))
        pretty_raw = run_cli("Scout", "--pretty")
        self.assertIn(b"\n  ", pretty_raw)
        self.assertEqual(json.loads(pretty_raw.decode("utf-8")), compact)

    def test_version(self):
        out = run_cli("--version").decode("utf-8")
        self.assertIn(phonetics.TOOL_VERSION, out)
        self.assertIn("schema", out)

    def test_comments_in_the_name_file_are_ignored(self):
        names = phonetics.read_name_file(BENCHMARK)
        self.assertNotIn("", names)
        for n in names:
            self.assertNotIn("#", n)

    def test_lexicon_path_is_resolved_from_the_script_not_the_cwd(self):
        proc = subprocess.run([sys.executable, SCRIPT, "Scout"], cwd="/",
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode("utf-8"))
        self.assertEqual(json.loads(proc.stdout.decode("utf-8"))["normalized"], "scout")


class TestOfflineAndPure(Base):

    def test_no_third_party_or_network_imports_at_run_time(self):
        with open(SCRIPT, "r", encoding="utf-8") as fh:
            src = fh.read()
        for forbidden in ("import cmudict", "import requests", "import urllib",
                          "import socket", "import random", "from random",
                          "import datetime", "import http"):
            self.assertNotIn(forbidden, src, forbidden)

    def test_time_is_never_read(self):
        with open(SCRIPT, "r", encoding="utf-8") as fh:
            src = fh.read()
        self.assertNotIn("time.time", src)
        self.assertNotIn("datetime", src)

    def test_lexicon_is_the_expected_size(self):
        self.assertGreater(len(self.lex.words), 100000)
        self.assertLess(len(self.lex.words), 120000)
        self.assertEqual(self.lex.max_phonemes, 10)
        self.assertGreater(self.lex.sample_size, 1000)

    def test_no_lexicon_entry_exceeds_the_cutoff(self):
        longest = max(len(v) for v in self.lex.words.values())
        self.assertLessEqual(longest, self.lex.max_phonemes)

    def test_lexicon_words_are_lowercase_alpha_only(self):
        for w in list(self.lex.words)[:5000]:
            self.assertTrue(w.isalpha() and w.islower(), w)


class TestPerformance(Base):

    def test_whole_benchmark_completes_quickly(self):
        start = time.monotonic()
        run_cli("--file", BENCHMARK)
        elapsed = time.monotonic() - start
        self.assertLess(elapsed, 10.0,
                        "20-name benchmark took {0:.1f}s".format(elapsed))

    def test_single_name_analysis_is_well_under_a_second(self):
        start = time.monotonic()
        for _ in range(10):
            phonetics.analyze("Palantir", self.lex)
        elapsed = (time.monotonic() - start) / 10.0
        self.assertLess(elapsed, 1.0,
                        "{0:.3f}s per name after lexicon load".format(elapsed))


if __name__ == "__main__":
    unittest.main()
