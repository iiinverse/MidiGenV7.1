# --------------------------------------------------
# CADENCE ENGINE (FINAL v1)
# --------------------------------------------------

import random
from typing import List


class CadenceType:
    AUTHENTIC = "authentic"   # V -> I
    PLAGAL = "plagal"         # IV -> I
    DECEPTIVE = "deceptive"   # V -> vi
    HALF = "half"             # ends on V


class CadenceEngine:

    def __init__(self, harmony_engine):
        """
        Requires HarmonyEngine for chord generation.
        """
        self.harmony = harmony_engine

    def build_cadence(
        self,
        root: str,
        scale_name: str,
        cadence_type: str
    ) -> List:

        if cadence_type == CadenceType.AUTHENTIC:

            return [
                self.harmony.degree_chord(root, scale_name, 5),
                self.harmony.degree_chord(root, scale_name, 1),
            ]

        if cadence_type == CadenceType.PLAGAL:

            return [
                self.harmony.degree_chord(root, scale_name, 4),
                self.harmony.degree_chord(root, scale_name, 1),
            ]

        if cadence_type == CadenceType.DECEPTIVE:

            return [
                self.harmony.degree_chord(root, scale_name, 5),
                self.harmony.degree_chord(root, scale_name, 6),
            ]

        if cadence_type == CadenceType.HALF:

            return [
                self.harmony.degree_chord(root, scale_name, 2),
                self.harmony.degree_chord(root, scale_name, 5),
            ]

        raise ValueError("Unknown cadence type")

    def force_resolution(
        self,
        progression: List,
        root: str,
        scale_name: str,
        cadence_type: str = CadenceType.AUTHENTIC
    ) -> List:

        cadence = self.build_cadence(root, scale_name, cadence_type)

        if not progression:
            return cadence

        resolved = list(progression)

        if len(resolved) >= 2:
            resolved[-2:] = cadence
        else:
            resolved.extend(cadence)

        return resolved

    def maybe_add_cadence(
        self,
        progression: List,
        root: str,
        scale_name: str,
        probability: float = 0.4
    ) -> List:

        if random.random() > probability:
            return progression

        cadence_type = random.choice([
            CadenceType.AUTHENTIC,
            CadenceType.PLAGAL,
            CadenceType.DECEPTIVE
        ])

        return self.force_resolution(
            progression,
            root,
            scale_name,
            cadence_type
        )