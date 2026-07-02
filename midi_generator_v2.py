from typing import Dict, List
import random


class MidiGeneratorV2:

    def __init__(self):
        pass

    # --------------------------------------------------
    # MAIN ENTRY
    # --------------------------------------------------

    def generate(
        self,
        layers: Dict,
        scale: List[int],
        root: int = 60,
        bars: int = 4,
        ticks_per_bar: int = 16
    ) -> List[Dict]:

        events = []

        for layer_name, items in layers.items():

            for item in items:

                if not item["enabled"]:
                    continue

                events.extend(
                    self._generate_layer(
                        item,
                        layer_name,
                        scale,
                        root,
                        bars,
                        ticks_per_bar
                    )
                )

        return events

    # --------------------------------------------------
    # LAYER GENERATION
    # --------------------------------------------------

    def _generate_layer(
        self,
        item: Dict,
        layer: str,
        scale: List[int],
        root: int,
        bars: int,
        tpb: int
    ) -> List[Dict]:

        events = []

        density = item["density"]
        activity = item["activity"]

        total_steps = bars * tpb

        for step in range(total_steps):

            if random.random() > density:
                continue

            time = step / tpb

            pitch = self._choose_pitch(layer, scale, root)

            velocity = self._velocity(activity)

            duration = self._duration(layer, tpb)

            events.append({
                "track": item["name"],
                "pitch": pitch,
                "velocity": velocity,
                "start": time,
                "duration": duration
            })

        return events

    # --------------------------------------------------
    # PITCH LOGIC
    # --------------------------------------------------

    def _choose_pitch(
        self,
        layer: str,
        scale: List[int],
        root: int
    ) -> int:

        if layer == "bass":
            return root - 12 + random.choice([0, 3, 5])

        if layer == "rhythm":
            return root + random.choice(scale)

        if layer == "melody":
            return root + random.choice(scale) + random.choice([12, 24])

        if layer == "harmony":
            return root + random.choice(scale)

        return root

    # --------------------------------------------------
    # VELOCITY
    # --------------------------------------------------

    def _velocity(self, activity: float) -> int:

        base = int(60 + activity * 60)
        return max(20, min(127, base + random.randint(-10, 10)))

    # --------------------------------------------------
    # DURATION
    # --------------------------------------------------

    def _duration(self, layer: str, tpb: int) -> float:

        if layer == "bass":
            return random.choice([1.0, 2.0])

        if layer == "melody":
            return random.choice([0.25, 0.5, 1.0])

        if layer == "rhythm":
            return random.choice([0.25, 0.5])

        return 1.0