from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Dict
import copy
import random


# --------------------------------------------------
# PHRASE MODEL
# --------------------------------------------------

@dataclass(slots=True)
class Phrase:
    """
    Musical phrase = timed collection of motifs.
    """

    motifs: List["Motif"]
    start_times: List[float] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)

    def clone(self) -> "Phrase":
        return copy.deepcopy(self)

    def total_duration(self) -> float:
        if not self.motifs:
            return 0.0

        max_end = 0.0

        for motif, start in zip(self.motifs, self.start_times):
            end = start + sum(motif.durations)
            max_end = max(max_end, end)

        return max_end


# --------------------------------------------------
# PHRASE BUILDER ENGINE
# --------------------------------------------------

class PhraseBuilder:

    def __init__(self):
        self.history: List[Phrase] = []
        self.seed: Optional[int] = None

    # -----------------------------
    # SEED
    # -----------------------------

    def set_seed(self, seed: int):
        self.seed = seed
        random.seed(seed)

    # -----------------------------
    # CORE BUILD
    # -----------------------------

    def build_linear(
        self,
        motifs: List["Motif"],
        spacing: float = 0.0
    ) -> Phrase:
        """
        Sequential motif placement in time.
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
    # STRUCTURE
    # -----------------------------

    def repeat_phrase(
        self,
        phrase: Phrase,
        times: int,
        gap: float = 0.0
    ) -> Phrase:
        """
        Repeats full phrase structure.
        """

        base = phrase.clone()

        motifs = []
        start_times = []

        unit = phrase.total_duration()

        for i in range(times):
            for m, t in zip(base.motifs, base.start_times):
                motifs.append(m.clone())
                start_times.append(t + i * (unit + gap))

        return Phrase(motifs, start_times)

    # -----------------------------
    # TRANSFORM
    # -----------------------------

    def transpose_phrase(
        self,
        phrase: Phrase,
        semitones: int
    ) -> Phrase:
        """
        Transpose all motifs in phrase.
        """

        p = phrase.clone()

        for m in p.motifs:
            for i in range(len(m.notes)):
                m.notes[i] += semitones

        return p

    def reverse_phrase(self, phrase: Phrase) -> Phrase:
        """
        Time reversal of phrase.
        """

        p = phrase.clone()

        total = phrase.total_duration()

        new_motifs = []
        new_times = []

        for m, t in zip(p.motifs, p.start_times):

            reversed_m = m.clone()

            reversed_m.notes.reverse()
            reversed_m.durations.reverse()
            reversed_m.velocities.reverse()

            new_start = total - t - sum(m.durations)

            new_motifs.append(reversed_m)
            new_times.append(new_start)

        sorted_pairs = sorted(zip(new_motifs, new_times), key=lambda x: x[1])

        if not sorted_pairs:
            return Phrase([], [])

        motifs, times = zip(*sorted_pairs)

        return Phrase(list(motifs), list(times))

    # -----------------------------
    # RHYTHMIC CONTROL
    # -----------------------------

    def tighten(self, phrase: Phrase, factor: float = 0.9) -> Phrase:
        """
        Compress time.
        """

        p = phrase.clone()

        p.start_times = [t * factor for t in p.start_times]

        for m in p.motifs:
            m.durations = [d * factor for d in m.durations]

        return p

    def stretch(self, phrase: Phrase, factor: float = 1.1) -> Phrase:
        """
        Expand time.
        """

        p = phrase.clone()

        p.start_times = [t * factor for t in p.start_times]

        for m in p.motifs:
            m.durations = [d * factor for d in m.durations]

        return p

    # -----------------------------
    # CALL / RESPONSE
    # -----------------------------

    def call_response(
        self,
        call: "Motif",
        response: "Motif",
        gap: float = 0.5
    ) -> Phrase:
        """
        A → B musical structure.
        """

        return Phrase(
            motifs=[call.clone(), response.clone()],
            start_times=[0.0, sum(call.durations) + gap]
        )

    # -----------------------------
    # DENSITY
    # -----------------------------

    def thin_motifs(
        self,
        phrase: Phrase,
        probability: float = 0.5
    ) -> Phrase:
        """
        Probabilistic motif removal.
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
    # HISTORY
    # -----------------------------

    def clear_history(self):
        self.history.clear()