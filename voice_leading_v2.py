# --------------------------------------------------
# VOICE LEADING ENGINE v2
# --------------------------------------------------

from typing import List, Tuple
import math


class VoiceLeadingEngineV2:

    # --------------------------------------------------
    # MAIN ENTRY
    # --------------------------------------------------

    def voice_lead_progression(
        self,
        chords: List,
        previous_chord=None
    ) -> List[List]:

        voiced = []

        prev = previous_chord

        for chord in chords:

            if prev is None:
                voicing = self.simple_voicing(chord)
            else:
                voicing = self.best_voice_lead(prev, chord)

            voiced.append(voicing)
            prev = voicing

        return voiced

    # --------------------------------------------------
    # SIMPLE INITIAL VOICING
    # --------------------------------------------------

    def simple_voicing(self, chord) -> List[int]:

        # базовое распределение: root position
        base = self.chord_to_pitches(chord)

        return sorted(base)

    # --------------------------------------------------
    # CORE VOICE LEADING ALGORITHM
    # --------------------------------------------------

    def best_voice_lead(self, prev, current) -> List[int]:

        prev_notes = prev
        target_notes = self.chord_to_pitches(current)

        best_voicing = None
        best_cost = float("inf")

        # пробуем все перестановки (inversions)
        permutations = self.generate_voicings(target_notes)

        for voicing in permutations:

            cost = self.voice_cost(prev_notes, voicing)

            if cost < best_cost:
                best_cost = cost
                best_voicing = voicing

        return best_voicing

    # --------------------------------------------------
    # COST FUNCTION (smoothness metric)
    # --------------------------------------------------

    def voice_cost(self, prev: List[int], current: List[int]) -> float:

        cost = 0.0

        for p, c in zip(prev, current):

            # расстояние между голосами
            cost += abs(p - c)

        # штраф за слишком большие скачки
        for i in range(1, len(current)):

            jump = abs(current[i] - current[i - 1])

            if jump > 12:
                cost += jump * 2

        return cost

    # --------------------------------------------------
    # CHORD → PITCHES
    # --------------------------------------------------

    def chord_to_pitches(self, chord) -> List[int]:

        # ожидается: chord.root_midi + intervals
        root = getattr(chord, "root_midi", 60)
        intervals = getattr(chord, "intervals", [0, 4, 7])

        return [root + i for i in intervals]

    # --------------------------------------------------
    # VOICING GENERATOR (inversions)
    # --------------------------------------------------

    def generate_voicings(self, pitches: List[int]) -> List[List[int]]:

        voicings = []

        n = len(pitches)

        for i in range(n):

            rotated = pitches[i:] + pitches[:i]

            # октава нормализация (упрощённо)
            adjusted = [
                p + (12 * (j // n))
                for j, p in enumerate(rotated)
            ]

            voicings.append(sorted(adjusted))

        return voicings