from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import copy


# --------------------------------------------------
# GENRE
# --------------------------------------------------

@dataclass(slots=True)
class Genre:

    name: str

    bpm_min: int

    bpm_max: int

    swing: float

    complexity: float

    density: float

    humanization: float

    preferred_scales: List[str]

    preferred_modes: List[str]

    preferred_time_signatures: List[str]

    chord_complexity: float

    modulation_probability: float

    melody_activity: float

    bass_activity: float

    drum_activity: float

    guitar_activity: float

    keyboard_activity: float

    orchestral_activity: float

    fx_activity: float

    moods: List[str]

    tags: List[str]

    metadata: Dict = field(
        default_factory=dict
    )

    def clone(self):

        return copy.deepcopy(
            self
        )


# --------------------------------------------------
# GENRE ENGINE
# --------------------------------------------------

class GenreEngine:

    def __init__(self):

        self.genres: Dict[str, Genre] = {}

        self._build_library()

    # --------------------------------------------------
    # REGISTER
    # --------------------------------------------------

    def add(
        self,
        genre: Genre
    ):

        self.genres[
            genre.name
        ] = genre

    def get(
        self,
        name: str
    ) -> Genre:

        return self.genres[
            name
        ].clone()

    def exists(
        self,
        name: str
    ):

        return name in self.genres

    def names(self):

        return sorted(
            self.genres.keys()
        )

    # --------------------------------------------------
    # DEFAULT GENRES
    # --------------------------------------------------

    def _build_library(self):

        self.add(

            Genre(

                name="Rock",

                bpm_min=100,

                bpm_max=145,

                swing=0.02,

                complexity=0.60,

                density=0.70,

                humanization=0.15,

                preferred_scales=[
                    "Major",
                    "Minor",
                    "Pentatonic"
                ],

                preferred_modes=[
                    "Ionian",
                    "Mixolydian",
                    "Aeolian"
                ],

                preferred_time_signatures=[
                    "4/4"
                ],

                chord_complexity=0.50,

                modulation_probability=0.15,

                melody_activity=0.65,

                bass_activity=0.80,

                drum_activity=0.90,

                guitar_activity=1.00,

                keyboard_activity=0.35,

                orchestral_activity=0.10,

                fx_activity=0.20,

                moods=[

                    "Energetic",

                    "Epic",

                    "Happy"

                ],

                tags=[

                    "band",

                    "guitar",

                    "live"

                ]

            )

        )

        self.add(

            Genre(

                name="Heavy Metal",

                bpm_min=120,

                bpm_max=220,

                swing=0.00,

                complexity=0.90,

                density=0.95,

                humanization=0.08,

                preferred_scales=[
                    "Minor",
                    "Phrygian",
                    "Harmonic Minor"
                ],

                preferred_modes=[
                    "Phrygian",
                    "Locrian",
                    "Aeolian"
                ],

                preferred_time_signatures=[
                    "4/4",
                    "6/8"
                ],

                chord_complexity=0.75,

                modulation_probability=0.25,

                melody_activity=0.80,

                bass_activity=0.90,

                drum_activity=1.00,

                guitar_activity=1.00,

                keyboard_activity=0.15,

                orchestral_activity=0.15,

                fx_activity=0.30,

                moods=[

                    "Aggressive",

                    "Dark",

                    "Epic"

                ],

                tags=[

                    "metal",

                    "riff",

                    "doublekick"

                ]

            )

        )
        
                self.add(

            Genre(

                name="Progressive Metal",

                bpm_min=95,

                bpm_max=180,

                swing=0.00,

                complexity=1.00,

                density=0.90,

                humanization=0.12,

                preferred_scales=[
                    "Minor",
                    "Harmonic Minor",
                    "Melodic Minor",
                    "Phrygian"
                ],

                preferred_modes=[
                    "Phrygian",
                    "Aeolian",
                    "Dorian",
                    "Lydian"
                ],

                preferred_time_signatures=[
                    "4/4",
                    "5/4",
                    "7/8",
                    "9/8"
                ],

                chord_complexity=0.95,

                modulation_probability=0.60,

                melody_activity=0.90,

                bass_activity=0.95,

                drum_activity=1.00,

                guitar_activity=1.00,

                keyboard_activity=0.70,

                orchestral_activity=0.40,

                fx_activity=0.50,

                moods=[
                    "Epic",
                    "Dark",
                    "Technical"
                ],

                tags=[
                    "prog",
                    "odd_meter",
                    "virtuoso"
                ]

            )

        )

        self.add(

            Genre(

                name="Metalcore",

                bpm_min=120,

                bpm_max=190,

                swing=0.00,

                complexity=0.82,

                density=0.95,

                humanization=0.08,

                preferred_scales=[
                    "Minor",
                    "Phrygian"
                ],

                preferred_modes=[
                    "Aeolian",
                    "Phrygian"
                ],

                preferred_time_signatures=[
                    "4/4"
                ],

                chord_complexity=0.60,

                modulation_probability=0.15,

                melody_activity=0.65,

                bass_activity=0.95,

                drum_activity=1.00,

                guitar_activity=1.00,

                keyboard_activity=0.25,

                orchestral_activity=0.20,

                fx_activity=0.35,

                moods=[
                    "Aggressive",
                    "Emotional",
                    "Epic"
                ],

                tags=[
                    "breakdown",
                    "modern",
                    "heavy"
                ]

            )

        )

        self.add(

            Genre(

                name="Djent",

                bpm_min=100,

                bpm_max=170,

                swing=0.00,

                complexity=0.98,

                density=0.96,

                humanization=0.06,

                preferred_scales=[
                    "Minor",
                    "Phrygian"
                ],

                preferred_modes=[
                    "Phrygian",
                    "Locrian"
                ],

                preferred_time_signatures=[
                    "4/4",
                    "7/8",
                    "9/8"
                ],

                chord_complexity=0.85,

                modulation_probability=0.45,

                melody_activity=0.70,

                bass_activity=1.00,

                drum_activity=1.00,

                guitar_activity=1.00,

                keyboard_activity=0.25,

                orchestral_activity=0.15,

                fx_activity=0.30,

                moods=[
                    "Mechanical",
                    "Dark",
                    "Technical"
                ],

                tags=[
                    "polyrhythm",
                    "groove",
                    "extended_range"
                ]

            )

        )

        self.add(

            Genre(

                name="Hard Rock",

                bpm_min=100,

                bpm_max=165,

                swing=0.03,

                complexity=0.60,

                density=0.75,

                humanization=0.18,

                preferred_scales=[
                    "Major",
                    "Minor",
                    "Pentatonic"
                ],

                preferred_modes=[
                    "Mixolydian",
                    "Aeolian"
                ],

                preferred_time_signatures=[
                    "4/4"
                ],

                chord_complexity=0.55,

                modulation_probability=0.12,

                melody_activity=0.70,

                bass_activity=0.85,

                drum_activity=0.90,

                guitar_activity=1.00,

                keyboard_activity=0.30,

                orchestral_activity=0.05,

                fx_activity=0.20,

                moods=[
                    "Energetic",
                    "Confident",
                    "Epic"
                ],

                tags=[
                    "riff",
                    "solo",
                    "arena"
                ]

            )

        )
        
                self.add(

            Genre(

                name="Cinematic",

                bpm_min=60,

                bpm_max=130,

                swing=0.00,

                complexity=0.85,

                density=0.80,

                humanization=0.20,

                preferred_scales=[
                    "Minor",
                    "Major",
                    "Harmonic Minor",
                    "Dorian"
                ],

                preferred_modes=[
                    "Aeolian",
                    "Dorian",
                    "Lydian"
                ],

                preferred_time_signatures=[
                    "4/4",
                    "3/4",
                    "6/8"
                ],

                chord_complexity=0.90,

                modulation_probability=0.55,

                melody_activity=0.70,

                bass_activity=0.60,

                drum_activity=0.45,

                guitar_activity=0.20,

                keyboard_activity=0.75,

                orchestral_activity=1.00,

                fx_activity=0.90,

                moods=[
                    "Epic",
                    "Emotional",
                    "Dark",
                    "Hopeful"
                ],

                tags=[
                    "film",
                    "orchestra",
                    "hybrid"
                ]

            )

        )

        self.add(

            Genre(

                name="Ambient",

                bpm_min=50,

                bpm_max=100,

                swing=0.00,

                complexity=0.45,

                density=0.35,

                humanization=0.25,

                preferred_scales=[
                    "Major",
                    "Minor",
                    "Lydian"
                ],

                preferred_modes=[
                    "Lydian",
                    "Ionian",
                    "Dorian"
                ],

                preferred_time_signatures=[
                    "4/4",
                    "3/4"
                ],

                chord_complexity=0.65,

                modulation_probability=0.35,

                melody_activity=0.20,

                bass_activity=0.30,

                drum_activity=0.10,

                guitar_activity=0.25,

                keyboard_activity=0.85,

                orchestral_activity=0.65,

                fx_activity=1.00,

                moods=[
                    "Calm",
                    "Dreamy",
                    "Floating"
                ],

                tags=[
                    "texture",
                    "space",
                    "atmosphere"
                ]

            )

        )

        self.add(

            Genre(

                name="Synthwave",

                bpm_min=80,

                bpm_max=125,

                swing=0.00,

                complexity=0.60,

                density=0.70,

                humanization=0.08,

                preferred_scales=[
                    "Minor",
                    "Major"
                ],

                preferred_modes=[
                    "Aeolian",
                    "Ionian"
                ],

                preferred_time_signatures=[
                    "4/4"
                ],

                chord_complexity=0.55,

                modulation_probability=0.15,

                melody_activity=0.75,

                bass_activity=0.85,

                drum_activity=0.75,

                guitar_activity=0.15,

                keyboard_activity=1.00,

                orchestral_activity=0.15,

                fx_activity=0.70,

                moods=[
                    "Retro",
                    "Night",
                    "Dreamy"
                ],

                tags=[
                    "80s",
                    "analog",
                    "neon"
                ]

            )

        )

        self.add(

            Genre(

                name="EDM",

                bpm_min=120,

                bpm_max=150,

                swing=0.00,

                complexity=0.65,

                density=0.90,

                humanization=0.05,

                preferred_scales=[
                    "Minor",
                    "Major"
                ],

                preferred_modes=[
                    "Aeolian",
                    "Ionian"
                ],

                preferred_time_signatures=[
                    "4/4"
                ],

                chord_complexity=0.45,

                modulation_probability=0.08,

                melody_activity=0.90,

                bass_activity=1.00,

                drum_activity=1.00,

                guitar_activity=0.00,

                keyboard_activity=0.90,

                orchestral_activity=0.05,

                fx_activity=1.00,

                moods=[
                    "Energetic",
                    "Happy",
                    "Festival"
                ],

                tags=[
                    "drop",
                    "festival",
                    "dance"
                ]

            )

        )
        
                self.add(

            Genre(

                name="LoFi",

                bpm_min=60,

                bpm_max=95,

                swing=0.12,

                complexity=0.45,

                density=0.45,

                humanization=0.25,

                preferred_scales=[
                    "Minor",
                    "Major",
                    "Dorian"
                ],

                preferred_modes=[
                    "Dorian",
                    "Aeolian"
                ],

                preferred_time_signatures=[
                    "4/4"
                ],

                chord_complexity=0.75,

                modulation_probability=0.10,

                melody_activity=0.35,

                bass_activity=0.50,

                drum_activity=0.40,

                guitar_activity=0.20,

                keyboard_activity=0.90,

                orchestral_activity=0.05,

                fx_activity=0.70,

                moods=[
                    "Chill",
                    "Warm",
                    "Nostalgic"
                ],

                tags=[
                    "study",
                    "vinyl",
                    "relaxed"
                ]

            )

        )

        self.add(

            Genre(

                name="Jazz",

                bpm_min=70,

                bpm_max=180,

                swing=0.35,

                complexity=0.95,

                density=0.75,

                humanization=0.30,

                preferred_scales=[
                    "Major",
                    "Minor",
                    "Dorian",
                    "Mixolydian"
                ],

                preferred_modes=[
                    "Dorian",
                    "Mixolydian",
                    "Ionian"
                ],

                preferred_time_signatures=[
                    "4/4",
                    "3/4",
                    "5/4"
                ],

                chord_complexity=1.00,

                modulation_probability=0.75,

                melody_activity=0.95,

                bass_activity=0.80,

                drum_activity=0.70,

                guitar_activity=0.45,

                keyboard_activity=0.95,

                orchestral_activity=0.05,

                fx_activity=0.05,

                moods=[
                    "Sophisticated",
                    "Warm",
                    "Improvised"
                ],

                tags=[
                    "swing",
                    "bebop",
                    "fusion"
                ]

            )

        )

        self.add(

            Genre(

                name="Blues",

                bpm_min=60,

                bpm_max=140,

                swing=0.25,

                complexity=0.60,

                density=0.65,

                humanization=0.20,

                preferred_scales=[
                    "Minor Pentatonic",
                    "Major Pentatonic",
                    "Blues"
                ],

                preferred_modes=[
                    "Mixolydian"
                ],

                preferred_time_signatures=[
                    "4/4",
                    "12/8"
                ],

                chord_complexity=0.55,

                modulation_probability=0.08,

                melody_activity=0.75,

                bass_activity=0.70,

                drum_activity=0.65,

                guitar_activity=1.00,

                keyboard_activity=0.55,

                orchestral_activity=0.00,

                fx_activity=0.05,

                moods=[
                    "Soulful",
                    "Emotional",
                    "Raw"
                ],

                tags=[
                    "guitar",
                    "groove",
                    "shuffle"
                ]

            )

        )

        self.add(

            Genre(

                name="Funk",

                bpm_min=80,

                bpm_max=130,

                swing=0.18,

                complexity=0.75,

                density=0.85,

                humanization=0.20,

                preferred_scales=[
                    "Minor Pentatonic",
                    "Dorian"
                ],

                preferred_modes=[
                    "Dorian",
                    "Mixolydian"
                ],

                preferred_time_signatures=[
                    "4/4"
                ],

                chord_complexity=0.65,

                modulation_probability=0.15,

                melody_activity=0.70,

                bass_activity=1.00,

                drum_activity=0.95,

                guitar_activity=0.90,

                keyboard_activity=0.55,

                orchestral_activity=0.00,

                fx_activity=0.10,

                moods=[
                    "Groovy",
                    "Energetic",
                    "Playful"
                ],

                tags=[
                    "groove",
                    "bass",
                    "rhythm"
                ]

            )

        )
        
                self.add(

            Genre(

                name="Pop",

                bpm_min=90,

                bpm_max=130,

                swing=0.03,

                complexity=0.45,

                density=0.80,

                humanization=0.08,

                preferred_scales=[
                    "Major",
                    "Minor"
                ],

                preferred_modes=[
                    "Ionian",
                    "Aeolian"
                ],

                preferred_time_signatures=[
                    "4/4"
                ],

                chord_complexity=0.40,

                modulation_probability=0.08,

                melody_activity=0.95,

                bass_activity=0.70,

                drum_activity=0.80,

                guitar_activity=0.45,

                keyboard_activity=0.70,

                orchestral_activity=0.10,

                fx_activity=0.35,

                moods=[
                    "Happy",
                    "Romantic",
                    "Bright"
                ],

                tags=[
                    "radio",
                    "commercial",
                    "hook"
                ]

            )

        )

        self.add(

            Genre(

                name="Hip-Hop",

                bpm_min=65,

                bpm_max=105,

                swing=0.20,

                complexity=0.55,

                density=0.75,

                humanization=0.15,

                preferred_scales=[
                    "Minor",
                    "Phrygian",
                    "Minor Pentatonic"
                ],

                preferred_modes=[
                    "Aeolian",
                    "Phrygian"
                ],

                preferred_time_signatures=[
                    "4/4"
                ],

                chord_complexity=0.30,

                modulation_probability=0.05,

                melody_activity=0.35,

                bass_activity=0.95,

                drum_activity=1.00,

                guitar_activity=0.10,

                keyboard_activity=0.40,

                orchestral_activity=0.05,

                fx_activity=0.55,

                moods=[
                    "Dark",
                    "Aggressive",
                    "Confident"
                ],

                tags=[
                    "808",
                    "groove",
                    "beat"
                ]

            )

        )

        self.add(

            Genre(

                name="Trap",

                bpm_min=120,

                bpm_max=170,

                swing=0.10,

                complexity=0.55,

                density=0.90,

                humanization=0.06,

                preferred_scales=[
                    "Minor",
                    "Phrygian",
                    "Harmonic Minor"
                ],

                preferred_modes=[
                    "Aeolian",
                    "Phrygian"
                ],

                preferred_time_signatures=[
                    "4/4"
                ],

                chord_complexity=0.25,

                modulation_probability=0.03,

                melody_activity=0.45,

                bass_activity=1.00,

                drum_activity=1.00,

                guitar_activity=0.00,

                keyboard_activity=0.45,

                orchestral_activity=0.00,

                fx_activity=0.85,

                moods=[
                    "Dark",
                    "Cold",
                    "Massive"
                ],

                tags=[
                    "808",
                    "hihat",
                    "modern"
                ]

            )

        )

        self.add(

            Genre(

                name="Classical",

                bpm_min=50,

                bpm_max=180,

                swing=0.00,

                complexity=1.00,

                density=0.80,

                humanization=0.30,

                preferred_scales=[
                    "Major",
                    "Minor",
                    "Harmonic Minor"
                ],

                preferred_modes=[
                    "Ionian",
                    "Aeolian",
                    "Dorian"
                ],

                preferred_time_signatures=[
                    "4/4",
                    "3/4",
                    "6/8"
                ],

                chord_complexity=1.00,

                modulation_probability=0.80,

                melody_activity=0.90,

                bass_activity=0.70,

                drum_activity=0.00,

                guitar_activity=0.00,

                keyboard_activity=0.70,

                orchestral_activity=1.00,

                fx_activity=0.00,

                moods=[
                    "Elegant",
                    "Epic",
                    "Dramatic"
                ],

                tags=[
                    "orchestra",
                    "symphony",
                    "counterpoint"
                ]

            )

        )
        
                self.add(

            Genre(

                name="Progressive Rock",

                bpm_min=70,

                bpm_max=170,

                swing=0.05,

                complexity=0.95,

                density=0.80,

                humanization=0.15,

                preferred_scales=[
                    "Major",
                    "Minor",
                    "Dorian",
                    "Lydian",
                    "Mixolydian"
                ],

                preferred_modes=[
                    "Lydian",
                    "Dorian",
                    "Mixolydian"
                ],

                preferred_time_signatures=[
                    "4/4",
                    "5/4",
                    "7/8",
                    "9/8"
                ],

                chord_complexity=0.95,

                modulation_probability=0.65,

                melody_activity=0.90,

                bass_activity=0.85,

                drum_activity=0.95,

                guitar_activity=0.95,

                keyboard_activity=0.85,

                orchestral_activity=0.25,

                fx_activity=0.35,

                moods=[
                    "Epic",
                    "Technical",
                    "Dynamic"
                ],

                tags=[
                    "odd-meter",
                    "fusion",
                    "progressive"
                ]

            )

        )

        self.add(

            Genre(

                name="Djent",

                bpm_min=90,

                bpm_max=180,

                swing=0.00,

                complexity=0.95,

                density=0.95,

                humanization=0.08,

                preferred_scales=[
                    "Phrygian",
                    "Minor",
                    "Harmonic Minor"
                ],

                preferred_modes=[
                    "Phrygian",
                    "Locrian"
                ],

                preferred_time_signatures=[
                    "4/4",
                    "7/8",
                    "5/4"
                ],

                chord_complexity=0.80,

                modulation_probability=0.25,

                melody_activity=0.65,

                bass_activity=1.00,

                drum_activity=1.00,

                guitar_activity=1.00,

                keyboard_activity=0.30,

                orchestral_activity=0.05,

                fx_activity=0.35,

                moods=[
                    "Aggressive",
                    "Mechanical",
                    "Massive"
                ],

                tags=[
                    "polyrhythm",
                    "8-string",
                    "modern-metal"
                ]

            )

        )

        self.add(

            Genre(

                name="Progressive Death Metal",

                bpm_min=100,

                bpm_max=220,

                swing=0.00,

                complexity=1.00,

                density=1.00,

                humanization=0.08,

                preferred_scales=[
                    "Phrygian",
                    "Harmonic Minor",
                    "Locrian"
                ],

                preferred_modes=[
                    "Phrygian",
                    "Locrian"
                ],

                preferred_time_signatures=[
                    "4/4",
                    "7/8",
                    "9/8"
                ],

                chord_complexity=0.95,

                modulation_probability=0.45,

                melody_activity=0.70,

                bass_activity=1.00,

                drum_activity=1.00,

                guitar_activity=1.00,

                keyboard_activity=0.25,

                orchestral_activity=0.10,

                fx_activity=0.30,

                moods=[
                    "Dark",
                    "Brutal",
                    "Technical"
                ],

                tags=[
                    "blastbeat",
                    "technical",
                    "extreme"
                ]

            )

        )
        
            # --------------------------------------------------
    # CORE OPERATIONS
    # --------------------------------------------------

    def add(
        self,
        genre: Genre
    ):

        self.library[
            genre.name
        ] = copy.deepcopy(
            genre
        )

    def get(
        self,
        name: str
    ) -> Genre:

        if name not in self.library:

            raise KeyError(
                f"Genre '{name}' not found."
            )

        return copy.deepcopy(
            self.library[name]
        )

    def exists(
        self,
        name: str
    ) -> bool:

        return name in self.library

    def remove(
        self,
        name: str
    ):

        if name in self.library:

            del self.library[name]

    def clear(self):

        self.library.clear()

    # --------------------------------------------------
    # LISTS
    # --------------------------------------------------

    def names(self):

        return sorted(
            self.library.keys()
        )

    def all(self):

        return [

            copy.deepcopy(g)

            for g

            in self.library.values()

        ]

    def count(self):

        return len(
            self.library
        )

    # --------------------------------------------------
    # RANDOM
    # --------------------------------------------------

    def random_genre(self):

        import random

        return self.get(

            random.choice(

                self.names()

            )

        )

    # --------------------------------------------------
    # FILTERING
    # --------------------------------------------------

    def by_tag(
        self,
        tag: str
    ):

        result = []

        for genre in self.library.values():

            if tag in genre.tags:

                result.append(

                    copy.deepcopy(
                        genre
                    )

                )

        return result

    def by_mood(
        self,
        mood: str
    ):

        result = []

        mood = mood.lower()

        for genre in self.library.values():

            values = [

                m.lower()

                for m

                in genre.moods

            ]

            if mood in values:

                result.append(

                    copy.deepcopy(
                        genre
                    )

                )

        return result

    # --------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------

    def recommend_for_mood(
        self,
        mood: str
    ):

        genres = self.by_mood(
            mood
        )

        if genres:

            return genres

        return self.all()

    def recommend_for_bpm(
        self,
        bpm: int
    ):

        result = []

        for genre in self.library.values():

            if (

                genre.bpm_min

                <= bpm

                <= genre.bpm_max

            ):

                result.append(

                    copy.deepcopy(
                        genre
                    )

                )

        return result

    # --------------------------------------------------
    # SIMILAR GENRES
    # --------------------------------------------------

    def similar_genres(
        self,
        name: str
    ):

        genre = self.get(
            name
        )

        result = []

        for other in self.library.values():

            if other.name == genre.name:

                continue

            score = 0

            score += len(

                set(

                    genre.preferred_scales

                )

                &

                set(

                    other.preferred_scales

                )

            )

            score += len(

                set(
                    genre.tags
                )

                &

                set(
                    other.tags
                )

            )

            if abs(

                genre.complexity

                -

                other.complexity

            ) < 0.15:

                score += 2

            if abs(

                genre.density

                -

                other.density

            ) < 0.15:

                score += 2

            result.append(

                (

                    score,

                    other.name

                )

            )

        result.sort(

            reverse=True

        )

        return [

            name

            for _, name

            in result[:5]

        ]

    # --------------------------------------------------
    # SERIALIZATION
    # --------------------------------------------------

    def to_dict(self):

        result = {}

        for name, genre in self.library.items():

            result[name] = copy.deepcopy(

                genre.__dict__

            )

        return result

    def from_dict(
        self,
        data
    ):

        self.library.clear()

        for values in data.values():

            self.add(

                Genre(

                    **copy.deepcopy(
                        values
                    )

                )

            )

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    def summary(self):

        return {

            "genres": self.count(),

            "names": self.names()

        }

    # --------------------------------------------------
    # RESET
    # --------------------------------------------------

    def reset(self):

        self.library.clear()

        self._build_library()