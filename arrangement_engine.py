from typing import List, Dict, Optional
import random


class ArrangementEngine:

    def __init__(self, mood_engine):
        self.mood_engine = mood_engine

    # --------------------------------------------------
    # MAIN ENTRY
    # --------------------------------------------------

    def build_arrangement(
        self,
        tracks: List,
        mood_name: str,
        intensity: float = 1.0
    ) -> Dict:

        mood = self.mood_engine.get(mood_name)
        profile = self.mood_engine.generation_profile(mood)

        # 1. classify tracks
        classified = self._classify_tracks(tracks)

        # 2. assign roles based on mood
        arrangement = self._assign_roles(classified, profile, intensity)

        # 3. density shaping
        arrangement = self._apply_density(arrangement, profile)

        # 4. final optimization
        arrangement = self._optimize_layers(arrangement)

        return {
            "mood": mood_name,
            "profile": profile,
            "arrangement": arrangement
        }

    # --------------------------------------------------
    # TRACK CLASSIFICATION
    # --------------------------------------------------

    def _classify_tracks(self, tracks: List) -> Dict[str, List]:

        groups = {
            "rhythm": [],
            "low": [],
            "harmony": [],
            "lead": [],
            "fx": []
        }

        for t in tracks:

            role = t.role.lower()

            if "drum" in role:
                groups["rhythm"].append(t)

            elif "bass" in role:
                groups["low"].append(t)

            elif "pad" in role or "string" in role or "piano" in role:
                groups["harmony"].append(t)

            elif "lead" in role or "melody" in role:
                groups["lead"].append(t)

            else:
                groups["fx"].append(t)

        return groups

    # --------------------------------------------------
    # ROLE ASSIGNMENT
    # --------------------------------------------------

    def _assign_roles(
        self,
        groups: Dict,
        profile: Dict,
        intensity: float
    ) -> Dict:

        result = {}

        # DRUMS always active if present
        for t in groups["rhythm"]:
            result[t.name] = {
                "role": "rhythm",
                "active": True,
                "density": profile["rhythmic_activity"] * intensity
            }

        # BASS = anchor
        for t in groups["low"]:
            result[t.name] = {
                "role": "bass",
                "active": profile["energy"] > 0.2,
                "density": profile["energy"] * intensity
            }

        # HARMONY = mood-driven
        for t in groups["harmony"]:
            result[t.name] = {
                "role": "harmony",
                "active": profile["harmonic_density"] > 0.3,
                "density": profile["harmonic_density"] * intensity
            }

        # LEAD = emotional focus
        for t in groups["lead"]:
            result[t.name] = {
                "role": "lead",
                "active": profile["melodic_activity"] > 0.25,
                "density": profile["melodic_activity"] * intensity
            }

        # FX = conditional
        for t in groups["fx"]:
            result[t.name] = {
                "role": "fx",
                "active": profile["darkness"] > 0.4,
                "density": profile["tension"] * 0.5
            }

        return result

    # --------------------------------------------------
    # DENSITY CONTROL
    # --------------------------------------------------

    def _apply_density(self, arrangement: Dict, profile: Dict) -> Dict:

        for name, data in arrangement.items():

            base = data["density"]

            # global mood shaping
            if profile["energy"] < 0.3:
                base *= 0.6

            if profile["energy"] > 0.8:
                base *= 1.3

            data["density"] = min(1.0, max(0.0, base))

        return arrangement

    # --------------------------------------------------
    # FINAL OPTIMIZATION
    # --------------------------------------------------

    def _optimize_layers(self, arrangement: Dict) -> Dict:

        active_count = sum(
            1 for v in arrangement.values() if v["active"]
        )

        # prevent overcrowding
        if active_count > 10:
            for k, v in arrangement.items():
                if v["role"] == "fx":
                    v["active"] = False

        return arrangement