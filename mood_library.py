from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import copy


# --------------------------------------------------
# MOOD MODEL (EXPANDED)
# --------------------------------------------------

@dataclass(slots=True)
class Mood:

    name: str

    # core emotional axis
    energy: float
    valence: float
    darkness: float
    tension: float

    # musical behavior
    rhythmic_activity: float
    melodic_activity: float
    harmonic_density: float
    dynamic_range: float

    # advanced generation control
    complexity: float = 0.5
    aggression: float = 0.5
    warmth: float = 0.5
    brightness: float = 0.5

    # performance shaping
    velocity_bias: int = 0
    swing: float = 0.0
    humanization: float = 0.0

    # articulation control
    articulation: str = "legato"

    # harmonic preferences
    preferred_modes: List[str] = field(default_factory=list)
    preferred_intervals: List[int] = field(default_factory=list)
    preferred_tensions: List[int] = field(default_factory=list)

    # stylistic mapping
    genre_affinity: List[str] = field(default_factory=list)
    instrument_affinity: List[str] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)

    def clone(self):
        return copy.deepcopy(self)
        
        from mood_library import Mood


class MoodLibrary:

    def __init__(self):
        self.moods = {}
        self._build()

    # --------------------------------------------------
    # CORE REGISTER
    # --------------------------------------------------

    def add(self, mood: Mood):
        self.moods[mood.name] = mood

    def get(self, name: str) -> Mood:
        return self.moods[name].clone()

    def names(self):
        return list(self.moods.keys())

    # --------------------------------------------------
    # DEFAULT MOODS
    # --------------------------------------------------

    def _build(self):

        # ==================================================
        # HAPPY / BRIGHT
        # ==================================================

        self.add(Mood(
            name="Happy",
            energy=0.75,
            valence=0.95,
            darkness=0.05,
            tension=0.20,
            rhythmic_activity=0.75,
            melodic_activity=0.85,
            harmonic_density=0.55,
            dynamic_range=0.70,
            complexity=0.45,
            aggression=0.10,
            warmth=0.85,
            brightness=0.95,
            velocity_bias=6,
            swing=0.05,
            humanization=0.10,
            articulation="legato",
            preferred_modes=["Ionian", "Lydian"],
            preferred_intervals=[3, 4, 5, 7],
            preferred_tensions=[9, 11],
            genre_affinity=["Pop", "Funk"],
            instrument_affinity=["Piano", "Keys", "Clean Electric Guitar"]
        ))

        self.add(Mood(
            name="Cheerful",
            energy=0.80,
            valence=0.92,
            darkness=0.08,
            tension=0.18,
            rhythmic_activity=0.78,
            melodic_activity=0.88,
            harmonic_density=0.52,
            dynamic_range=0.72,
            complexity=0.40,
            aggression=0.08,
            warmth=0.90,
            brightness=0.98,
            velocity_bias=8,
            swing=0.08,
            humanization=0.12,
            articulation="legato",
            preferred_modes=["Ionian"],
            preferred_intervals=[3, 5, 7],
            preferred_tensions=[9],
            genre_affinity=["Pop"],
            instrument_affinity=["Piano", "Bright Piano"]
        ))

        # ==================================================
        # SAD / EMOTIONAL
        # ==================================================

        self.add(Mood(
            name="Sad",
            energy=0.30,
            valence=0.15,
            darkness=0.55,
            tension=0.40,
            rhythmic_activity=0.30,
            melodic_activity=0.60,
            harmonic_density=0.65,
            dynamic_range=0.55,
            complexity=0.55,
            aggression=0.05,
            warmth=0.30,
            brightness=0.25,
            velocity_bias=-10,
            swing=0.00,
            humanization=0.20,
            articulation="legato",
            preferred_modes=["Aeolian", "Dorian"],
            preferred_intervals=[2, 3, 7, 10],
            preferred_tensions=[9, 11],
            genre_affinity=["Cinematic", "Ambient"],
            instrument_affinity=["Strings Ensemble", "Piano", "Pad"]
        ))

        self.add(Mood(
            name="Melancholic",
            energy=0.35,
            valence=0.12,
            darkness=0.60,
            tension=0.48,
            rhythmic_activity=0.35,
            melodic_activity=0.72,
            harmonic_density=0.70,
            dynamic_range=0.60,
            complexity=0.60,
            aggression=0.10,
            warmth=0.25,
            brightness=0.20,
            velocity_bias=-8,
            swing=0.02,
            humanization=0.22,
            articulation="legato",
            preferred_modes=["Aeolian", "Dorian"],
            preferred_intervals=[2, 3, 7, 10],
            preferred_tensions=[9, 11],
            genre_affinity=["Cinematic"],
            instrument_affinity=["Piano", "Strings Ensemble"]
        ))

        # ==================================================
        # DARK / HORROR
        # ==================================================

        self.add(Mood(
            name="Dark",
            energy=0.70,
            valence=0.05,
            darkness=1.00,
            tension=0.92,
            rhythmic_activity=0.75,
            melodic_activity=0.55,
            harmonic_density=0.85,
            dynamic_range=0.80,
            complexity=0.80,
            aggression=0.70,
            warmth=0.10,
            brightness=0.05,
            velocity_bias=12,
            swing=0.00,
            humanization=0.15,
            articulation="staccato",
            preferred_modes=["Phrygian", "Locrian", "Aeolian"],
            preferred_intervals=[1, 6, 10, 11],
            preferred_tensions=[b9, 11, 13] if False else [1, 11],  # placeholder safe
            genre_affinity=["Metal", "Horror", "Cinematic"],
            instrument_affinity=["Distorted Guitar", "Strings", "FX"]
        ))

        self.add(Mood(
            name="Horror",
            energy=0.80,
            valence=0.02,
            darkness=1.00,
            tension=1.00,
            rhythmic_activity=0.60,
            melodic_activity=0.40,
            harmonic_density=0.90,
            dynamic_range=0.90,
            complexity=0.85,
            aggression=0.85,
            warmth=0.05,
            brightness=0.02,
            velocity_bias=15,
            swing=0.00,
            humanization=0.25,
            articulation="accent",
            preferred_modes=["Locrian", "Phrygian"],
            preferred_intervals=[1, 6, 11],
            preferred_tensions=[1, 11],
            genre_affinity=["Horror", "Cinematic"],
            instrument_affinity=["FX", "Strings Ensemble", "Noise FX"]
        ))
        
        