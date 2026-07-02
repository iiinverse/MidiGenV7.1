from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import random
import copy


# --------------------------------------------------
# CONSTANTS
# --------------------------------------------------

MIN_PARAMETER = 0.0
MAX_PARAMETER = 1.0

DEFAULT_MOOD = "Neutral"

DEFAULT_TRANSITION_BARS = 8


# --------------------------------------------------
# MOOD MODEL
# --------------------------------------------------

@dataclass(slots=True)
class Mood:

    name: str

    energy: float

    valence: float

    tension: float

    darkness: float

    rhythmic_activity: float

    harmonic_density: float

    melodic_activity: float

    dynamic_range: float

    articulation: str

    velocity_bias: int

    preferred_modes: List[str]

    preferred_intervals: List[int]

    syncopation: float = 0.50

    chromaticism: float = 0.20

    ornamentation: float = 0.30

    arpeggio_usage: float = 0.40

    counterpoint: float = 0.25

    modulation_probability: float = 0.10

    rhythmic_complexity: float = 0.50

    melodic_complexity: float = 0.50

    harmonic_complexity: float = 0.50

    bass_activity: float = 0.50

    drum_activity: float = 0.50

    guitar_activity: float = 0.50

    keyboard_activity: float = 0.50

    pad_activity: float = 0.40

    string_activity: float = 0.40

    brass_activity: float = 0.30

    choir_activity: float = 0.20

    lead_activity: float = 0.60

    humanize_timing: float = 0.05

    humanize_velocity: float = 0.05

    humanize_length: float = 0.02

    pause_probability: float = 0.10

    accent_probability: float = 0.35

    octave_jump_probability: float = 0.20

    metadata: Dict = field(
        default_factory=dict
    )

    def clone(self):

        return copy.deepcopy(self)


# --------------------------------------------------
# TRACK MOOD
# --------------------------------------------------

@dataclass(slots=True)
class TrackMood:

    role: str

    mood: Mood

    weight: float = 1.0

    override_energy: Optional[float] = None

    override_density: Optional[float] = None

    override_complexity: Optional[float] = None

    override_velocity: Optional[int] = None

    metadata: Dict = field(
        default_factory=dict
    )

    def clone(self):

        return copy.deepcopy(self)


# --------------------------------------------------
# SECTION MOOD
# --------------------------------------------------

@dataclass(slots=True)
class SectionMood:

    section: str

    mood_name: str

    intensity: float = 1.0

    bars: int = 8

    transition_in: int = 2

    transition_out: int = 2

    metadata: Dict = field(
        default_factory=dict
    )


# --------------------------------------------------
# MOOD TRANSITION
# --------------------------------------------------

@dataclass(slots=True)
class MoodTransition:

    from_mood: str

    to_mood: str

    bars: int = DEFAULT_TRANSITION_BARS

    curve: str = "linear"

    metadata: Dict = field(
        default_factory=dict
    )


# --------------------------------------------------
# MOOD PROFILE
# --------------------------------------------------

@dataclass(slots=True)
class MoodProfile:

    main_mood: str = DEFAULT_MOOD

    secondary_mood: Optional[str] = None

    intensity: float = 1.0

    variation: float = 0.20

    evolution: float = 0.50

    randomness: float = 0.10

    genre_bias: float = 0.50

    emotional_depth: float = 0.60

    cinematic_factor: float = 0.30

    aggression: float = 0.50

    warmth: float = 0.50

    brightness: float = 0.50

    darkness: float = 0.50

    metadata: Dict = field(
        default_factory=dict
    )
    # --------------------------------------------------
# MOOD BLENDER
# --------------------------------------------------

