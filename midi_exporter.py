# --------------------------------------------------
# MIDI EXPORTER
# --------------------------------------------------

from typing import List
from mido import Message, MidiFile, MidiTrack, MetaMessage


class MIDIExporter:

    def __init__(self, tempo: int = 120):

        self.tempo = tempo

    # --------------------------------------------------
    # MAIN EXPORT FUNCTION
    # --------------------------------------------------

    def export(
        self,
        melody: List[List[int]],
        chords: List[List[int]],
        filename: str = "output.mid"
    ):

        mid = MidiFile()

        melody_track = MidiTrack()
        chord_track = MidiTrack()

        mid.tracks.append(melody_track)
        mid.tracks.append(chord_track)

        # tempo
        melody_track.append(MetaMessage('set_tempo', tempo=self.bpm_to_microseconds()))

        # --------------------------------------------------
        # MELODY TRACK
        # --------------------------------------------------

        self.write_track(melody_track, melody, channel=0, velocity=90)

        # --------------------------------------------------
        # CHORD TRACK
        # --------------------------------------------------

        self.write_track(chord_track, chords, channel=1, velocity=70)

        mid.save(filename)

        return filename

    # --------------------------------------------------
    # WRITE TRACK
    # --------------------------------------------------

    def write_track(
        self,
        track: MidiTrack,
        events: List[List[int]],
        channel: int,
        velocity: int
    ):

        time = 0

        for chord_or_notes in events:

            if not chord_or_notes:
                continue

            # NOTE ON
            for note in chord_or_notes:

                track.append(
                    Message(
                        'note_on',
                        note=note,
                        velocity=velocity,
                        time=time,
                        channel=channel
                    )
                )

                time = 0

            # NOTE OFF
            for note in chord_or_notes:

                track.append(
                    Message(
                        'note_off',
                        note=note,
                        velocity=0,
                        time=480,
                        channel=channel
                    )
                )

                time = 0

    # --------------------------------------------------
    # TEMPO CONVERSION
    # --------------------------------------------------

    def bpm_to_microseconds(self):

        return int(60000000 / self.tempo)