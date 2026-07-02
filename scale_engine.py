"""
MGV7 Scale Engine
Core music theory module.

Author: OpenAI
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple
import math


# -------------------------------------------------------
# NOTES
# -------------------------------------------------------

NOTES_SHARP = (
    "C", "C#", "D", "D#", "E", "F",
    "F#", "G", "G#", "A", "A#", "B"
)

NOTES_FLAT = (
    "C", "Db", "D", "Eb", "E", "F",
    "Gb", "G", "Ab", "A", "Bb", "B"
)

NOTE_INDEX: Dict[str, int] = {
    "C": 0,
    "B#": 0,

    "C#": 1,
    "Db": 1,

    "D": 2,

    "D#": 3,
    "Eb": 3,

    "E": 4,
    "Fb": 4,

    "E#": 5,
    "F": 5,

    "F#": 6,
    "Gb": 6,

    "G": 7,

    "G#": 8,
    "Ab": 8,

    "A": 9,

    "A#": 10,
    "Bb": 10,

    "B": 11,
    "Cb": 11,
}


# -------------------------------------------------------
# INTERVALS
# -------------------------------------------------------

INTERVALS: Dict[str, int] = {
    "P1": 0,
    "m2": 1,
    "M2": 2,
    "m3": 3,
    "M3": 4,
    "P4": 5,
    "TT": 6,
    "P5": 7,
    "m6": 8,
    "M6": 9,
    "m7": 10,
    "M7": 11,
    "P8": 12,
}


# -------------------------------------------------------
# SCALES
# -------------------------------------------------------

SCALES: Dict[str, Tuple[int, ...]] = {

    "major": (0, 2, 4, 5, 7, 9, 11),

    "natural_minor": (0, 2, 3, 5, 7, 8, 10),

    "harmonic_minor": (0, 2, 3, 5, 7, 8, 11),

    "melodic_minor": (0, 2, 3, 5, 7, 9, 11),

    "dorian": (0, 2, 3, 5, 7, 9, 10),

    "phrygian": (0, 1, 3, 5, 7, 8, 10),

    "lydian": (0, 2, 4, 6, 7, 9, 11),

    "mixolydian": (0, 2, 4, 5, 7, 9, 10),

    "locrian": (0, 1, 3, 5, 6, 8, 10),

    "major_pentatonic": (0, 2, 4, 7, 9),

    "minor_pentatonic": (0, 3, 5, 7, 10),

    "blues": (0, 3, 5, 6, 7, 10),

    "whole_tone": (0, 2, 4, 6, 8, 10),

    "chromatic": tuple(range(12)),
}


# -------------------------------------------------------
# NOTE
# -------------------------------------------------------

@dataclass(frozen=True)
class Note:

    name: str
    octave: int = 4

    def __post_init__(self):

        if self.name not in NOTE_INDEX:
            raise ValueError(f"Unknown note: {self.name}")

    @property
    def semitone(self) -> int:
        return NOTE_INDEX[self.name]

    @property
    def midi(self) -> int:
        return (self.octave + 1) * 12 + self.semitone

    @property
    def frequency(self) -> float:
        return 440.0 * (2 ** ((self.midi - 69) / 12))

    def transpose(self, semitones: int) -> "Note":

        midi = self.midi + semitones

        octave = midi // 12 - 1

        note = NOTES_SHARP[midi % 12]

        return Note(note, octave)

    @classmethod
    def from_midi(cls, midi: int) -> "Note":

        octave = midi // 12 - 1

        note = NOTES_SHARP[midi % 12]

        return cls(note, octave)

    def __str__(self):

        return f"{self.name}{self.octave}"
# -------------------------------------------------------
# SCALE
# -------------------------------------------------------

@dataclass(frozen=True)
class Scale:
    root: Note
    name: str
    intervals: Tuple[int, ...]

    @property
    def notes(self) -> List[Note]:
        return [
            self.root.transpose(interval)
            for interval in self.intervals
        ]

    @property
    def pitch_classes(self) -> List[int]:
        return [
            note.semitone
            for note in self.notes
        ]

    def contains(self, note: Note | str) -> bool:

        if isinstance(note, str):
            note = Note(note)

        return note.semitone in self.pitch_classes

    @property
    def degrees(self) -> Dict[int, Note]:

        return {
            degree + 1: note
            for degree, note in enumerate(self.notes)
        }

    def degree(self, index: int) -> Note:

        if index < 1 or index > len(self.notes):
            raise ValueError("Degree out of range.")

        return self.notes[index - 1]

    def __iter__(self):
        return iter(self.notes)

    def __len__(self):
        return len(self.notes)

    def __str__(self):

        return f"{self.root.name} {self.name}"


# -------------------------------------------------------
# SCALE ENGINE
# -------------------------------------------------------

class ScaleEngine:

    def __init__(self):

        self.scales = dict(SCALES)

    def register_scale(
        self,
        name: str,
        intervals: Iterable[int]
    ):

        self.scales[name] = tuple(intervals)

    def scale_names(self) -> List[str]:

        return sorted(self.scales.keys())

    def exists(self, scale_name: str) -> bool:

        return scale_name in self.scales

    def get_scale(
        self,
        root: str | Note,
        scale_name: str
    ) -> Scale:

        if scale_name not in self.scales:
            raise ValueError(f"Unknown scale '{scale_name}'")

        if isinstance(root, str):
            root = Note(root)

        return Scale(
            root=root,
            name=scale_name,
            intervals=self.scales[scale_name]
        )

    def get_notes(
        self,
        root: str | Note,
        scale_name: str
    ) -> List[Note]:

        return self.get_scale(root, scale_name).notes

    def contains(
        self,
        root: str,
        scale_name: str,
        note: str | Note
    ) -> bool:

        return self.get_scale(root, scale_name).contains(note)

    def transpose_notes(
        self,
        notes: Iterable[Note],
        semitones: int
    ) -> List[Note]:

        return [
            note.transpose(semitones)
            for note in notes
        ]
           # ---------------------------------------------------
    # MIDI
    # ---------------------------------------------------

    @staticmethod
    def note_to_midi(note: str, octave: int = 4) -> int:

        if note not in NOTE_INDEX:
            raise ValueError(f"Unknown note '{note}'")

        return (octave + 1) * 12 + NOTE_INDEX[note]

    @staticmethod
    def midi_to_note(midi: int) -> Note:

        if midi < 0 or midi > 127:
            raise ValueError("MIDI note must be between 0 and 127.")

        octave = midi // 12 - 1
        name = NOTES_SHARP[midi % 12]

        return Note(name, octave)

    @staticmethod
    def midi_to_frequency(midi: int) -> float:

        return 440.0 * (2 ** ((midi - 69) / 12))

    # ---------------------------------------------------
    # KEYS
    # ---------------------------------------------------

    def relative_minor(self, major_root: str) -> str:

        note = Note(major_root)

        return NOTES_SHARP[(note.semitone + 9) % 12]

    def relative_major(self, minor_root: str) -> str:

        note = Note(minor_root)

        return NOTES_SHARP[(note.semitone + 3) % 12]

    def parallel_minor(self, major_root: str) -> str:

        return major_root

    def parallel_major(self, minor_root: str) -> str:

        return minor_root

    # ---------------------------------------------------
    # SCALE DETECTION
    # ---------------------------------------------------

    def detect_scale(
        self,
        notes: Iterable[Note | str]
    ) -> List[tuple[str, str]]:

        pitch_classes = set()

        for note in notes:

            if isinstance(note, str):
                note = Note(note)

            pitch_classes.add(note.semitone)

        matches = []

        for root in NOTES_SHARP:

            root_pc = NOTE_INDEX[root]

            for scale_name, intervals in self.scales.items():

                scale = {
                    (root_pc + interval) % 12
                    for interval in intervals
                }

                if pitch_classes.issubset(scale):

                    matches.append((root, scale_name))

        return matches

    # ---------------------------------------------------
    # DEGREES
    # ---------------------------------------------------

    def degree(
        self,
        root: str,
        scale_name: str,
        degree: int
    ) -> Note:

        return self.get_scale(root, scale_name).degree(degree)

    def degrees(
        self,
        root: str,
        scale_name: str
    ) -> Dict[int, Note]:

        return self.get_scale(root, scale_name).degrees
            # ---------------------------------------------------
    # DIATONIC TRIADS
    # ---------------------------------------------------

    def diatonic_triads(
        self,
        root: str,
        scale_name: str
    ) -> List[Dict[str, object]]:

        scale = self.get_scale(root, scale_name)
        notes = scale.notes
        size = len(notes)

        result: List[Dict[str, object]] = []

        roman_major = (
            "I", "ii", "iii", "IV", "V", "vi", "vii°"
        )

        roman_minor = (
            "i", "ii°", "III", "iv", "v", "VI", "VII"
        )

        romans = roman_major if scale_name == "major" else roman_minor

        for i in range(size):

            root_note = notes[i]
            third = notes[(i + 2) % size]
            fifth = notes[(i + 4) % size]

            root_pc = root_note.semitone
            third_pc = third.semitone
            fifth_pc = fifth.semitone

            int3 = (third_pc - root_pc) % 12
            int5 = (fifth_pc - root_pc) % 12

            if (int3, int5) == (4, 7):
                quality = "maj"

            elif (int3, int5) == (3, 7):
                quality = "min"

            elif (int3, int5) == (3, 6):
                quality = "dim"

            elif (int3, int5) == (4, 8):
                quality = "aug"

            else:
                quality = "unknown"

            result.append({
                "degree": i + 1,
                "roman": romans[i] if i < len(romans) else str(i + 1),
                "quality": quality,
                "notes": [
                    root_note,
                    third,
                    fifth
                ]
            })

        return result

    # ---------------------------------------------------
    # INTERVAL HELPERS
    # ---------------------------------------------------

    @staticmethod
    def interval_between(
        first: Note,
        second: Note
    ) -> int:

        return (second.semitone - first.semitone) % 12

    @staticmethod
    def interval_name(
        semitones: int
    ) -> str:

        semitones %= 12

        for name, value in INTERVALS.items():
            if value % 12 == semitones:
                return name

        return f"{semitones}st"

    # ---------------------------------------------------
    # UTILITIES
    # ---------------------------------------------------

    @staticmethod
    def normalize_note(name: str) -> str:

        if name not in NOTE_INDEX:
            raise ValueError(f"Unknown note '{name}'")

        return NOTES_SHARP[NOTE_INDEX[name]]

    @staticmethod
    def unique_notes(
        notes: Iterable[Note]
    ) -> List[Note]:

        seen = set()
        result = []

        for note in notes:

            if note.midi in seen:
                continue

            seen.add(note.midi)
            result.append(note)

        return result

    @staticmethod
    def sort_notes(
        notes: Iterable[Note]
    ) -> List[Note]:

        return sorted(notes, key=lambda n: n.midi)
            # ---------------------------------------------------
    # MODE CONVERSION
    # ---------------------------------------------------

    MODE_ROTATIONS = {
        "ionian": 0,
        "dorian": 1,
        "phrygian": 2,
        "lydian": 3,
        "mixolydian": 4,
        "aeolian": 5,
        "locrian": 6,
    }

    def rotate_scale(
        self,
        root: str,
        scale_name: str,
        rotation: int
    ) -> Scale:

        scale = self.get_scale(root, scale_name)

        intervals = list(scale.intervals)

        rotation %= len(intervals)

        rotated = intervals[rotation:] + intervals[:rotation]

        base = rotated[0]

        rotated = tuple(
            (i - base) % 12
            for i in rotated
        )

        return Scale(
            root=scale.notes[rotation],
            name=f"{scale_name}_mode_{rotation}",
            intervals=rotated
        )

    def get_mode(
        self,
        root: str,
        mode: str
    ) -> Scale:

        if mode not in self.MODE_ROTATIONS:
            raise ValueError(f"Unknown mode '{mode}'")

        return self.rotate_scale(
            root,
            "major",
            self.MODE_ROTATIONS[mode]
        )

    # ---------------------------------------------------
    # SCALE DISTANCE
    # ---------------------------------------------------

    def similarity(
        self,
        scale_a: Scale,
        scale_b: Scale
    ) -> float:

        a = set(scale_a.pitch_classes)
        b = set(scale_b.pitch_classes)

        union = len(a | b)

        if union == 0:
            return 0.0

        return len(a & b) / union

    # ---------------------------------------------------
    # SCALE COMPARISON
    # ---------------------------------------------------

    def common_notes(
        self,
        scale_a: Scale,
        scale_b: Scale
    ) -> List[Note]:

        common = set(scale_a.pitch_classes) & set(scale_b.pitch_classes)

        result = []

        for note in scale_a.notes:

            if note.semitone in common:
                result.append(note)

        return result

    def missing_notes(
        self,
        scale_a: Scale,
        scale_b: Scale
    ) -> List[Note]:

        other = set(scale_b.pitch_classes)

        result = []

        for note in scale_a.notes:

            if note.semitone not in other:
                result.append(note)

        return result

    # ---------------------------------------------------
    # NOTE OPERATIONS
    # ---------------------------------------------------

    def quantize_to_scale(
        self,
        notes: Iterable[Note],
        root: str,
        scale_name: str
    ) -> List[Note]:

        scale = self.get_scale(root, scale_name)

        pcs = scale.pitch_classes

        result = []

        for note in notes:

            if note.semitone in pcs:
                result.append(note)
                continue

            nearest = min(
                pcs,
                key=lambda x: min(
                    (x - note.semitone) % 12,
                    (note.semitone - x) % 12
                )
            )

            midi = note.midi

            octave = midi // 12 - 1

            result.append(
                Note(
                    NOTES_SHARP[nearest],
                    octave
                )
            )

        return result

    # ---------------------------------------------------
    # RANDOM SCALE NOTE
    # ---------------------------------------------------

    def random_note(
        self,
        root: str,
        scale_name: str,
        octave: int = 4
    ) -> Note:

        import random

        scale = self.get_scale(root, scale_name)

        pitch = random.choice(scale.pitch_classes)

        return Note(
            NOTES_SHARP[pitch],
            octave
        )
            # ---------------------------------------------------
    # CIRCLE OF FIFTHS
    # ---------------------------------------------------

    CIRCLE_OF_FIFTHS = (
        "C",
        "G",
        "D",
        "A",
        "E",
        "B",
        "F#",
        "C#",
        "G#",
        "D#",
        "A#",
        "F",
    )

    def circle_position(self, root: str) -> int:

        root = self.normalize_note(root)

        if root not in self.CIRCLE_OF_FIFTHS:
            raise ValueError(f"{root} not in circle of fifths.")

        return self.CIRCLE_OF_FIFTHS.index(root)

    def next_fifth(self, root: str) -> str:

        pos = self.circle_position(root)

        return self.CIRCLE_OF_FIFTHS[
            (pos + 1) % 12
        ]

    def previous_fifth(self, root: str) -> str:

        pos = self.circle_position(root)

        return self.CIRCLE_OF_FIFTHS[
            (pos - 1) % 12
        ]

    # ---------------------------------------------------
    # CAMELOT WHEEL
    # ---------------------------------------------------

    CAMELOT_MAJOR = {
        "B": "1B",
        "F#": "2B",
        "Db": "3B",
        "Ab": "4B",
        "Eb": "5B",
        "Bb": "6B",
        "F": "7B",
        "C": "8B",
        "G": "9B",
        "D": "10B",
        "A": "11B",
        "E": "12B",
    }

    CAMELOT_MINOR = {
        "Ab": "1A",
        "Eb": "2A",
        "Bb": "3A",
        "F": "4A",
        "C": "5A",
        "G": "6A",
        "D": "7A",
        "A": "8A",
        "E": "9A",
        "B": "10A",
        "F#": "11A",
        "Db": "12A",
    }

    def camelot(
        self,
        root: str,
        scale_name: str
    ) -> str | None:

        if scale_name == "major":
            return self.CAMELOT_MAJOR.get(root)

        if "minor" in scale_name:
            return self.CAMELOT_MINOR.get(root)

        return None

    # ---------------------------------------------------
    # TRANSPOSITION
    # ---------------------------------------------------

    def transpose_scale(
        self,
        scale: Scale,
        semitones: int
    ) -> Scale:

        root = scale.root.transpose(semitones)

        return Scale(
            root=root,
            name=scale.name,
            intervals=scale.intervals
        )

    def transpose_melody(
        self,
        melody: Iterable[Note],
        semitones: int
    ) -> List[Note]:

        return [
            note.transpose(semitones)
            for note in melody
        ]

    # ---------------------------------------------------
    # RANGE
    # ---------------------------------------------------

    @staticmethod
    def clamp_range(
        notes: Iterable[Note],
        minimum: int,
        maximum: int
    ) -> List[Note]:

        result = []

        for note in notes:

            midi = note.midi

            while midi < minimum:
                midi += 12

            while midi > maximum:
                midi -= 12

            result.append(
                Note.from_midi(midi)
            )

        return result

    # ---------------------------------------------------
    # SCALE EXPANSION
    # ---------------------------------------------------

    def expand_scale(
        self,
        root: str,
        scale_name: str,
        octaves: int = 2
    ) -> List[Note]:

        scale = self.get_scale(root, scale_name)

        result: List[Note] = []

        for octave in range(octaves):

            for note in scale.notes:

                result.append(
                    Note(
                        note.name,
                        note.octave + octave
                    )
                )

        return result

    # ---------------------------------------------------
    # CHORD TONES
    # ---------------------------------------------------

    def chord_tones(
        self,
        root: str,
        scale_name: str,
        degree: int
    ) -> Tuple[Note, Note, Note]:

        scale = self.get_scale(root, scale_name)

        notes = scale.notes

        size = len(notes)

        degree -= 1

        return (
            notes[degree % size],
            notes[(degree + 2) % size],
            notes[(degree + 4) % size],
        )
            # ---------------------------------------------------
    # SCALE ANALYZER
    # ---------------------------------------------------

    def analyze_notes(
        self,
        notes: Iterable[Note]
    ) -> Dict[str, object]:

        notes = list(notes)

        if not notes:
            return {
                "count": 0,
                "lowest": None,
                "highest": None,
                "range": 0,
                "average_pitch": None,
                "pitch_classes": [],
            }

        midi = [n.midi for n in notes]

        pitch_classes = sorted({
            n.semitone
            for n in notes
        })

        return {
            "count": len(notes),
            "lowest": min(notes, key=lambda n: n.midi),
            "highest": max(notes, key=lambda n: n.midi),
            "range": max(midi) - min(midi),
            "average_pitch": sum(midi) / len(midi),
            "pitch_classes": pitch_classes,
        }

    # ---------------------------------------------------
    # KEY DETECTION
    # ---------------------------------------------------

    def detect_key(
        self,
        notes: Iterable[Note]
    ) -> List[Dict[str, object]]:

        notes = list(notes)

        if not notes:
            return []

        pitch_classes = {
            n.semitone
            for n in notes
        }

        candidates = []

        for root in NOTES_SHARP:

            root_pc = NOTE_INDEX[root]

            for scale_name, intervals in self.scales.items():

                pcs = {
                    (root_pc + i) % 12
                    for i in intervals
                }

                common = len(
                    pitch_classes & pcs
                )

                missing = len(
                    pcs - pitch_classes
                )

                extra = len(
                    pitch_classes - pcs
                )

                score = (
                    common * 5
                    - missing
                    - extra * 2
                )

                candidates.append({
                    "root": root,
                    "scale": scale_name,
                    "score": score,
                    "matches": common,
                    "missing": missing,
                    "extra": extra,
                })

        candidates.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return candidates

    # ---------------------------------------------------
    # SCALE DISTANCE
    # ---------------------------------------------------

    def nearest_scale(
        self,
        notes: Iterable[Note]
    ) -> Dict[str, object] | None:

        candidates = self.detect_key(notes)

        if not candidates:
            return None

        return candidates[0]

    # ---------------------------------------------------
    # DEGREE DETECTION
    # ---------------------------------------------------

    def note_degree(
        self,
        root: str,
        scale_name: str,
        note: Note
    ) -> int | None:

        scale = self.get_scale(root, scale_name)

        for degree, scale_note in enumerate(
            scale.notes,
            start=1
        ):

            if scale_note.semitone == note.semitone:
                return degree

        return None

    def melody_degrees(
        self,
        root: str,
        scale_name: str,
        melody: Iterable[Note]
    ) -> List[int | None]:

        return [
            self.note_degree(
                root,
                scale_name,
                note
            )
            for note in melody
        ]

    # ---------------------------------------------------
    # SCALE STATISTICS
    # ---------------------------------------------------

    def statistics(
        self,
        root: str,
        scale_name: str
    ) -> Dict[str, object]:

        scale = self.get_scale(
            root,
            scale_name
        )

        return {
            "root": scale.root.name,
            "scale": scale.name,
            "notes": [n.name for n in scale.notes],
            "pitch_classes": scale.pitch_classes,
            "degrees": len(scale.notes),
            "camelot": self.camelot(
                root,
                scale_name
            ),
        }
            # ---------------------------------------------------
    # SCALE TRANSFORMATIONS
    # ---------------------------------------------------

    def invert_scale(
        self,
        root: str,
        scale_name: str
    ) -> List[int]:

        scale = self.get_scale(root, scale_name)

        intervals = list(scale.intervals)

        result = []

        for value in intervals:
            result.append((12 - value) % 12)

        return sorted(set(result))

    def mirror_melody(
        self,
        melody: Iterable[Note],
        axis: Note
    ) -> List[Note]:

        result = []

        for note in melody:

            distance = note.midi - axis.midi

            result.append(
                Note.from_midi(
                    axis.midi - distance
                )
            )

        return result

    def reverse_melody(
        self,
        melody: Iterable[Note]
    ) -> List[Note]:

        return list(reversed(list(melody)))

    def transpose_to_key(
        self,
        melody: Iterable[Note],
        old_root: str,
        new_root: str
    ) -> List[Note]:

        old_pc = NOTE_INDEX[old_root]
        new_pc = NOTE_INDEX[new_root]

        shift = (new_pc - old_pc) % 12

        return self.transpose_melody(
            melody,
            shift
        )

    # ---------------------------------------------------
    # SCALE MATRICES
    # ---------------------------------------------------

    def interval_matrix(
        self,
        scale: Scale
    ) -> List[List[int]]:

        matrix = []

        for first in scale.notes:

            row = []

            for second in scale.notes:

                row.append(
                    (second.semitone - first.semitone) % 12
                )

            matrix.append(row)

        return matrix

    def degree_matrix(
        self,
        scale: Scale
    ) -> Dict[int, Dict[int, int]]:

        matrix = {}

        for i, first in enumerate(scale.notes):

            matrix[i + 1] = {}

            for j, second in enumerate(scale.notes):

                matrix[i + 1][j + 1] = (
                    second.semitone - first.semitone
                ) % 12

        return matrix

    # ---------------------------------------------------
    # SCALE CACHE
    # ---------------------------------------------------

    _scale_cache: Dict[
        tuple[str, str],
        Scale
    ] = {}

    def cached_scale(
        self,
        root: str,
        scale_name: str
    ) -> Scale:

        key = (
            root,
            scale_name
        )

        if key not in self._scale_cache:

            self._scale_cache[key] = self.get_scale(
                root,
                scale_name
            )

        return self._scale_cache[key]

    def clear_cache(self):

        self._scale_cache.clear()

    # ---------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------

    def validate_scale(
        self,
        scale_name: str
    ) -> bool:

        if scale_name not in self.scales:
            return False

        values = self.scales[scale_name]

        if not values:
            return False

        if values[0] != 0:
            return False

        if any(
            interval < 0 or interval > 11
            for interval in values
        ):
            return False

        if len(values) != len(set(values)):
            return False

        return True

    def validate_all(self) -> bool:

        return all(
            self.validate_scale(name)
            for name in self.scales
        )

    # ---------------------------------------------------
    # EXPORT
    # ---------------------------------------------------

    def export_scale(
        self,
        root: str,
        scale_name: str
    ) -> Dict[str, object]:

        scale = self.get_scale(
            root,
            scale_name
        )

        return {
            "root": root,
            "scale": scale_name,
            "intervals": list(scale.intervals),
            "notes": [
                note.name
                for note in scale.notes
            ],
            "pitch_classes": scale.pitch_classes,
        }


__all__ = [
    "Note",
    "Scale",
    "ScaleEngine",
    "SCALES",
    "INTERVALS",
    "NOTE_INDEX",
    "NOTES_SHARP",
    "NOTES_FLAT",
]
    # ---------------------------------------------------
    # ENHARMONIC SPELLING
    # ---------------------------------------------------

    ENHARMONIC_EQUIVALENTS = {
        "B#": "C",
        "Cb": "B",
        "E#": "F",
        "Fb": "E",
        "C#": "Db",
        "Db": "C#",
        "D#": "Eb",
        "Eb": "D#",
        "F#": "Gb",
        "Gb": "F#",
        "G#": "Ab",
        "Ab": "G#",
        "A#": "Bb",
        "Bb": "A#",
    }

    def enharmonic(self, note: str) -> str:

        return self.ENHARMONIC_EQUIVALENTS.get(note, note)

    # ---------------------------------------------------
    # SCALE MODES
    # ---------------------------------------------------

    def modes(
        self,
        root: str,
        scale_name: str
    ) -> List[Scale]:

        scale = self.get_scale(root, scale_name)

        modes: List[Scale] = []

        notes = scale.notes
        intervals = list(scale.intervals)

        for rotation in range(len(intervals)):

            current = intervals[rotation:] + intervals[:rotation]

            base = current[0]

            current = tuple(
                (value - base) % 12
                for value in current
            )

            modes.append(
                Scale(
                    root=notes[rotation],
                    name=f"{scale_name}_mode_{rotation+1}",
                    intervals=current
                )
            )

        return modes

    # ---------------------------------------------------
    # SCALE RELATIONS
    # ---------------------------------------------------

    def shared_pitch_classes(
        self,
        first: Scale,
        second: Scale
    ) -> List[int]:

        return sorted(
            set(first.pitch_classes)
            &
            set(second.pitch_classes)
        )

    def difference_pitch_classes(
        self,
        first: Scale,
        second: Scale
    ) -> List[int]:

        return sorted(
            set(first.pitch_classes)
            -
            set(second.pitch_classes)
        )

    # ---------------------------------------------------
    # OCTAVE OPERATIONS
    # ---------------------------------------------------

    def octave_up(
        self,
        notes: Iterable[Note]
    ) -> List[Note]:

        return [
            note.transpose(12)
            for note in notes
        ]

    def octave_down(
        self,
        notes: Iterable[Note]
    ) -> List[Note]:

        return [
            note.transpose(-12)
            for note in notes
        ]

    # ---------------------------------------------------
    # NEAREST SCALE NOTE
    # ---------------------------------------------------

    def nearest_note(
        self,
        root: str,
        scale_name: str,
        note: Note
    ) -> Note:

        scale = self.get_scale(root, scale_name)

        best = None
        best_distance = 999

        for candidate in scale.notes:

            distance = min(
                abs(candidate.semitone - note.semitone),
                12 - abs(candidate.semitone - note.semitone)
            )

            if distance < best_distance:

                best_distance = distance
                best = candidate

        return Note(
            best.name,
            note.octave
        )

    # ---------------------------------------------------
    # SCALE FIT SCORE
    # ---------------------------------------------------

    def fit_score(
        self,
        root: str,
        scale_name: str,
        melody: Iterable[Note]
    ) -> float:

        melody = list(melody)

        if not melody:
            return 0.0

        scale = self.get_scale(root, scale_name)

        ok = 0

        for note in melody:

            if scale.contains(note):
                ok += 1

        return ok / len(melody)

    # ---------------------------------------------------
    # MIDI NORMALIZATION
    # ---------------------------------------------------

    @staticmethod
    def normalize_midi(
        notes: Iterable[int]
    ) -> List[int]:

        return [
            note % 12
            for note in notes
        ]

    # ---------------------------------------------------
    # UNIQUE PITCH CLASSES
    # ---------------------------------------------------

    @staticmethod
    def unique_pitch_classes(
        notes: Iterable[Note]
    ) -> List[int]:

        return sorted({
            note.semitone
            for note in notes
        })

    # ---------------------------------------------------
    # SCALE SORT
    # ---------------------------------------------------

    @staticmethod
    def sort_by_pitch(
        notes: Iterable[Note]
    ) -> List[Note]:

        return sorted(
            notes,
            key=lambda n: (n.octave, n.semitone)
        )
            # ---------------------------------------------------
    # SCALE LIBRARY
    # ---------------------------------------------------

    EXTRA_SCALES: Dict[str, Tuple[int, ...]] = {

        # Jazz
        "bebop_major": (0, 2, 4, 5, 7, 8, 9, 11),
        "bebop_dominant": (0, 2, 4, 5, 7, 9, 10, 11),
        "bebop_minor": (0, 2, 3, 4, 5, 7, 9, 10),

        # Symmetric
        "octatonic_wh": (0, 2, 3, 5, 6, 8, 9, 11),
        "octatonic_hw": (0, 1, 3, 4, 6, 7, 9, 10),

        # Pentatonic
        "egyptian": (0, 2, 5, 7, 10),
        "man_gong": (0, 2, 4, 7, 9),
        "ritusen": (0, 2, 5, 7, 9),
        "hirajoshi": (0, 2, 3, 7, 8),
        "iwato": (0, 1, 5, 6, 10),
        "insen": (0, 1, 5, 7, 10),
        "kumoi": (0, 2, 3, 7, 9),

        # Exotic
        "arabian": (0, 2, 4, 5, 6, 8, 10),
        "persian": (0, 1, 4, 5, 6, 8, 11),
        "byzantine": (0, 1, 4, 5, 7, 8, 11),
        "hungarian_minor": (0, 2, 3, 6, 7, 8, 11),
        "hungarian_major": (0, 3, 4, 6, 7, 9, 10),
        "ukrainian_dorian": (0, 2, 3, 6, 7, 9, 10),
        "romanian_minor": (0, 2, 3, 6, 7, 9, 10),
        "neapolitan_major": (0, 1, 3, 5, 7, 9, 11),
        "neapolitan_minor": (0, 1, 3, 5, 7, 8, 11),
        "enigmatic": (0, 1, 4, 6, 8, 10, 11),
        "prometheus": (0, 2, 4, 6, 9, 10),
        "lydian_augmented": (0, 2, 4, 6, 8, 9, 11),
        "leading_whole_tone": (0, 2, 4, 6, 8, 10, 11),
        "double_harmonic": (0, 1, 4, 5, 7, 8, 11),

        # Minor family
        "melodic_minor_desc": (0, 2, 3, 5, 7, 8, 10),
        "harmonic_major": (0, 2, 4, 5, 7, 8, 11),

        # Utility
        "tritone": (0, 6),
        "power": (0, 7),
    }

    def register_builtin_scales(self) -> None:

        self.scales.update(self.EXTRA_SCALES)

    # ---------------------------------------------------
    # SCALE LOOKUP
    # ---------------------------------------------------

    def all_scales(self) -> List[str]:

        return sorted(self.scales.keys())

    def scale_count(self) -> int:

        return len(self.scales)

    def has_scale(
        self,
        name: str
    ) -> bool:

        return name in self.scales

    def intervals(
        self,
        scale_name: str
    ) -> Tuple[int, ...]:

        if scale_name not in self.scales:
            raise ValueError(scale_name)

        return self.scales[scale_name]

    # ---------------------------------------------------
    # SCALE CREATION
    # ---------------------------------------------------

    def create_scale(
        self,
        name: str,
        intervals: Iterable[int],
        overwrite: bool = False
    ):

        if (
            name in self.scales
            and
            not overwrite
        ):
            raise ValueError(
                f"Scale '{name}' already exists."
            )

        cleaned = sorted({
            int(i) % 12
            for i in intervals
        })

        if cleaned[0] != 0:
            cleaned.insert(0, 0)

        self.scales[name] = tuple(cleaned)

    def remove_scale(
        self,
        name: str
    ):

        if name in self.scales:
            del self.scales[name]

    # ---------------------------------------------------
    # SCALE ROTATION
    # ---------------------------------------------------

    def rotate_intervals(
        self,
        intervals: Iterable[int],
        rotation: int
    ) -> Tuple[int, ...]:

        intervals = list(intervals)

        rotation %= len(intervals)

        values = (
            intervals[rotation:]
            +
            intervals[:rotation]
        )

        first = values[0]

        return tuple(
            (v - first) % 12
            for v in values
        )

    # ---------------------------------------------------
    # ENGINE INITIALIZATION
    # ---------------------------------------------------

    def initialize(self):

        self.register_builtin_scales()

        return self
            # ---------------------------------------------------
    # DIATONIC SEVENTH CHORDS
    # ---------------------------------------------------

    def diatonic_seventh_chords(
        self,
        root: str,
        scale_name: str
    ) -> List[Dict[str, object]]:

        scale = self.get_scale(root, scale_name)

        notes = scale.notes
        size = len(notes)

        result: List[Dict[str, object]] = []

        for degree in range(size):

            chord = [
                notes[degree % size],
                notes[(degree + 2) % size],
                notes[(degree + 4) % size],
                notes[(degree + 6) % size],
            ]

            pcs = [n.semitone for n in chord]

            i3 = (pcs[1] - pcs[0]) % 12
            i5 = (pcs[2] - pcs[0]) % 12
            i7 = (pcs[3] - pcs[0]) % 12

            if (i3, i5, i7) == (4, 7, 11):
                quality = "maj7"

            elif (i3, i5, i7) == (4, 7, 10):
                quality = "7"

            elif (i3, i5, i7) == (3, 7, 10):
                quality = "min7"

            elif (i3, i5, i7) == (3, 6, 10):
                quality = "m7b5"

            elif (i3, i5, i7) == (3, 6, 9):
                quality = "dim7"

            elif (i3, i5, i7) == (4, 8, 11):
                quality = "maj7#5"

            else:
                quality = "unknown"

            result.append({
                "degree": degree + 1,
                "quality": quality,
                "notes": chord,
                "intervals": (
                    i3,
                    i5,
                    i7
                ),
            })

        return result

    # ---------------------------------------------------
    # SCALE SCORE
    # ---------------------------------------------------

    def score_scale(
        self,
        root: str,
        scale_name: str,
        melody: Iterable[Note]
    ) -> Dict[str, object]:

        melody = list(melody)

        scale = self.get_scale(
            root,
            scale_name
        )

        inside = 0
        outside = 0

        outside_notes = []

        for note in melody:

            if scale.contains(note):
                inside += 1
            else:
                outside += 1
                outside_notes.append(note)

        total = max(
            len(melody),
            1
        )

        return {
            "inside": inside,
            "outside": outside,
            "coverage": inside / total,
            "outside_notes": outside_notes,
        }

    # ---------------------------------------------------
    # SCALE CORRECTION
    # ---------------------------------------------------

    def force_scale(
        self,
        melody: Iterable[Note],
        root: str,
        scale_name: str
    ) -> List[Note]:

        result = []

        scale = self.get_scale(
            root,
            scale_name
        )

        pcs = scale.pitch_classes

        for note in melody:

            if note.semitone in pcs:

                result.append(note)

                continue

            best_pitch = min(
                pcs,
                key=lambda pc: min(
                    (pc - note.semitone) % 12,
                    (note.semitone - pc) % 12
                )
            )

            midi = (
                note.octave + 1
            ) * 12 + best_pitch

            result.append(
                Note.from_midi(midi)
            )

        return result

    # ---------------------------------------------------
    # SCALE GENERATOR
    # ---------------------------------------------------

    def generate_scale(
        self,
        root: str,
        scale_name: str,
        octaves: int = 2,
        ascending: bool = True
    ) -> List[Note]:

        scale = self.expand_scale(
            root,
            scale_name,
            octaves
        )

        if not ascending:
            scale.reverse()

        return scale

    # ---------------------------------------------------
    # SCALE SUMMARY
    # ---------------------------------------------------

    def summary(
        self,
        root: str,
        scale_name: str
    ) -> str:

        scale = self.get_scale(
            root,
            scale_name
        )

        return (
            f"{root} {scale_name}: "
            + ", ".join(
                note.name
                for note in scale.notes
            )
        )
            # ---------------------------------------------------
    # STABLE / UNSTABLE DEGREES
    # ---------------------------------------------------

    STABLE_DEGREES = {
        "major": (1, 3, 5),
        "natural_minor": (1, 3, 5),
        "harmonic_minor": (1, 3, 5),
        "melodic_minor": (1, 3, 5),
    }

    def stable_degrees(
        self,
        scale_name: str
    ) -> tuple[int, ...]:

        return self.STABLE_DEGREES.get(
            scale_name,
            (1, 3, 5)
        )

    def unstable_degrees(
        self,
        scale_name: str
    ) -> tuple[int, ...]:

        stable = set(
            self.stable_degrees(scale_name)
        )

        size = len(
            self.scales[scale_name]
        )

        return tuple(
            degree
            for degree in range(1, size + 1)
            if degree not in stable
        )

    def is_stable_degree(
        self,
        scale_name: str,
        degree: int
    ) -> bool:

        return degree in self.stable_degrees(scale_name)

    # ---------------------------------------------------
    # TENDENCY TONES
    # ---------------------------------------------------

    def tendency_degree(
        self,
        scale_name: str,
        degree: int
    ) -> int:

        if scale_name == "major":

            mapping = {
                7: 1,
                4: 3,
                6: 5,
                2: 1,
            }

            return mapping.get(
                degree,
                degree
            )

        mapping = {
            2: 1,
            6: 5,
            7: 1,
        }

        return mapping.get(
            degree,
            degree
        )

    def resolve_degree(
        self,
        root: str,
        scale_name: str,
        degree: int
    ) -> Note:

        target = self.tendency_degree(
            scale_name,
            degree
        )

        return self.degree(
            root,
            scale_name,
            target
        )

    # ---------------------------------------------------
    # NEIGHBOR NOTES
    # ---------------------------------------------------

    def upper_neighbor(
        self,
        root: str,
        scale_name: str,
        degree: int
    ) -> Note:

        scale = self.get_scale(
            root,
            scale_name
        )

        return scale.degree(
            (degree % len(scale.notes)) + 1
        )

    def lower_neighbor(
        self,
        root: str,
        scale_name: str,
        degree: int
    ) -> Note:

        scale = self.get_scale(
            root,
            scale_name
        )

        size = len(scale.notes)

        return scale.degree(
            ((degree - 2) % size) + 1
        )

    # ---------------------------------------------------
    # PASSING NOTES
    # ---------------------------------------------------

    def passing_notes(
        self,
        root: str,
        scale_name: str,
        start_degree: int,
        end_degree: int
    ) -> List[Note]:

        scale = self.get_scale(
            root,
            scale_name
        )

        result = []

        if start_degree < end_degree:

            for degree in range(
                start_degree,
                end_degree + 1
            ):
                result.append(
                    scale.degree(degree)
                )

        else:

            for degree in range(
                start_degree,
                end_degree - 1,
                -1
            ):
                result.append(
                    scale.degree(degree)
                )

        return result

    # ---------------------------------------------------
    # CHORD SCALE RELATIONSHIP
    # ---------------------------------------------------

    def chord_scale_degrees(
        self,
        chord: Iterable[Note],
        root: str,
        scale_name: str
    ) -> List[int | None]:

        result = []

        for note in chord:

            result.append(
                self.note_degree(
                    root,
                    scale_name,
                    note
                )
            )

        return result

    # ---------------------------------------------------
    # VOICE LEADING
    # ---------------------------------------------------

    def nearest_voice_leading(
        self,
        source: Iterable[Note],
        target: Iterable[Note]
    ) -> List[tuple[Note, Note]]:

        source = sorted(
            source,
            key=lambda n: n.midi
        )

        target = sorted(
            target,
            key=lambda n: n.midi
        )

        result = []

        used = set()

        for s in source:

            best = None
            best_distance = 999

            for index, t in enumerate(target):

                if index in used:
                    continue

                distance = abs(
                    s.midi - t.midi
                )

                if distance < best_distance:

                    best_distance = distance
                    best = (index, t)

            if best:

                used.add(best[0])

                result.append(
                    (s, best[1])
                )

        return result
            # ---------------------------------------------------
    # MOTION ANALYSIS
    # ---------------------------------------------------

    @staticmethod
    def melodic_motion(
        melody: Iterable[Note]
    ) -> List[int]:

        melody = list(melody)

        if len(melody) < 2:
            return []

        return [
            melody[i + 1].midi - melody[i].midi
            for i in range(len(melody) - 1)
        ]

    @staticmethod
    def melodic_intervals(
        melody: Iterable[Note]
    ) -> List[int]:

        return [
            abs(interval)
            for interval in ScaleEngine.melodic_motion(melody)
        ]

    @staticmethod
    def contour(
        melody: Iterable[Note]
    ) -> List[int]:

        melody = list(melody)

        if len(melody) < 2:
            return []

        contour = []

        for i in range(len(melody) - 1):

            diff = melody[i + 1].midi - melody[i].midi

            if diff > 0:
                contour.append(1)

            elif diff < 0:
                contour.append(-1)

            else:
                contour.append(0)

        return contour

    # ---------------------------------------------------
    # LEAP ANALYSIS
    # ---------------------------------------------------

    @staticmethod
    def leap_indices(
        melody: Iterable[Note],
        threshold: int = 5
    ) -> List[int]:

        melody = list(melody)

        result = []

        for i in range(len(melody) - 1):

            if abs(
                melody[i + 1].midi -
                melody[i].midi
            ) >= threshold:

                result.append(i)

        return result

    @staticmethod
    def step_indices(
        melody: Iterable[Note]
    ) -> List[int]:

        melody = list(melody)

        result = []

        for i in range(len(melody) - 1):

            distance = abs(
                melody[i + 1].midi -
                melody[i].midi
            )

            if distance in (1, 2):

                result.append(i)

        return result

    # ---------------------------------------------------
    # RHYTHM-INDEPENDENT PHRASE ANALYSIS
    # ---------------------------------------------------

    @staticmethod
    def highest_note(
        melody: Iterable[Note]
    ) -> Note | None:

        melody = list(melody)

        if not melody:
            return None

        return max(
            melody,
            key=lambda n: n.midi
        )

    @staticmethod
    def lowest_note(
        melody: Iterable[Note]
    ) -> Note | None:

        melody = list(melody)

        if not melody:
            return None

        return min(
            melody,
            key=lambda n: n.midi
        )

    @staticmethod
    def melodic_range(
        melody: Iterable[Note]
    ) -> int:

        melody = list(melody)

        if len(melody) < 2:
            return 0

        return (
            max(n.midi for n in melody)
            -
            min(n.midi for n in melody)
        )

    # ---------------------------------------------------
    # SCALE TENSION
    # ---------------------------------------------------

    DEGREE_TENSION_MAJOR = {
        1: 0.00,
        2: 0.55,
        3: 0.15,
        4: 0.90,
        5: 0.05,
        6: 0.45,
        7: 1.00,
    }

    DEGREE_TENSION_MINOR = {
        1: 0.00,
        2: 0.60,
        3: 0.20,
        4: 0.70,
        5: 0.10,
        6: 0.80,
        7: 0.95,
    }

    def degree_tension(
        self,
        scale_name: str,
        degree: int
    ) -> float:

        if "minor" in scale_name:

            return self.DEGREE_TENSION_MINOR.get(
                degree,
                0.5
            )

        return self.DEGREE_TENSION_MAJOR.get(
            degree,
            0.5
        )

    def melody_tension(
        self,
        melody: Iterable[Note],
        root: str,
        scale_name: str
    ) -> float:

        melody = list(melody)

        if not melody:
            return 0.0

        tension = 0.0

        for note in melody:

            degree = self.note_degree(
                root,
                scale_name,
                note
            )

            if degree is None:

                tension += 1.0

            else:

                tension += self.degree_tension(
                    scale_name,
                    degree
                )

        return tension / len(melody)
            # ---------------------------------------------------
    # PHRASE ANALYSIS
    # ---------------------------------------------------

    @staticmethod
    def phrase_center(
        melody: Iterable[Note]
    ) -> float:

        melody = list(melody)

        if not melody:
            return 0.0

        return sum(
            note.midi
            for note in melody
        ) / len(melody)

    @staticmethod
    def pitch_histogram(
        melody: Iterable[Note]
    ) -> Dict[int, int]:

        histogram: Dict[int, int] = {}

        for note in melody:

            histogram.setdefault(
                note.semitone,
                0
            )

            histogram[note.semitone] += 1

        return histogram

    @staticmethod
    def octave_histogram(
        melody: Iterable[Note]
    ) -> Dict[int, int]:

        histogram: Dict[int, int] = {}

        for note in melody:

            histogram.setdefault(
                note.octave,
                0
            )

            histogram[note.octave] += 1

        return histogram

    @staticmethod
    def note_histogram(
        melody: Iterable[Note]
    ) -> Dict[str, int]:

        histogram: Dict[str, int] = {}

        for note in melody:

            histogram.setdefault(
                note.name,
                0
            )

            histogram[note.name] += 1

        return histogram

    # ---------------------------------------------------
    # INTERVAL STATISTICS
    # ---------------------------------------------------

    @staticmethod
    def interval_histogram(
        melody: Iterable[Note]
    ) -> Dict[int, int]:

        melody = list(melody)

        histogram: Dict[int, int] = {}

        if len(melody) < 2:
            return histogram

        for i in range(len(melody) - 1):

            interval = abs(
                melody[i + 1].midi -
                melody[i].midi
            )

            histogram.setdefault(
                interval,
                0
            )

            histogram[interval] += 1

        return histogram

    @staticmethod
    def average_interval(
        melody: Iterable[Note]
    ) -> float:

        intervals = ScaleEngine.melodic_intervals(
            melody
        )

        if not intervals:
            return 0.0

        return sum(intervals) / len(intervals)

    @staticmethod
    def largest_interval(
        melody: Iterable[Note]
    ) -> int:

        intervals = ScaleEngine.melodic_intervals(
            melody
        )

        if not intervals:
            return 0

        return max(intervals)

    # ---------------------------------------------------
    # REPETITION ANALYSIS
    # ---------------------------------------------------

    @staticmethod
    def repeated_notes(
        melody: Iterable[Note]
    ) -> int:

        melody = list(melody)

        repeats = 0

        for i in range(len(melody) - 1):

            if melody[i].midi == melody[i + 1].midi:

                repeats += 1

        return repeats

    @staticmethod
    def repeated_pitch_classes(
        melody: Iterable[Note]
    ) -> int:

        melody = list(melody)

        repeats = 0

        for i in range(len(melody) - 1):

            if (
                melody[i].semitone ==
                melody[i + 1].semitone
            ):

                repeats += 1

        return repeats

    # ---------------------------------------------------
    # MELODIC DENSITY
    # ---------------------------------------------------

    @staticmethod
    def unique_pitch_count(
        melody: Iterable[Note]
    ) -> int:

        return len({

            note.midi

            for note in melody

        })

    @staticmethod
    def unique_pitch_class_count(
        melody: Iterable[Note]
    ) -> int:

        return len({

            note.semitone

            for note in melody

        })

    @staticmethod
    def melodic_entropy(
        melody: Iterable[Note]
    ) -> float:

        histogram = ScaleEngine.note_histogram(
            melody
        )

        total = sum(
            histogram.values()
        )

        if total == 0:
            return 0.0

        entropy = 0.0

        for count in histogram.values():

            p = count / total

            entropy -= p * math.log2(p)

        return entropy

    # ---------------------------------------------------
    # MOTIF DETECTION
    # ---------------------------------------------------

    @staticmethod
    def find_repeated_patterns(
        melody: Iterable[Note],
        length: int = 4
    ) -> Dict[Tuple[int, ...], int]:

        melody = list(melody)

        patterns: Dict[
            Tuple[int, ...],
            int
        ] = {}

        if len(melody) < length:
            return patterns

        midi = [
            note.midi
            for note in melody
        ]

        for i in range(
            len(midi) - length + 1
        ):

            pattern = tuple(
                midi[i:i + length]
            )

            patterns.setdefault(
                pattern,
                0
            )

            patterns[pattern] += 1

        return {

            pattern: count

            for pattern, count

            in patterns.items()

            if count > 1

        }
            # ---------------------------------------------------
    # SCALE PROFILE
    # ---------------------------------------------------

    def profile(
        self,
        root: str,
        scale_name: str
    ) -> Dict[str, object]:

        scale = self.get_scale(root, scale_name)

        return {
            "root": root,
            "name": scale_name,
            "note_count": len(scale.notes),
            "notes": [n.name for n in scale.notes],
            "midi": [n.midi for n in scale.notes],
            "pitch_classes": scale.pitch_classes,
            "intervals": list(scale.intervals),
            "camelot": self.camelot(root, scale_name),
            "relative_major": (
                self.relative_major(root)
                if "minor" in scale_name
                else None
            ),
            "relative_minor": (
                self.relative_minor(root)
                if "major" == scale_name
                else None
            ),
        }

    # ---------------------------------------------------
    # NOTE WEIGHTS
    # ---------------------------------------------------

    def weighted_pitch_classes(
        self,
        melody: Iterable[Note]
    ) -> Dict[int, float]:

        melody = list(melody)

        if not melody:
            return {}

        histogram = {}

        for note in melody:

            histogram.setdefault(
                note.semitone,
                0.0
            )

            histogram[note.semitone] += 1.0

        total = sum(histogram.values())

        return {
            pc: value / total
            for pc, value in histogram.items()
        }

    # ---------------------------------------------------
    # SCALE CONFIDENCE
    # ---------------------------------------------------

    def confidence(
        self,
        melody: Iterable[Note],
        root: str,
        scale_name: str
    ) -> float:

        melody = list(melody)

        if not melody:
            return 0.0

        scale = self.get_scale(
            root,
            scale_name
        )

        weights = self.weighted_pitch_classes(
            melody
        )

        score = 0.0

        for pc, weight in weights.items():

            if pc in scale.pitch_classes:
                score += weight

        return round(score, 4)

    # ---------------------------------------------------
    # DEGREE WEIGHTS
    # ---------------------------------------------------

    def degree_distribution(
        self,
        melody: Iterable[Note],
        root: str,
        scale_name: str
    ) -> Dict[int, int]:

        distribution = {}

        for note in melody:

            degree = self.note_degree(
                root,
                scale_name,
                note
            )

            if degree is None:
                continue

            distribution.setdefault(
                degree,
                0
            )

            distribution[degree] += 1

        return distribution

    # ---------------------------------------------------
    # MELODIC GRAVITY
    # ---------------------------------------------------

    def gravity(
        self,
        melody: Iterable[Note],
        root: str,
        scale_name: str
    ) -> float:

        distribution = self.degree_distribution(
            melody,
            root,
            scale_name
        )

        if not distribution:
            return 0.0

        gravity_score = 0.0

        for degree, count in distribution.items():

            gravity_score += (
                (1.0 - self.degree_tension(
                    scale_name,
                    degree
                ))
                * count
            )

        return gravity_score / sum(
            distribution.values()
        )

    # ---------------------------------------------------
    # SCALE SIGNATURE
    # ---------------------------------------------------

    def signature(
        self,
        root: str,
        scale_name: str
    ) -> str:

        scale = self.get_scale(
            root,
            scale_name
        )

        return "-".join(
            map(
                str,
                scale.pitch_classes
            )
        )

    # ---------------------------------------------------
    # SCALE HASH
    # ---------------------------------------------------

    def scale_hash(
        self,
        root: str,
        scale_name: str
    ) -> int:

        return hash(
            (
                root,
                scale_name,
                tuple(
                    self.get_scale(
                        root,
                        scale_name
                    ).pitch_classes
                )
            )
        )

    # ---------------------------------------------------
    # ENGINE INFO
    # ---------------------------------------------------

    def info(self) -> Dict[str, object]:

        return {
            "registered_scales": len(self.scales),
            "built_in_scales": len(SCALES),
            "extended_scales": len(self.EXTRA_SCALES),
            "cached_scales": len(self._scale_cache),
            "intervals": len(INTERVALS),
            "supported_notes": len(NOTE_INDEX),
        }
        