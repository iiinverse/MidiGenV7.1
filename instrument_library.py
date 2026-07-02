from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from typing import Dict
from typing import List
from typing import Optional

import copy
import random


# --------------------------------------------------
# INSTRUMENT
# --------------------------------------------------

@dataclass(slots=True)
class Instrument:

    # -----------------------------
    # Identity
    # -----------------------------

    name: str

    family: str

    category: str

    gm_program: int

    # -----------------------------
    # MIDI
    # -----------------------------

    default_channel: Optional[int] = None

    default_volume: int = 100

    default_pan: int = 64

    octave_shift: int = 0

    min_pitch: int = 21

    max_pitch: int = 108

    preferred_octave_low: int = 2

    preferred_octave_high: int = 6

    # -----------------------------
    # Musical Behaviour
    # -----------------------------

    preferred_density: float = 0.50

    preferred_complexity: float = 0.50

    preferred_velocity: int = 90

    polyphonic: bool = True

    max_polyphony: int = 8

    # -----------------------------
    # Character
    # -----------------------------

    energy: float = 0.50

    aggression: float = 0.50

    brightness: float = 0.50

    warmth: float = 0.50

    attack: float = 0.50

    sustain: float = 0.50

    # -----------------------------
    # Usage
    # -----------------------------

    genres: List[str] = field(
        default_factory=list
    )

    roles: List[str] = field(
        default_factory=list
    )

    articulations: List[str] = field(
        default_factory=list
    )

    tags: List[str] = field(
        default_factory=list
    )

    compatible_with: List[str] = field(
        default_factory=list
    )

    incompatible_with: List[str] = field(
        default_factory=list
    )

    metadata: Dict = field(
        default_factory=dict
    )

    # --------------------------------------------------

    def clone(self):

        return copy.deepcopy(
            self
        )


# --------------------------------------------------
# LIBRARY
# --------------------------------------------------

