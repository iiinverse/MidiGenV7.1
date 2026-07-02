# --------------------------------------------------
# TENSION ENGINE (FINAL v1)
# --------------------------------------------------

from typing import List


class TensionEngine:

    def __init__(self):

        self.function_tension = {
            "T": 0.2,   # tonic
            "S": 0.5,   # subdominant
            "D": 0.9    # dominant
        }

    def chord_tension(self, chord, harmonic_function: str) -> float:

        base = self.function_tension.get(harmonic_function, 0.3)

        interval_count = len(getattr(chord, "intervals", []))
        interval_factor = interval_count / 7.0

        return min(1.0, base + interval_factor * 0.2)

    def tension_curve(self, chords: List, functions: List[str]) -> List[float]:

        length = min(len(chords), len(functions))

        curve = []

        for i in range(length):

            curve.append(
                self.chord_tension(chords[i], functions[i])
            )

        return curve

    def normalize_curve(self, curve: List[float]) -> List[float]:

        if not curve:
            return []

        min_v = min(curve)
        max_v = max(curve)

        if abs(max_v - min_v) < 1e-9:
            return [0.5] * len(curve)

        return [
            (c - min_v) / (max_v - min_v)
            for c in curve
        ]

    def energy_profile(
        self,
        chords: List,
        functions: List[str],
        smoothing: float = 0.3
    ) -> List[float]:

        raw = self.tension_curve(chords, functions)
        norm = self.normalize_curve(raw)

        smoothed = []
        prev = 0.0

        for v in norm:
            v = v * (1 - smoothing) + prev * smoothing
            smoothed.append(v)
            prev = v

        return smoothed