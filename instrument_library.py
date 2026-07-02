from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import copy

# --------------------------------------------------
# INSTRUMENT MODEL
# --------------------------------------------------

@dataclass(slots=True)
class Instrument:

    name: str

    category: str

    gm_program: int

    default_channel: Optional[int] = None

    default_volume: int = 100

    default_pan: int = 64

    octave_shift: int = 0

    metadata: Dict = field(
        default_factory=dict
    )

    def clone(self):

        return copy.deepcopy(
            self
        )

# --------------------------------------------------
# INSTRUMENT LIBRARY
# --------------------------------------------------

class InstrumentLibrary:

    def __init__(self):

        self.instruments: Dict[str, Instrument] = {}

        self._build_defaults()

    # --------------------------------------------------
    # DEFAULT LIBRARY
    # --------------------------------------------------

    def _build_defaults(self):

        # -------------------------
        # PIANO / KEYS
        # -------------------------

        self.add(

            Instrument(
                name="Grand Piano",
                category="Piano",
                gm_program=0
            )

        )

        self.add(

            Instrument(
                name="Bright Piano",
                category="Piano",
                gm_program=1
            )

        )

        self.add(

            Instrument(
                name="Electric Piano",
                category="Keys",
                gm_program=4
            )

        )

        self.add(

            Instrument(
                name="Rhodes",
                category="Keys",
                gm_program=4
            )

        )

        self.add(

            Instrument(
                name="Clavinet",
                category="Keys",
                gm_program=7
            )

        )

        self.add(

            Instrument(
                name="Rock Organ",
                category="Organ",
                gm_program=16
            )

        )

        self.add(

            Instrument(
                name="Jazz Organ",
                category="Organ",
                gm_program=17
            )

        )

        # -------------------------
        # SYNTH LEADS
        # -------------------------

        self.add(

            Instrument(
                name="Lead Saw",
                category="Synth Lead",
                gm_program=81
            )

        )

        self.add(

            Instrument(
                name="Lead Square",
                category="Synth Lead",
                gm_program=80
            )

        )

        self.add(

            Instrument(
                name="Lead Mono",
                category="Synth Lead",
                gm_program=82
            )

        )

        self.add(

            Instrument(
                name="Pluck Synth",
                category="Synth Lead",
                gm_program=87
            )

        )

        # -------------------------
        # PADS
        # -------------------------

        self.add(

            Instrument(
                name="Warm Pad",
                category="Pad",
                gm_program=89
            )

        )

        self.add(

            Instrument(
                name="Choir Pad",
                category="Pad",
                gm_program=91
            )

        )

        self.add(

            Instrument(
                name="Ambient Pad",
                category="Pad",
                gm_program=94
            )

        )

        # -------------------------
        # STRINGS
        # -------------------------

        self.add(

            Instrument(
                name="Strings Ensemble",
                category="Strings",
                gm_program=48
            )

        )

        self.add(

            Instrument(
                name="Violin Section",
                category="Strings",
                gm_program=49
            )

        )

        self.add(

            Instrument(
                name="Cello Section",
                category="Strings",
                gm_program=42,
                octave_shift=-1
            )

        )

        # -------------------------
        # CHOIR
        # -------------------------

        self.add(

            Instrument(
                name="Choir Aahs",
                category="Choir",
                gm_program=52
            )

        )

        self.add(

            Instrument(
                name="Choir Oohs",
                category="Choir",
                gm_program=53
            )

        )

        # -------------------------
        # BRASS
        # -------------------------

        self.add(

            Instrument(
                name="French Horn",
                category="Brass",
                gm_program=60
            )

        )

        self.add(

            Instrument(
                name="Trumpet Section",
                category="Brass",
                gm_program=56
            )

        )

        self.add(

            Instrument(
                name="Trombone Section",
                category="Brass",
                gm_program=57
            )

        )
        # -------------------------
        # GUITARS
        # -------------------------

        self.add(

            Instrument(
                name="Clean Electric Guitar",
                category="Guitar",
                gm_program=27
            )

        )

        self.add(

            Instrument(
                name="Jazz Guitar",
                category="Guitar",
                gm_program=26
            )

        )

        self.add(

            Instrument(
                name="Crunch Guitar",
                category="Rock Guitar",
                gm_program=29
            )

        )

        self.add(

            Instrument(
                name="Rhythm Guitar",
                category="Rock Guitar",
                gm_program=30
            )

        )

        self.add(

            Instrument(
                name="Heavy Rhythm Guitar",
                category="Metal Guitar",
                gm_program=30
            )

        )

        self.add(

            Instrument(
                name="High Gain Lead",
                category="Metal Guitar",
                gm_program=30
            )

        )

        self.add(

            Instrument(
                name="Shred Lead",
                category="Metal Guitar",
                gm_program=30
            )

        )

        self.add(

            Instrument(
                name="7-String Guitar",
                category="Metal Guitar",
                gm_program=30,
                octave_shift=-1
            )

        )

        self.add(

            Instrument(
                name="8-String Guitar",
                category="Metal Guitar",
                gm_program=30,
                octave_shift=-1
            )

        )

        self.add(

            Instrument(
                name="Baritone Guitar",
                category="Metal Guitar",
                gm_program=30,
                octave_shift=-1
            )

        )

        self.add(

            Instrument(
                name="Acoustic Steel",
                category="Acoustic Guitar",
                gm_program=25
            )

        )

        self.add(

            Instrument(
                name="Acoustic Nylon",
                category="Acoustic Guitar",
                gm_program=24
            )

        )

        self.add(

            Instrument(
                name="12-String Guitar",
                category="Acoustic Guitar",
                gm_program=25
            )

        )

        # -------------------------
        # BASSES
        # -------------------------

        self.add(

            Instrument(
                name="Finger Bass",
                category="Bass",
                gm_program=33
            )

        )

        self.add(

            Instrument(
                name="Pick Bass",
                category="Bass",
                gm_program=34
            )

        )

        self.add(

            Instrument(
                name="Fretless Bass",
                category="Bass",
                gm_program=35
            )

        )

        self.add(

            Instrument(
                name="Metal Bass",
                category="Bass",
                gm_program=34
            )

        )

        self.add(

            Instrument(
                name="Synth Bass",
                category="Synth Bass",
                gm_program=38
            )

        )

        self.add(

            Instrument(
                name="Sub Bass",
                category="Synth Bass",
                gm_program=39,
                octave_shift=-1
            )

        )

        # -------------------------
        # DRUM KITS
        # -------------------------

        self.add(

            Instrument(
                name="Rock Kit",
                category="Drums",
                gm_program=0,
                default_channel=9
            )

        )

        self.add(

            Instrument(
                name="Metal Kit",
                category="Drums",
                gm_program=0,
                default_channel=9
            )

        )

        self.add(

            Instrument(
                name="Jazz Kit",
                category="Drums",
                gm_program=0,
                default_channel=9
            )

        )

        self.add(

            Instrument(
                name="Electronic Kit",
                category="Drums",
                gm_program=0,
                default_channel=9
            )

        )

        self.add(

            Instrument(
                name="Hybrid Kit",
                category="Drums",
                gm_program=0,
                default_channel=9
            )

        )

        # -------------------------
        # FX
        # -------------------------

        self.add(

            Instrument(
                name="Sweep FX",
                category="FX",
                gm_program=97
            )

        )

        self.add(

            Instrument(
                name="Noise FX",
                category="FX",
                gm_program=98
            )

        )

        self.add(

            Instrument(
                name="Impact FX",
                category="FX",
                gm_program=99
            )

        )

        self.add(

            Instrument(
                name="Atmosphere FX",
                category="FX",
                gm_program=100
            )

        )

    # --------------------------------------------------
    # CORE OPERATIONS
    # --------------------------------------------------

    def add(
        self,
        instrument: Instrument
    ):

        self.instruments[
            instrument.name
        ] = instrument

    def get(
        self,
        name: str
    ) -> Instrument:

        if name not in self.instruments:

            raise KeyError(
                f"Instrument '{name}' not found."
            )

        return self.instruments[
            name
        ].clone()

    def exists(
        self,
        name: str
    ) -> bool:

        return name in self.instruments

    def all_names(self):

        return sorted(

            self.instruments.keys()

        )

    def categories(self):

        return sorted({

            inst.category

            for inst

            in self.instruments.values()

        })

    def by_category(
        self,
        category: str
    ):

        return sorted([

            inst.name

            for inst

            in self.instruments.values()

            if inst.category == category

        ])
        
            # --------------------------------------------------
    # ROLE RECOMMENDATIONS
    # --------------------------------------------------

    def recommended_for_role(
        self,
        role: str
    ) -> List[Instrument]:

        role_map = {

            "Lead Guitar": [
                "High Gain Lead",
                "Shred Lead",
                "Clean Electric Guitar"
            ],

            "Rhythm Guitar L": [
                "Heavy Rhythm Guitar",
                "Crunch Guitar",
                "Rhythm Guitar"
            ],

            "Rhythm Guitar R": [
                "Heavy Rhythm Guitar",
                "Crunch Guitar",
                "Rhythm Guitar"
            ],

            "Bass": [
                "Metal Bass",
                "Finger Bass",
                "Pick Bass",
                "Synth Bass"
            ],

            "Drums": [
                "Rock Kit",
                "Metal Kit",
                "Electronic Kit"
            ],

            "Piano": [
                "Grand Piano",
                "Bright Piano"
            ],

            "Keys": [
                "Electric Piano",
                "Rhodes",
                "Rock Organ"
            ],

            "Pad": [
                "Warm Pad",
                "Ambient Pad",
                "Choir Pad"
            ],

            "Strings": [
                "Strings Ensemble",
                "Cello Section",
                "Violin Section"
            ],

            "Choir": [
                "Choir Aahs",
                "Choir Oohs"
            ],

            "Brass": [
                "French Horn",
                "Trumpet Section",
                "Trombone Section"
            ],

            "Lead Synth": [
                "Lead Saw",
                "Lead Square",
                "Lead Mono"
            ],

            "FX": [
                "Sweep FX",
                "Impact FX",
                "Atmosphere FX"
            ]
        }

        result = []

        for name in role_map.get(role, []):

            if self.exists(name):

                result.append(
                    self.get(name)
                )

        return result

    # --------------------------------------------------
    # GENRE PRESETS
    # --------------------------------------------------

    def genre_preset(
        self,
        genre: str
    ) -> Dict[str, str]:

        presets = {

            "Rock": {

                "Drums": "Rock Kit",

                "Bass": "Pick Bass",

                "Rhythm Guitar L": "Crunch Guitar",

                "Rhythm Guitar R": "Crunch Guitar",

                "Lead Guitar": "Clean Electric Guitar",

                "Piano": "Grand Piano"

            },

            "Heavy Metal": {

                "Drums": "Metal Kit",

                "Bass": "Metal Bass",

                "Rhythm Guitar L": "Heavy Rhythm Guitar",

                "Rhythm Guitar R": "Heavy Rhythm Guitar",

                "Lead Guitar": "High Gain Lead"

            },

            "Progressive Metal": {

                "Drums": "Metal Kit",

                "Bass": "Metal Bass",

                "Rhythm Guitar L": "7-String Guitar",

                "Rhythm Guitar R": "7-String Guitar",

                "Lead Guitar": "Shred Lead",

                "Pad": "Ambient Pad",

                "Strings": "Strings Ensemble"

            },

            "Ambient": {

                "Pad": "Ambient Pad",

                "Strings": "Strings Ensemble",

                "Piano": "Grand Piano",

                "Lead Synth": "Lead Saw"

            },

            "Techno": {

                "Drums": "Electronic Kit",

                "Bass": "Synth Bass",

                "Lead Synth": "Lead Saw",

                "Pad": "Warm Pad",

                "FX": "Sweep FX"

            }

        }

        return copy.deepcopy(

            presets.get(

                genre,

                {}

            )

        )

    # --------------------------------------------------
    # RANDOM SELECTION
    # --------------------------------------------------

    def random_from_category(
        self,
        category: str
    ) -> Optional[Instrument]:

        items = self.by_category(
            category
        )

        if not items:

            return None

        import random

        return self.get(

            random.choice(
                items
            )

        )
        
            # --------------------------------------------------
    # TAG FILTERING
    # --------------------------------------------------

    def by_tag(
        self,
        tag: str
    ) -> List[Instrument]:

        result = []

        for instrument in self.instruments.values():

            tags = instrument.metadata.get(
                "tags",
                []
            )

            if tag in tags:

                result.append(
                    instrument.clone()
                )

        return result

    # --------------------------------------------------
    # USER LIBRARY
    # --------------------------------------------------

    def register_user_instrument(
        self,
        instrument: Instrument
    ):

        self.add(
            instrument
        )

    def remove(
        self,
        name: str
    ):

        if name in self.instruments:

            del self.instruments[
                name
            ]

    # --------------------------------------------------
    # LIBRARY INFO
    # --------------------------------------------------

    def count(self) -> int:

        return len(
            self.instruments
        )

    def summary(self):

        result = {}

        for category in self.categories():

            result[category] = len(

                self.by_category(
                    category
                )

            )

        return result

    # --------------------------------------------------
    # RESET
    # --------------------------------------------------

    def reset(self):

        self.instruments.clear()

        self._build_defaults()