class InstrumentLibrary:

    def __init__(self):

        self.instruments: Dict[
            str,
            Instrument
        ] = {}

        self.genre_presets = {}

        self.role_presets = {}

        self.compatibility_map = {}

        self._build_library()

    # --------------------------------------------------
    # REGISTRATION
    # --------------------------------------------------

    def register(
        self,
        instrument: Instrument
    ):

        self.instruments[
            instrument.name
        ] = instrument

    def exists(
        self,
        name: str
    ):

        return name in self.instruments

    def get(
        self,
        name: str
    ) -> Instrument:

        if name not in self.instruments:

            raise KeyError(
                f"Unknown instrument: {name}"
            )

        return self.instruments[
            name
        ].clone()

    def remove(
        self,
        name: str
    ):

        if name in self.instruments:

            del self.instruments[
                name
            ]

    def names(self):

        return sorted(

            self.instruments.keys()

        )

    def count(self):

        return len(
            self.instruments
        )
        
            # --------------------------------------------------
    # BASIC FILTERS
    # --------------------------------------------------

    def all(self):

        return [

            instrument.clone()

            for instrument

            in self.instruments.values()

        ]

    def families(self):

        return sorted({

            instrument.family

            for instrument

            in self.instruments.values()

        })

    def categories(self):

        return sorted({

            instrument.category

            for instrument

            in self.instruments.values()

        })

    def by_family(
        self,
        family: str
    ):

        return [

            instrument.clone()

            for instrument

            in self.instruments.values()

            if instrument.family == family

        ]

    def by_category(
        self,
        category: str
    ):

        return [

            instrument.clone()

            for instrument

            in self.instruments.values()

            if instrument.category == category

        ]

    def by_genre(
        self,
        genre: str
    ):

        return [

            instrument.clone()

            for instrument

            in self.instruments.values()

            if genre in instrument.genres

        ]

    def by_role(
        self,
        role: str
    ):

        return [

            instrument.clone()

            for instrument

            in self.instruments.values()

            if role in instrument.roles

        ]

    def by_tag(
        self,
        tag: str
    ):

        return [

            instrument.clone()

            for instrument

            in self.instruments.values()

            if tag in instrument.tags

        ]

    # --------------------------------------------------
    # CHARACTER FILTERS
    # --------------------------------------------------

    def energetic(
        self,
        minimum: float = 0.70
    ):

        return [

            instrument.clone()

            for instrument

            in self.instruments.values()

            if instrument.energy >= minimum

        ]

    def soft(
        self,
        maximum: float = 0.35
    ):

        return [

            instrument.clone()

            for instrument

            in self.instruments.values()

            if instrument.aggression <= maximum

        ]

    def bright(
        self,
        minimum: float = 0.70
    ):

        return [

            instrument.clone()

            for instrument

            in self.instruments.values()

            if instrument.brightness >= minimum

        ]

    def warm(
        self,
        minimum: float = 0.70
    ):

        return [

            instrument.clone()

            for instrument

            in self.instruments.values()

            if instrument.warmth >= minimum

        ]

    # --------------------------------------------------
    # PERFORMANCE FILTERS
    # --------------------------------------------------

    def polyphonic(self):

        return [

            instrument.clone()

            for instrument

            in self.instruments.values()

            if instrument.polyphonic

        ]

    def monophonic(self):

        return [

            instrument.clone()

            for instrument

            in self.instruments.values()

            if not instrument.polyphonic

        ]

    def playable_in_range(
        self,
        low: int,
        high: int
    ):

        return [

            instrument.clone()

            for instrument

            in self.instruments.values()

            if instrument.min_pitch <= low
            and
            instrument.max_pitch >= high

        ]

    # --------------------------------------------------
    # RANDOM
    # --------------------------------------------------

    def random_instrument(self):

        if not self.instruments:

            return None

        return random.choice(

            list(

                self.instruments.values()

            )

        ).clone()

    def random_family(
        self,
        family: str
    ):

        items = self.by_family(
            family
        )

        if not items:

            return None

        return random.choice(
            items
        )

    def random_category(
        self,
        category: str
    ):

        items = self.by_category(
            category
        )

        if not items:

            return None

        return random.choice(
            items
        )

    def random_role(
        self,
        role: str
    ):

        items = self.by_role(
            role
        )

        if not items:

            return None

        return random.choice(
            items
        )
        
            # --------------------------------------------------
    # SMART INSTRUMENT SELECTION
    # --------------------------------------------------

    def recommend(
        self,
        role: str,
        genre: Optional[str] = None,
        mood: Optional[str] = None,
        energy: Optional[float] = None,
        exclude: Optional[List[str]] = None
    ) -> List[Instrument]:

        exclude = exclude or []

        candidates = []

        for instrument in self.instruments.values():

            if instrument.name in exclude:
                continue

            if role not in instrument.roles:
                continue

            score = 0.0

            # Genre compatibility
            if genre:

                if genre in instrument.genres:
                    score += 5.0

            # Mood compatibility
            if mood:

                moods = instrument.metadata.get(
                    "moods",
                    []
                )

                if mood in moods:
                    score += 4.0

            # Energy similarity
            if energy is not None:

                score += max(
                    0.0,
                    2.0 - abs(
                        instrument.energy - energy
                    ) * 2.0
                )

            # Preferred instrument bonus
            if instrument.metadata.get(
                "preferred",
                False
            ):
                score += 1.5

            candidates.append(
                (
                    score,
                    instrument.clone()
                )
            )

        candidates.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return [

            item

            for _score, item

            in candidates

        ]

    # --------------------------------------------------
    # BUILD COMPLETE BAND
    # --------------------------------------------------

    def build_band(
        self,
        genre: str,
        mood: str,
        energy: float
    ) -> Dict[str, Instrument]:

        roles = [

            "Drums",

            "Bass",

            "Rhythm Guitar L",

            "Rhythm Guitar R",

            "Lead Guitar",

            "Piano",

            "Keys",

            "Pad",

            "Strings",

            "Choir",

            "Brass",

            "Lead Synth",

            "Arpeggio",

            "FX",

            "Melody"

        ]

        band = {}

        used = []

        for role in roles:

            options = self.recommend(

                role=role,

                genre=genre,

                mood=mood,

                energy=energy,

                exclude=used

            )

            if not options:
                continue

            chosen = options[0]

            band[role] = chosen

            used.append(
                chosen.name
            )

        return band

    # --------------------------------------------------
    # COMPATIBILITY
    # --------------------------------------------------

    def compatibility_score(

        self,

        first: Instrument,

        second: Instrument

    ) -> float:

        score = 0.0

        shared = set(first.genres) & set(second.genres)

        score += len(shared) * 2.0

        score += max(

            0.0,

            1.0 - abs(

                first.energy -

                second.energy

            )

        )

        score += max(

            0.0,

            1.0 - abs(

                first.brightness -

                second.brightness

            )

        )

        score += max(

            0.0,

            1.0 - abs(

                first.warmth -

                second.warmth

            )

        )

        return score
        
            # --------------------------------------------------
    # COMPLETE GENRE PRESETS
    # --------------------------------------------------

    def available_genres(self) -> List[str]:

        genres = set()

        for instrument in self.instruments.values():

            genres.update(
                instrument.genres
            )

        return sorted(genres)

    # --------------------------------------------------
    # AUTO ASSIGN
    # --------------------------------------------------

    def assign_to_tracks(
        self,
        track_manager,
        genre: str,
        mood: str,
        energy: float
    ):

        band = self.build_band(
            genre=genre,
            mood=mood,
            energy=energy
        )

        for track in track_manager.all_tracks():

            if track.role not in band:
                continue

            instrument = band[
                track.role
            ]

            track.instrument = instrument.name

            if instrument.default_channel is not None:

                track.midi_channel = (
                    instrument.default_channel
                )

            track.metadata["gm_program"] = (
                instrument.gm_program
            )

            track.metadata["family"] = (
                instrument.family
            )

            track.metadata["genres"] = list(
                instrument.genres
            )

    # --------------------------------------------------
    # EXPORT
    # --------------------------------------------------

    def export_library(self):

        data = []

        for instrument in self.instruments.values():

            data.append({

                "name": instrument.name,

                "family": instrument.family,

                "category": instrument.category,

                "gm_program": instrument.gm_program,

                "default_channel": instrument.default_channel,

                "default_volume": instrument.default_volume,

                "default_pan": instrument.default_pan,

                "octave_shift": instrument.octave_shift,

                "min_pitch": instrument.min_pitch,

                "max_pitch": instrument.max_pitch,

                "energy": instrument.energy,

                "brightness": instrument.brightness,

                "warmth": instrument.warmth,

                "aggression": instrument.aggression,

                "polyphonic": instrument.polyphonic,

                "roles": list(
                    instrument.roles
                ),

                "genres": list(
                    instrument.genres
                ),

                "tags": list(
                    instrument.tags
                ),

                "metadata": copy.deepcopy(
                    instrument.metadata
                )

            })

        return data

    # --------------------------------------------------
    # IMPORT
    # --------------------------------------------------

    def import_library(
        self,
        data
    ):

        self.instruments.clear()

        for item in data:

            self.add(

                Instrument(

                    name=item["name"],

                    family=item["family"],

                    category=item["category"],

                    gm_program=item["gm_program"],

                    default_channel=item.get(
                        "default_channel"
                    ),

                    default_volume=item.get(
                        "default_volume",
                        100
                    ),

                    default_pan=item.get(
                        "default_pan",
                        64
                    ),

                    octave_shift=item.get(
                        "octave_shift",
                        0
                    ),

                    min_pitch=item.get(
                        "min_pitch",
                        0
                    ),

                    max_pitch=item.get(
                        "max_pitch",
                        127
                    ),

                    energy=item.get(
                        "energy",
                        0.5
                    ),

                    brightness=item.get(
                        "brightness",
                        0.5
                    ),

                    warmth=item.get(
                        "warmth",
                        0.5
                    ),

                    aggression=item.get(
                        "aggression",
                        0.5
                    ),

                    polyphonic=item.get(
                        "polyphonic",
                        True
                    ),

                    roles=list(
                        item.get(
                            "roles",
                            []
                        )
                    ),

                    genres=list(
                        item.get(
                            "genres",
                            []
                        )
                    ),

                    tags=list(
                        item.get(
                            "tags",
                            []
                        )
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
    # SUMMARY
    # --------------------------------------------------

    def summary(self):

        return {

            "instrument_count": len(
                self.instruments
            ),

            "families": len(
                self.families()
            ),

            "categories": len(
                self.categories()
            ),

            "genres": len(
                self.available_genres()
            )

        }