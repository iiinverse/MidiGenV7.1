from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import copy


# --------------------------------------------------
# CONSTANTS
# --------------------------------------------------

MAX_TRACKS = 15


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


DEFAULT_COLORS = {

    "Drums": "#ff5555",

    "Bass": "#55aa55",

    "Rhythm Guitar L": "#ffaa00",

    "Rhythm Guitar R": "#ffaa55",

    "Lead Guitar": "#ff8800",

    "Piano": "#66ccff",

    "Keys": "#44aaff",

    "Pad": "#aa88ff",

    "Strings": "#aa55ff",

    "Brass": "#ffcc44",

    "Choir": "#ddddff",

    "Arpeggio": "#55ffff",

    "Lead Synth": "#ff44ff",

    "FX": "#999999",

    "Melody": "#ffffff"

}


# --------------------------------------------------
# TRACK
# --------------------------------------------------

@dataclass(slots=True)
class Track:

    name: str

    role: str

    instrument: str

    midi_channel: int

    color: str

    muted: bool = False

    solo: bool = False

    enabled: bool = True

    volume: int = 100

    pan: int = 64

    events: List = field(
        default_factory=list
    )

    metadata: Dict = field(
        default_factory=dict
    )

    # --------------------------------------------------
    # GENERATION SETTINGS
    # --------------------------------------------------

    complexity: float = 0.50

    density: float = 0.50

    humanize_timing: float = 0.10

    humanize_velocity: float = 0.08

    humanize_pitch: float = 0.00

    locked: bool = False

    frozen: bool = False

    generation_priority: int = 0

    mood_override: Optional[str] = None

    tags: List[str] = field(
        default_factory=list
    )

    group: str = "Default"

    drag_enabled: bool = True

    export_path: Optional[str] = None

    temporary_mid: Optional[str] = None
    
    def clone(self):

        return copy.deepcopy(
            self
        )


# --------------------------------------------------
# TRACK MANAGER
# --------------------------------------------------

