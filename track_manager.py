from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import copy

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

MAX_LAYERS = 15
DRUM_CHANNEL = 9  # MIDI channel 10 (0-based)

DEFAULT_COLORS = {
    "Drums": "#ff5555",
    "Bass": "#55aa55",
    "Guitar": "#ffaa00",
    "Lead": "#ff8800",
    "Pad": "#aa88ff",
    "Keys": "#66ccff",
    "Strings": "#cc88ff",
    "FX": "#999999",
    "Piano": "#ffffff",
}

# --------------------------------------------------
# LAYER MODEL
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

    # --- GENERATION CONTROL ---
    density: float = 0.5
    complexity: float = 0.5
    humanize: float = 0.1

    mood_override: Optional[str] = None

    # --- UI / DRAG & DROP READY ---
    drag_enabled: bool = True
    locked: bool = False

    # --- EVENTS ---
    events: List = field(default_factory=list)

    # --- META ---
    metadata: Dict = field(default_factory=dict)

    def clone(self):
        return copy.deepcopy(self)


# --------------------------------------------------
# TRACK MANAGER
# --------------------------------------------------

class TrackManager:

    def __init__(self):
        self.tracks: List[Track] = []
        self.history: List[List[Track]] = []

    # --------------------------------------------------
    # CORE
    # --------------------------------------------------

    def all(self) -> List[Track]:
        return self.tracks

    def count(self) -> int:
        return len(self.tracks)

    def can_add(self) -> bool:
        return len(self.tracks) < MAX_LAYERS

    # --------------------------------------------------
    # ADD / REMOVE LAYERS
    # --------------------------------------------------

    def add_layer(
        self,
        name: str,
        role: str,
        instrument: str,
        color: Optional[str] = None,
        midi_channel: Optional[int] = None
    ) -> Track:

        if not self.can_add():
            raise ValueError("Max 15 layers reached")

        if midi_channel is None:
            midi_channel = self._find_free_channel(role)

        if role == "Drums":
            midi_channel = DRUM_CHANNEL

        track = Track(
            name=name,
            role=role,
            instrument=instrument,
            midi_channel=midi_channel,
            color=color or DEFAULT_COLORS.get(role, "#ffffff")
        )

        self.tracks.append(track)
        self._snapshot()

        return track

    def remove_layer(self, name: str):
        self.tracks = [t for t in self.tracks if t.name != name]
        self._snapshot()

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------

    def get(self, name: str) -> Optional[Track]:
        for t in self.tracks:
            if t.name == name:
                return t
        return None

    def by_role(self, role: str) -> List[Track]:
        return [t for t in self.tracks if t.role == role]

    # --------------------------------------------------
    # ENABLE / MUTE / SOLO
    # --------------------------------------------------

    def mute(self, name: str):
        t = self.get(name)
        if t:
            t.muted = True

    def unmute(self, name: str):
        t = self.get(name)
        if t:
            t.muted = False

    def solo(self, name: str):
        for t in self.tracks:
            t.solo = False

        t = self.get(name)
        if t:
            t.solo = True

    def clear_solo(self):
        for t in self.tracks:
            t.solo = False

    # --------------------------------------------------
    # MIDI CHANNELS
    # --------------------------------------------------

    def _find_free_channel(self, role: str) -> int:
        used = {t.midi_channel for t in self.tracks}

        for ch in range(16):
            if ch == DRUM_CHANNEL:
                continue
            if ch not in used:
                return ch

        raise ValueError("No free MIDI channels")

    def used_channels(self) -> List[int]:
        return sorted({t.midi_channel for t in self.tracks})

    # --------------------------------------------------
    # GENERATION CONTROL
    # --------------------------------------------------

    def set_density(self, name: str, value: float):
        t = self.get(name)
        if t:
            t.density = max(0.0, min(1.0, value))

    def set_complexity(self, name: str, value: float):
        t = self.get(name)
        if t:
            t.complexity = max(0.0, min(1.0, value))

    # --------------------------------------------------
    # EXPORT (IMPORTANT)
    # --------------------------------------------------

    def export_layers(self) -> List[Dict]:

        solo_mode = any(t.solo for t in self.tracks)

        out = []

        for t in self.tracks:

            if not t.enabled:
                continue

            if t.muted:
                continue

            if solo_mode and not t.solo:
                continue

            out.append({
                "name": t.name,
                "role": t.role,
                "instrument": t.instrument,
                "channel": t.midi_channel,
                "density": t.density,
                "complexity": t.complexity,
                "humanize": t.humanize,
                "events": copy.deepcopy(t.events),
                "metadata": copy.deepcopy(t.metadata)
            })

        return out

    # --------------------------------------------------
    # SNAPSHOT / UNDO
    # --------------------------------------------------

    def _snapshot(self):
        self.history.append(copy.deepcopy(self.tracks))

    def undo(self):
        if len(self.history) < 2:
            return

        self.history.pop()
        self.tracks = copy.deepcopy(self.history[-1])

    # --------------------------------------------------
    # RESET
    # --------------------------------------------------

    def reset(self):
        self.tracks.clear()
        self.history.clear()
        
    def reorder_tracks(self, new_order: List[str]):
            
    def set_limit(self, max_tracks=15):