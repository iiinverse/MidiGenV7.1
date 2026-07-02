"""
MGV7 Harmony Engine

High-level harmonic intelligence.

Depends:
    scale_engine.py
    chord_engine.py
"""

from __future__ import annotations

import random

from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Iterable
from typing import Optional

from scale_engine import (
    Note,
    ScaleEngine,
)

from chord_engine import (
    Chord,
    ChordEngine,
)


# ==========================================================
# HARMONIC STATE
# ==========================================================

@dataclass(slots=True)
class HarmonicState:

    chord: Chord

    degree: int

    function: str

    tension: float

    weight: float = 1.0


# ==========================================================
# HARMONY ENGINE
# ==========================================================

class HarmonyEngine:

    def __init__(self):

        self.scale_engine = ScaleEngine()

        self.chord_engine = ChordEngine()

    # --------------------------------------------------
    # DEGREE
    # --------------------------------------------------

    def degree_chord(

        self,

        root: str,

        scale_name: str,

        degree: int

    ) -> Chord:

        return self.chord_engine.degree_to_chord(

            root,

            scale_name,

            degree

        )

    # --------------------------------------------------
    # FUNCTION
    # --------------------------------------------------

    def harmonic_function(

        self,

        root: str,

        scale_name: str,

        degree: int

    ) -> HarmonicState:

        chord = self.degree_chord(

            root,

            scale_name,

            degree

        )

        function = self.chord_engine.harmonic_function(

            degree,

            scale_name

        )

        return HarmonicState(

            chord=chord,

            degree=degree,

            function=function,

            tension=self.chord_engine.tension(chord)

        )

    # --------------------------------------------------
    # SCALE MAP
    # --------------------------------------------------

    def harmonic_map(

        self,

        root: str,

        scale_name: str

    ) -> List[HarmonicState]:

        result = []

        for degree in range(1, 8):

            result.append(

                self.harmonic_function(

                    root,

                    scale_name,

                    degree

                )

            )

        return result

    # --------------------------------------------------
    # TONIC
    # --------------------------------------------------

    def tonic(

        self,

        root: str,

        scale_name: str

    ) -> HarmonicState:

        return self.harmonic_function(

            root,

            scale_name,

            1

        )

    # --------------------------------------------------
    # SUBDOMINANT
    # --------------------------------------------------

    def subdominant(

        self,

        root: str,

        scale_name: str

    ) -> HarmonicState:

        choices = [2, 4]

        degree = random.choice(

            choices

        )

        return self.harmonic_function(

            root,

            scale_name,

            degree

        )

    # --------------------------------------------------
    # DOMINANT
    # --------------------------------------------------

    def dominant(

        self,

        root: str,

        scale_name: str

    ) -> HarmonicState:

        choices = [5, 7]

        degree = random.choice(

            choices

        )

        return self.harmonic_function(

            root,

            scale_name,

            degree

        )

    # --------------------------------------------------
    # CADENCE
    # --------------------------------------------------

    def authentic_cadence(

        self,

        root: str,

        scale_name: str

    ) -> List[Chord]:

        return [

            self.degree_chord(

                root,

                scale_name,

                5

            ),

            self.degree_chord(

                root,

                scale_name,

                1

            )

        ]

    def plagal_cadence(

        self,

        root: str,

        scale_name: str

    ) -> List[Chord]:

        return [

            self.degree_chord(

                root,

                scale_name,

                4

            ),

            self.degree_chord(

                root,

                scale_name,

                1

            )

        ]

    def deceptive_cadence(

        self,

        root: str,

        scale_name,

    ) -> List[Chord]:

        return [

            self.degree_chord(

                root,

                scale_name,

                5

            ),

            self.degree_chord(

                root,

                scale_name,

                6

            )

        ]

    def half_cadence(

        self,

        root: str,

        scale_name: str

    ) -> List[Chord]:

        return [

            self.degree_chord(

                root,

                scale_name,

                2

            ),

            self.degree_chord(

                root,

                scale_name,

                5

            )

        ]
            # --------------------------------------------------
    # FUNCTIONAL PROGRESSION GENERATOR
    # --------------------------------------------------

    FUNCTION_GRAPH = {

        "T": ("S", "D", "T"),

        "S": ("D", "T"),

        "D": ("T", "S"),

    }

    FUNCTION_DEGREES_MAJOR = {

        "T": (1, 3, 6),

        "S": (2, 4),

        "D": (5, 7),

    }

    FUNCTION_DEGREES_MINOR = {

        "T": (1, 3),

        "S": (2, 4, 6),

        "D": (5, 7),

    }

    def degree_pool(
        self,
        function: str,
        scale_name: str
    ) -> tuple[int, ...]:

        if "minor" in scale_name:

            return self.FUNCTION_DEGREES_MINOR.get(
                function,
                ()
            )

        return self.FUNCTION_DEGREES_MAJOR.get(
            function,
            ()
        )

    def random_degree(
        self,
        function: str,
        scale_name: str
    ) -> int:

        return random.choice(

            self.degree_pool(

                function,

                scale_name

            )

        )

    def next_function(
        self,
        current: str
    ) -> str:

        return random.choice(

            self.FUNCTION_GRAPH[current]

        )

    # --------------------------------------------------
    # GENERATE FUNCTION CHAIN
    # --------------------------------------------------

    def generate_functions(
        self,
        length: int = 8,
        start: str = "T"
    ) -> List[str]:

        result = [start]

        current = start

        while len(result) < length:

            current = self.next_function(
                current
            )

            result.append(current)

        return result

    # --------------------------------------------------
    # GENERATE CHORD PROGRESSION
    # --------------------------------------------------

    def generate_progression(
        self,
        root: str,
        scale_name: str,
        length: int = 8
    ) -> List[Chord]:

        functions = self.generate_functions(
            length
        )

        progression = []

        for function in functions:

            degree = self.random_degree(
                function,
                scale_name
            )

            progression.append(

                self.degree_chord(

                    root,

                    scale_name,

                    degree

                )

            )

        return progression

    # --------------------------------------------------
    # SCORE PROGRESSION
    # --------------------------------------------------

    def progression_score(
        self,
        progression: Iterable[Chord]
    ) -> float:

        progression = list(progression)

        if len(progression) < 2:
            return 0.0

        score = 0.0

        previous = progression[0]

        for chord in progression[1:]:

            movement = self.chord_engine.voice_leading_distance(

                previous,

                chord

            )

            tension = self.chord_engine.tension(
                chord
            )

            score += (

                max(
                    0,
                    30 - movement
                )

                + tension * 10

            )

            previous = chord

        return score / (len(progression) - 1)

    # --------------------------------------------------
    # BEST OF N
    # --------------------------------------------------

    def generate_best_progression(
        self,
        root: str,
        scale_name: str,
        length: int = 8,
        attempts: int = 50
    ) -> List[Chord]:

        best = None

        best_score = -1.0

        for _ in range(attempts):

            progression = self.generate_progression(

                root,

                scale_name,

                length

            )

            score = self.progression_score(
                progression
            )

            if score > best_score:

                best_score = score

                best = progression

        return best

    # --------------------------------------------------
    # VOICE LEADING OPTIMIZATION
    # --------------------------------------------------

    def optimize(
        self,
        progression: Iterable[Chord]
    ):

        return self.chord_engine.optimize_progression(
            progression
        )
            # --------------------------------------------------
    # SECONDARY DOMINANTS
    # --------------------------------------------------

    SECONDARY_DOMINANTS = {
        2: 6,
        3: 7,
        4: 1,
        5: 2,
        6: 3,
        7: 4,
    }

    def secondary_dominant(
        self,
        root: str,
        scale_name: str,
        target_degree: int
    ) -> Optional[Chord]:

        if target_degree not in self.SECONDARY_DOMINANTS:
            return None

        target = self.degree_chord(
            root,
            scale_name,
            target_degree
        )

        dominant_pc = (
            NOTE_INDEX[target.root.name] + 7
        ) % 12

        dominant_root = NOTES_SHARP[
            dominant_pc
        ]

        return self.chord_engine.create(
            dominant_root,
            "7",
            target.root.octave
        )

    # --------------------------------------------------
    # TRITONE SUBSTITUTION
    # --------------------------------------------------

    def tritone_substitution(
        self,
        chord: Chord
    ) -> Optional[Chord]:

        if chord.quality != "7":
            return None

        substitute_root = NOTES_SHARP[
            (
                NOTE_INDEX[chord.root.name]
                + 6
            ) % 12
        ]

        return self.chord_engine.create(
            substitute_root,
            "7",
            chord.root.octave
        )

    # --------------------------------------------------
    # BORROWED CHORDS
    # --------------------------------------------------

    BORROWED_MAJOR = (
        "bIII",
        "iv",
        "bVI",
        "bVII"
    )

    BORROWED_MINOR = (
        "I",
        "IV",
        "V"
    )

    def borrowed_pool(
        self,
        scale_name: str
    ) -> tuple[str, ...]:

        if "minor" in scale_name:
            return self.BORROWED_MINOR

        return self.BORROWED_MAJOR

    # --------------------------------------------------
    # MODAL INTERCHANGE
    # --------------------------------------------------

    def modal_interchange(
        self,
        root: str,
        scale_name: str
    ) -> List[str]:

        if "minor" in scale_name:

            return [
                "major",
                "dorian",
                "phrygian",
                "melodic_minor"
            ]

        return [
            "natural_minor",
            "lydian",
            "mixolydian",
            "harmonic_major"
        ]

    # --------------------------------------------------
    # CHROMATIC MEDIANTS
    # --------------------------------------------------

    def chromatic_mediants(
        self,
        chord: Chord
    ) -> List[Chord]:

        root = NOTE_INDEX[
            chord.root.name
        ]

        qualities = (
            chord.quality,
        )

        result = []

        for interval in (3, 4, 8, 9):

            note = NOTES_SHARP[
                (root + interval) % 12
            ]

            for quality in qualities:

                if quality not in self.chord_engine.chords:
                    continue

                result.append(

                    self.chord_engine.create(
                        note,
                        quality,
                        chord.root.octave
                    )

                )

        return result

    # --------------------------------------------------
    # PARALLEL KEY
    # --------------------------------------------------

    def parallel_major(
        self,
        root: str
    ) -> str:

        return root

    def parallel_minor(
        self,
        root: str
    ) -> str:

        return root

    # --------------------------------------------------
    # HARMONIC COLOR
    # --------------------------------------------------

    def harmonic_color(
        self,
        progression: Iterable[Chord]
    ) -> Dict[str, float]:

        progression = list(progression)

        if not progression:

            return {
                "brightness": 0.0,
                "tension": 0.0,
                "complexity": 0.0,
            }

        brightness = 0.0
        tension = 0.0
        complexity = 0.0

        for chord in progression:

            if self.chord_engine.is_major(chord):
                brightness += 1.0

            elif self.chord_engine.is_minor(chord):
                brightness += 0.4

            elif self.chord_engine.is_diminished(chord):
                brightness -= 0.7

            elif self.chord_engine.is_augmented(chord):
                brightness += 0.2

            tension += self.chord_engine.tension(
                chord
            )

            complexity += len(chord.notes)

        total = len(progression)

        return {

            "brightness":
                brightness / total,

            "tension":
                tension / total,

            "complexity":
                complexity / total,

        }
            # --------------------------------------------------
    # MELODY HARMONIZATION
    # --------------------------------------------------

    def harmonize_note(
        self,
        note: Note,
        root: str,
        scale_name: str
    ) -> Chord:

        degree = self.scale_engine.note_degree(
            root,
            scale_name,
            note
        )

        if degree is None:
            degree = 1

        return self.degree_chord(
            root,
            scale_name,
            degree
        )

    def harmonize_melody(
        self,
        melody: Iterable[Note],
        root: str,
        scale_name: str
    ) -> List[Chord]:

        result = []

        previous = None

        for note in melody:

            chord = self.harmonize_note(
                note,
                root,
                scale_name
            )

            if previous is not None:

                inversion = self.chord_engine.best_inversion(
                    previous,
                    chord
                )

                chord = Chord(
                    root=chord.root,
                    quality=chord.quality,
                    intervals=chord.intervals,
                    bass=inversion[0]
                )

            result.append(chord)

            previous = chord

        return result

    # --------------------------------------------------
    # STRONG BEAT HARMONIZATION
    # --------------------------------------------------

    def harmonize_strong_beats(
        self,
        melody: Iterable[Note],
        accents: Iterable[bool],
        root: str,
        scale_name: str
    ) -> List[Optional[Chord]]:

        melody = list(melody)
        accents = list(accents)

        result = []

        previous = None

        for note, accent in zip(
            melody,
            accents
        ):

            if not accent:

                result.append(None)
                continue

            chord = self.harmonize_note(
                note,
                root,
                scale_name
            )

            if previous:

                best = self.chord_engine.best_inversion(
                    previous,
                    chord
                )

                chord = Chord(
                    root=chord.root,
                    quality=chord.quality,
                    intervals=chord.intervals,
                    bass=best[0]
                )

            result.append(chord)

            previous = chord

        return result

    # --------------------------------------------------
    # EMOTION PROFILES
    # --------------------------------------------------

    EMOTION_PROFILES = {

        "happy": (
            1, 5, 6, 4
        ),

        "sad": (
            6, 4, 1, 5
        ),

        "dark": (
            1, 7, 6, 5
        ),

        "hopeful": (
            1, 2, 4, 5
        ),

        "cinematic": (
            1, 3, 4, 6
        ),

        "epic": (
            1, 5, 4, 5
        ),

        "ambient": (
            1, 4, 2, 5
        ),

    }

    def emotion_progression(
        self,
        emotion: str,
        root: str,
        scale_name: str
    ) -> List[Chord]:

        if emotion not in self.EMOTION_PROFILES:

            raise ValueError(
                emotion
            )

        return [

            self.degree_chord(
                root,
                scale_name,
                degree
            )

            for degree

            in self.EMOTION_PROFILES[
                emotion
            ]

        ]

    # --------------------------------------------------
    # PROGRESSION VARIATION
    # --------------------------------------------------

    def vary_progression(
        self,
        progression: Iterable[Chord],
        probability: float = 0.30
    ) -> List[Chord]:

        progression = list(progression)

        result = []

        for chord in progression:

            if random.random() < probability:

                substitute = self.tritone_substitution(
                    chord
                )

                if substitute:

                    result.append(substitute)

                    continue

            result.append(chord)

        return result

    # --------------------------------------------------
    # LOOP OPTIMIZATION
    # --------------------------------------------------

    def optimize_loop(
        self,
        progression: Iterable[Chord],
        passes: int = 5
    ) -> List[List[Note]]:

        progression = list(progression)

        best = None

        best_score = 10**9

        for _ in range(passes):

            voiced = self.optimize(
                progression
            )

            score = 0

            for current, nxt in zip(
                voiced[:-1],
                voiced[1:]
            ):

                for a, b in zip(current, nxt):

                    score += abs(
                        a.midi - b.midi
                    )

            if score < best_score:

                best_score = score

                best = voiced

        return best
        # --------------------------------------------------