class TrackManager:

    def __init__(self):

        self.tracks: List[Track] = []

        self.history = []

    # --------------------------------------------------
    # CREATE DEFAULT PROJECT
    # --------------------------------------------------

    def create_default_project(
        self
    ):

        self.tracks.clear()

        channel = 0

        for role in DEFAULT_TRACK_ORDER:

            if len(self.tracks) >= MAX_TRACKS:
                break

            if channel == 9:
                channel += 1

            instrument = role

            track = Track(

                name=role,

                role=role,

                instrument=instrument,

                midi_channel=channel,

                color=DEFAULT_COLORS.get(
                    role,
                    "#ffffff"
                )

            )

            self.tracks.append(
                track
            )

            channel += 1

        self.history.append(
            copy.deepcopy(
                self.tracks
            )
        )

        return self.tracks

    # --------------------------------------------------
    # BASIC ACCESS
    # --------------------------------------------------

    def all_tracks(self):

        return self.tracks

    def enabled_tracks(self):

        return [

            t

            for t

            in self.tracks

            if t.enabled

        ]

    def muted_tracks(self):

        return [

            t

            for t

            in self.tracks

            if t.muted

        ]

    def solo_tracks(self):

        return [

            t

            for t

            in self.tracks

            if t.solo

        ]

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------

    def get_track(
        self,
        name: str
    ) -> Optional[Track]:

        for track in self.tracks:

            if track.name == name:

                return track

        return None

    def get_by_role(
        self,
        role: str
    ) -> Optional[Track]:

        for track in self.tracks:

            if track.role == role:

                return track

        return None

    # --------------------------------------------------
    # ADD TRACK
    # --------------------------------------------------

    def add_track(

        self,

        name: str,

        role: str,

        instrument: str,

        midi_channel: int,

        color: str = "#ffffff"

    ):

        if len(self.tracks) >= MAX_TRACKS:

            raise ValueError(

                f"Maximum number of tracks is {MAX_TRACKS}"

            )

        self.tracks.append(

            Track(

                name=name,

                role=role,

                instrument=instrument,

                midi_channel=midi_channel,

                color=color

            )

        )
            # --------------------------------------------------
    # REMOVE TRACK
    # --------------------------------------------------

    def remove_track(
        self,
        name: str
    ):

        self.tracks = [

            track

            for track

            in self.tracks

            if track.name != name

        ]

    # --------------------------------------------------
    # RENAME
    # --------------------------------------------------

    def rename_track(
        self,
        old_name: str,
        new_name: str
    ):

        track = self.get_track(
            old_name
        )

        if track is None:

            raise ValueError(
                f"Track '{old_name}' not found."
            )

        track.name = new_name

    # --------------------------------------------------
    # ROLE
    # --------------------------------------------------

    def set_role(
        self,
        name: str,
        role: str
    ):

        track = self.get_track(
            name
        )

        if track is None:

            raise ValueError(
                f"Track '{name}' not found."
            )

        track.role = role

    # --------------------------------------------------
    # INSTRUMENT
    # --------------------------------------------------

    def set_instrument(
        self,
        name: str,
        instrument: str
    ):

        track = self.get_track(
            name
        )

        if track is None:

            raise ValueError(
                f"Track '{name}' not found."
            )

        track.instrument = instrument

    # --------------------------------------------------
    # COLOR
    # --------------------------------------------------

    def set_color(
        self,
        name: str,
        color: str
    ):

        track = self.get_track(
            name
        )

        if track:

            track.color = color

    # --------------------------------------------------
    # VOLUME
    # --------------------------------------------------

    def set_volume(
        self,
        name: str,
        volume: int
    ):

        volume = max(
            0,
            min(
                127,
                volume
            )
        )

        track = self.get_track(
            name
        )

        if track:

            track.volume = volume

    # --------------------------------------------------
    # PAN
    # --------------------------------------------------

    def set_pan(
        self,
        name: str,
        pan: int
    ):

        pan = max(
            0,
            min(
                127,
                pan
            )
        )

        track = self.get_track(
            name
        )

        if track:

            track.pan = pan

    # --------------------------------------------------
    # ENABLE
    # --------------------------------------------------

    def enable_track(
        self,
        name: str
    ):

        track = self.get_track(
            name
        )

        if track:

            track.enabled = True

    def disable_track(
        self,
        name: str
    ):

        track = self.get_track(
            name
        )

        if track:

            track.enabled = False

    # --------------------------------------------------
    # MUTE
    # --------------------------------------------------

    def mute(
        self,
        name: str
    ):

        track = self.get_track(
            name
        )

        if track:

            track.muted = True

    def unmute(
        self,
        name: str
    ):

        track = self.get_track(
            name
        )

        if track:

            track.muted = False

    # --------------------------------------------------
    # SOLO
    # --------------------------------------------------

    def solo(
        self,
        name: str
    ):

        for track in self.tracks:

            track.solo = False

        track = self.get_track(
            name
        )

        if track:

            track.solo = True

    def clear_solo(
        self
    ):

        for track in self.tracks:

            track.solo = False

    # --------------------------------------------------
    # EVENTS
    # --------------------------------------------------

    def add_event(
        self,
        track_name: str,
        event
    ):

        track = self.get_track(
            track_name
        )

        if track:

            track.events.append(
                event
            )

    def clear_events(
        self,
        track_name: str
    ):

        track = self.get_track(
            track_name
        )

        if track:

            track.events.clear()

    def clear_all_events(
        self
    ):

        for track in self.tracks:

            track.events.clear()
                # --------------------------------------------------
    # MIDI CHANNEL MANAGEMENT
    # --------------------------------------------------

    def used_channels(self):

        return sorted({

            track.midi_channel

            for track

            in self.tracks

        })

    def available_channels(self):

        channels = []

        for channel in range(16):

            # Channel 10 (index 9) reserved for drums
            if channel == 9:
                continue

            if channel not in self.used_channels():

                channels.append(channel)

        return channels

    def assign_channel(
        self,
        track_name: str,
        channel: int
    ):

        if channel < 0 or channel > 15:

            raise ValueError(
                "Invalid MIDI channel."
            )

        track = self.get_track(
            track_name
        )

        if track is None:

            raise ValueError(
                f"Track '{track_name}' not found."
            )

        # Allow drums only on channel 10
        if track.role == "Drums":

            if channel != 9:

                raise ValueError(
                    "Drums must use MIDI channel 10."
                )

        else:

            if channel == 9:

                raise ValueError(
                    "Channel 10 is reserved for drums."
                )

        track.midi_channel = channel

    def auto_assign_channels(self):

        channel = 0

        for track in self.tracks:

            if track.role == "Drums":

                track.midi_channel = 9

                continue

            while channel == 9:

                channel += 1

            track.midi_channel = channel

            channel += 1

            if channel > 15:

                break

    # --------------------------------------------------
    # TRACK ORDER
    # --------------------------------------------------

    def move_track(
        self,
        old_index: int,
        new_index: int
    ):

        track = self.tracks.pop(
            old_index
        )

        self.tracks.insert(
            new_index,
            track
        )

    def sort_default(self):

        order = {

            name: index

            for index, name

            in enumerate(
                DEFAULT_TRACK_ORDER
            )

        }

        self.tracks.sort(

            key=lambda track:

            order.get(
                track.role,
                999
            )

        )

    # --------------------------------------------------
    # PROJECT INFO
    # --------------------------------------------------

    def track_count(self):

        return len(
            self.tracks
        )

    def enabled_count(self):

        return len(

            self.enabled_tracks()

        )

    def has_solo(self):

        return any(

            track.solo

            for track

            in self.tracks

        )

    # --------------------------------------------------
    # VALIDATION
    # --------------------------------------------------

    def validate(self):

        errors = []

        if len(self.tracks) > MAX_TRACKS:

            errors.append(

                "Too many tracks."

            )

        names = set()

        for track in self.tracks:

            if track.name in names:

                errors.append(

                    f"Duplicate track name: {track.name}"

                )

            names.add(

                track.name

            )

        return errors

    # --------------------------------------------------
    # SERIALIZATION
    # --------------------------------------------------

    def to_dict(self):

    result = []

    for track in self.tracks:

        result.append({

            "name": track.name,

            "role": track.role,

            "instrument": track.instrument,

            "midi_channel": track.midi_channel,

            "color": track.color,

            "muted": track.muted,

            "solo": track.solo,

            "enabled": track.enabled,

            "volume": track.volume,

            "pan": track.pan,

            "complexity": track.complexity,

            "density": track.density,

            "humanize_timing": track.humanize_timing,

            "humanize_velocity": track.humanize_velocity,

            "humanize_pitch": track.humanize_pitch,

            "locked": track.locked,

            "frozen": track.frozen,

            "generation_priority": track.generation_priority,

            "mood_override": track.mood_override,

            "tags": copy.deepcopy(

                track.tags

            ),

            "group": track.group,

            "drag_enabled": track.drag_enabled,

            "export_path": track.export_path,

            "temporary_mid": track.temporary_mid,

            "metadata": copy.deepcopy(

                track.metadata

            )

        })

    return result
    
    def from_dict(
    self,
    data
):

    self.tracks.clear()

    for item in data:

        self.tracks.append(

            Track(

                name=item["name"],

                role=item["role"],

                instrument=item["instrument"],

                midi_channel=item["midi_channel"],

                color=item["color"],

                muted=item.get(
                    "muted",
                    False
                ),

                solo=item.get(
                    "solo",
                    False
                ),

                enabled=item.get(
                    "enabled",
                    True
                ),

                volume=item.get(
                    "volume",
                    100
                ),

                pan=item.get(
                    "pan",
                    64
                ),

                complexity=item.get(
                    "complexity",
                    0.50
                ),

                density=item.get(
                    "density",
                    0.50
                ),

                humanize_timing=item.get(
                    "humanize_timing",
                    0.10
                ),

                humanize_velocity=item.get(
                    "humanize_velocity",
                    0.08
                ),

                humanize_pitch=item.get(
                    "humanize_pitch",
                    0.00
                ),

                locked=item.get(
                    "locked",
                    False
                ),

                frozen=item.get(
                    "frozen",
                    False
                ),

                generation_priority=item.get(
                    "generation_priority",
                    0
                ),

                mood_override=item.get(
                    "mood_override",
                    None
                ),

                tags=copy.deepcopy(

                    item.get(
                        "tags",
                        []
                    )

                ),

                group=item.get(
                    "group",
                    "Default"
                ),

                drag_enabled=item.get(
                    "drag_enabled",
                    True
                ),

                export_path=item.get(
                    "export_path",
                    None
                ),

                temporary_mid=item.get(
                    "temporary_mid",
                    None
                ),

                metadata=copy.deepcopy(

                    item.get(
                        "metadata",
                        {}
                    )

                )

            )

        )
        
    # --------------------------------------------------
    # GROUP OPERATIONS
    # --------------------------------------------------

    def enable_all(self):

        for track in self.tracks:

            track.enabled = True

    def disable_all(self):

        for track in self.tracks:

            track.enabled = False

    def mute_all(self):

        for track in self.tracks:

            track.muted = True

    def unmute_all(self):

        for track in self.tracks:

            track.muted = False

    def clear_all_solo(self):

        for track in self.tracks:

            track.solo = False

    # --------------------------------------------------
    # ROLE FILTERS
    # --------------------------------------------------

    def tracks_by_role(
        self,
        role: str
    ):

        return [

            track

            for track

            in self.tracks

            if track.role == role

        ]

    def tracks_by_instrument(
        self,
        instrument: str
    ):

        return [

            track

            for track

            in self.tracks

            if track.instrument == instrument

        ]

    # --------------------------------------------------
    # EXPORT PREPARATION
    # --------------------------------------------------

    def exportable_tracks(self):

        tracks = []

        solo_mode = self.has_solo()

        for track in self.tracks:

            if not track.enabled:

                continue

            if track.muted:

                continue

            if solo_mode and not track.solo:

                continue

            tracks.append(
                track
            )

        return tracks

    # --------------------------------------------------
    # MIDI EXPORT PAYLOAD
    # --------------------------------------------------

    def export_payload(self):

        payload = []

        for track in self.exportable_tracks():

            payload.append({

                "name": track.name,

                "role": track.role,

                "instrument": track.instrument,

                "channel": track.midi_channel,

                "volume": track.volume,

                "pan": track.pan,

                "events": copy.deepcopy(
                    track.events
                )

            })

        return payload
    # --------------------------------------------------
    # LOCK / FREEZE
    # --------------------------------------------------

    def lock_track(
        self,
        name: str
    ):

        track = self.get_track(
            name
        )

        if track:

            track.locked = True

    def unlock_track(
        self,
        name: str
    ):

        track = self.get_track(
            name
        )

        if track:

            track.locked = False

    def freeze_track(
        self,
        name: str
    ):

        track = self.get_track(
            name
        )

        if track:

            track.frozen = True

    def unfreeze_track(
        self,
        name: str
    ):

        track = self.get_track(
            name
        )

        if track:

            track.frozen = False

    def locked_tracks(self):

        return [

            track

            for track

            in self.tracks

            if track.locked

        ]

    def frozen_tracks(self):

        return [

            track

            for track

            in self.tracks

            if track.frozen

        ]

    # --------------------------------------------------
    # COMPLEXITY
    # --------------------------------------------------

    def set_complexity(
        self,
        name: str,
        value: float
    ):

        value = max(

            0.0,

            min(

                1.0,

                value

            )

        )

        track = self.get_track(
            name
        )

        if track:

            track.complexity = value

    def set_density(
        self,
        name: str,
        value: float
    ):

        value = max(

            0.0,

            min(

                1.0,

                value

            )

        )

        track = self.get_track(
            name
        )

        if track:

            track.density = value

    # --------------------------------------------------
    # HUMANIZE
    # --------------------------------------------------

    def set_humanize(

        self,

        name: str,

        timing: Optional[float] = None,

        velocity: Optional[float] = None,

        pitch: Optional[float] = None

    ):

        track = self.get_track(
            name
        )

        if track is None:

            return

        if timing is not None:

            track.humanize_timing = max(

                0.0,

                min(

                    1.0,

                    timing

                )

            )

        if velocity is not None:

            track.humanize_velocity = max(

                0.0,

                min(

                    1.0,

                    velocity

                )

            )

        if pitch is not None:

            track.humanize_pitch = max(

                0.0,

                min(

                    1.0,

                    pitch

                )

            )

    # --------------------------------------------------
    # MOOD
    # --------------------------------------------------

    def set_mood_override(

        self,

        name: str,

        mood: Optional[str]

    ):

        track = self.get_track(
            name
        )

        if track:

            track.mood_override = mood

    def clear_mood_override(
        self,
        name: str
    ):

        track = self.get_track(
            name
        )

        if track:

            track.mood_override = None

    # --------------------------------------------------
    # GENERATION PRIORITY
    # --------------------------------------------------

    def set_priority(

        self,

        name: str,

        priority: int

    ):

        track = self.get_track(
            name
        )

        if track:

            track.generation_priority = priority

    def generation_order(self):

        return sorted(

            self.tracks,

            key=lambda t:

            t.generation_priority

        )
        
            # --------------------------------------------------
    # GROUP MANAGEMENT
    # --------------------------------------------------

    def set_group(
        self,
        track_name: str,
        group: str
    ):

        track = self.get_track(
            track_name
        )

        if track:

            track.group = group

    def group_tracks(
        self,
        group: str
    ):

        return [

            track

            for track

            in self.tracks

            if track.group == group

        ]

    def groups(self):

        return sorted({

            track.group

            for track

            in self.tracks

        })

    def mute_group(
        self,
        group: str
    ):

        for track in self.group_tracks(group):

            track.muted = True

    def unmute_group(
        self,
        group: str
    ):

        for track in self.group_tracks(group):

            track.muted = False

    def enable_group(
        self,
        group: str
    ):

        for track in self.group_tracks(group):

            track.enabled = True

    def disable_group(
        self,
        group: str
    ):

        for track in self.group_tracks(group):

            track.enabled = False

    # --------------------------------------------------
    # TAGS
    # --------------------------------------------------

    def add_tag(
        self,
        track_name: str,
        tag: str
    ):

        track = self.get_track(track_name)

        if track is None:

            return

        if tag not in track.tags:

            track.tags.append(tag)

    def remove_tag(
        self,
        track_name: str,
        tag: str
    ):

        track = self.get_track(track_name)

        if track is None:

            return

        if tag in track.tags:

            track.tags.remove(tag)

    def clear_tags(
        self,
        track_name: str
    ):

        track = self.get_track(track_name)

        if track:

            track.tags.clear()

    def tracks_with_tag(
        self,
        tag: str
    ):

        return [

            track

            for track

            in self.tracks

            if tag in track.tags

        ]

    # --------------------------------------------------
    # DRAG & DROP
    # --------------------------------------------------

    def set_export_path(
        self,
        track_name: str,
        path: str
    ):

        track = self.get_track(track_name)

        if track:

            track.export_path = path

    def set_temporary_mid(
        self,
        track_name: str,
        path: str
    ):

        track = self.get_track(track_name)

        if track:

            track.temporary_mid = path

    def prepare_drag_drop(
        self,
        track_name: str
    ):

        track = self.get_track(track_name)

        if track is None:

            return None

        if not track.drag_enabled:

            return None

        return {

            "track": track.name,

            "role": track.role,

            "instrument": track.instrument,

            "temporary_mid": track.temporary_mid,

            "export_path": track.export_path

        }

    # --------------------------------------------------
    # GENERATION FILTERS
    # --------------------------------------------------

    def generation_tracks(self):

        tracks = []

        solo_mode = self.has_solo()

        for track in sorted(

            self.tracks,

            key=lambda t:

            t.generation_priority

        ):

            if not track.enabled:

                continue

            if track.locked:

                continue

            if track.frozen:

                continue

            if track.muted:

                continue

            if solo_mode and not track.solo:

                continue

            tracks.append(track)

        return tracks

    # --------------------------------------------------
    # QUICK PRESETS
    # --------------------------------------------------

    def apply_complexity_all(
        self,
        value: float
    ):

        value = max(
            0.0,
            min(
                1.0,
                value
            )
        )

        for track in self.tracks:

            track.complexity = value

    def apply_density_all(
        self,
        value: float
    ):

        value = max(
            0.0,
            min(
                1.0,
                value
            )
        )

        for track in self.tracks:

            track.density = value

    def apply_humanize_all(
        self,
        timing: float,
        velocity: float,
        pitch: float
    ):

        for track in self.tracks:

            track.humanize_timing = timing

            track.humanize_velocity = velocity

            track.humanize_pitch = pitch

    # --------------------------------------------------
    # STATISTICS
    # --------------------------------------------------

    def statistics(self):

        return {

            "tracks": len(self.tracks),

            "enabled": len(self.enabled_tracks()),

            "muted": len(self.muted_tracks()),

            "solo": len(self.solo_tracks()),

            "locked": len(self.locked_tracks()),

            "frozen": len(self.frozen_tracks()),

            "groups": len(self.groups())

        }
        
    # --------------------------------------------------
    # PROJECT RESET
    # --------------------------------------------------

    def reset_project(self):

        self.tracks.clear()

        self.history.clear()

    # --------------------------------------------------
    # SNAPSHOT
    # --------------------------------------------------

    def snapshot(self):

        self.history.append(

            copy.deepcopy(
                self.tracks
            )

        )

    def undo(self):

        if len(self.history) < 2:

            return

        self.history.pop()

        self.tracks = copy.deepcopy(

            self.history[-1]

        )

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    def summary(self):

        return {

            "track_count": self.track_count(),

            "enabled": self.enabled_count(),

            "muted": len(
                self.muted_tracks()
            ),

            "solo": len(
                self.solo_tracks()
            ),

            "channels": self.used_channels()

        }
        