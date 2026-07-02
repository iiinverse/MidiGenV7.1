# --------------------------------------------------
# STRUCTURE ENGINE v1
# --------------------------------------------------

from typing import List, Dict


class StructureEngine:

    # --------------------------------------------------
    # MAIN STRUCTURE BUILDER
    # --------------------------------------------------

    def build_structure(
        self,
        length_bars: int = 32
    ) -> List[Dict]:

        structure = []

        # фиксированная форма v1 (можем потом усложнять)
        # A = exposition
        # B = development
        # C = climax
        # D = resolution

        sections = [
            ("A", 0.25),
            ("B", 0.25),
            ("C", 0.25),
            ("D", 0.25),
        ]

        bar_cursor = 0

        for name, ratio in sections:

            bars = int(length_bars * ratio)

            structure.append({
                "section": name,
                "start_bar": bar_cursor,
                "end_bar": bar_cursor + bars,
                "energy_target": self._energy_profile(name),
                "bars": bars
            })

            bar_cursor += bars

        return structure

    # --------------------------------------------------
    # ENERGY MAP OF SECTIONS
    # --------------------------------------------------

    def _energy_profile(self, section: str) -> Dict:

        if section == "A":
            return {
                "tension": 0.3,
                "density": 0.4
            }

        if section == "B":
            return {
                "tension": 0.5,
                "density": 0.6
            }

        if section == "C":
            return {
                "tension": 0.9,
                "density": 0.9
            }

        if section == "D":
            return {
                "tension": 0.4,
                "density": 0.3
            }

        return {
            "tension": 0.5,
            "density": 0.5
        }

    # --------------------------------------------------
    # SECTION MAPPING HELPERS
    # --------------------------------------------------

    def get_section_at_bar(
        self,
        structure: List[Dict],
        bar: int
    ) -> Dict:

        for section in structure:

            if section["start_bar"] <= bar < section["end_bar"]:
                return section

        return structure[-1]

    # --------------------------------------------------
    # GLOBAL ENERGY CURVE
    # --------------------------------------------------

    def build_energy_curve(
        self,
        structure: List[Dict]
    ) -> List[float]:

        curve = []

        for section in structure:

            for _ in range(section["bars"]):

                curve.append(
                    section["energy_target"]["tension"]
                )

        return curve