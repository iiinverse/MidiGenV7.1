import random


class TrackRules:

    # -----------------------------
    # BASS
    # -----------------------------
    def generate_bass(self, track, chords, mood):

        events = []

        time = 0

        for chord in chords:

            root = chord["root"]

            events.append({
                "track": track.name,
                "pitch": root - 12,
                "start": time,
                "duration": 1.0,
                "velocity": 90
            })

            time += 1.0

        return events

    # -----------------------------
    # DRUMS
    # -----------------------------
    def generate_drums(self, track, chords, mood):

        events = []

        time = 0

        for _ in chords:

            events.append({
                "track": track.name,
                "pitch": 36,  # kick
                "start": time,
                "duration": 0.1,
                "velocity": 100
            })

            time += 0.5

        return events

    # -----------------------------
    # GUITAR
    # -----------------------------
    def generate_guitar(self, track, chords, mood):

        events = []

        time = 0

        for chord in chords:

            for note in chord["notes"]:

                events.append({
                    "track": track.name,
                    "pitch": note,
                    "start": time,
                    "duration": 0.8,
                    "velocity": 80
                })

            time += 1.0

        return events

    # -----------------------------
    # PAD
    # -----------------------------
    def generate_pad(self, track, chords, mood):

        events = []

        time = 0

        for chord in chords:

            for note in chord["notes"]:

                events.append({
                    "track": track.name,
                    "pitch": note,
                    "start": time,
                    "duration": 2.0,
                    "velocity": 60
                })

            time += 2.0

        return events

    # -----------------------------
    # LEAD
    # -----------------------------
    def generate_lead(self, track, chords, mood):

        events = []

        time = 0

        scale = [60, 62, 64, 67, 69, 71]

        for _ in chords:

            note = random.choice(scale)

            events.append({
                "track": track.name,
                "pitch": note,
                "start": time,
                "duration": 0.5,
                "velocity": 100
            })

            time += 0.5

        return events