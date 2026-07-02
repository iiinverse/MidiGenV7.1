from __future__ import annotations

from typing import List, Dict, Any
import statistics


# --------------------------------------------------
# MUSIC EVALUATOR (V7.1)
# --------------------------------------------------

class MusicEvaluator:

    def __init__(self):
        self.history = []

    # --------------------------------------------------
    # MAIN ENTRY
    # --------------------------------------------------

    def evaluate(self, events: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        events format:
        {
            "pitch": int,
            "velocity": int,
            "duration": float,
            "start": float,
            "track": str
        }
        """

        result = {
            "harmonic_stability": self.harmonic_stability(events),
            "tension_curve": self.tension_curve(events),
            "variation_score": self.variation_score(events),
            "range_control": self.range_control(events),
        }

        result["total_score"] = self._aggregate(result)

        self.history.append(result)

        return result

    # --------------------------------------------------
    # METRIC 1: HARMONIC STABILITY
    # --------------------------------------------------

    def harmonic_stability(self, events) -> float:
        if len(events) < 2:
            return 1.0

        intervals = []

        for i in range(1, len(events)):
            intervals.append(
                abs(events[i]["pitch"] - events[i - 1]["pitch"])
            )

        avg_jump = statistics.mean(intervals)

        # penalize large jumps
        score = max(0.0, 1.0 - (avg_jump / 12))

        return round(score, 4)

    # --------------------------------------------------
    # METRIC 2: TENSION CURVE
    # --------------------------------------------------

    def tension_curve(self, events) -> float:
        if not events:
            return 0.0

        pitches = [e["pitch"] for e in events]

        min_p = min(pitches)
        max_p = max(pitches)

        if max_p == min_p:
            return 0.2

        variance = statistics.pvariance(pitches)

        # normalized tension estimate
        score = min(1.0, variance / 400)

        return round(score, 4)

    # --------------------------------------------------
    # METRIC 3: VARIATION SCORE
    # --------------------------------------------------

    def variation_score(self, events) -> float:
        if not events:
            return 0.0

        pitches = [e["pitch"] for e in events]

        unique = len(set(pitches))
        total = len(pitches)

        return round(unique / total, 4)

    # --------------------------------------------------
    # METRIC 4: RANGE CONTROL
    # --------------------------------------------------

    def range_control(self, events) -> float:
        if not events:
            return 0.0

        pitches = [e["pitch"] for e in events]

        out_of_range = sum(
            1 for p in pitches if p < 36 or p > 96
        )

        score = 1.0 - (out_of_range / len(pitches))

        return round(score, 4)

    # --------------------------------------------------
    # AGGREGATION
    # --------------------------------------------------

    def _aggregate(self, scores: Dict[str, float]) -> float:
        return round(
            (
                scores["harmonic_stability"] * 0.30 +
                scores["tension_curve"] * 0.25 +
                scores["variation_score"] * 0.25 +
                scores["range_control"] * 0.20
            ),
            4
        )