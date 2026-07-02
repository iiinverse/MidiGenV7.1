from __future__ import annotations

from typing import Dict, Optional
import copy

from mood_library import Mood, MoodLibrary


# --------------------------------------------------
# MOOD ENGINE (CORE SYSTEM)
# --------------------------------------------------

class MoodEngine:

    def __init__(self):

        self.library = MoodLibrary()

        self.active_mood: Optional[Mood] = None

        self.secondary_mood: Optional[Mood] = None

        self.blend_ratio: float = 0.0

    # --------------------------------------------------
    # LOAD / SET MOOD
    # --------------------------------------------------

    def set_mood(self, name: str):

        self.active_mood = self.library.get(name)
        self.secondary_mood = None
        self.blend_ratio = 0.0

    def set_blend(self, mood_a: str, mood_b: str, ratio: float = 0.5):

        self.active_mood = self.library.get(mood_a)
        self.secondary_mood = self.library.get(mood_b)
        self.blend_ratio = max(0.0, min(1.0, ratio))

    # --------------------------------------------------
    # GET CURRENT MOOD (RESOLVED)
    # --------------------------------------------------

    def current(self) -> Mood:

        if not self.active_mood:
            return self.library.get("Happy")

        if not self.secondary_mood:
            return self.active_mood

        return self._blend(
            self.active_mood,
            self.secondary_mood,
            self.blend_ratio
        )

    # --------------------------------------------------
    # INTERNAL BLEND
    # --------------------------------------------------

    def _blend(self, a: Mood, b: Mood, t: float) -> Mood:

        inv = 1.0 - t

        return Mood(

            name=f"{a.name}/{b.name}",

            energy=a.energy * inv + b.energy * t,
            valence=a.valence * inv + b.valence * t,
            darkness=a.darkness * inv + b.darkness * t,
            tension=a.tension * inv + b.tension * t,

            rhythmic_activity=a.rhythmic_activity * inv + b.rhythmic_activity * t,
            melodic_activity=a.melodic_activity * inv + b.melodic_activity * t,
            harmonic_density=a.harmonic_density * inv + b.harmonic_density * t,
            dynamic_range=a.dynamic_range * inv + b.dynamic_range * t,

            complexity=a.complexity * inv + b.complexity * t,
            aggression=a.aggression * inv + b.aggression * t,
            warmth=a.warmth * inv + b.warmth * t,
            brightness=a.brightness * inv + b.brightness * t,

            velocity_bias=int(a.velocity_bias * inv + b.velocity_bias * t),

            swing=a.swing * inv + b.swing * t,
            humanization=a.humanization * inv + b.humanization * t,

            articulation=b.articulation if t > 0.5 else a.articulation,

            preferred_modes=list(dict.fromkeys(
                a.preferred_modes + b.preferred_modes
            )),

            preferred_intervals=list(dict.fromkeys(
                a.preferred_intervals + b.preferred_intervals
            )),

            preferred_tensions=list(dict.fromkeys(
                a.preferred_tensions + b.preferred_tensions
            )),

            genre_affinity=list(dict.fromkeys(
                a.genre_affinity + b.genre_affinity
            )),

            instrument_affinity=list(dict.fromkeys(
                a.instrument_affinity + b.instrument_affinity
            )),

            metadata={}
        )

    # --------------------------------------------------
    # GENERATION PROFILE (MAIN OUTPUT)
    # --------------------------------------------------

    def generation_profile(self, track_role: str = None) -> Dict:

        mood = self.current()

        profile = {

            "energy": mood.energy,
            "valence": mood.valence,
            "darkness": mood.darkness,
            "tension": mood.tension,

            "rhythmic_activity": mood.rhythmic_activity,
            "melodic_activity": mood.melodic_activity,
            "harmonic_density": mood.harmonic_density,
            "dynamic_range": mood.dynamic_range,

            "complexity": mood.complexity,
            "aggression": mood.aggression,
            "warmth": mood.warmth,
            "brightness": mood.brightness,

            "velocity_bias": mood.velocity_bias,
            "swing": mood.swing,
            "humanization": mood.humanization,

            "articulation": mood.articulation,

            "modes": mood.preferred_modes,
            "intervals": mood.preferred_intervals,
            "tensions": mood.preferred_tensions,

            "genres": mood.genre_affinity,
            "instruments": mood.instrument_affinity
        }

        # --------------------------------------------------
        # TRACK-DEPENDENT MODIFICATION (IMPORTANT FOR 15 TRACKS)
        # --------------------------------------------------

        if track_role:

            if track_role == "Drums":
                profile["rhythmic_activity"] *= 1.3
                profile["humanization"] *= 0.8

            if "Guitar" in track_role:
                profile["aggression"] *= 1.2

            if track_role == "Pad":
                profile["dynamic_range"] *= 0.8
                profile["harmonic_density"] *= 1.2

            if track_role == "Bass":
                profile["energy"] *= 1.1

            if track_role == "Lead Guitar":
                profile["melodic_activity"] *= 1.3

        return profile

    # --------------------------------------------------
    # QUICK HELPERS
    # --------------------------------------------------

    def mood_name(self) -> str:

        if self.secondary_mood:
            return f"{self.active_mood.name}/{self.secondary_mood.name}"

        return self.active_mood.name if self.active_mood else "None"

    def reset(self):

        self.active_mood = None
        self.secondary_mood = None
        self.blend_ratio = 0.0