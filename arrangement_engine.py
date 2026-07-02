from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
import copy
import random


# --------------------------------------------------
# TRACK MODEL
# --------------------------------------------------

@dataclass(slots=True)
class Track:
    """
    A track contains phrases assigned to a single instrument layer.
    """

    name: str
    phrases: List["Phrase"] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)

    def clone(self) -> "Track":
        return copy.deepcopy(self)

    def total_duration(self) -> float:
        if not self.phrases:
            return 0.0
        return max(
            (p.total_duration() for p in self.phrases),
            default=0.0
        )


# --------------------------------------------------
# ARRANGEMENT MODEL
# --------------------------------------------------

@dataclass(slots=True)
class Arrangement:
    """
    Full song structure composed of multiple tracks.
    """

    tracks: List[Track] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)

    def clone(self) -> "Arrangement":
        return copy.deepcopy(self)

    def total_duration(self) -> float:
        return max(
            (t.total_duration() for t in self.tracks),
            default=0.0
        )


# --------------------------------------------------
# ARRANGEMENT ENGINE
# --------------------------------------------------

class ArrangementEngine:

    def __init__(self):
        self.history: List[Arrangement] = []
        self.seed: Optional[int] = None

    # -----------------------------
    # SEED CONTROL
    # -----------------------------

    def set_seed(self, seed: int):
        self.seed = seed
        random.seed(seed)

    # -----------------------------
    # CORE BUILD
    # -----------------------------

    def build_single_track(
        self,
        name: str,
        phrase: "Phrase"
    ) -> Arrangement:
        """
        Wraps a single phrase into a track arrangement.
        """

        track = Track(
            name=name,
            phrases=[phrase.clone()]
        )

        arrangement = Arrangement(tracks=[track])

        self.history.append(arrangement.clone())
        return arrangement

    # -----------------------------
    # MULTI TRACK LAYERING
    # -----------------------------

    def layer_tracks(
        self,
        tracks: List[Track]
    ) -> Arrangement:
        """
        Combines multiple tracks into full arrangement.
        """

        arrangement = Arrangement(
            tracks=[t.clone() for t in tracks]
        )

        self.history.append(arrangement.clone())
        return arrangement

    # -----------------------------
    # SONG STRUCTURE BUILDER
    # -----------------------------

    def build_structure(
        self,
        base_phrase: "Phrase",
        structure: List[Tuple[str, int]]
    ) -> Arrangement:
        """
        Builds song form like:
        [
            ("intro", 1),
            ("drop", 2),
            ("break", 1)
        ]
        """

        tracks: List[Track] = []

        for section_name, repeats in structure:

            phrases = []

            for _ in range(repeats):
                phrases.append(base_phrase.clone())

            track = Track(
                name=section_name,
                phrases=phrases
            )

            tracks.append(track)

        arrangement = Arrangement(tracks=tracks)

        self.history.append(arrangement.clone())
        return arrangement

    # -----------------------------
    # TRANSFORMATIONS
    # -----------------------------

    def transpose_arrangement(
        self,
        arrangement: Arrangement,
        semitones: int
    ) -> Arrangement:
        """
        Transposes all notes in entire arrangement.
        """

        arr = arrangement.clone()

        for track in arr.tracks:
            for phrase in track.phrases:
                for motif in phrase.motifs:
                    for i in range(len(motif.notes)):
                        motif.notes[i] += semitones

        return arr

    def reverse_arrangement(
        self,
        arrangement: Arrangement
    ) -> Arrangement:
        """
        Reverses temporal order of full arrangement.
        """

        arr = arrangement.clone()

        for track in arr.tracks:
            track.phrases.reverse()

            for phrase in track.phrases:
                phrase.motifs.reverse()
                phrase.start_times.reverse()

        return arr

    # -----------------------------
    # EXPORT PREP (FOR NEXT MODULE)
    # -----------------------------

    def flatten(self, arrangement: Arrangement) -> List[Dict]:
        """
        Converts full arrangement into flat event list.
        (For MIDI exporter later)
        """

        events = []

        for track in arrangement.tracks:
            for phrase in track.phrases:
                for motif, start in zip(phrase.motifs, phrase.start_times):
                    for note, dur, vel in zip(
                        motif.notes,
                        motif.durations,
                        motif.velocities
                    ):
                        events.append({
                            "track": track.name,
                            "pitch": note,
                            "duration": dur,
                            "velocity": vel,
                            "start": start,
                        })

        return events

    # -----------------------------
    # HISTORY
    # -----------------------------

    def clear_history(self):
        self.history.clear()