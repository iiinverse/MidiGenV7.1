from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import copy


# --------------------------------------------------
# CONSTANTS
# --------------------------------------------------

MAX_TRACKS = 15
MIDI_DRUM_CHANNEL = 9


DEFAULT_TRACK_ORDER = [
    "Drums",
    "Bass",
    "Rhythm Guitar L",
    "Rhythm Guitar R",
    "Lead Guitar",
    "Piano",
    "Keys",
    "Pad",
    "Strings",
    "Brass",
    "Choir",
    "Arpeggio",
    "Lead Synth",
    "FX",
    "Melody"
]


# --------------------------------------------------
# TRACK MODEL
# --------------------------------------------------

@dataclass(slots=True)
class Track:

    name: str
    role: str
    instrument: str
    midi_channel: int
    color: str = "#ffffff"

    enabled: bool = True
    muted: bool = False
    solo: bool = False

    volume: int = 100
    pan: int = 64

    events: List = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)

    def clone(self):
        return copy.deepcopy(self)


# --------------------------------------------------
# TRACK MANAGER CORE
# --------------------------------------------------

class TrackManager:

    def __init__(self):
        self.tracks: List[Track] = []
        self.history: List[List[Track]] = []

    # -----------------------------
    # PROJECT INIT
    # -----------------------------

    def create_default_project(self):
        self.tracks.clear()

        channel = 0

        for role in DEFAULT_TRACK_ORDER:
            if len(self.tracks) >= MAX_TRACKS:
                break

            if role == "Drums":
                channel = MIDI_DRUM_CHANNEL
            else:
                while channel == MIDI_DRUM_CHANNEL:
                    channel += 1

            track = Track(
                name=role,
                role=role,
                instrument=role,
                midi_channel=channel
            )

            self.tracks.append(track)

            if role != "Drums":
                channel += 1

        self._snapshot()
        return self.tracks

    # -----------------------------
    # BASIC ACCESS
    # -----------------------------

    def all(self) -> List[Track]:
        return self.tracks

    def get(self, name: str) -> Optional[Track]:
        return next((t for t in self.tracks if t.name == name), None)

    def count(self) -> int:
        return len(self.tracks)

    # -----------------------------
    # ADD / REMOVE
    # -----------------------------

    def add_track(self, track: Track):
        if len(self.tracks) >= MAX_TRACKS:
            raise ValueError("Max 15 tracks reached")

        self.tracks.append(track)
        self._snapshot()

    def remove_track(self, name: str):
        self.tracks = [t for t in self.tracks if t.name != name]
        self._snapshot()

    # -----------------------------
    # DRAG & DROP (MOVE)
    # -----------------------------

    def move_track(self, from_index: int, to_index: int):
        if from_index < 0 or from_index >= len(self.tracks):
            return

        track = self.tracks.pop(from_index)
        self.tracks.insert(to_index, track)

        self._snapshot()

    # -----------------------------
    # MIDI CHANNEL AUTO FIX
    # -----------------------------

    def reassign_channels(self):
        channel = 0

        for t in self.tracks:
            if t.role == "Drums":
                t.midi_channel = MIDI_DRUM_CHANNEL
                continue

            while channel == MIDI_DRUM_CHANNEL:
                channel += 1

            t.midi_channel = channel
            channel += 1

    # -----------------------------
    # EXPORT HELPERS
    # -----------------------------

    def export_tracks(self) -> List[Track]:
        solo_mode = any(t.solo for t in self.tracks)

        result = []

        for t in self.tracks:
            if not t.enabled:
                continue
            if t.muted:
                continue
            if solo_mode and not t.solo:
                continue

            result.append(t)

        return result

    # -----------------------------
    # SNAPSHOT / UNDO
    # -----------------------------

    def _snapshot(self):
        self.history.append(copy.deepcopy(self.tracks))

    def undo(self):
        if len(self.history) < 2:
            return

        self.history.pop()
        self.tracks = copy.deepcopy(self.history[-1])

    # -----------------------------
    # SUMMARY
    # -----------------------------

    def summary(self):
        return {
            "tracks": len(self.tracks),
            "enabled": len([t for t in self.tracks if t.enabled]),
            "muted": len([t for t in self.tracks if t.muted]),
            "solo": len([t for t in self.tracks if t.solo]),
        }