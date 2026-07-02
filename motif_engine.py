from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import copy
import random


# --------------------------------------------------
# CORE DATA MODEL
# --------------------------------------------------

@dataclass(slots=True)
class Motif:
    """
    Core motif representation.

    Parallel arrays are used for deterministic transformations:
    - notes: MIDI pitch values (int)
    - durations: note lengths (float)
    - velocities: MIDI velocity (int)
    """

    notes: List[int]
    durations: List[float]
    velocities: List[int]

    metadata: Dict = field(default_factory=dict)

    def length(self) -> int:
        return len(self.notes)

    def clone(self) -> "Motif":
        return copy.deepcopy(self)


# --------------------------------------------------
# MOTIF ENGINE
# --------------------------------------------------

class MotifEngine:

    def __init__(self):
        self.library: Dict[str, Motif] = {}
        self.history: List[Motif] = []
        self.seed: Optional[int] = None

    # -----------------------------
    # SEED CONTROL
    # -----------------------------

    def set_seed(self, seed: int):
        self.seed = seed
        random.seed(seed)

    # -----------------------------
    # LIBRARY SYSTEM
    # -----------------------------

    def save(self, name: str, motif: Motif):
        self.library[name] = motif.clone()

    def load(self, name: str) -> Motif:
        return self.library[name].clone()

    def delete(self, name: str):
        self.library.pop(name, None)

    def names(self) -> List[str]:
        return sorted(self.library.keys())

    def clear_library(self):
        self.library.clear()

    # -----------------------------
    # CREATION
    # -----------------------------

    def create(
        self,
        notes: List[int],
        durations: Optional[List[float]] = None,
        velocities: Optional[List[int]] = None
    ) -> Motif:

        n = list(notes)

        d = durations if durations is not None else [1.0] * len(n)
        v = velocities if velocities is not None else [90] * len(n)

        motif = Motif(
            notes=n,
            durations=list(d),
            velocities=list(v),
        )

        self.history.append(motif.clone())
        return motif

    # -----------------------------
    # BASIC TRANSFORMS
    # -----------------------------

    def transpose(self, motif: Motif, semitones: int) -> Motif:
        m = motif.clone()
        m.notes = [p + semitones for p in m.notes]
        return m

    def reverse(self, motif: Motif) -> Motif:
        m = motif.clone()
        m.notes.reverse()
        m.durations.reverse()
        m.velocities.reverse()
        return m

    def repeat(self, motif: Motif, times: int) -> Motif:
        m = motif.clone()
        m.notes *= times
        m.durations *= times
        m.velocities *= times
        return m

    # -----------------------------
    # PITCH OPERATIONS
    # -----------------------------

    def invert(self, motif: Motif, center: Optional[int] = None) -> Motif:
        m = motif.clone()

        if not m.notes:
            return m

        pivot = center if center is not None else m.notes[0]

        m.notes = [
            pivot - (note - pivot)
            for note in m.notes
        ]

        return m

    def mirror(self, motif: Motif, center: int = 60) -> Motif:
        return self.invert(motif, center)

    def octave_up(self, motif: Motif) -> Motif:
        return self.transpose(motif, 12)

    def octave_down(self, motif: Motif) -> Motif:
        return self.transpose(motif, -12)

    # -----------------------------
    # RHYTHMIC OPERATIONS
    # -----------------------------

    def augment(self, motif: Motif, factor: float = 2.0) -> Motif:
        m = motif.clone()
        m.durations = [d * factor for d in m.durations]
        return m

    def diminish(self, motif: Motif, factor: float = 0.5) -> Motif:
        m = motif.clone()
        m.durations = [d * factor for d in m.durations]
        return m

    def swing(self, motif: Motif, amount: float = 0.15) -> Motif:
        m = motif.clone()

        for i in range(0, len(m.durations) - 1, 2):
            delta = m.durations[i] * amount
            m.durations[i] += delta
            m.durations[i + 1] = max(0.05, m.durations[i + 1] - delta)

        return m

    def randomize_velocity(self, motif: Motif, amount: int = 10) -> Motif:
        m = motif.clone()

        m.velocities = [
            max(1, min(127, v + random.randint(-amount, amount)))
            for v in m.velocities
        ]

        return m

    # -----------------------------
    # STRUCTURAL OPERATIONS
    # -----------------------------

    def retrograde(self, motif: Motif) -> Motif:
        return self.reverse(motif)

    def retrograde_inversion(self, motif: Motif) -> Motif:
        return self.invert(self.reverse(motif))

    def sequence(self, motif: Motif, repeats: int, interval: int) -> Motif:
        base = motif.clone()
        result = motif.clone()

        for i in range(1, repeats):
            transposed = self.transpose(base, interval * i)

            result.notes.extend(transposed.notes)
            result.durations.extend(transposed.durations)
            result.velocities.extend(transposed.velocities)

        return result

    # -----------------------------
    # DENSITY CONTROL
    # -----------------------------

    def thin(self, motif: Motif, probability: float = 0.5) -> Motif:
        m = motif.clone()

        notes, durations, velocities = [], [], []

        for n, d, v in zip(m.notes, m.durations, m.velocities):
            if random.random() <= probability:
                notes.append(n)
                durations.append(d)
                velocities.append(v)

        m.notes = notes
        m.durations = durations
        m.velocities = velocities

        return m

    def duplicate_notes(self, motif: Motif, probability: float = 0.25) -> Motif:
        m = motif.clone()

        notes, durations, velocities = [], [], []

        for n, d, v in zip(m.notes, m.durations, m.velocities):
            notes.append(n)
            durations.append(d)
            velocities.append(v)

            if random.random() < probability:
                notes.append(n)
                durations.append(d)
                velocities.append(v)

        m.notes = notes
        m.durations = durations
        m.velocities = velocities

        return m

    # -----------------------------
    # UTIL
    # -----------------------------

    def clear_history(self):
        self.history.clear()