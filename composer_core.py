# --------------------------------------------------
# COMPOSER CORE v1
# --------------------------------------------------

from typing import List, Dict


class ComposerCore:

    def __init__(
        self,
        harmony_engine,
        cadence_engine,
        tension_engine,
        voice_leading_engine
    ):

        self.harmony = harmony_engine
        self.cadence = cadence_engine
        self.tension = tension_engine
        self.voice = voice_leading_engine

    # --------------------------------------------------
    # MAIN ENTRY
    # --------------------------------------------------

    def compose(
        self,
        melody: List,
        root: str,
        scale_name: str,
        emotion: str = "cinematic",
        cadence_probability: float = 0.5
    ) -> Dict:

        # 1. HARMONY GENERATION
        chords = self.harmony.harmonize_melody(
            melody,
            root,
            scale_name
        )

        # 2. EMOTIONAL PROGRESSION (optional override)
        emotion_chords = self.harmony.emotion_progression(
            emotion,
            root,
            scale_name
        )

        # (fallback blend)
        if len(emotion_chords) > 0:

            chords = self._blend_chords(
                chords,
                emotion_chords
            )

        # 3. CADENCE ENFORCEMENT
        chords = self.cadence.maybe_add_cadence(
            chords,
            root,
            scale_name,
            cadence_probability
        )

        # 4. FUNCTION ANALYSIS FOR TENSION
        functions = self.harmony.analyze_progression_functions(
            chords,
            root,
            scale_name
        )

        tension = self.tension.energy_profile(
            chords,
            [f.value for f in functions]
        )

        # 5. VOICE LEADING
        voiced = self.voice.voice_lead_progression(chords)

        # 6. OUTPUT STRUCTURE
        return {
            "chords": chords,
            "functions": functions,
            "tension": tension,
            "voiced": voiced
        }

    # --------------------------------------------------
    # SIMPLE BLEND SYSTEM
    # --------------------------------------------------

    def _blend_chords(
        self,
        base: List,
        emotion: List
    ) -> List:

        result = []

        for i in range(min(len(base), len(emotion))):

            # мягкое смешивание логики
            result.append(base[i])

        # если emotion длиннее — добавляем хвост
        if len(emotion) > len(base):
            result.extend(emotion[len(base):])

        return result
        