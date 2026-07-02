# --------------------------------------------------
# EXPRESSION LAYER v1
# --------------------------------------------------

import random
from typing import List


class ExpressionLayer:

    def __init__(
        self,
        timing_strength: float = 0.02,
        velocity_strength: float = 0.2
    ):

        self.timing_strength = timing_strength
        self.velocity_strength = velocity_strength

    # --------------------------------------------------
    # MAIN ENTRY
    # --------------------------------------------------

    def apply_expression(
        self,
        voiced_chords: List[List[int]],
        durations: List[int],
        tension: List[float]
    ):

        expressed = []

        for i, chord in enumerate(voiced_chords):

            if not chord:
                expressed.append({
                    "notes": [],
                    "duration": durations[i] if i < len(durations) else 480,
                    "velocity": 0,
                    "timing_offset": 0
                })
                continue

            # --------------------------------------------------
            # TIMING HUMANIZATION
            # --------------------------------------------------

            timing_offset = self._timing_drift()

            # --------------------------------------------------
            # VELOCITY SHAPING
            # --------------------------------------------------

            vel = self._velocity_from_tension(
                tension,
                i
            )

            # --------------------------------------------------
            # ARTICULATION
            # --------------------------------------------------

            articulation = self._articulation(tension, i)

            expressed.append({
                "notes": chord,
                "duration": self._apply_articulation(
                    durations[i],
                    articulation
                ),
                "velocity": vel,
                "timing_offset": timing_offset,
                "articulation": articulation
            })

        return expressed

    # --------------------------------------------------
    # HUMAN TIMING DRIFT
    # --------------------------------------------------

    def _timing_drift(self) -> float:

        return random.uniform(
            -self.timing_strength,
            self.timing_strength
        )

    # --------------------------------------------------
    # VELOCITY FROM TENSION
    # --------------------------------------------------

    def _velocity_from_tension(
        self,
        tension: List[float],
        index: int
    ) -> int:

        if index >= len(tension):
            return 80

        t = tension[index]

        return int(50 + t * 70)  # 50–120 range

    # --------------------------------------------------
    # ARTICULATION MODEL
    # --------------------------------------------------

    def _articulation(
        self,
        tension: List[float],
        index: int
    ) -> str:

        if index >= len(tension):
            return "normal"

        t = tension[index]

        if t > 0.7:
            return "staccato"

        if t < 0.3:
            return "legato"

        return "normal"

    # --------------------------------------------------
    # APPLY ARTICULATION TO DURATION
    # --------------------------------------------------

    def _apply_articulation(
        self,
        duration: int,
        articulation: str
    ) -> int:

        if articulation == "staccato":
            return int(duration * 0.6)

        if articulation == "legato":
            return int(duration * 1.2)

        return duration