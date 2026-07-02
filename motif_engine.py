from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from typing import List
from typing import Tuple
from typing import Optional
from typing import Iterable
from typing import Dict

import copy
import random


# --------------------------------------------------
# MOTIF
# --------------------------------------------------

@dataclass(slots=True)
class Motif:

    notes: List

    durations: List[float]

    velocities: List[int]

    metadata: Dict = field(
        default_factory=dict
    )


# --------------------------------------------------
# MOTIF ENGINE
# --------------------------------------------------

class MotifEngine:

    def __init__(self):

        self.library = {}

        self.history = []

        self.seed = None

    # --------------------------------------------------
    # RANDOM
    # --------------------------------------------------

    def set_seed(
        self,
        seed: int
    ):

        self.seed = seed

        random.seed(seed)

    # --------------------------------------------------
    # LIBRARY
    # --------------------------------------------------

    def save(
        self,
        name: str,
        motif: Motif
    ):

        self.library[name] = copy.deepcopy(
            motif
        )

    def load(
        self,
        name: str
    ) -> Motif:

        return copy.deepcopy(

            self.library[name]

        )

    def names(
        self
    ):

        return sorted(

            self.library.keys()

        )

    def delete(
        self,
        name: str
    ):

        if name in self.library:

            del self.library[
                name
            ]

    def clear_library(
        self
    ):

        self.library.clear()

    # --------------------------------------------------
    # CREATION
    # --------------------------------------------------

    def create(
        self,
        notes,
        durations=None,
        velocities=None
    ) -> Motif:

        notes = list(
            notes
        )

        if durations is None:

            durations = [

                1.0

                for _

                in notes

            ]

        if velocities is None:

            velocities = [

                90

                for _

                in notes

            ]

        motif = Motif(

            notes=notes,

            durations=list(
                durations
            ),

            velocities=list(
                velocities
            )

        )

        self.history.append(

            motif

        )

        return motif

    # --------------------------------------------------
    # COPY
    # --------------------------------------------------

    def clone(
        self,
        motif: Motif
    ):

        return copy.deepcopy(
            motif
        )

    # --------------------------------------------------
    # BASIC OPERATIONS
    # --------------------------------------------------

    def reverse(
        self,
        motif: Motif
    ):

        motif = self.clone(
            motif
        )

        motif.notes.reverse()

        motif.durations.reverse()

        motif.velocities.reverse()

        return motif

    def repeat(
        self,
        motif: Motif,
        times: int
    ):

        result = self.clone(
            motif
        )

        result.notes *= times

        result.durations *= times

        result.velocities *= times

        return result

    def transpose(
        self,
        motif: Motif,
        semitones: int
    ):

        motif = self.clone(
            motif
        )

        for note in motif.notes:

            note.midi += semitones

        return motif

    def octave_up(
        self,
        motif
    ):

        return self.transpose(

            motif,

            12

        )

    def octave_down(
        self,
        motif
    ):

        return self.transpose(

            motif,

            -12

        )
            # --------------------------------------------------
    # RHYTHMIC VARIATIONS
    # --------------------------------------------------

    def augment(
        self,
        motif: Motif,
        factor: float = 2.0
    ):

        motif = self.clone(
            motif
        )

        motif.durations = [

            value * factor

            for value

            in motif.durations

        ]

        return motif

    def diminish(
        self,
        motif: Motif,
        factor: float = 0.5
    ):

        motif = self.clone(
            motif
        )

        motif.durations = [

            value * factor

            for value

            in motif.durations

        ]

        return motif

    def swing(
        self,
        motif: Motif,
        amount: float = 0.15
    ):

        motif = self.clone(
            motif
        )

        for index in range(

            len(
                motif.durations
            ) - 1

        ):

            if index % 2 == 0:

                delta = (

                    motif.durations[index]

                    * amount

                )

                motif.durations[index] += delta

                motif.durations[index + 1] -= delta

        return motif

    def randomize_velocity(
        self,
        motif: Motif,
        amount: int = 10
    ):

        motif = self.clone(
            motif
        )

        motif.velocities = [

            max(

                1,

                min(

                    127,

                    velocity +

                    random.randint(

                        -amount,

                        amount

                    )

                )

            )

            for velocity

            in motif.velocities

        ]

        return motif

    # --------------------------------------------------
    # INTERVAL OPERATIONS
    # --------------------------------------------------

    def invert(
        self,
        motif: Motif
    ):

        motif = self.clone(
            motif
        )

        if not motif.notes:

            return motif

        pivot = motif.notes[0].midi

        for note in motif.notes:

            interval = (

                note.midi -

                pivot

            )

            note.midi = (

                pivot -

                interval

            )

        return motif

    def retrograde(
        self,
        motif: Motif
    ):

        return self.reverse(
            motif
        )

    def retrograde_inversion(
        self,
        motif: Motif
    ):

        return self.retrograde(

            self.invert(
                motif
            )

        )

    def mirror(
        self,
        motif: Motif,
        center: int = 60
    ):

        motif = self.clone(
            motif
        )

        for note in motif.notes:

            distance = (

                note.midi -

                center

            )

            note.midi = (

                center -

                distance

            )

        return motif

    # --------------------------------------------------
    # SEQUENCE
    # --------------------------------------------------

    def sequence(
        self,
        motif: Motif,
        repeats: int,
        interval: int
    ):

        result = self.clone(
            motif
        )

        original = self.clone(
            motif
        )

        for step in range(

            1,

            repeats

        ):

            current = self.transpose(

                original,

                interval * step

            )

            result.notes.extend(

                current.notes

            )

            result.durations.extend(

                current.durations

            )

            result.velocities.extend(

                current.velocities

            )

        return result

    # --------------------------------------------------
    # DENSITY
    # --------------------------------------------------

    def thin(
        self,
        motif: Motif,
        probability: float = 0.50
    ):

        motif = self.clone(
            motif
        )

        notes = []

        durations = []

        velocities = []

        for note, duration, velocity in zip(

            motif.notes,

            motif.durations,

            motif.velocities

        ):

            if random.random() <= probability:

                notes.append(
                    note
                )

                durations.append(
                    duration
                )

                velocities.append(
                    velocity
                )

        motif.notes = notes

        motif.durations = durations

        motif.velocities = velocities

        return motif

    def duplicate_notes(
        self,
        motif: Motif,
        probability: float = 0.25
    ):

        motif = self.clone(
            motif
        )

        notes = []

        durations = []

        velocities = []

        for note, duration, velocity in zip(

            motif.notes,

            motif.durations,

            motif.velocities

        ):

            notes.append(
                note
            )

            durations.append(
                duration
            )

            velocities.append(
                velocity
            )

            if random.random() < probability:

                notes.append(

                    copy.deepcopy(
                        note
                    )

                )

                durations.append(

                    duration

                )

                velocities.append(

                    velocity

                )

        motif.notes = notes

        motif.durations = durations

        motif.velocities = velocities

        return motif
        # motif_engine.py

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import random
import copy


