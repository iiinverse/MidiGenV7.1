from typing import List, Dict
import copy


class ArrangementEngineV2:

    def __init__(self, mood_engine):
        self.mood_engine = mood_engine

    # --------------------------------------------------
    # MAIN BUILD
    # --------------------------------------------------

    def build(self, tracks: List, mood_name: str) -> Dict:

        mood = self.mood_engine.get(mood_name)
        profile = self.mood_engine.generation_profile(mood)

        layers = self._create_layers(tracks)

        layers = self._apply_mood(layers, profile)

        layers = self._balance_layers(layers, profile)

        return {
            "mood": mood_name,
            "profile": profile,
            "layers": layers
        }

    # --------------------------------------------------
    # LAYER CREATION
    # --------------------------------------------------

    def _create_layers(self, tracks: List) -> Dict:

        layers = {
            "rhythm": [],
            "bass": [],
            "harmony": [],
            "melody": [],
            "texture": []
        }

        for t in tracks:

            r = t.role.lower()

            if "drum" in r:
                layers["rhythm"].append(self._wrap(t, "rhythm"))

            elif "bass" in r:
                layers["bass"].append(self._wrap(t, "bass"))

            elif any(x in r for x in ["pad", "string", "piano", "keys"]):
                layers["harmony"].append(self._wrap(t, "harmony"))

            elif any(x in r for x in ["lead", "melody"]):
                layers["melody"].append(self._wrap(t, "melody"))

            else:
                layers["texture"].append(self._wrap(t, "texture"))

        return layers

    # --------------------------------------------------
    # WRAPPER
    # --------------------------------------------------

    def _wrap(self, track, layer_type: str) -> Dict:

        return {
            "name": track.name,
            "track": track,
            "layer": layer_type,

            # музыкальное поведение (пока заготовка)
            "density": 0.5,
            "activity": 0.5,
            "velocity_bias": 0,
            "enabled": True
        }

    # --------------------------------------------------
    # MOOD APPLICATION
    # --------------------------------------------------

    def _apply_mood(self, layers: Dict, profile: Dict) -> Dict:

        for layer_name, items in layers.items():

            for item in items:

                if layer_name == "rhythm":
                    item["activity"] = profile["rhythmic_activity"]

                elif layer_name == "bass":
                    item["activity"] = profile["energy"]

                elif layer_name == "harmony":
                    item["activity"] = profile["harmonic_density"]

                elif layer_name == "melody":
                    item["activity"] = profile["melodic_activity"]

                elif layer_name == "texture":
                    item["activity"] = profile["darkness"]

                # density scaling
                item["density"] = (
                    item["activity"] * profile["dynamic_range"]
                )

        return layers

    # --------------------------------------------------
    # BALANCING ENGINE
    # --------------------------------------------------

    def _balance_layers(self, layers: Dict, profile: Dict) -> Dict:

        total = 0
        for v in layers.values():
            total += len(v)

        # если перегруз
        if total > 12:

            # отключаем texture first
            for item in layers["texture"]:
                item["enabled"] = False

        # если слишком тихо
        if profile["energy"] < 0.3:

            for item in layers["melody"]:
                item["density"] *= 0.7

        # если агрессивно
        if profile["energy"] > 0.8:

            for item in layers["rhythm"]:
                item["density"] *= 1.3

        return layers