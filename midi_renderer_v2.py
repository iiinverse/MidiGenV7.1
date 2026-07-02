# --------------------------------------------------
# MIDI RENDERER v2 (MONSTER)
# --------------------------------------------------

from typing import List, Dict
from mido import MidiFile, MidiTrack, Message, MetaMessage


class MIDIRendererV2:

    def __init__(self, tempo: int = 120):

        self.tempo = tempo

    # --------------------------------------------------
    # MAIN ENTRY
    # --------------------------------------------------

    def render(
        self,
        composition: Dict,
        durations: List[int],
        filename: str = "output.mid"
    ):

        mid = MidiFile()

        track = MidiTrack()
        mid.tracks.append(track)

        track.append(
            MetaMessage(
                'set_tempo',
                tempo=self.bpm_to_microseconds()
            )
        )

        # voices from voice_leading_v2
        voiced = composition["voiced"]

        time_cursor = 0

        # --------------------------------------------------
        # EVENT RENDER LOOP
        # --------------------------------------------------

        for i, chord in enumerate(voiced):

            if i >= len(durations):
                break

            duration = durations[i]

            if not chord:
                time_cursor += duration
                continue

            # NOTE ON (all voices)
            for note in chord:

                track.append(
                    Message(
                        'note_on',
                        note=note,
                        velocity=self.velocity_from_energy(composition, i),
                        time=time_cursor
                    )
                )

                time_cursor = 0

            # NOTE OFF (delayed)
            for note in chord:

                track.append(
                    Message(
                        'note_off',
                        note=note,
                        velocity=0,
                        time=duration
                    )
                )

                time_cursor = 0

        mid.save(filename)

        return filename

    # --------------------------------------------------
    # EXPRESSIVE VELOCITY
    # --------------------------------------------------

    def velocity_from_energy(
        self,
        composition: Dict,
        index: int
    ) -> int:

        tension = composition.get("tension", [])

        if index >= len(tension):
            return 80

        t = tension[index]

        return int(60 + t * 60)  # 60–120 range

    # --------------------------------------------------
    # TEMPO
    # --------------------------------------------------

    def bpm_to_microseconds(self):

        return int(60000000 / self.tempo)