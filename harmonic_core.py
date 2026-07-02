from typing import List, Dict


class HarmonicCore:

    def __init__(self, root: str, scale: List[int], chords: List[Dict]):

        self.root = root
        self.scale = scale
        self.chords = chords

    # --------------------------------------------------
    # SCALE VALIDATION
    # --------------------------------------------------

    def is_in_scale(self, note: int) -> bool:

        return (note % 12) in self.scale

    # --------------------------------------------------
    # SAFE NOTE (fix out-of-scale notes)
    # --------------------------------------------------

    def snap_to_scale(self, note: int) -> int:

        if self.is_in_scale(note):
            return note

        # ищем ближайшую ноту в гамме
        candidates = []

        base_octave = note // 12

        for s in self.scale:

            candidates.append(base_octave * 12 + s)

            candidates.append((base_octave - 1) * 12 + s)

            candidates.append((base_octave + 1) * 12 + s)

        return min(candidates, key=lambda x: abs(x - note))

    # --------------------------------------------------
    # CHORD NOTES SAFE ACCESS
    # --------------------------------------------------

    def get_chord_notes(self, index: int) -> List[int]:

        if index >= len(self.chords):
            index = len(self.chords) - 1

        return self.chords[index]["notes"]

    # --------------------------------------------------
    # ROOT NOTE
    # --------------------------------------------------

    def get_root(self, index: int) -> int:

        if index >= len(self.chords):
            index = len(self.chords) - 1

        return self.chords[index]["root"]