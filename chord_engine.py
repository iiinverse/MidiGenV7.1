"""
MGV7 Chord Engine

Professional harmony engine.

Depends on:
    scale_engine.py
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Tuple
from typing import Iterable
from typing import Optional

from scale_engine import (
    Note,
    Scale,
    ScaleEngine,
    NOTE_INDEX,
    NOTES_SHARP,
)


# ==========================================================
# CHORD DEFINITIONS
# ==========================================================

CHORD_INTERVALS: Dict[str, Tuple[int, ...]] = {

    # Power
    "5": (0, 7),

    # Triads
    "maj": (0, 4, 7),
    "min": (0, 3, 7),
    "dim": (0, 3, 6),
    "aug": (0, 4, 8),

    "sus2": (0, 2, 7),
    "sus4": (0, 5, 7),

    # Sixth
    "6": (0, 4, 7, 9),
    "m6": (0, 3, 7, 9),

    # Seventh
    "7": (0, 4, 7, 10),
    "maj7": (0, 4, 7, 11),
    "m7": (0, 3, 7, 10),
    "mMaj7": (0, 3, 7, 11),

    "dim7": (0, 3, 6, 9),
    "m7b5": (0, 3, 6, 10),

    "aug7": (0, 4, 8, 10),
    "augMaj7": (0, 4, 8, 11),

    # Ninth

    "9": (0, 4, 7, 10, 14),
    "maj9": (0, 4, 7, 11, 14),
    "m9": (0, 3, 7, 10, 14),

    "add9": (0, 4, 7, 14),
    "madd9": (0, 3, 7, 14),

    # Eleventh

    "11": (0, 4, 7, 10, 14, 17),
    "m11": (0, 3, 7, 10, 14, 17),

    # Thirteenth

    "13": (0, 4, 7, 10, 14, 17, 21),
    "maj13": (0, 4, 7, 11, 14, 17, 21),
    "m13": (0, 3, 7, 10, 14, 17, 21),

    # Altered

    "7b5": (0, 4, 6, 10),
    "7#5": (0, 4, 8, 10),

    "7b9": (0, 4, 7, 10, 13),
    "7#9": (0, 4, 7, 10, 15),

    "7#11": (0, 4, 7, 10, 18),
    "7b13": (0, 4, 7, 10, 20),

    "maj7#11": (0, 4, 7, 11, 18),

    "maj7b5": (0, 4, 6, 11),

    "maj7#5": (0, 4, 8, 11),

    # Jazz

    "69": (0, 4, 7, 9, 14),

    "m69": (0, 3, 7, 9, 14),

    "7sus4": (0, 5, 7, 10),

    "9sus4": (0, 5, 7, 10, 14),

    "13sus4": (0, 5, 7, 10, 14, 17, 21),

    # Cluster

    "cluster2": (0, 1, 2),

    "cluster3": (0, 1, 2, 3),

    "quartal": (0, 5, 10),

    "quintal": (0, 7, 14),

}


# ==========================================================
# CHORD
# ==========================================================

@dataclass(frozen=True)
class Chord:

    root: Note

    quality: str

    intervals: Tuple[int, ...]

    bass: Optional[Note] = None

    @property
    def notes(self) -> List[Note]:

        return [

            self.root.transpose(interval)

            for interval in self.intervals

        ]

    @property
    def midi(self) -> List[int]:

        return [

            note.midi

            for note in self.notes

        ]

    @property
    def pitch_classes(self):

        return [

            note.semitone

            for note in self.notes

        ]

    @property
    def name(self):

        if self.bass is None:

            return f"{self.root.name}{self.quality}"

        return f"{self.root.name}{self.quality}/{self.bass.name}"

    def contains(

        self,

        note: Note

    ) -> bool:

        return note.semitone in self.pitch_classes

    def __len__(self):

        return len(self.notes)

    def __iter__(self):

        return iter(self.notes)

    def __str__(self):

        return self.name


# ==========================================================
# CHORD ENGINE
# ==========================================================

class ChordEngine:

    def __init__(self):

        self.scale_engine = ScaleEngine()

        self.chords = dict(CHORD_INTERVALS)
            # ---------------------------------------------------
    # REGISTRY
    # ---------------------------------------------------

    def register_chord(
        self,
        name: str,
        intervals: Iterable[int]
    ) -> None:

        values = sorted({
            int(i)
            for i in intervals
        })

        if not values:
            raise ValueError("Chord cannot be empty.")

        if values[0] != 0:
            values.insert(0, 0)

        self.chords[name] = tuple(values)

    def remove_chord(
        self,
        name: str
    ) -> None:

        if name in self.chords:
            del self.chords[name]

    def exists(
        self,
        quality: str
    ) -> bool:

        return quality in self.chords

    def chord_names(self) -> List[str]:

        return sorted(self.chords.keys())

    def interval_definition(
        self,
        quality: str
    ) -> Tuple[int, ...]:

        if quality not in self.chords:
            raise ValueError(
                f"Unknown chord '{quality}'"
            )

        return self.chords[quality]

    # ---------------------------------------------------
    # CHORD CREATION
    # ---------------------------------------------------

    def create(
        self,
        root: str | Note,
        quality: str,
        octave: int = 4
    ) -> Chord:

        if quality not in self.chords:
            raise ValueError(
                f"Unknown chord '{quality}'"
            )

        if isinstance(root, str):
            root = Note(root, octave)

        return Chord(
            root=root,
            quality=quality,
            intervals=self.chords[quality]
        )

    def slash(
        self,
        root: str | Note,
        quality: str,
        bass: str | Note,
        octave: int = 4
    ) -> Chord:

        chord = self.create(
            root,
            quality,
            octave
        )

        if isinstance(bass, str):
            bass = Note(
                bass,
                octave
            )

        return Chord(
            root=chord.root,
            quality=quality,
            intervals=chord.intervals,
            bass=bass
        )

    # ---------------------------------------------------
    # INVERSIONS
    # ---------------------------------------------------

    def inversion(
        self,
        chord: Chord,
        inversion: int
    ) -> List[Note]:

        notes = [
            Note.from_midi(n.midi)
            for n in chord.notes
        ]

        inversion %= len(notes)

        for _ in range(inversion):

            first = notes.pop(0)

            notes.append(
                Note.from_midi(
                    first.midi + 12
                )
            )

        return notes

    def all_inversions(
        self,
        chord: Chord
    ) -> List[List[Note]]:

        return [

            self.inversion(
                chord,
                inversion
            )

            for inversion
            in range(len(chord))

        ]

    # ---------------------------------------------------
    # VOICING
    # ---------------------------------------------------

    def closed_voicing(
        self,
        chord: Chord
    ) -> List[Note]:

        return sorted(
            chord.notes,
            key=lambda n: n.midi
        )

    def open_voicing(
        self,
        chord: Chord
    ) -> List[Note]:

        notes = self.closed_voicing(
            chord
        )

        if len(notes) < 4:
            return notes

        result = [
            notes[0],
            Note.from_midi(
                notes[1].midi + 12
            ),
            notes[2],
            Note.from_midi(
                notes[3].midi + 12
            )
        ]

        if len(notes) > 4:

            for note in notes[4:]:

                result.append(
                    Note.from_midi(
                        note.midi + 12
                    )
                )

        return sorted(
            result,
            key=lambda n: n.midi
        )

    def drop2(
        self,
        chord: Chord
    ) -> List[Note]:

        notes = sorted(
            chord.notes,
            key=lambda n: n.midi
        )

        if len(notes) < 4:
            return notes

        notes[-2] = Note.from_midi(
            notes[-2].midi - 12
        )

        return sorted(
            notes,
            key=lambda n: n.midi
        )

    def drop3(
        self,
        chord: Chord
    ) -> List[Note]:

        notes = sorted(
            chord.notes,
            key=lambda n: n.midi
        )

        if len(notes) < 4:
            return notes

        notes[-3] = Note.from_midi(
            notes[-3].midi - 12
        )

        return sorted(
            notes,
            key=lambda n: n.midi
        )

    # ---------------------------------------------------
    # INTERVAL ANALYSIS
    # ---------------------------------------------------

    @staticmethod
    def intervals(
        chord: Chord
    ) -> List[int]:

        root = chord.root.semitone

        return [

            (note.semitone - root) % 12

            for note

            in chord.notes

        ]

    @staticmethod
    def span(
        chord: Chord
    ) -> int:

        notes = sorted(
            chord.notes,
            key=lambda n: n.midi
        )

        return (
            notes[-1].midi -
            notes[0].midi
        )

    @staticmethod
    def density(
        chord: Chord
    ) -> float:

        if len(chord.notes) < 2:
            return 0.0

        return (
            ChordEngine.span(chord)
            /
            (len(chord.notes) - 1)
        )

    @staticmethod
    def highest(
        chord: Chord
    ) -> Note:

        return max(
            chord.notes,
            key=lambda n: n.midi
        )

    @staticmethod
    def lowest(
        chord: Chord
    ) -> Note:

        return min(
            chord.notes,
            key=lambda n: n.midi
        )
            # ---------------------------------------------------
    # CHORD DETECTION
    # ---------------------------------------------------

    def detect(
        self,
        notes: Iterable[Note]
    ) -> List[Dict[str, object]]:

        notes = list(notes)

        if len(notes) < 2:
            return []

        pitch_classes = sorted({
            n.semitone
            for n in notes
        })

        candidates = []

        for root_pc in pitch_classes:

            for quality, definition in self.chords.items():

                expected = sorted({
                    (root_pc + (i % 12)) % 12
                    for i in definition
                })

                common = len(
                    set(expected) &
                    set(pitch_classes)
                )

                missing = len(
                    set(expected) -
                    set(pitch_classes)
                )

                extra = len(
                    set(pitch_classes) -
                    set(expected)
                )

                score = (
                    common * 100
                    - missing * 25
                    - extra * 15
                )

                candidates.append({
                    "root": NOTES_SHARP[root_pc],
                    "quality": quality,
                    "score": score,
                    "common": common,
                    "missing": missing,
                    "extra": extra,
                    "expected": expected,
                })

        candidates.sort(
            key=lambda x: (
                x["score"],
                x["common"],
                -x["missing"]
            ),
            reverse=True
        )

        return candidates

    def detect_best(
        self,
        notes: Iterable[Note]
    ) -> Optional[Dict[str, object]]:

        result = self.detect(notes)

        if not result:
            return None

        return result[0]

    # ---------------------------------------------------
    # MIDI DETECTION
    # ---------------------------------------------------

    def detect_midi(
        self,
        midi_notes: Iterable[int]
    ) -> List[Dict[str, object]]:

        return self.detect(

            Note.from_midi(m)

            for m in midi_notes

        )

    def detect_best_midi(
        self,
        midi_notes: Iterable[int]
    ) -> Optional[Dict[str, object]]:

        result = self.detect_midi(
            midi_notes
        )

        if not result:
            return None

        return result[0]

    # ---------------------------------------------------
    # ROOT DETECTION
    # ---------------------------------------------------

    @staticmethod
    def probable_root(
        notes: Iterable[Note]
    ) -> Optional[Note]:

        notes = sorted(
            notes,
            key=lambda n: n.midi
        )

        if not notes:
            return None

        histogram = {}

        for note in notes:

            histogram.setdefault(
                note.semitone,
                0
            )

            histogram[note.semitone] += 1

        winner = max(
            histogram.items(),
            key=lambda item: (
                item[1],
                -item[0]
            )
        )[0]

        lowest = min(
            notes,
            key=lambda n: n.midi
        )

        return Note(
            NOTES_SHARP[winner],
            lowest.octave
        )

    # ---------------------------------------------------
    # CHORD SIMILARITY
    # ---------------------------------------------------

    @staticmethod
    def similarity(
        first: Chord,
        second: Chord
    ) -> float:

        a = set(first.pitch_classes)
        b = set(second.pitch_classes)

        union = len(a | b)

        if union == 0:
            return 0.0

        return len(a & b) / union

    @staticmethod
    def distance(
        first: Chord,
        second: Chord
    ) -> int:

        return abs(
            first.root.midi -
            second.root.midi
        )

    # ---------------------------------------------------
    # INVERSION DETECTION
    # ---------------------------------------------------

    def inversion_index(
        self,
        notes: Iterable[Note],
        quality: str
    ) -> int:

        notes = sorted(
            notes,
            key=lambda n: n.midi
        )

        if len(notes) < 2:
            return 0

        detected = self.detect_best(notes)

        if detected is None:
            return 0

        root = NOTE_INDEX[
            detected["root"]
        ]

        lowest = notes[0].semitone

        intervals = [

            (root + i) % 12

            for i

            in self.interval_definition(
                quality
            )

        ]

        for index, value in enumerate(intervals):

            if value == lowest:
                return index

        return 0

    # ---------------------------------------------------
    # CHORD SUMMARY
    # ---------------------------------------------------

    def summary(
        self,
        chord: Chord
    ) -> Dict[str, object]:

        return {

            "name": chord.name,

            "quality": chord.quality,

            "root": chord.root.name,

            "bass": (
                chord.bass.name
                if chord.bass
                else chord.root.name
            ),

            "notes": [
                n.name
                for n in chord.notes
            ],

            "midi": [
                n.midi
                for n in chord.notes
            ],

            "pitch_classes": chord.pitch_classes,

            "intervals": list(
                chord.intervals
            ),

            "voices": len(chord),

            "span": self.span(chord),

            "density": self.density(chord),

        }
            # ---------------------------------------------------
    # VOICE LEADING
    # ---------------------------------------------------

    def voice_leading_distance(
        self,
        first: Chord,
        second: Chord
    ) -> int:

        a = sorted(
            first.notes,
            key=lambda n: n.midi
        )

        b = sorted(
            second.notes,
            key=lambda n: n.midi
        )

        length = min(
            len(a),
            len(b)
        )

        distance = 0

        for i in range(length):

            distance += abs(
                a[i].midi -
                b[i].midi
            )

        return distance

    def best_inversion(
        self,
        source: Chord,
        target: Chord
    ) -> List[Note]:

        best = None
        best_distance = 10**9

        for inversion in self.all_inversions(target):

            distance = 0

            source_notes = sorted(
                source.notes,
                key=lambda n: n.midi
            )

            target_notes = sorted(
                inversion,
                key=lambda n: n.midi
            )

            for s, t in zip(
                source_notes,
                target_notes
            ):

                distance += abs(
                    s.midi - t.midi
                )

            if distance < best_distance:

                best_distance = distance
                best = target_notes

        return best

    # ---------------------------------------------------
    # DIATONIC CHORDS
    # ---------------------------------------------------

    def diatonic(
        self,
        root: str,
        scale_name: str
    ) -> List[Chord]:

        chords = []

        for info in self.scale_engine.diatonic_triads(
            root,
            scale_name
        ):

            quality_map = {
                "maj": "maj",
                "min": "min",
                "dim": "dim",
                "aug": "aug",
            }

            quality = quality_map.get(
                info["quality"],
                "maj"
            )

            chord = self.create(
                info["notes"][0].name,
                quality,
                info["notes"][0].octave
            )

            chords.append(chord)

        return chords

    def diatonic7(
        self,
        root: str,
        scale_name: str
    ) -> List[Chord]:

        chords = []

        for info in self.scale_engine.diatonic_seventh_chords(
            root,
            scale_name
        ):

            quality = info["quality"]

            if quality not in self.chords:
                continue

            root_note = info["notes"][0]

            chords.append(

                self.create(
                    root_note.name,
                    quality,
                    root_note.octave
                )

            )

        return chords

    # ---------------------------------------------------
    # SCALE COMPATIBILITY
    # ---------------------------------------------------

    def compatible_scales(
        self,
        chord: Chord
    ) -> List[Dict[str, str]]:

        matches = []

        pcs = set(
            chord.pitch_classes
        )

        for root in NOTES_SHARP:

            for scale_name in self.scale_engine.scale_names():

                scale = self.scale_engine.get_scale(
                    root,
                    scale_name
                )

                if pcs.issubset(
                    set(scale.pitch_classes)
                ):

                    matches.append({

                        "root": root,

                        "scale": scale_name

                    })

        return matches

    # ---------------------------------------------------
    # QUALITY HELPERS
    # ---------------------------------------------------

    def is_major(
        self,
        chord: Chord
    ) -> bool:

        return chord.quality.startswith("maj") \
            or chord.quality == "6"

    def is_minor(
        self,
        chord: Chord
    ) -> bool:

        return chord.quality.startswith("m") \
            and not chord.quality.startswith("maj")

    def is_diminished(
        self,
        chord: Chord
    ) -> bool:

        return "dim" in chord.quality

    def is_augmented(
        self,
        chord: Chord
    ) -> bool:

        return "aug" in chord.quality

    def is_dominant(
        self,
        chord: Chord
    ) -> bool:

        return (
            chord.quality == "7"
            or chord.quality.startswith("9")
            or chord.quality.startswith("13")
        )

    # ---------------------------------------------------
    # EXPORT
    # ---------------------------------------------------

    def export(
        self,
        chord: Chord
    ) -> Dict[str, object]:

        return {

            "name": chord.name,

            "root": chord.root.name,

            "quality": chord.quality,

            "intervals": list(
                chord.intervals
            ),

            "notes": [

                note.name

                for note

                in chord.notes

            ],

            "midi": [

                note.midi

                for note

                in chord.notes

            ],

            "pitch_classes": chord.pitch_classes,

            "bass": (

                chord.bass.name

                if chord.bass

                else None

            )

        }

    def __len__(self):

        return len(self.chords)

    def __contains__(
        self,
        quality: str
    ):

        return quality in self.chords

    def __iter__(self):

        return iter(
            sorted(
                self.chords.items()
            )
        )
            # ---------------------------------------------------
    # FUNCTIONAL HARMONY
    # ---------------------------------------------------

    FUNCTIONS_MAJOR = {
        1: "T",
        2: "S",
        3: "T",
        4: "S",
        5: "D",
        6: "T",
        7: "D",
    }

    FUNCTIONS_MINOR = {
        1: "T",
        2: "S",
        3: "T",
        4: "S",
        5: "D",
        6: "S",
        7: "D",
    }

    def harmonic_function(
        self,
        degree: int,
        scale_name: str
    ) -> str:

        if "minor" in scale_name:

            return self.FUNCTIONS_MINOR.get(
                degree,
                "?"
            )

        return self.FUNCTIONS_MAJOR.get(
            degree,
            "?"
        )

    def degree_to_chord(
        self,
        root: str,
        scale_name: str,
        degree: int
    ) -> Chord:

        chords = self.diatonic(
            root,
            scale_name
        )

        return chords[degree - 1]

    def function_progression(
        self,
        root: str,
        scale_name: str,
        functions: Iterable[str]
    ) -> List[Chord]:

        result = []

        chords = self.diatonic(
            root,
            scale_name
        )

        mapping = {}

        for degree in range(1, len(chords) + 1):

            func = self.harmonic_function(
                degree,
                scale_name
            )

            mapping.setdefault(
                func,
                []
            )

            mapping[func].append(
                chords[degree - 1]
            )

        for func in functions:

            if func in mapping:

                result.append(
                    mapping[func][0]
                )

        return result

    # ---------------------------------------------------
    # ROMAN NUMERALS
    # ---------------------------------------------------

    ROMAN_MAJOR = (
        "I",
        "ii",
        "iii",
        "IV",
        "V",
        "vi",
        "vii°",
    )

    ROMAN_MINOR = (
        "i",
        "ii°",
        "III",
        "iv",
        "v",
        "VI",
        "VII",
    )

    def roman(
        self,
        degree: int,
        scale_name: str
    ) -> str:

        if "minor" in scale_name:

            return self.ROMAN_MINOR[
                degree - 1
            ]

        return self.ROMAN_MAJOR[
            degree - 1
        ]

    def roman_progression(
        self,
        degrees: Iterable[int],
        scale_name: str
    ) -> List[str]:

        return [

            self.roman(
                degree,
                scale_name
            )

            for degree

            in degrees

        ]

    # ---------------------------------------------------
    # CHORD TENSION
    # ---------------------------------------------------

    TENSION = {
        "5": 0.05,

        "maj": 0.15,
        "min": 0.18,

        "sus2": 0.25,
        "sus4": 0.35,

        "6": 0.30,
        "m6": 0.35,

        "7": 0.65,
        "maj7": 0.55,
        "m7": 0.45,

        "9": 0.75,
        "11": 0.85,
        "13": 0.95,

        "dim": 0.80,
        "dim7": 1.00,
        "m7b5": 0.90,

        "aug": 0.75,
        "aug7": 0.90,
    }

    def tension(
        self,
        chord: Chord
    ) -> float:

        return self.TENSION.get(
            chord.quality,
            0.50
        )

    # ---------------------------------------------------
    # RESOLUTION
    # ---------------------------------------------------

    def wants_resolution(
        self,
        chord: Chord
    ) -> bool:

        return self.tension(
            chord
        ) >= 0.70

    def resolve(
        self,
        chord: Chord
    ) -> Optional[Chord]:

        if chord.quality == "7":

            return self.create(

                NOTES_SHARP[
                    (NOTE_INDEX[chord.root.name] + 5) % 12
                ],

                "maj",

                chord.root.octave

            )

        if chord.quality == "dim7":

            return self.create(

                NOTES_SHARP[
                    (NOTE_INDEX[chord.root.name] + 1) % 12
                ],

                "maj",

                chord.root.octave

            )

        if chord.quality == "m7b5":

            return self.create(

                NOTES_SHARP[
                    (NOTE_INDEX[chord.root.name] + 1) % 12
                ],

                "min",

                chord.root.octave

            )

        return None

    # ---------------------------------------------------
    # CHORD COLLECTION
    # ---------------------------------------------------

    def all_chords(
        self,
        octave: int = 4
    ) -> List[Chord]:

        result = []

        for root in NOTES_SHARP:

            for quality in self.chords:

                result.append(

                    self.create(
                        root,
                        quality,
                        octave
                    )

                )

        return result

    def chord_count(self) -> int:

        return len(self.chords)
            # ---------------------------------------------------
    # CHORD PROGRESSION ANALYSIS
    # ---------------------------------------------------

    def progression_distance(
        self,
        progression: Iterable[Chord]
    ) -> int:

        progression = list(progression)

        if len(progression) < 2:
            return 0

        distance = 0

        for current, nxt in zip(
            progression[:-1],
            progression[1:]
        ):

            distance += self.voice_leading_distance(
                current,
                nxt
            )

        return distance

    def optimize_progression(
        self,
        progression: Iterable[Chord]
    ) -> List[List[Note]]:

        progression = list(progression)

        if not progression:
            return []

        optimized = [
            self.closed_voicing(
                progression[0]
            )
        ]

        previous = progression[0]

        for chord in progression[1:]:

            best = self.best_inversion(
                previous,
                chord
            )

            optimized.append(best)

            previous = Chord(
                root=chord.root,
                quality=chord.quality,
                intervals=chord.intervals,
                bass=best[0]
            )

        return optimized

    # ---------------------------------------------------
    # COMMON PROGRESSIONS
    # ---------------------------------------------------

    COMMON_PROGRESSIONS = {

        "I-V-vi-IV":
            (1, 5, 6, 4),

        "ii-V-I":
            (2, 5, 1),

        "I-IV-V-I":
            (1, 4, 5, 1),

        "vi-IV-I-V":
            (6, 4, 1, 5),

        "I-vi-ii-V":
            (1, 6, 2, 5),

        "I-V-IV":
            (1, 5, 4),

        "i-VI-III-VII":
            (1, 6, 3, 7),

        "i-iv-V-i":
            (1, 4, 5, 1),

        "12bar":
            (
                1,1,1,1,
                4,4,1,1,
                5,4,1,5
            ),

    }

    def progression(
        self,
        name: str,
        root: str,
        scale_name: str
    ) -> List[Chord]:

        if name not in self.COMMON_PROGRESSIONS:

            raise ValueError(name)

        return [

            self.degree_to_chord(
                root,
                scale_name,
                degree
            )

            for degree

            in self.COMMON_PROGRESSIONS[name]

        ]

    # ---------------------------------------------------
    # TRANSPOSE
    # ---------------------------------------------------

    def transpose(
        self,
        chord: Chord,
        semitones: int
    ) -> Chord:

        return Chord(

            root=chord.root.transpose(
                semitones
            ),

            quality=chord.quality,

            intervals=chord.intervals,

            bass=(
                chord.bass.transpose(
                    semitones
                )
                if chord.bass
                else None
            )

        )

    def transpose_progression(
        self,
        progression: Iterable[Chord],
        semitones: int
    ) -> List[Chord]:

        return [

            self.transpose(
                chord,
                semitones
            )

            for chord

            in progression

        ]

    # ---------------------------------------------------
    # RANDOM GENERATION
    # ---------------------------------------------------

    def random_chord(
        self,
        octave: int = 4
    ) -> Chord:

        import random

        return self.create(

            random.choice(
                NOTES_SHARP
            ),

            random.choice(
                list(self.chords.keys())
            ),

            octave

        )

    def random_progression(
        self,
        length: int = 4,
        octave: int = 4
    ) -> List[Chord]:

        import random

        return [

            self.random_chord(
                octave
            )

            for _ in range(length)

        ]

    # ---------------------------------------------------
    # STATISTICS
    # ---------------------------------------------------

    def statistics(self) -> Dict[str, object]:

        triads = 0
        sevenths = 0
        extended = 0

        for intervals in self.chords.values():

            size = len(intervals)

            if size == 3:
                triads += 1

            elif size == 4:
                sevenths += 1

            else:
                extended += 1

        return {

            "registered_chords":
                len(self.chords),

            "triads":
                triads,

            "seventh_chords":
                sevenths,

            "extended":
                extended,

            "scale_engine":
                self.scale_engine.__class__.__name__,

        }

# ==========================================================
# PUBLIC API
# ==========================================================

__all__ = [

    "Chord",

    "ChordEngine",

    "CHORD_INTERVALS",

]