class MoodBlender:

    @staticmethod
    def blend(
        first: Mood,
        second: Mood,
        ratio: float = 0.5
    ) -> Mood:

        ratio = max(0.0, min(1.0, ratio))
        inv = 1.0 - ratio

        def lerp(a, b):
            return a * inv + b * ratio

        return Mood(

            name=f"{first.name}_{second.name}",

            energy=lerp(first.energy, second.energy),

            valence=lerp(first.valence, second.valence),

            tension=lerp(first.tension, second.tension),

            darkness=lerp(first.darkness, second.darkness),

            rhythmic_activity=lerp(
                first.rhythmic_activity,
                second.rhythmic_activity
            ),

            harmonic_density=lerp(
                first.harmonic_density,
                second.harmonic_density
            ),

            melodic_activity=lerp(
                first.melodic_activity,
                second.melodic_activity
            ),

            dynamic_range=lerp(
                first.dynamic_range,
                second.dynamic_range
            ),

            articulation=second.articulation,

            velocity_bias=int(
                lerp(
                    first.velocity_bias,
                    second.velocity_bias
                )
            ),

            preferred_modes=list(
                dict.fromkeys(
                    first.preferred_modes +
                    second.preferred_modes
                )
            ),

            preferred_intervals=list(
                dict.fromkeys(
                    first.preferred_intervals +
                    second.preferred_intervals
                )
            ),

            syncopation=lerp(
                first.syncopation,
                second.syncopation
            ),

            chromaticism=lerp(
                first.chromaticism,
                second.chromaticism
            ),

            ornamentation=lerp(
                first.ornamentation,
                second.ornamentation
            ),

            arpeggio_usage=lerp(
                first.arpeggio_usage,
                second.arpeggio_usage
            ),

            counterpoint=lerp(
                first.counterpoint,
                second.counterpoint
            ),

            modulation_probability=lerp(
                first.modulation_probability,
                second.modulation_probability
            ),

            rhythmic_complexity=lerp(
                first.rhythmic_complexity,
                second.rhythmic_complexity
            ),

            melodic_complexity=lerp(
                first.melodic_complexity,
                second.melodic_complexity
            ),

            harmonic_complexity=lerp(
                first.harmonic_complexity,
                second.harmonic_complexity
            ),

            bass_activity=lerp(
                first.bass_activity,
                second.bass_activity
            ),

            drum_activity=lerp(
                first.drum_activity,
                second.drum_activity
            ),

            guitar_activity=lerp(
                first.guitar_activity,
                second.guitar_activity
            ),

            keyboard_activity=lerp(
                first.keyboard_activity,
                second.keyboard_activity
            ),

            pad_activity=lerp(
                first.pad_activity,
                second.pad_activity
            ),

            string_activity=lerp(
                first.string_activity,
                second.string_activity
            ),

            brass_activity=lerp(
                first.brass_activity,
                second.brass_activity
            ),

            choir_activity=lerp(
                first.choir_activity,
                second.choir_activity
            ),

            lead_activity=lerp(
                first.lead_activity,
                second.lead_activity
            ),

            humanize_timing=lerp(
                first.humanize_timing,
                second.humanize_timing
            ),

            humanize_velocity=lerp(
                first.humanize_velocity,
                second.humanize_velocity
            ),

            humanize_length=lerp(
                first.humanize_length,
                second.humanize_length
            ),

            pause_probability=lerp(
                first.pause_probability,
                second.pause_probability
            ),

            accent_probability=lerp(
                first.accent_probability,
                second.accent_probability
            ),

            octave_jump_probability=lerp(
                first.octave_jump_probability,
                second.octave_jump_probability
            )
        )

    @staticmethod
    def blend_many(
        moods: List[Mood]
    ) -> Mood:

        if not moods:
            raise ValueError("No moods supplied.")

        result = moods[0].clone()

        for mood in moods[1:]:

            result = MoodBlender.blend(
                result,
                mood,
                0.5
            )

        return result


# --------------------------------------------------
# MOOD TIMELINE
# --------------------------------------------------

class MoodTimeline:

    def __init__(self):

        self.sections: List[SectionMood] = []

    def add_section(
        self,
        section: SectionMood
    ):

        self.sections.append(section)

    def clear(self):

        self.sections.clear()

    def total_bars(self):

        return sum(
            s.bars
            for s in self.sections
        )

    def section_at_bar(
        self,
        bar: int
    ) -> Optional[SectionMood]:

        cursor = 0

        for section in self.sections:

            cursor += section.bars

            if bar < cursor:

                return section

        return None

    def all_sections(self):

        return list(self.sections)
        
        # --------------------------------------------------
# MOOD ENGINE
# --------------------------------------------------

