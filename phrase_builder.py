from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
import copy
import random

# --------------------------------------------------
# PHRASE MODEL
# --------------------------------------------------

@dataclass(slots=True)
class Phrase:
    """
    A phrase is a structured sequence of motifs arranged in time.
    """

    motifs: List["Motif"]
    start_times: List[float] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)

    def clone(self) -> "Phrase":
        return copy.deepcopy(self)

    def total_duration(self) -> float:
        if not self.motifs:
            return 0.0

        end_times = []

        for motif, start in zip(self.motifs, self.start_times):
            duration = sum(motif.durations)
            end_times.append(start + duration)

        return max(end_times) if end_times else 0.0


# --------------------------------------------------
# PHRASE BUILDER ENGINE
# --------------------------------------------------

class PhraseBuilder:

    def __init__(self):
        self.history: List[Phrase] = []
        self.seed: Optional[int] = None

    # -----------------------------
    # SEED CONTROL
    # -----------------------------

    def set_seed(self, seed: int):
        self.seed = seed
        random.seed(seed)

    # -----------------------------
    # CORE BUILDING BLOCK
    # -----------------------------

    def build_linear(
        self,
        motifs: List["Motif"],
        spacing: float = 0.0
    ) -> Phrase:
        """
        Places motifs sequentially in time.
        """

        start_times = []
        cursor = 0.0

        for m in motifs:
            start_times.append(cursor)
            cursor += sum(m.durations) + spacing

        phrase = Phrase(
            motifs=[m.clone() for m in motifs],
            start_times=start_times
        )

        self.history.append(phrase.clone())
        return phrase

    # -----------------------------
    # STRUCTURAL VARIATION
    # -----------------------------

    def repeat_phrase(
        self,
        phrase: Phrase,
        times: int,
        gap: float = 0.0
    ) -> Phrase:
        """
        Repeats entire phrase structure over time.
        """

        base = phrase.clone()

        motifs = []
        start_times = []

        unit_duration = phrase.total_duration()

        for i in range(times):
            for m, t in zip(base.motifs, base.start_times):
                motifs.append(m.clone())
                start_times.append(t + i * (unit_duration + gap))

        return Phrase(
            motifs=motifs,
            start_times=start_times
        )

    # -----------------------------
    # MOTIF LEVEL MANIPULATION
    # -----------------------------

    def transpose_phrase(
        self,
        phrase: Phrase,
        semitones: int
    ) -> Phrase:
        """
        Transposes entire phrase.
        """

        p = phrase.clone()

        for m in p.motifs:
            for i in range(len(m.notes)):
                m.notes[i] += semitones

        return p

    def reverse_phrase(self, phrase: Phrase) -> Phrase:
        """
        Reverses phrase in time (not musical inversion).
        """

        p = phrase.clone()

        total = phrase.total_duration()

        new_motifs = []
        new_times = []

        for m, t in zip(p.motifs, p.start_times):
            reversed_m = m.clone()

            reversed_m.durations = list(reversed(reversed_m.durations))
            reversed_m.notes = list(reversed(reversed_m.notes))
            reversed_m.velocities = list(reversed(reversed_m.velocities))

            new_start = total - t - sum(m.durations)

            new_motifs.append(reversed_m)
            new_times.append(new_start)

        # sort by time
        paired = sorted(zip(new_motifs, new_times), key=lambda x: x[1])

        motifs, times = zip(*paired) if paired else ([], [])

        return Phrase(list(motifs), list(times))

    # -----------------------------
    # RHYTHMIC SHIFTING
    # -----------------------------

    def tighten(self, phrase: Phrase, factor: float = 0.9) -> Phrase:
        """
        Compresses time structure.
        """

        p = phrase.clone()

        p.start_times = [t * factor for t in p.start_times]

        for m in p.motifs:
            m.durations = [d * factor for d in m.durations]

        return p

    def stretch(self, phrase: Phrase, factor: float = 1.1) -> Phrase:
        """
        Expands time structure.
        """

        p = phrase.clone()

        p.start_times = [t * factor for t in p.start_times]

        for m in p.motifs:
            m.durations = [d * factor for d in m.durations]

        return p

    # -----------------------------
    # CALL / RESPONSE STRUCTURE
    # -----------------------------

    def call_response(
        self,
        call: "Motif",
        response: "Motif",
        gap: float = 0.5
    ) -> Phrase:
        """
        Classic musical structure: A → B
        """

        motifs = [call.clone(), response.clone()]
        start_times = [0.0, sum(call.durations) + gap]

        return Phrase(motifs, start_times)

    # -----------------------------
    # DENSITY CONTROL
    # -----------------------------

    def thin_motifs(
        self,
        phrase: Phrase,
        probability: float = 0.5
    ) -> Phrase:
        """
        Removes motifs probabilistically.
        """

        p = phrase.clone()

        motifs = []
        times = []

        for m, t in zip(p.motifs, p.start_times):
            if random.random() < probability:
                motifs.append(m.clone())
                times.append(t)

        return Phrase(motifs, times)

    # -----------------------------
    # UTILITY
    # -----------------------------

    def clear_history(self):
        self.history.clear()