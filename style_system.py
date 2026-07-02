from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


# --------------------------------------------------
# STYLE PROFILE
# --------------------------------------------------

@dataclass
class StyleProfile:
    name: str

    motif_density: float
    pitch_range: int
    rhythmic_variation: float
    harmonic_complexity: float
    tension_speed: float
    repetition_bias: float


# --------------------------------------------------
# STYLE SYSTEM (V7.1)
# --------------------------------------------------

class StyleSystem:

    def __init__(self):

        self.styles: Dict[str, StyleProfile] = {

            "techno": StyleProfile(
                name="techno",
                motif_density=0.7,
                pitch_range=18,
                rhythmic_variation=0.6,
                harmonic_complexity=0.3,
                tension_speed=0.8,
                repetition_bias=0.9
            ),

            "ambient": StyleProfile(
                name="ambient",
                motif_density=0.3,
                pitch_range=36,
                rhythmic_variation=0.2,
                harmonic_complexity=0.7,
                tension_speed=0.2,
                repetition_bias=0.6
            ),

            "cinematic": StyleProfile(
                name="cinematic",
                motif_density=0.5,
                pitch_range=48,
                rhythmic_variation=0.5,
                harmonic_complexity=0.9,
                tension_speed=0.7,
                repetition_bias=0.5
            ),

            "jazz": StyleProfile(
                name="jazz",
                motif_density=0.6,
                pitch_range=36,
                rhythmic_variation=0.8,
                harmonic_complexity=0.95,
                tension_speed=0.5,
                repetition_bias=0.4
            ),

            "minimal": StyleProfile(
                name="minimal",
                motif_density=0.2,
                pitch_range=12,
                rhythmic_variation=0.3,
                harmonic_complexity=0.2,
                tension_speed=0.3,
                repetition_bias=0.95
            )
        }

    # --------------------------------------------------
    # GET STYLE
    # --------------------------------------------------

    def get(self, name: str) -> StyleProfile:
        return self.styles[name]

    # --------------------------------------------------
    # APPLY STYLE MODIFIERS
    # --------------------------------------------------

    def apply_to_motif_params(self, style: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inject style bias into motif generation parameters.
        """

        s = self.get(style)

        params = params.copy()

        # rhythm control
        if "step_range" in params:
            base = params["step_range"]
            scale = int(s.pitch_range / 10)

            params["step_range"] = (
                -abs(base[0]) - scale,
                abs(base[1]) + scale
            )

        # density control
        if "density" in params:
            params["density"] *= s.motif_density

        return params

    # --------------------------------------------------
    # STYLE INJECTION INTO HARMONY
    # --------------------------------------------------

    def apply_to_harmony_params(self, style: str, params: Dict[str, Any]) -> Dict[str, Any]:

        s = self.get(style)

        params = params.copy()

        if "complexity" in params:
            params["complexity"] *= s.harmonic_complexity

        return params

    # --------------------------------------------------
    # STYLE SUMMARY
    # --------------------------------------------------

    def describe(self, style: str) -> Dict[str, Any]:
        s = self.get(style)

        return {
            "name": s.name,
            "motif_density": s.motif_density,
            "pitch_range": s.pitch_range,
            "rhythmic_variation": s.rhythmic_variation,
            "harmonic_complexity": s.harmonic_complexity,
            "tension_speed": s.tension_speed,
            "repetition_bias": s.repetition_bias,
        }