from typing import List, Dict
import random


class TrackGenerator:

    def __init__(self, harmonic_core):

        self.h = harmonic_core

    # --------------------------------------------------
    # MAIN ENTRY
    # --------------------------------------------------

    def generate(self, track, mood) -> List[Dict]:

        role = track.role

        if role == "Bass":
            return self._bass(track, mood)

        if role == "Drums":
            return self._drums(track, mood)

        if role in ["Rhythm Guitar L", "Rhythm Guitar R"]:
            return self._guitar(track, mood)

        if role == "Pad":
            return self._pad(track, mood)

        if role == "Lead Guitar":
            return self._lead(track, mood)

        return []

    # --------------------------------------------------
    # BASS (ROOT + GROOVE)
    # --------------------------------------------------

    def _bass(self, track, mood):

        events = []
        time = 0

        for i in range(len(self.h.chords)):

            root = self.h.get_root(i)

            note = root - 12

            note = self.h.snap_to_scale(note)

            events.append({
                "track": track.name,
                "pitch": note,
                "start": time,
                "duration": 1.0,
                "velocity": int(80 + mood.energy * 20)
            })

            time += 1.0

        return events

    # --------------------------------------------------
    # DRUMS (GRID + ENERGY)
    # --------------------------------------------------

    def _drums(self, track, mood):

        events = []
        time = 0

        step = 0.5 if mood.rhythmic_activity > 0.6 else 1.0

        for _ in self.h.chords:

            # kick
            events.append({
                "track": track.name,
                "pitch": 36,
                "start": time,
                "duration": 0.1,
                "velocity": 100
            })

            # snare (optional)
            if mood.energy > 0.5:

                events.append({
                    "track": track.name,
                    "pitch": 38,
                    "start": time + step / 2,
                    "duration": 0.1,
                    "velocity": 90
                })

            time += step

        return events

    # --------------------------------------------------
    # GUITAR (CHORD VOICING)
    # --------------------------------------------------

    def _guitar(self, track, mood):

        events = []
        time = 0

        for i in range(len(self.h.chords)):

            notes = self.h.get_chord_notes(i)

            for n in notes[:3]:  # triads only

                events.append({
                    "track": track.name,
                    "pitch": n,
                    "start": time,
                    "duration": 0.8,
                    "velocity": int(70 + mood.energy * 30)
                })

            time += 1.0

        return events

    # --------------------------------------------------
    # PAD (SUSTAINED HARMONY)
    # --------------------------------------------------

    def _pad(self, track, mood):

        events = []
        time = 0

        for i in range(len(self.h.chords)):

            notes = self.h.get_chord_notes(i)

            for n in notes:

                events.append({
                    "track": track.name,
                    "pitch": n,
                    "start": time,
                    "duration": 2.5,
                    "velocity": int(50 + mood.valence * 20)
                })

            time += 2.0

        return events

    # --------------------------------------------------
    # LEAD (SCALE-BASED MELODY)
    # --------------------------------------------------

    def _lead(self, track, mood):

        events = []
        time = 0

        scale = self.h.scale

        for _ in self.h.chords:

            base = random.choice(scale) + 60

            note = self.h.snap_to_scale(base)

            events.append({
                "track": track.name,
                "pitch": note,
                "start": time,
                "duration": 0.5,
                "velocity": int(90 + mood.energy * 10)
            })

            time += 0.5

        return events