# HARMONIC FUNCTION ENGINE
# --------------------------------------------------

from enum import Enum


class HarmonicFunction(str, Enum):
    TONIC = "T"
    SUBDOMINANT = "S"
    DOMINANT = "D"


def chord_function(self, degree: int) -> HarmonicFunction:
    """
    Maps scale degree to harmonic function.
    Assumes major/minor functional harmony model.
    """

    tonic = {1, 6, 3}
    subdominant = {2, 4}
    dominant = {5, 7}

    if degree in tonic:
        return HarmonicFunction.TONIC

    if degree in subdominant:
        return HarmonicFunction.SUBDOMINANT

    return HarmonicFunction.DOMINANT


def analyze_progression_functions(
    self,
    progression: Iterable[Chord],
    root: str,
    scale_name: str
) -> List[HarmonicFunction]:

    result = []

    for chord in progression:

        degree = self.scale_engine.chord_degree(
            root,
            scale_name,
            chord
        )

        if degree is None:
            degree = 1

        result.append(
            self.chord_function(degree)
        )

    return result
    # --------------------------------------------------
# HARMONIC CONTEXT TRACKER
# --------------------------------------------------

def get_previous_functions(
    self,
    chords: List[Chord],
    root: str,
    scale_name: str,
    window: int = 3
) -> List[str]:

    recent = chords[-window:] if len(chords) > window else chords

    functions = []

    for chord in recent:

        degree = self.scale_engine.chord_degree(
            root,
            scale_name,
            chord
        )

        if degree is None:
            degree = 1

        func = self.chord_function(degree)
        functions.append(func.value)

    return functions
    def harmonize_note(
    self,
    note: Note,
    root: str,
    scale_name: str,
    context: Optional[List[Chord]] = None
) -> Chord:

    degree = self.scale_engine.note_degree(
        root,
        scale_name,
        note
    )

    if degree is None:
        degree = 1

    base_chord = self.degree_chord(
        root,
        scale_name,
        degree
    )

    # ------------------------------------------
    # CONTEXTUAL ADJUSTMENT
    # ------------------------------------------

    if context:

        last = context[-1]

        last_degree = self.scale_engine.chord_degree(
            root,
            scale_name,
            last
        )

        if last_degree is not None:

            last_func = self.chord_function(last_degree)
            current_func = self.chord_function(degree)

            # избежание резких скачков функции
            if (
                last_func == HarmonicFunction.DOMINANT and
                current_func == HarmonicFunction.TONIC
            ):
                # усиливаем разрешение через inversion
                inversion = self.chord_engine.best_inversion(
                    last,
                    base_chord
                )

                base_chord = Chord(
                    root=base_chord.root,
                    quality=base_chord.quality,
                    intervals=base_chord.intervals,
                    bass=inversion[0]
                )

    return base_chord
    def harmonize_melody(
    self,
    melody: Iterable[Note],
    root: str,
    scale_name: str
) -> List[Chord]:

    result = []

    previous = []

    for note in melody:

        chord = self.harmonize_note(
            note,
            root,
            scale_name,
            context=previous
        )

        if previous:

            inversion = self.chord_engine.best_inversion(
                previous[-1],
                chord
            )

            chord = Chord(
                root=chord.root,
                quality=chord.quality,
                intervals=chord.intervals,
                bass=inversion[0]
            )

        result.append(chord)
        previous.append(chord)

    return result
    