class MoodEngine:

    def __init__(self):

        self._moods: Dict[str, Mood] = {}

        self.timeline = MoodTimeline()

        self.profile = MoodProfile()

        self._build_default_library()

    # --------------------------------------------------
    # LIBRARY
    # --------------------------------------------------

    def register(
        self,
        mood: Mood
    ):

        self._moods[mood.name] = mood.clone()

    def unregister(
        self,
        name: str
    ):

        self._moods.pop(name, None)

    def exists(
        self,
        name: str
    ) -> bool:

        return name in self._moods

    def get(
        self,
        name: str
    ) -> Mood:

        if name not in self._moods:

            raise KeyError(
                f"Mood '{name}' not found."
            )

        return self._moods[name].clone()

    def names(self):

        return sorted(self._moods.keys())

    def count(self):

        return len(self._moods)

    def all(self):

        return [

            mood.clone()

            for mood

            in self._moods.values()

        ]

    # --------------------------------------------------
    # FILTERS
    # --------------------------------------------------

    def by_energy(

        self,

        minimum=0.0,

        maximum=1.0

    ):

        return [

            m.clone()

            for m

            in self._moods.values()

            if minimum <= m.energy <= maximum

        ]

    def by_darkness(

        self,

        minimum=0.0,

        maximum=1.0

    ):

        return [

            m.clone()

            for m

            in self._moods.values()

            if minimum <= m.darkness <= maximum

        ]

    def by_tension(

        self,

        minimum=0.0,

        maximum=1.0

    ):

        return [

            m.clone()

            for m

            in self._moods.values()

            if minimum <= m.tension <= maximum

        ]

    def by_valence(

        self,

        minimum=0.0,

        maximum=1.0

    ):

        return [

            m.clone()

            for m

            in self._moods.values()

            if minimum <= m.valence <= maximum

        ]

    # --------------------------------------------------
    # RANDOM
    # --------------------------------------------------

    def random(

        self

    ) -> Mood:

        return self.get(

            random.choice(

                self.names()

            )

        )

    def random_by_energy(

        self,

        minimum,

        maximum

    ):

        moods = self.by_energy(

            minimum,

            maximum

        )

        if not moods:

            return self.random()

        return random.choice(

            moods

        )

    # --------------------------------------------------
    # PROFILE
    # --------------------------------------------------

    def set_profile(

        self,

        profile: MoodProfile

    ):

        self.profile = copy.deepcopy(

            profile

        )

    def current_profile(

        self

    ):

        return copy.deepcopy(

            self.profile

        )

    # --------------------------------------------------
    # TIMELINE
    # --------------------------------------------------

    def clear_timeline(

        self

    ):

        self.timeline.clear()

    def add_section(

        self,

        section: SectionMood

    ):

        self.timeline.add_section(

            section

        )

    def mood_for_bar(

        self,

        bar: int

    ) -> Mood:

        section = self.timeline.section_at_bar(

            bar

        )

        if section is None:

            return self.get(

                self.profile.main_mood

            )

        return self.get(

            section.mood_name

        )

    # --------------------------------------------------
    # TRACK RESOLUTION
    # --------------------------------------------------

    def resolve_track_mood(

        self,

        role: str

    ) -> Mood:

        mood = self.get(

            self.profile.main_mood

        )

        result = mood.clone()

        if role == "Drums":

            result.drum_activity *= 1.15

            result.rhythmic_activity *= 1.10

        elif role == "Bass":

            result.bass_activity *= 1.15

        elif "Guitar" in role:

            result.guitar_activity *= 1.20

        elif role == "Pad":

            result.pad_activity *= 1.25

        elif role == "Strings":

            result.string_activity *= 1.20

        elif role == "Brass":

            result.brass_activity *= 1.20

        elif role == "Choir":

            result.choir_activity *= 1.20

        elif role == "Lead Synth":

            result.lead_activity *= 1.20

        return result

    # --------------------------------------------------
    # GENERATION PROFILE
    # --------------------------------------------------

    def generation_profile(

        self,

        mood: Mood

    ):

        return {

            "energy": mood.energy,

            "tension": mood.tension,

            "darkness": mood.darkness,

            "density": mood.harmonic_density,

            "rhythm": mood.rhythmic_activity,

            "melody": mood.melodic_activity,

            "velocity_bias": mood.velocity_bias,

            "syncopation": mood.syncopation,

            "chromaticism": mood.chromaticism,

            "counterpoint": mood.counterpoint,

            "arpeggio": mood.arpeggio_usage,

            "pause_probability": mood.pause_probability,

            "accent_probability": mood.accent_probability,

            "humanize_velocity": mood.humanize_velocity,

            "humanize_timing": mood.humanize_timing,

            "humanize_length": mood.humanize_length,

            "rhythmic_complexity": mood.rhythmic_complexity,

            "melodic_complexity": mood.melodic_complexity,

            "harmonic_complexity": mood.harmonic_complexity

        }

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    def summary(

        self

    ):

        return {

            "registered_moods": self.count(),

            "main_mood": self.profile.main_mood,

            "timeline_sections": len(

                self.timeline.sections

            )

        }
        
        