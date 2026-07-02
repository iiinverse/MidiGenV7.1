from typing import Dict, List


class ArrangementFlattener:

    def flatten(self, composition: Dict) -> List[Dict]:

        flat = []

        for track in composition["tracks"]:

            name = track["name"]

            for e in track["events"]:

                flat.append({
                    "track": name,
                    "pitch": e["pitch"],
                    "start": e["start"],
                    "duration": e["duration"],
                    "velocity": e["velocity"]
                })

        return flat