# -----------------------------
# Core Data Structures
# -----------------------------

@dataclass
class NoteEvent:
    pitch: int
    velocity: int
    duration: float
    start_time: float = 0.0


@dataclass
class Motif:
    """
    A motif is a short musical idea represented as a sequence of NoteEvents.
    """
    notes: List[NoteEvent] = field(default_factory=list)
    name: Optional[str] = None

    def clone(self) -> "Motif":
        return copy.deepcopy(self)

    def total_duration(self) -> float:
        if not self.notes:
            return 0.0
        last = max(n.start_time + n.duration for n in self.notes)
        return last

    def transpose(self, semitones: int) -> "Motif":
        for n in self.notes:
            n.pitch += semitones
        return self

    def invert(self, center_pitch: Optional[int] = None) -> "Motif":
        if not self.notes:
            return self

        if center_pitch is None:
            center_pitch = self.notes[0].pitch

        for n in self.notes:
            interval = n.pitch - center_pitch
            n.pitch = center_pitch - interval
        return self

    def retrograde(self) -> "Motif":
        self.notes.reverse()
        return self

    def stretch_time(self, factor: float) -> "Motif":
        for n in self.notes:
            n.start_time *= factor
            n.duration *= factor
        return self

    def shift_velocity(self, delta: int) -> "Motif":
        for n in self.notes:
            n.velocity = max(1, min(127, n.velocity + delta))
        return self


