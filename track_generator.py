from typing import List, Dict


class TrackGenerator:

    def __init__(self, rules_engine):
        self.rules = rules_engine

    def generate_track_events(
        self,
        track,
        chords: List[Dict],
        mood
    ) -> List[Dict]:

        role = track.role

        if role == "Bass":
            return self.rules.generate_bass(track, chords, mood)

        if role == "Drums":
            return self.rules.generate_drums(track, chords, mood)

        if role in ["Rhythm Guitar L", "Rhythm Guitar R"]:
            return self.rules.generate_guitar(track, chords, mood)

        if role == "Pad":
            return self.rules.generate_pad(track, chords, mood)

        if role == "Lead Guitar":
            return self.rules.generate_lead(track, chords, mood)

        return []