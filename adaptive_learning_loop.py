from __future__ import annotations

from typing import Dict, Any, List
import copy
import statistics


# --------------------------------------------------
# ADAPTIVE LEARNING LOOP (V7.1)
# --------------------------------------------------

class AdaptiveLearningLoop:

    def __init__(self, style_system, evaluator):

        self.style_system = style_system
        self.evaluator = evaluator

        self.memory: List[Dict[str, Any]] = []

        self.learning_rate = 0.1

    # --------------------------------------------------
    # MAIN UPDATE STEP
    # --------------------------------------------------

    def update(
        self,
        style_name: str,
        generation_params: Dict[str, Any],
        evaluation_result: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Adjusts generation parameters based on evaluation feedback.
        """

        self.memory.append({
            "style": style_name,
            "params": copy.deepcopy(generation_params),
            "score": evaluation_result["total_score"]
        })

        adjusted = copy.deepcopy(generation_params)

        score = evaluation_result["total_score"]

        # --------------------------------------------------
        # RULE 1: LOW SCORE → REDUCE COMPLEXITY
        # --------------------------------------------------

        if score < 0.5:

            adjusted["complexity"] = max(
                0.1,
                generation_params.get("complexity", 1.0) * (1 - self.learning_rate)
            )

            adjusted["density"] = max(
                0.1,
                generation_params.get("density", 1.0) * (1 - self.learning_rate)
            )

        # --------------------------------------------------
        # RULE 2: HIGH SCORE → AMPLIFY CHARACTERISTICS
        # --------------------------------------------------

        else:

            adjusted["complexity"] = generation_params.get("complexity", 1.0) * (1 + self.learning_rate * 0.5)

            adjusted["density"] = generation_params.get("density", 1.0) * (1 + self.learning_rate * 0.5)

        # --------------------------------------------------
        # RULE 3: STABILITY CORRECTION
        # --------------------------------------------------

        stability = evaluation_result.get("harmonic_stability", 0.5)

        if stability < 0.4:

            adjusted["step_range"] = (
                -2,
                2
            )

        # --------------------------------------------------
        # RULE 4: VARIATION CONTROL
        # --------------------------------------------------

        variation = evaluation_result.get("variation_score", 0.5)

        if variation < 0.3:

            adjusted["mutation_intensity"] = min(
                0.8,
                generation_params.get("mutation_intensity", 0.2) + 0.1
            )

        elif variation > 0.8:

            adjusted["mutation_intensity"] = max(
                0.05,
                generation_params.get("mutation_intensity", 0.2) - 0.1
            )

        return adjusted

    # --------------------------------------------------
    # GLOBAL ANALYSIS
    # --------------------------------------------------

    def analyze_trend(self) -> Dict[str, float]:
        """
        Looks at system evolution over time.
        """

        if not self.memory:
            return {"trend": 0.0}

        scores = [m["score"] for m in self.memory[-10:]]

        return {
            "avg_score": statistics.mean(scores),
            "trend": scores[-1] - scores[0] if len(scores) > 1 else 0.0
        }

    # --------------------------------------------------
    # RESET LEARNING
    # --------------------------------------------------

    def reset(self):
        self.memory.clear()