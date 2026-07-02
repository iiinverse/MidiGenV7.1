# --------------------------------------------------
# TIME LAYER v1
# --------------------------------------------------

from typing import List


class TimeLayer:

    def __init__(self, base_step: int = 480):

        self.base_step = base_step

    # --------------------------------------------------
    # CHORD DURATION ENGINE
    # --------------------------------------------------

    def chord_durations(
        self,
        chords: List,
        tension: List[float]
    ) -> List[int]:

        durations = []

        for t in tension:

            # чем выше напряжение — тем короче гармония
            if t < 0.3:
                durations.append(self.base_step * 2)   # long pad
            elif t < 0.6:
                durations.append(self.base_step)       # normal
            else:
                durations.append(self.base_step // 2)  # fast movement

        return durations

    # --------------------------------------------------
    # MELODY DURATION ENGINE
    # --------------------------------------------------

    def melody_durations(
        self,
        melody: List
    ) -> List[int]:

        # простая мотивная структура
        pattern = [
            self.base_step // 2,
            self.base_step // 2,
            self.base_step,
            self.base_step // 2
        ]

        return [
            pattern[i % len(pattern)]
            for i in range(len(melody))
        ]

    # --------------------------------------------------
    # RHYTHMIC GRID ALIGNMENT
    # --------------------------------------------------

    def align_to_grid(self, durations: List[int]) -> List[int]:

        return [
            max(120, int(round(d / 60) * 60))
            for d in durations
        ]