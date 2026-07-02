from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import copy


# --------------------------------------------------
# GENRE MODEL
# --------------------------------------------------

@dataclass(slots=True)
class Genre:

    name: str

    bpm_range: Tuple[int, int]

    time_signatures: List[str]

    default_scale: str

    default_mode: str

    energy: float

    complexity: float

    groove: float

    density: float

    swing: float

    preferred_roles: List[str]

    metadata: Dict = field(
        default_factory=dict
    )

    def clone(self):

        return copy.deepcopy(
            self
        )


# --------------------------------------------------
# GENRE LIBRARY
# --------------------------------------------------

class GenreLibrary:

    def __init__(self):

        self.genres: Dict[str, Genre] = {}

        self._build_defaults()

    # --------------------------------------------------
    # DEFAULT GENRES
    # --------------------------------------------------

    def _build_defaults(self):

        self.add(

            Genre(

                name="Rock",

                bpm_range=(95, 145),

                time_signatures=["4/4"],

                default_scale="Major",

                default_mode="Ionian",

                energy=0.75,

                complexity=0.55,

                groove=0.70,

                density=0.60,

                swing=0.02,

                preferred_roles=[

                    "Drums",

                    "Bass",

                    "Rhythm Guitar L",

                    "Rhythm Guitar R",

                    "Lead Guitar"

                ]

            )

        )

        self.add(

            Genre(

                name="Hard Rock",

                bpm_range=(105, 160),

                time_signatures=["4/4"],

                default_scale="Minor",

                default_mode="Aeolian",

                energy=0.82,

                complexity=0.62,

                groove=0.68,

                density=0.68,

                swing=0.01,

                preferred_roles=[

                    "Drums",

                    "Bass",

                    "Rhythm Guitar L",

                    "Rhythm Guitar R",

                    "Lead Guitar",

                    "Organ"

                ]

            )

        )

        self.add(

            Genre(

                name="Heavy Metal",

                bpm_range=(120, 190),

                time_signatures=[

                    "4/4"

                ],

                default_scale="Minor",

                default_mode="Phrygian",

                energy=0.95,

                complexity=0.80,

                groove=0.60,

                density=0.88,

                swing=0.0,

                preferred_roles=[

                    "Drums",

                    "Bass",

                    "Rhythm Guitar L",

                    "Rhythm Guitar R",

                    "Lead Guitar"

                ]

            )

        )

        self.add(

            Genre(

                name="Progressive Metal",

                bpm_range=(90, 190),

                time_signatures=[

                    "4/4",

                    "5/4",

                    "7/8",

                    "9/8"

                ],

                default_scale="Minor",

                default_mode="Phrygian",

                energy=0.92,

                complexity=1.0,

                groove=0.72,

                density=0.86,

                swing=0.0,

                preferred_roles=[

                    "Drums",

                    "Bass",

                    "Rhythm Guitar L",

                    "Rhythm Guitar R",

                    "Lead Guitar",

                    "Pad",

                    "Strings"

                ]

            )

        )

        self.add(

            Genre(

                name="Ambient",

                bpm_range=(50, 90),

                time_signatures=[

                    "4/4",

                    "3/4"

                ],

                default_scale="Major",

                default_mode="Lydian",

                energy=0.20,

                complexity=0.40,

                groove=0.15,

                density=0.30,

                swing=0.00,

                preferred_roles=[

                    "Pad",

                    "Strings",

                    "Choir",

                    "Lead Synth"

                ]

            )

        )

        self.add(

            Genre(

                name="Techno",

                bpm_range=(120, 138),

                time_signatures=["4/4"],

                default_scale="Minor",

                default_mode="Aeolian",

                energy=0.90,

                complexity=0.60,

                groove=0.95,

                density=0.75,

                swing=0.03,

                preferred_roles=[

                    "Drums",

                    "Bass",

                    "Lead Synth",

                    "Pad",

                    "FX"

                ]

            )

        )
                self.add(

            Genre(

                name="Thrash Metal",

                bpm_range=(160, 230),

                time_signatures=["4/4"],

                default_scale="Minor",

                default_mode="Phrygian",

                energy=1.00,

                complexity=0.82,

                groove=0.55,

                density=0.95,

                swing=0.00,

                preferred_roles=[

                    "Drums",

                    "Bass",

                    "Rhythm Guitar L",

                    "Rhythm Guitar R",

                    "Lead Guitar"

                ]

            )

        )

        self.add(

            Genre(

                name="Death Metal",

                bpm_range=(140, 240),

                time_signatures=["4/4"],

                default_scale="Minor",

                default_mode="Phrygian",

                energy=1.00,

                complexity=0.90,

                groove=0.50,

                density=1.00,

                swing=0.00,

                preferred_roles=[

                    "Drums",

                    "Bass",

                    "Rhythm Guitar L",

                    "Rhythm Guitar R",

                    "Lead Guitar"

                ]

            )

        )

        self.add(

            Genre(

                name="Black Metal",

                bpm_range=(120,220),

                time_signatures=["4/4","6/8"],

                default_scale="Minor",

                default_mode="Locrian",

                energy=0.95,

                complexity=0.80,

                groove=0.45,

                density=0.90,

                swing=0.00,

                preferred_roles=[

                    "Drums",

                    "Bass",

                    "Rhythm Guitar L",

                    "Rhythm Guitar R",

                    "Lead Guitar",

                    "Choir",

                    "Strings"

                ]

            )

        )

        self.add(

            Genre(

                name="Metalcore",

                bpm_range=(120,190),

                time_signatures=["4/4"],

                default_scale="Minor",

                default_mode="Aeolian",

                energy=0.96,

                complexity=0.80,

                groove=0.82,

                density=0.92,

                swing=0.00,

                preferred_roles=[

                    "Drums",

                    "Bass",

                    "Rhythm Guitar L",

                    "Rhythm Guitar R",

                    "Lead Guitar",

                    "FX"

                ]

            )

        )

        self.add(

            Genre(

                name="Djent",

                bpm_range=(90,170),

                time_signatures=[

                    "4/4",

                    "5/4",

                    "7/8"

                ],

                default_scale="Minor",

                default_mode="Phrygian",

                energy=0.94,

                complexity=1.00,

                groove=0.90,

                density=0.88,

                swing=0.00,

                preferred_roles=[

                    "Drums",

                    "Bass",

                    "Rhythm Guitar L",

                    "Rhythm Guitar R",

                    "Lead Guitar",

                    "Pad"

                ]

            )

        )

        self.add(

            Genre(

                name="Punk",

                bpm_range=(140,210),

                time_signatures=["4/4"],

                default_scale="Major",

                default_mode="Mixolydian",

                energy=0.92,

                complexity=0.40,

                groove=0.80,

                density=0.70,

                swing=0.00,

                preferred_roles=[

                    "Drums",

                    "Bass",

                    "Rhythm Guitar L",

                    "Rhythm Guitar R"

                ]

            )

        )

        self.add(

            Genre(

                name="Pop Punk",

                bpm_range=(130,190),

                time_signatures=["4/4"],

                default_scale="Major",

                default_mode="Ionian",

                energy=0.90,

                complexity=0.45,

                groove=0.82,

                density=0.72,

                swing=0.00,

                preferred_roles=[

                    "Drums",

                    "Bass",

                    "Rhythm Guitar L",

                    "Rhythm Guitar R",

                    "Lead Guitar"

                ]

            )

        )
                self.add(

            Genre(

                name="Blues",

                bpm_range=(60,140),

                time_signatures=["4/4","12/8"],

                default_scale="Major",

                default_mode="Mixolydian",

                energy=0.45,

                complexity=0.55,

                groove=0.92,

                density=0.45,

                swing=0.35,

                preferred_roles=[

                    "Drums",

                    "Bass",

                    "Rhythm Guitar L",

                    "Lead Guitar",

                    "Organ",

                    "Piano"

                ]

            )

        )

        self.add(

            Genre(

                name="Jazz",

                bpm_range=(70,220),

                time_signatures=[

                    "4/4",

                    "3/4",

                    "5/4",

                    "7/4"

                ],

                default_scale="Major",

                default_mode="Dorian",

                energy=0.55,

                complexity=1.00,

                groove=0.90,

                density=0.70,

                swing=0.65,

                preferred_roles=[

                    "Drums",

                    "Bass",

                    "Piano",

                    "Brass",

                    "Lead Guitar"

                ]

            )

        )

        self.add(

            Genre(

                name="Funk",

                bpm_range=(90,130),

                time_signatures=["4/4"],

                default_scale="Minor",

                default_mode="Dorian",

                energy=0.82,

                complexity=0.72,

                groove=1.00,

                density=0.70,

                swing=0.18,

                preferred_roles=[

                    "Drums",

                    "Bass",

                    "Rhythm Guitar L",

                    "Keys",

                    "Brass"

                ]

            )

        )

        self.add(

            Genre(

                name="Soul",

                bpm_range=(70,115),

                time_signatures=["4/4"],

                default_scale="Major",

                default_mode="Ionian",

                energy=0.55,

                complexity=0.60,

                groove=0.85,

                density=0.55,

                swing=0.12,

                preferred_roles=[

                    "Drums",

                    "Bass",

                    "Piano",

                    "Choir",

                    "Brass"

                ]

            )

        )

        self.add(

            Genre(

                name="House",

                bpm_range=(118,128),

                time_signatures=["4/4"],

                default_scale="Minor",

                default_mode="Aeolian",

                energy=0.82,

                complexity=0.52,

                groove=0.98,

                density=0.72,

                swing=0.05,

                preferred_roles=[

                    "Drums",

                    "Bass",

                    "Lead Synth",

                    "Pad",

                    "FX"

                ]

            )

        )

        self.add(

            Genre(

                name="Deep House",

                bpm_range=(118,124),

                time_signatures=["4/4"],

                default_scale="Minor",

                default_mode="Dorian",

                energy=0.60,

                complexity=0.60,

                groove=0.96,

                density=0.58,

                swing=0.08,

                preferred_roles=[

                    "Drums",

                    "Bass",

                    "Pad",

                    "Lead Synth",

                    "FX"

                ]

            )

        )

        self.add(

            Genre(

                name="Progressive House",

                bpm_range=(126,132),

                time_signatures=["4/4"],

                default_scale="Major",

                default_mode="Lydian",

                energy=0.86,

                complexity=0.72,

                groove=0.92,

                density=0.72,

                swing=0.02,

                preferred_roles=[

                    "Drums",

                    "Bass",

                    "Pad",

                    "Lead Synth",

                    "Arpeggio",

                    "FX"

                ]

            )

        )

        self.add(

            Genre(

                name="Melodic Techno",

                bpm_range=(120,128),

                time_signatures=["4/4"],

                default_scale="Minor",

                default_mode="Aeolian",

                energy=0.84,

                complexity=0.75,

                groove=0.94,

                density=0.68,

                swing=0.02,

                preferred_roles=[

                    "Drums",

                    "Bass",

                    "Lead Synth",

                    "Pad",

                    "Strings",

                    "FX"

                ]

            )

        )

        self.add(

            Genre(

                name="Trance",

                bpm_range=(132,145),

                time_signatures=["4/4"],

                default_scale="Minor",

                default_mode="Aeolian",

                energy=0.92,

                complexity=0.72,

                groove=0.92,

                density=0.74,

                swing=0.00,

                preferred_roles=[

                    "Drums",

                    "Bass",

                    "Lead Synth",

                    "Pad",

                    "Arpeggio"

                ]

            )

        )

        self.add(

            Genre(

                name="Psy Trance",

                bpm_range=(138,150),

                time_signatures=["4/4"],

                default_scale="Minor",

                default_mode="Phrygian",

                energy=0.98,

                complexity=0.86,

                groove=0.96,

                density=0.88,

                swing=0.00,

                preferred_roles=[

                    "Drums",

                    "Bass",

                    "Lead Synth",

                    "Pad",

                    "FX"

                ]

            )

        )
                self.add(

            Genre(

                name="Drum & Bass",

                bpm_range=(160,180),

                time_signatures=["4/4"],

                default_scale="Minor",

                default_mode="Aeolian",

                energy=0.98,

                complexity=0.84,

                groove=0.95,

                density=0.92,

                swing=0.04,

                preferred_roles=[

                    "Drums",
                    "Bass",
                    "Lead Synth",
                    "Pad",
                    "FX"

                ]

            )

        )

        self.add(

            Genre(

                name="Dubstep",

                bpm_range=(138,150),

                time_signatures=["4/4"],

                default_scale="Minor",

                default_mode="Phrygian",

                energy=0.97,

                complexity=0.82,

                groove=0.90,

                density=0.90,

                swing=0.00,

                preferred_roles=[

                    "Drums",
                    "Bass",
                    "Lead Synth",
                    "FX",
                    "Pad"

                ]

            )

        )

        self.add(

            Genre(

                name="Trap",

                bpm_range=(120,170),

                time_signatures=["4/4"],

                default_scale="Minor",

                default_mode="Aeolian",

                energy=0.88,

                complexity=0.70,

                groove=0.92,

                density=0.70,

                swing=0.20,

                preferred_roles=[

                    "Drums",
                    "Bass",
                    "Lead Synth",
                    "Pad"

                ]

            )

        )

        self.add(

            Genre(

                name="Hip-Hop",

                bpm_range=(75,105),

                time_signatures=["4/4"],

                default_scale="Minor",

                default_mode="Dorian",

                energy=0.62,

                complexity=0.60,

                groove=0.98,

                density=0.56,

                swing=0.28,

                preferred_roles=[

                    "Drums",
                    "Bass",
                    "Pad",
                    "Lead Synth"

                ]

            )

        )

        self.add(

            Genre(

                name="Lo-Fi",

                bpm_range=(60,95),

                time_signatures=["4/4"],

                default_scale="Major",

                default_mode="Ionian",

                energy=0.30,

                complexity=0.42,

                groove=0.82,

                density=0.34,

                swing=0.18,

                preferred_roles=[

                    "Drums",
                    "Bass",
                    "Piano",
                    "Pad"

                ]

            )

        )

        self.add(

            Genre(

                name="Synthwave",

                bpm_range=(90,120),

                time_signatures=["4/4"],

                default_scale="Minor",

                default_mode="Aeolian",

                energy=0.72,

                complexity=0.62,

                groove=0.82,

                density=0.58,

                swing=0.02,

                preferred_roles=[

                    "Drums",
                    "Bass",
                    "Lead Synth",
                    "Pad",
                    "Arpeggio"

                ]

            )

        )

        self.add(

            Genre(

                name="Future Bass",

                bpm_range=(130,160),

                time_signatures=["4/4"],

                default_scale="Major",

                default_mode="Lydian",

                energy=0.90,

                complexity=0.76,

                groove=0.84,

                density=0.72,

                swing=0.08,

                preferred_roles=[

                    "Drums",
                    "Bass",
                    "Lead Synth",
                    "Pad",
                    "FX"

                ]

            )

        )

        self.add(

            Genre(

                name="EDM",

                bpm_range=(124,132),

                time_signatures=["4/4"],

                default_scale="Minor",

                default_mode="Aeolian",

                energy=0.92,

                complexity=0.68,

                groove=0.94,

                density=0.74,

                swing=0.02,

                preferred_roles=[

                    "Drums",
                    "Bass",
                    "Lead Synth",
                    "Pad",
                    "FX",
                    "Arpeggio"

                ]

            )

        )

        self.add(

            Genre(

                name="Cinematic",

                bpm_range=(55,110),

                time_signatures=[

                    "4/4",
                    "3/4",
                    "6/8"

                ],

                default_scale="Minor",

                default_mode="Aeolian",

                energy=0.60,

                complexity=0.82,

                groove=0.40,

                density=0.72,

                swing=0.00,

                preferred_roles=[

                    "Strings",
                    "Brass",
                    "Choir",
                    "Pad",
                    "FX",
                    "Piano"

                ]

            )

        )

        self.add(

            Genre(

                name="Orchestral",

                bpm_range=(50,150),

                time_signatures=[

                    "4/4",
                    "3/4",
                    "6/8",
                    "5/4"

                ],

                default_scale="Major",

                default_mode="Ionian",

                energy=0.66,

                complexity=0.96,

                groove=0.34,

                density=0.80,

                swing=0.00,

                preferred_roles=[

                    "Strings",
                    "Brass",
                    "Choir",
                    "Piano"

                ]

            )

        )

        self.add(

            Genre(

                name="IDM",

                bpm_range=(90,170),

                time_signatures=[

                    "4/4",
                    "5/4",
                    "7/8"

                ],

                default_scale="Minor",

                default_mode="Locrian",

                energy=0.82,

                complexity=1.00,

                groove=0.72,

                density=0.82,

                swing=0.08,

                preferred_roles=[

                    "Drums",
                    "Bass",
                    "Lead Synth",
                    "FX"

                ]

            )

        )

        self.add(

            Genre(

                name="Minimal",

                bpm_range=(118,128),

                time_signatures=["4/4"],

                default_scale="Minor",

                default_mode="Aeolian",

                energy=0.58,

                complexity=0.36,

                groove=0.94,

                density=0.30,

                swing=0.04,

                preferred_roles=[

                    "Drums",
                    "Bass",
                    "Lead Synth"

                ]

            )

        )

        self.add(

            Genre(

                name="Chillout",

                bpm_range=(70,110),

                time_signatures=["4/4"],

                default_scale="Major",

                default_mode="Lydian",

                energy=0.34,

                complexity=0.46,

                groove=0.72,

                density=0.36,

                swing=0.06,

                preferred_roles=[

                    "Pad",
                    "Piano",
                    "Strings",
                    "Lead Synth"

                ]

            )

        )
            # --------------------------------------------------
    # CORE OPERATIONS
    # --------------------------------------------------

    def add(
        self,
        genre: Genre
    ):

        self.genres[
            genre.name
        ] = genre

    def get(
        self,
        name: str
    ) -> Genre:

        if name not in self.genres:

            raise KeyError(

                f"Genre '{name}' not found."

            )

        return self.genres[
            name
        ].clone()

    def exists(
        self,
        name: str
    ) -> bool:

        return name in self.genres

    def remove(
        self,
        name: str
    ):

        if name in self.genres:

            del self.genres[
                name
            ]

    # --------------------------------------------------
    # COLLECTIONS
    # --------------------------------------------------

    def all_genres(self):

        return sorted(

            self.genres.keys()

        )

    def count(self):

        return len(

            self.genres

        )

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------

    def by_energy(
        self,
        minimum: float = 0.0,
        maximum: float = 1.0
    ):

        return [

            genre.clone()

            for genre

            in self.genres.values()

            if minimum <= genre.energy <= maximum

        ]

    def by_complexity(
        self,
        minimum: float = 0.0,
        maximum: float = 1.0
    ):

        return [

            genre.clone()

            for genre

            in self.genres.values()

            if minimum <= genre.complexity <= maximum

        ]

    def by_bpm(
        self,
        bpm: int
    ):

        result = []

        for genre in self.genres.values():

            low, high = genre.bpm_range

            if low <= bpm <= high:

                result.append(

                    genre.clone()

                )

        return result

    def by_role(
        self,
        role: str
    ):

        return [

            genre.clone()

            for genre

            in self.genres.values()

            if role in genre.preferred_roles

        ]

    # --------------------------------------------------
    # RANDOM
    # --------------------------------------------------

    def random_genre(self):

        import random

        return self.get(

            random.choice(

                self.all_genres()

            )

        )

    # --------------------------------------------------
    # SERIALIZATION
    # --------------------------------------------------

    def to_dict(self):

        return {

            name: copy.deepcopy(

                genre.__dict__

            )

            for name, genre

            in self.genres.items()

        }

    def from_dict(
        self,
        data
    ):

        self.genres.clear()

        for values in data.values():

            self.add(

                Genre(

                    **copy.deepcopy(
                        values
                    )

                )

            )

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    def summary(self):

        return {

            "genres": self.count(),

            "names": self.all_genres()

        }

    # --------------------------------------------------
    # RESET
    # --------------------------------------------------

    def reset(self):

        self.genres.clear()

        self._build_defaults()