# -----------------------------
# Motif Generator
# -----------------------------

class MotifEngine:
    """
    Generates and transforms musical motifs.
    Designed to be used as a building block for MIDI phrase generation.
    """

    def __init__(
        self,
        scale: List[int],
        base_velocity: int = 90,
        seed: Optional[int] = None
    ):
        self.scale = scale
        self.base_velocity = base_velocity

        if seed is not None:
            random.seed(seed)

    # -------------------------
    # Basic motif generation
    # -------------------------

    def generate_random_motif(
        self,
        length: int = 8,
        start_pitch: Optional[int] = None,
        step_range: Tuple[int, int] = (-5, 5),
        duration_choices: List[float] = [0.25, 0.5, 1.0]
    ) -> Motif:

        if start_pitch is None:
            start_pitch = random.choice(self.scale)

        notes = []
        current_pitch = start_pitch
        time_cursor = 0.0

        for _ in range(length):
            step = random.randint(*step_range)
            current_pitch = self._snap_to_scale(current_pitch + step)

            duration = random.choice(duration_choices)
            velocity = int(self.base_velocity + random.randint(-10, 10))

            notes.append(
                NoteEvent(
                    pitch=current_pitch,
                    velocity=velocity,
                    duration=duration,
                    start_time=time_cursor
                )
            )

            time_cursor += duration

        return Motif(notes=notes, name="random_motif")

    # -------------------------
    # Motif mutation system
    # -------------------------

    def mutate(self, motif: Motif, intensity: float = 0.2) -> Motif:
        """
        Applies controlled random mutations:
        - pitch drift
        - rhythm jitter
        - velocity noise
        """
        new_motif = motif.clone()

        for note in new_motif.notes:
            if random.random() < intensity:
                note.pitch = self._snap_to_scale(
                    note.pitch + random.randint(-2, 2)
                )

            if random.random() < intensity:
                note.duration = max(
                    0.1,
                    note.duration + random.uniform(-0.1, 0.1)
                )

            if random.random() < intensity:
                note.velocity = max(
                    1,
                    min(127, note.velocity + random.randint(-15, 15))
                )

        return new_motif

    # -------------------------
    # Motif expansion
    # -------------------------

    def expand_motif(self, motif: Motif, repeats: int = 2) -> Motif:
        """
        Repeats motif with slight variations over time.
        """
        expanded_notes = []
        time_offset = 0.0

        for i in range(repeats):
            clone = motif.clone()

            # progressive variation per repeat
            transpose_amount = random.choice([-2, -1, 0, 1, 2]) * i
            clone.transpose(transpose_amount)

            velocity_shift = i * 3

            for note in clone.notes:
                note.start_time += time_offset
                note.velocity = max(1, min(127, note.velocity + velocity_shift))

            expanded_notes.extend(clone.notes)

            time_offset += clone.total_duration()

        return Motif(notes=expanded_notes, name="expanded_motif")

    # -------------------------
    # Utility functions
    # -------------------------

    def _snap_to_scale(self, pitch: int) -> int:
        """
        Snap a MIDI note to nearest scale tone.
        """
        return min(self.scale, key=lambda x: abs(x - pitch))


# -----------------------------
# Example usage (optional)
# -----------------------------

if __name__ == "__main__":
    engine = MotifEngine(scale=[60, 62, 64, 65, 67, 69, 71, 72], seed=42)

    motif = engine.generate_random_motif(length=8)
    mutated = engine.mutate(motif, intensity=0.3)
    expanded = engine.expand_motif(mutated, repeats=3)

    print("Original:", motif)
    print("Mutated:", mutated)
    print("Expanded:", expanded)
        