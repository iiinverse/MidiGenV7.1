from typing import List, Dict
import random


class CompositionMapper:

    def __init__(self):
        pass

    # --------------------------------------------------
    # MAIN ENTRY
    # --------------------------------------------------

    def build(self, chords: List, mood_profile: Dict, layers: List[Dict]) -> Dict:

        result = {
            "tracks": []
        }

        for layer in layers:

            role = layer["role"]

            generator = self._get_generator(role)

            events = generator(
                chords=chords,
                mood=mood_profile,
                layer=layer
            )

            result["tracks"].append({
                "name": layer["name"],
                "role": role,
                "channel": layer["channel"],
                "instrument": layer["instrument"],
                "events": events
            })

        return result

    # --------------------------------------------------
    # ROUTING
    # --------------------------------------------------

    def _get_generator(self, role: str):

        return {
            "Drums": self._gen_drums,
            "Bass": self._gen_bass,
            "Rhythm Guitar L": self._gen_guitar_rhythm,
            "Rhythm Guitar R": self._gen_guitar_rhythm,
            "Lead Guitar": self._gen_lead,
            "Pad": self._gen_pad,
            "Keys": self._gen_pad,
            "Strings": self._gen_pad,
            "Lead Synth": self._gen_lead,
            "FX": self._gen_fx,
            "Piano": self._gen_piano
        }.get(role, self._gen_pad)

    # --------------------------------------------------
    # DRUMS
    # --------------------------------------------------

    def _gen_drums(self, chords, mood, layer):

        density = layer["density"]
        events = []

        step = 0

        for _ in range(len(chords) * 4):

            if random.random() < density:

                events.append({
                    "type": "note",
                    "pitch": 36,  # kick base
                    "velocity": int(60 + mood["rhythmic_activity"] * 40),
                    "start": step,
                    "duration": 1
                })

            step += 1

        return events

    # --------------------------------------------------
    # BASS
    # --------------------------------------------------

    def _gen_bass(self, chords, mood, layer):

        events = []
        step = 0

        for chord in chords:

            root = chord[0]

            events.append({
                "type": "note",
                "pitch": root - 12,
                "velocity": int(70 + mood["energy"] * 30),
                "start": step,
                "duration": 4
            })

            step += 4

        return events

    # --------------------------------------------------
    # GUITAR RHYTHM
    # --------------------------------------------------

    def _gen_guitar_rhythm(self, chords, mood, layer):

        events = []
        step = 0

        for chord in chords:

            for i in range(4):

                if random.random() < layer["density"]:

                    events.append({
                        "type": "note",
                        "pitch": chord[i % len(chord)],
                        "velocity": int(60 + mood["energy"] * 40),
                        "start": step + i,
                        "duration": 1
                    })

            step += 4

        return events

    # --------------------------------------------------
    # PAD / STRINGS
    # --------------------------------------------------

    def _gen_pad(self, chords, mood, layer):

        events = []
        step = 0

        for chord in chords:

            for note in chord:

                events.append({
                    "type": "note",
                    "pitch": note,
                    "velocity": int(40 + mood["darkness"] * 20),
                    "start": step,
                    "duration": 8
                })

            step += 4

        return events

    # --------------------------------------------------
    # LEAD
    # --------------------------------------------------

    def _gen_lead(self, chords, mood, layer):

        events = []
        step = 0

        for chord in chords:

            note = random.choice(chord)

            events.append({
                "type": "note",
                "pitch": note,
                "velocity": int(80 + mood["valence"] * 20),
                "start": step,
                "duration": 2
            })

            step += 4

        return events

    # --------------------------------------------------
    # PIANO
    # --------------------------------------------------

    def _gen_piano(self, chords, mood, layer):

        return self._gen_pad(chords, mood, layer)

    # --------------------------------------------------
    # FX
    # --------------------------------------------------

    def _gen_fx(self, chords, mood, layer):

        events = []

        for i in range(len(chords)):

            if random.random() < 0.3:

                events.append({
                    "type": "note",
                    "pitch": 84,
                    "velocity": 50,
                    "start": i * 4,
                    "duration": 2
                })

        return events