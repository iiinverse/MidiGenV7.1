from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List
import copy


# --------------------------------------------------
# MOOD MODEL
# --------------------------------------------------

@dataclass(slots=True)
class Mood:

    name: str

    energy: float

    valence: float

    tension: float

    darkness: float

    rhythmic_activity: float

    harmonic_density: float

    melodic_activity: float

    dynamic_range: float

    articulation: str

    velocity_bias: int

    preferred_modes: List[str]

    preferred_intervals: List[int]

    metadata: Dict = field(
        default_factory=dict
    )

    def clone(self):

        return copy.deepcopy(
            self
        )


# --------------------------------------------------
# MOOD ENGINE
# --------------------------------------------------

class MoodEngine:

    def __init__(self):

        self.moods: Dict[str, Mood] = {}

        self._build_defaults()

    # --------------------------------------------------
    # DEFAULT MOODS
    # --------------------------------------------------

    def _build_defaults(self):

        self.add(

            Mood(

                name="Happy",

                energy=0.75,

                valence=0.95,

                tension=0.20,

                darkness=0.05,

                rhythmic_activity=0.75,

                harmonic_density=0.55,

                melodic_activity=0.82,

                dynamic_range=0.72,

                articulation="legato",

                velocity_bias=5,

                preferred_modes=[

                    "Ionian",

                    "Lydian",

                    "Mixolydian"

                ],

                preferred_intervals=[

                    3,
                    4,
                    5,
                    7

                ]

            )

        )

        self.add(

            Mood(

                name="Sad",

                energy=0.35,

                valence=0.15,

                tension=0.40,

                darkness=0.55,

                rhythmic_activity=0.32,

                harmonic_density=0.62,

                melodic_activity=0.55,

                dynamic_range=0.55,

                articulation="legato",

                velocity_bias=-10,

                preferred_modes=[

                    "Aeolian",

                    "Dorian"

                ],

                preferred_intervals=[

                    2,
                    3,
                    7,
                    10

                ]

            )

        )

        self.add(

            Mood(

                name="Dark",

                energy=0.72,

                valence=0.05,

                tension=0.92,

                darkness=1.00,

                rhythmic_activity=0.76,

                harmonic_density=0.86,

                melodic_activity=0.58,

                dynamic_range=0.82,

                articulation="staccato",

                velocity_bias=12,

                preferred_modes=[

                    "Phrygian",

                    "Locrian",

                    "Aeolian"

                ],

                preferred_intervals=[

                    1,
                    6,
                    10,
                    11

                ]

            )

        )

        self.add(

            Mood(

                name="Epic",

                energy=0.92,

                valence=0.78,

                tension=0.72,

                darkness=0.32,

                rhythmic_activity=0.84,

                harmonic_density=0.92,

                melodic_activity=0.82,

                dynamic_range=1.00,

                articulation="accent",

                velocity_bias=18,

                preferred_modes=[

                    "Ionian",

                    "Lydian",

                    "Dorian"

                ],

                preferred_intervals=[

                    5,
                    7,
                    12

                ]

            )

        )

        self.add(

            Mood(

                name="Aggressive",

                energy=1.00,

                valence=0.22,

                tension=1.00,

                darkness=0.82,

                rhythmic_activity=1.00,

                harmonic_density=0.82,

                melodic_activity=0.62,

                dynamic_range=0.92,

                articulation="staccato",

                velocity_bias=20,

                preferred_modes=[

                    "Phrygian",

                    "Locrian"

                ],

                preferred_intervals=[

                    1,
                    6,
                    7

                ]

            )

        )

        self.add(

            Mood(

                name="Relaxed",

                energy=0.22,

                valence=0.72,

                tension=0.10,

                darkness=0.10,

                rhythmic_activity=0.22,

                harmonic_density=0.42,

                melodic_activity=0.42,

                dynamic_range=0.42,

                articulation="legato",

                velocity_bias=-15,

                preferred_modes=[

                    "Lydian",

                    "Ionian"

                ],

                preferred_intervals=[

                    3,
                    5,
                    7

                ]

            )

        )
                self.add(

            Mood(

                name="Melancholic",

                energy=0.30,

                valence=0.12,

                tension=0.48,

                darkness=0.60,

                rhythmic_activity=0.34,

                harmonic_density=0.70,

                melodic_activity=0.74,

                dynamic_range=0.60,

                articulation="legato",

                velocity_bias=-8,

                preferred_modes=[

                    "Aeolian",
                    "Dorian"

                ],

                preferred_intervals=[

                    2,
                    3,
                    7,
                    10

                ]

            )

        )

        self.add(

            Mood(

                name="Hopeful",

                energy=0.68,

                valence=0.92,

                tension=0.28,

                darkness=0.05,

                rhythmic_activity=0.64,

                harmonic_density=0.58,

                melodic_activity=0.84,

                dynamic_range=0.72,

                articulation="legato",

                velocity_bias=6,

                preferred_modes=[

                    "Ionian",
                    "Lydian"

                ],

                preferred_intervals=[

                    4,
                    5,
                    7,
                    12

                ]

            )

        )

        self.add(

            Mood(

                name="Heroic",

                energy=0.95,

                valence=0.82,

                tension=0.74,

                darkness=0.18,

                rhythmic_activity=0.90,

                harmonic_density=0.90,

                melodic_activity=0.86,

                dynamic_range=1.00,

                articulation="accent",

                velocity_bias=16,

                preferred_modes=[

                    "Ionian",
                    "Lydian"

                ],

                preferred_intervals=[

                    5,
                    7,
                    12

                ]

            )

        )

        self.add(

            Mood(

                name="Romantic",

                energy=0.46,

                valence=0.82,

                tension=0.22,

                darkness=0.08,

                rhythmic_activity=0.42,

                harmonic_density=0.82,

                melodic_activity=0.86,

                dynamic_range=0.72,

                articulation="legato",

                velocity_bias=2,

                preferred_modes=[

                    "Ionian",
                    "Lydian",
                    "Dorian"

                ],

                preferred_intervals=[

                    3,
                    4,
                    7,
                    9

                ]

            )

        )

        self.add(

            Mood(

                name="Dreamy",

                energy=0.36,

                valence=0.72,

                tension=0.20,

                darkness=0.18,

                rhythmic_activity=0.28,

                harmonic_density=0.74,

                melodic_activity=0.64,

                dynamic_range=0.52,

                articulation="legato",

                velocity_bias=-4,

                preferred_modes=[

                    "Lydian",
                    "Ionian"

                ],

                preferred_intervals=[

                    5,
                    7,
                    9

                ]

            )

        )

        self.add(

            Mood(

                name="Mysterious",

                energy=0.56,

                valence=0.24,

                tension=0.82,

                darkness=0.82,

                rhythmic_activity=0.56,

                harmonic_density=0.80,

                melodic_activity=0.62,

                dynamic_range=0.70,

                articulation="tenuto",

                velocity_bias=4,

                preferred_modes=[

                    "Locrian",
                    "Phrygian"

                ],

                preferred_intervals=[

                    1,
                    6,
                    10

                ]

            )

        )

        self.add(

            Mood(

                name="Horror",

                energy=0.78,

                valence=0.02,

                tension=1.00,

                darkness=1.00,

                rhythmic_activity=0.58,

                harmonic_density=0.92,

                melodic_activity=0.42,

                dynamic_range=0.90,

                articulation="accent",

                velocity_bias=12,

                preferred_modes=[

                    "Locrian",
                    "Phrygian"

                ],

                preferred_intervals=[

                    1,
                    6,
                    11

                ]

            )

        )

        self.add(

            Mood(

                name="Energetic",

                energy=1.00,

                valence=0.82,

                tension=0.62,

                darkness=0.10,

                rhythmic_activity=1.00,

                harmonic_density=0.72,

                melodic_activity=0.82,

                dynamic_range=0.92,

                articulation="accent",

                velocity_bias=18,

                preferred_modes=[

                    "Ionian",
                    "Mixolydian"

                ],

                preferred_intervals=[

                    4,
                    5,
                    7

                ]

            )

        )

        self.add(

            Mood(

                name="Peaceful",

                energy=0.16,

                valence=0.82,

                tension=0.04,

                darkness=0.02,

                rhythmic_activity=0.18,

                harmonic_density=0.46,

                melodic_activity=0.40,

                dynamic_range=0.40,

                articulation="legato",

                velocity_bias=-18,

                preferred_modes=[

                    "Lydian",
                    "Ionian"

                ],

                preferred_intervals=[

                    5,
                    7,
                    9

                ]

            )

        )

        self.add(

            Mood(

                name="Suspense",

                energy=0.66,

                valence=0.18,

                tension=0.96,

                darkness=0.84,

                rhythmic_activity=0.60,

                harmonic_density=0.82,

                melodic_activity=0.54,

                dynamic_range=0.82,

                articulation="tenuto",

                velocity_bias=8,

                preferred_modes=[

                    "Locrian",
                    "Phrygian"

                ],

                preferred_intervals=[

                    1,
                    6,
                    10,
                    11

                ]

            )

        )
            # --------------------------------------------------
    # CORE OPERATIONS
    # --------------------------------------------------

    def add(
        self,
        mood: Mood
    ):

        self.moods[
            mood.name
        ] = mood

    def get(
        self,
        name: str
    ) -> Mood:

        if name not in self.moods:

            raise KeyError(

                f"Mood '{name}' not found."

            )

        return self.moods[
            name
        ].clone()

    def exists(
        self,
        name: str
    ) -> bool:

        return name in self.moods

    def remove(
        self,
        name: str
    ):

        if name in self.moods:

            del self.moods[
                name
            ]

    # --------------------------------------------------
    # COLLECTIONS
    # --------------------------------------------------

    def names(self):

        return sorted(

            self.moods.keys()

        )

    def count(self):

        return len(

            self.moods

        )

    # --------------------------------------------------
    # FILTERS
    # --------------------------------------------------

    def by_energy(
        self,
        minimum: float = 0.0,
        maximum: float = 1.0
    ):

        return [

            mood.clone()

            for mood

            in self.moods.values()

            if minimum <= mood.energy <= maximum

        ]

    def by_darkness(
        self,
        minimum: float = 0.0,
        maximum: float = 1.0
    ):

        return [

            mood.clone()

            for mood

            in self.moods.values()

            if minimum <= mood.darkness <= maximum

        ]

    def by_tension(
        self,
        minimum: float = 0.0,
        maximum: float = 1.0
    ):

        return [

            mood.clone()

            for mood

            in self.moods.values()

            if minimum <= mood.tension <= maximum

        ]

    def by_valence(
        self,
        minimum: float = 0.0,
        maximum: float = 1.0
    ):

        return [

            mood.clone()

            for mood

            in self.moods.values()

            if minimum <= mood.valence <= maximum

        ]

    # --------------------------------------------------
    # RANDOM
    # --------------------------------------------------

    def random_mood(self):

        import random

        return self.get(

            random.choice(

                self.names()

            )

        )

    # --------------------------------------------------
    # MOOD BLENDING
    # --------------------------------------------------

    def blend(
        self,
        first: Mood,
        second: Mood,
        ratio: float = 0.5
    ) -> Mood:

        ratio = max(
            0.0,
            min(
                1.0,
                ratio
            )
        )

        inv = 1.0 - ratio

        return Mood(

            name=f"{first.name}/{second.name}",

            energy=first.energy * inv + second.energy * ratio,

            valence=first.valence * inv + second.valence * ratio,

            tension=first.tension * inv + second.tension * ratio,

            darkness=first.darkness * inv + second.darkness * ratio,

            rhythmic_activity=(
                first.rhythmic_activity * inv +
                second.rhythmic_activity * ratio
            ),

            harmonic_density=(
                first.harmonic_density * inv +
                second.harmonic_density * ratio
            ),

            melodic_activity=(
                first.melodic_activity * inv +
                second.melodic_activity * ratio
            ),

            dynamic_range=(
                first.dynamic_range * inv +
                second.dynamic_range * ratio
            ),

            articulation=second.articulation,

            velocity_bias=int(

                first.velocity_bias * inv +

                second.velocity_bias * ratio

            ),

            preferred_modes=list(

                dict.fromkeys(

                    first.preferred_modes +

                    second.preferred_modes

                )

            ),

            preferred_intervals=list(

                dict.fromkeys(

                    first.preferred_intervals +

                    second.preferred_intervals

                )

            )

        )

    # --------------------------------------------------
    # GENERATION PARAMETERS
    # --------------------------------------------------

    def generation_profile(
        self,
        mood: Mood
    ):

        return {

            "energy": mood.energy,

            "density": mood.harmonic_density,

            "tension": mood.tension,

            "darkness": mood.darkness,

            "rhythmic_activity": mood.rhythmic_activity,

            "melodic_activity": mood.melodic_activity,

            "dynamic_range": mood.dynamic_range,

            "velocity_bias": mood.velocity_bias,

            "articulation": mood.articulation,

            "preferred_modes": list(

                mood.preferred_modes

            ),

            "preferred_intervals": list(

                mood.preferred_intervals

            )

        }

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    def summary(self):

        return {

            "count": self.count(),

            "moods": self.names()

        }

    # --------------------------------------------------
    # RESET
    # --------------------------------------------------

    def reset(self):

        self.moods.clear()

        self._build_defaults()