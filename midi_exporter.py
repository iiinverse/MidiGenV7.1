from typing import List, Dict
from mido import Message, MidiFile, MidiTrack, MetaMessage


# --------------------------------------------------
# MIDI EXPORTER (V7.1 INTEGRATED)
# --------------------------------------------------

class MIDIExporter:

    def __init__(self, tempo: int = 120):
        self.tempo = tempo

    # --------------------------------------------------
    # MAIN EXPORT FUNCTION
    # --------------------------------------------------

    def export(
        self,
        events: List[Dict],
        filename: str = "output.mid"
    ) -> str:
        """
        Expects flattened arrangement:
        [
            {
                "track": str,
                "pitch": int,
                "duration": float,
                "velocity": int,
                "start": float
            }
        ]
        """

        mid = MidiFile()

        # group by track
        tracks_map = {}

        for e in events:
            t = e["track"]
            if t not in tracks_map:
                tracks_map[t] = MidiTrack()
                mid.tracks.append(tracks_map[t])

        # tempo track (first track)
        tempo_track = MidiTrack()
        mid.tracks.insert(0, tempo_track)

        tempo_track.append(
            MetaMessage(
                "set_tempo",
                tempo=self.bpm_to_microseconds()
            )
        )

        # --------------------------------------------------
        # WRITE EVENTS
        # --------------------------------------------------

        for track_name, track in tracks_map.items():

            track_events = [e for e in events if e["track"] == track_name]

            # sort by time
            track_events.sort(key=lambda x: x["start"])

            current_time = 0

            for e in track_events:

                delta = int((e["start"] - current_time) * 480)
                current_time = e["start"]

                # NOTE ON
                track.append(
                    Message(
                        "note_on",
                        note=e["pitch"],
                        velocity=e["velocity"],
                        time=max(delta, 0),
                        channel=0
                    )
                )

                # NOTE OFF (fixed duration)
                off_time = int(e["duration"] * 480)

                track.append(
                    Message(
                        "note_off",
                        note=e["pitch"],
                        velocity=0,
                        time=off_time,
                        channel=0
                    )
                )

        mid.save(filename)
        return filename

    # --------------------------------------------------
    # TEMPO
    # --------------------------------------------------

    def bpm_to_microseconds(self) -> int:
        return int(60000000 / self.tempo)