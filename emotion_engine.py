from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from typing import Dict
from typing import List
from typing import Tuple
from typing import Optional
from typing import Iterable

import random


# --------------------------------------------------
# EMOTION PROFILE
# --------------------------------------------------

@dataclass(slots=True)
class EmotionProfile:

    name: str

    harmonic_tension: float

    rhythmic_density: float

    melodic_activity: float

    velocity_bias: int

    octave_bias: int

    chord_complexity: float

    dissonance: float

    cadence_strength: float

    modulation_probability: float

    ornament_probability: float

    sustain_factor: float

    swing_amount: float

    humanization: float


# --------------------------------------------------
# EMOTION BLEND
# --------------------------------------------------

@dataclass(slots=True)
class EmotionBlend:

    emotions: Dict[str, float] = field(
        default_factory=dict
    )

    normalize: bool = True

    evolution: bool = False

    seed: Optional[int] = None

    def total_weight(self):

        return sum(
            self.emotions.values()
        )

    def normalized(self):

        if not self.normalize:

            return dict(
                self.emotions
            )

        total = self.total_weight()

        if total <= 0:

            return {}

        return {

            emotion:

            weight / total

            for emotion, weight

            in self.emotions.items()

        }


# --------------------------------------------------
# EMOTION ENGINE
# --------------------------------------------------

class EmotionEngine:

    DEFAULT_PROFILES = {

        "happy": EmotionProfile(

            "happy",

            harmonic_tension=0.25,

            rhythmic_density=0.85,

            melodic_activity=0.90,

            velocity_bias=10,

            octave_bias=1,

            chord_complexity=0.55,

            dissonance=0.15,

            cadence_strength=0.90,

            modulation_probability=0.10,

            ornament_probability=0.70,

            sustain_factor=0.45,

            swing_amount=0.08,

            humanization=0.30

        ),

        "sad": EmotionProfile(

            "sad",

            harmonic_tension=0.45,

            rhythmic_density=0.40,

            melodic_activity=0.50,

            velocity_bias=-10,

            octave_bias=-1,

            chord_complexity=0.70,

            dissonance=0.35,

            cadence_strength=0.70,

            modulation_probability=0.25,

            ornament_probability=0.20,

            sustain_factor=0.85,

            swing_amount=0.02,

            humanization=0.20

        ),

        "dark": EmotionProfile(

            "dark",

            harmonic_tension=0.90,

            rhythmic_density=0.60,

            melodic_activity=0.40,

            velocity_bias=5,

            octave_bias=-1,

            chord_complexity=0.90,

            dissonance=0.75,

            cadence_strength=0.55,

            modulation_probability=0.55,

            ornament_probability=0.15,

            sustain_factor=0.90,

            swing_amount=0.01,

            humanization=0.15

        ),

        "hopeful": EmotionProfile(

            "hopeful",

            harmonic_tension=0.40,

            rhythmic_density=0.65,

            melodic_activity=0.80,

            velocity_bias=5,

            octave_bias=1,

            chord_complexity=0.65,

            dissonance=0.20,

            cadence_strength=0.85,

            modulation_probability=0.15,

            ornament_probability=0.55,

            sustain_factor=0.60,

            swing_amount=0.03,

            humanization=0.25

        ),

        "cinematic": EmotionProfile(

            "cinematic",

            harmonic_tension=0.75,

            rhythmic_density=0.55,

            melodic_activity=0.65,

            velocity_bias=8,

            octave_bias=1,

            chord_complexity=0.95,

            dissonance=0.45,

            cadence_strength=0.80,

            modulation_probability=0.45,

            ornament_probability=0.35,

            sustain_factor=0.95,

            swing_amount=0.00,

            humanization=0.20

        ),

        "epic": EmotionProfile(

            "epic",

            harmonic_tension=0.85,

            rhythmic_density=0.90,

            melodic_activity=0.80,

            velocity_bias=18,

            octave_bias=2,

            chord_complexity=0.80,

            dissonance=0.30,

            cadence_strength=1.00,

            modulation_probability=0.35,

            ornament_probability=0.30,

            sustain_factor=0.70,

            swing_amount=0.00,

            humanization=0.15

        ),

        "ambient": EmotionProfile(

            "ambient",

            harmonic_tension=0.30,

            rhythmic_density=0.20,

            melodic_activity=0.25,

            velocity_bias=-15,

            octave_bias=0,

            chord_complexity=1.00,

            dissonance=0.25,

            cadence_strength=0.35,

            modulation_probability=0.50,

            ornament_probability=0.10,

            sustain_factor=1.00,

            swing_amount=0.00,

            humanization=0.35

        )

    }

    def __init__(self):

        self.profiles = dict(
            self.DEFAULT_PROFILES
        )

        self.last_blend = None

        self.history = []
            # --------------------------------------------------
    # PROFILE MANAGEMENT
    # --------------------------------------------------

    def register_profile(
        self,
        profile: EmotionProfile
    ):

        self.profiles[
            profile.name
        ] = profile

    def unregister_profile(
        self,
        name: str
    ):

        if name in self.profiles:

            del self.profiles[
                name
            ]

    def profile(
        self,
        name: str
    ) -> EmotionProfile:

        return self.profiles[
            name
        ]

    def available_profiles(
        self
    ) -> List[str]:

        return sorted(
            self.profiles.keys()
        )

    # --------------------------------------------------
    # BLENDING
    # --------------------------------------------------

    def create_blend(
        self,
        **weights
    ) -> EmotionBlend:

        blend = EmotionBlend(
            emotions=weights
        )

        self.last_blend = blend

        return blend

    def normalize(
        self,
        blend: EmotionBlend
    ) -> Dict[str, float]:

        return blend.normalized()

    # --------------------------------------------------
    # INTERNAL
    # --------------------------------------------------

    def _weighted(
        self,
        blend: EmotionBlend,
        attribute: str
    ):

        weights = blend.normalized()

        value = 0.0

        for emotion, weight in weights.items():

            profile = self.profiles[
                emotion
            ]

            value += (

                getattr(
                    profile,
                    attribute
                )

                * weight

            )

        return value

    # --------------------------------------------------
    # PUBLIC PARAMETERS
    # --------------------------------------------------

    def harmonic_tension(
        self,
        blend: EmotionBlend
    ):

        return self._weighted(

            blend,

            "harmonic_tension"

        )

    def rhythmic_density(
        self,
        blend: EmotionBlend
    ):

        return self._weighted(

            blend,

            "rhythmic_density"

        )

    def melodic_activity(
        self,
        blend: EmotionBlend
    ):

        return self._weighted(

            blend,

            "melodic_activity"

        )

    def chord_complexity(
        self,
        blend: EmotionBlend
    ):

        return self._weighted(

            blend,

            "chord_complexity"

        )

    def dissonance(
        self,
        blend: EmotionBlend
    ):

        return self._weighted(

            blend,

            "dissonance"

        )

    def cadence_strength(
        self,
        blend: EmotionBlend
    ):

        return self._weighted(

            blend,

            "cadence_strength"

        )

    def sustain_factor(
        self,
        blend: EmotionBlend
    ):

        return self._weighted(

            blend,

            "sustain_factor"

        )

    def ornament_probability(
        self,
        blend: EmotionBlend
    ):

        return self._weighted(

            blend,

            "ornament_probability"

        )

    def modulation_probability(
        self,
        blend: EmotionBlend
    ):

        return self._weighted(

            blend,

            "modulation_probability"

        )

    def swing_amount(
        self,
        blend: EmotionBlend
    ):

        return self._weighted(

            blend,

            "swing_amount"

        )

    def humanization(
        self,
        blend: EmotionBlend
    ):

        return self._weighted(

            blend,

            "humanization"

        )

    # --------------------------------------------------
    # INTEGER PARAMETERS
    # --------------------------------------------------

    def velocity_bias(
        self,
        blend: EmotionBlend
    ):

        weights = blend.normalized()

        value = 0.0

        for emotion, weight in weights.items():

            value += (

                self.profiles[
                    emotion
                ].velocity_bias

                * weight

            )

        return round(
            value
        )

    def octave_bias(
        self,
        blend: EmotionBlend
    ):

        weights = blend.normalized()

        value = 0.0

        for emotion, weight in weights.items():

            value += (

                self.profiles[
                    emotion
                ].octave_bias

                * weight

            )

        return round(
            value
        )
            # --------------------------------------------------
    # EVOLUTION ENGINE
    # --------------------------------------------------

    def evolve(
        self,
        timeline: Iterable[Tuple[float, EmotionBlend]]
    ):

        timeline = sorted(
            timeline,
            key=lambda x: x[0]
        )

        self.timeline = list(
            timeline
        )

    def emotion_at(
        self,
        position: float
    ) -> EmotionBlend:

        if not hasattr(
            self,
            "timeline"
        ):

            return EmotionBlend()

        if not self.timeline:

            return EmotionBlend()

        current = self.timeline[0][1]

        for point, blend in self.timeline:

            if position >= point:

                current = blend

            else:

                break

        return current

    # --------------------------------------------------
    # SECTION SUPPORT
    # --------------------------------------------------

    def section_blend(
        self,
        section: str
    ):

        presets = {

            "intro":

                self.create_blend(
                    ambient=0.80,
                    hopeful=0.20
                ),

            "verse":

                self.create_blend(
                    cinematic=0.60,
                    hopeful=0.40
                ),

            "pre_chorus":

                self.create_blend(
                    cinematic=0.70,
                    epic=0.30
                ),

            "chorus":

                self.create_blend(
                    epic=0.60,
                    happy=0.20,
                    cinematic=0.20
                ),

            "bridge":

                self.create_blend(
                    dark=0.60,
                    cinematic=0.40
                ),

            "solo":

                self.create_blend(
                    epic=0.50,
                    cinematic=0.50
                ),

            "outro":

                self.create_blend(
                    ambient=0.70,
                    sad=0.30
                )

        }

        return presets.get(

            section.lower(),

            self.create_blend(
                cinematic=1.0
            )

        )

    # --------------------------------------------------
    # RANDOM BLENDS
    # --------------------------------------------------

    def random_blend(
        self,
        count: int = 3
    ):

        names = list(
            self.profiles.keys()
        )

        random.shuffle(
            names
        )

        names = names[:count]

        weights = {}

        remaining = 1.0

        for index, name in enumerate(names):

            if index == len(names) - 1:

                weights[name] = remaining

                break

            value = round(

                random.uniform(
                    0.10,
                    remaining
                ),

                2

            )

            weights[name] = value

            remaining -= value

        return self.create_blend(
            **weights
        )

    # --------------------------------------------------
    # PROJECT PROCESSING
    # --------------------------------------------------

    def process(
        self,
        project,
        settings=None
    ):

        metadata = project.setdefault(

            "metadata",

            {}

        )

        blend = metadata.get(

            "emotion_blend"

        )

        if blend is None:

            emotion = metadata.get(

                "emotion",

                "cinematic"

            )

            blend = self.create_blend(

                **{

                    emotion: 1.0

                }

            )

        elif isinstance(
            blend,
            dict
        ):

            blend = EmotionBlend(
                emotions=blend
            )

        metadata["emotion_profile"] = {

            "harmonic_tension":

                self.harmonic_tension(
                    blend
                ),

            "rhythmic_density":

                self.rhythmic_density(
                    blend
                ),

            "melodic_activity":

                self.melodic_activity(
                    blend
                ),

            "velocity_bias":

                self.velocity_bias(
                    blend
                ),

            "octave_bias":

                self.octave_bias(
                    blend
                ),

            "dissonance":

                self.dissonance(
                    blend
                ),

            "complexity":

                self.chord_complexity(
                    blend
                ),

            "cadence_strength":

                self.cadence_strength(
                    blend
                ),

            "modulation_probability":

                self.modulation_probability(
                    blend
                ),

            "ornament_probability":

                self.ornament_probability(
                    blend
                ),

            "sustain_factor":

                self.sustain_factor(
                    blend
                ),

            "humanization":

                self.humanization(
                    blend
                ),

            "swing":

                self.swing_amount(
                    blend
                )

        }

        self.history.append(

            metadata[
                "emotion_profile"
            ]

        )

        return project
            # --------------------------------------------------
    # ANALYSIS
    # --------------------------------------------------

    def analyse_blend(
        self,
        blend: EmotionBlend
    ):

        return {

            "weights":

                blend.normalized(),

            "harmonic_tension":

                self.harmonic_tension(
                    blend
                ),

            "rhythmic_density":

                self.rhythmic_density(
                    blend
                ),

            "melodic_activity":

                self.melodic_activity(
                    blend
                ),

            "velocity_bias":

                self.velocity_bias(
                    blend
                ),

            "octave_bias":

                self.octave_bias(
                    blend
                ),

            "complexity":

                self.chord_complexity(
                    blend
                ),

            "dissonance":

                self.dissonance(
                    blend
                ),

            "cadence_strength":

                self.cadence_strength(
                    blend
                ),

            "modulation":

                self.modulation_probability(
                    blend
                ),

            "ornaments":

                self.ornament_probability(
                    blend
                ),

            "sustain":

                self.sustain_factor(
                    blend
                ),

            "humanization":

                self.humanization(
                    blend
                ),

            "swing":

                self.swing_amount(
                    blend
                )

        }

    # --------------------------------------------------
    # BLEND COMPARISON
    # --------------------------------------------------

    def compare(
        self,
        first: EmotionBlend,
        second: EmotionBlend
    ):

        a = self.analyse_blend(
            first
        )

        b = self.analyse_blend(
            second
        )

        report = {}

        for key in a:

            if key == "weights":

                continue

            report[key] = (

                b[key] -

                a[key]

            )

        return report

    # --------------------------------------------------
    # HISTORY
    # --------------------------------------------------

    def last_profile(
        self
    ):

        if not self.history:

            return None

        return self.history[-1]

    def history_size(
        self
    ):

        return len(
            self.history
        )

    def clear_history(
        self
    ):

        self.history.clear()

    # --------------------------------------------------
    # PRESETS
    # --------------------------------------------------

    def cinematic_epic(
        self
    ):

        return self.create_blend(

            cinematic=0.60,

            epic=0.40

        )

    def dark_cinematic(
        self
    ):

        return self.create_blend(

            dark=0.55,

            cinematic=0.45

        )

    def hopeful_epic(
        self
    ):

        return self.create_blend(

            hopeful=0.50,

            epic=0.50

        )

    def ambient_dark(
        self
    ):

        return self.create_blend(

            ambient=0.65,

            dark=0.35

        )

    def emotional_piano(
        self
    ):

        return self.create_blend(

            sad=0.45,

            hopeful=0.35,

            cinematic=0.20

        )

    def trailer(
        self
    ):

        return self.create_blend(

            epic=0.45,

            cinematic=0.35,

            dark=0.20

        )

    # --------------------------------------------------
    # SERIALIZATION
    # --------------------------------------------------

    def to_dict(
        self,
        blend: EmotionBlend
    ):

        return {

            "emotions":

                dict(
                    blend.emotions
                ),

            "normalize":

                blend.normalize,

            "evolution":

                blend.evolution,

            "seed":

                blend.seed

        }

    def from_dict(
        self,
        data
    ):

        return EmotionBlend(

            emotions=data.get(
                "emotions",
                {}
            ),

            normalize=data.get(
                "normalize",
                True
            ),

            evolution=data.get(
                "evolution",
                False
            ),

            seed=data.get(
                "seed"
            )

        )

    # --------------------------------------------------
    # INFORMATION
    # --------------------------------------------------

    @staticmethod
    def version():

        return "MidiGenV7 Emotion Engine"

    def __len__(
        self
    ):

        return len(
            self.profiles
        )

    def __repr__(
        self
    ):

        return (

            f"<EmotionEngine "

            f"profiles={len(self.profiles)} "

            f"history={len(self.history)}>"

        )
            # --------------------------------------------------
    # ADAPTIVE EMOTION CURVE
    # --------------------------------------------------

    def build_emotion_curve(
        self,
        sections: Iterable[str]
    ):

        curve = []

        sections = list(
            sections
        )

        total = max(
            1,
            len(sections) - 1
        )

        for index, section in enumerate(
            sections
        ):

            position = index / total

            curve.append(

                (

                    position,

                    self.section_blend(
                        section
                    )

                )

            )

        self.timeline = curve

        return curve

    def interpolate(
        self,
        first: EmotionBlend,
        second: EmotionBlend,
        factor: float
    ) -> EmotionBlend:

        factor = max(
            0.0,
            min(
                1.0,
                factor
            )
        )

        emotions = set(

            first.emotions.keys()

        ) | set(

            second.emotions.keys()

        )

        values = {}

        for emotion in emotions:

            a = first.emotions.get(
                emotion,
                0.0
            )

            b = second.emotions.get(
                emotion,
                0.0
            )

            values[emotion] = (

                a +

                (b - a)

                * factor

            )

        return EmotionBlend(

            emotions=values,

            normalize=True

        )

    def interpolate_curve(
        self,
        position: float
    ):

        if not hasattr(
            self,
            "timeline"
        ):

            return EmotionBlend()

        if len(
            self.timeline
        ) < 2:

            return self.timeline[0][1]

        previous = self.timeline[0]

        for current in self.timeline[1:]:

            if position <= current[0]:

                local = (

                    position -

                    previous[0]

                ) / (

                    current[0] -

                    previous[0]

                )

                return self.interpolate(

                    previous[1],

                    current[1],

                    local

                )

            previous = current

        return self.timeline[-1][1]

    # --------------------------------------------------
    # PROJECT ENRICHMENT
    # --------------------------------------------------

    def enrich_metadata(
        self,
        metadata
    ):

        blend = metadata.get(
            "emotion_blend"
        )

        if isinstance(
            blend,
            EmotionBlend
        ):

            metadata[
                "emotion_analysis"
            ] = self.analyse_blend(
                blend
            )

        return metadata

    def enrich_project(
        self,
        project
    ):

        metadata = project.setdefault(
            "metadata",
            {}
        )

        self.enrich_metadata(
            metadata
        )

        return project

    # --------------------------------------------------
    # QUALITY ESTIMATION
    # --------------------------------------------------

    def emotional_energy(
        self,
        blend: EmotionBlend
    ):

        return (

            self.rhythmic_density(
                blend
            )

            +

            self.melodic_activity(
                blend
            )

            +

            self.harmonic_tension(
                blend
            )

        ) / 3.0

    def emotional_darkness(
        self,
        blend: EmotionBlend
    ):

        return (

            self.dissonance(
                blend
            )

            +

            (

                1.0 -

                self.cadence_strength(
                    blend
                )

            )

        ) / 2.0

    def emotional_warmth(
        self,
        blend: EmotionBlend
    ):

        return (

            self.sustain_factor(
                blend
            )

            +

            (

                1.0 -

                self.dissonance(
                    blend
                )

            )

        ) / 2.0

    def emotional_motion(
        self,
        blend: EmotionBlend
    ):

        return (

            self.melodic_activity(
                blend
            )

            *

            self.rhythmic_density(
                blend
            )

        )

    # --------------------------------------------------
    # PROFILE SEARCH
    # --------------------------------------------------

    def closest_profile(
        self,
        blend: EmotionBlend
    ):

        target = self.analyse_blend(
            blend
        )

        winner = None

        best_score = 10**9

        for name in self.available_profiles():

            profile = self.create_blend(

                **{

                    name: 1.0

                }

            )

            report = self.analyse_blend(
                profile
            )

            score = 0.0

            for key in report:

                if key == "weights":

                    continue

                score += abs(

                    report[key]

                    -

                    target[key]

                )

            if score < best_score:

                best_score = score

                winner = name

        return winner

    # --------------------------------------------------
    # ENGINE RESET
    # --------------------------------------------------

    def reset(
        self
    ):

        self.history.clear()

        self.last_blend = None

        if hasattr(
            self,
            "timeline"
        ):

            self.timeline.clear()

        return True

    # --------------------------------------------------
    # ENGINE STATUS
    # --------------------------------------------------

    def status(
        self
    ):

        return {

            "profiles":

                len(
                    self.profiles
                ),

            "history":

                len(
                    self.history
                ),

            "timeline":

                len(

                    getattr(

                        self,

                        "timeline",

                        []

                    )

                ),

            "last_blend":

                self.last_blend is not None,

            "version":

                self.version()

        }
            # --------------------------------------------------
    # ADVANCED EMOTION TRANSFORMATIONS
    # --------------------------------------------------

    def amplify(
        self,
        blend: EmotionBlend,
        factor: float = 1.25
    ) -> EmotionBlend:

        values = {}

        for emotion, weight in blend.emotions.items():

            values[emotion] = weight * factor

        return EmotionBlend(

            emotions=values,

            normalize=True

        )

    def soften(
        self,
        blend: EmotionBlend,
        factor: float = 0.75
    ) -> EmotionBlend:

        values = {}

        for emotion, weight in blend.emotions.items():

            values[emotion] = weight * factor

        return EmotionBlend(

            emotions=values,

            normalize=True

        )

    def invert(
        self,
        blend: EmotionBlend
    ):

        values = {}

        total = len(
            self.profiles
        )

        for name in self.available_profiles():

            values[name] = 1.0

        for emotion, weight in blend.normalized().items():

            values[emotion] = max(

                0.0,

                1.0 - weight

            )

        return EmotionBlend(

            emotions=values,

            normalize=True

        )

    def mutate(
        self,
        blend: EmotionBlend,
        amount: float = 0.15
    ):

        values = dict(
            blend.emotions
        )

        for emotion in values:

            values[emotion] += random.uniform(

                -amount,

                amount

            )

            values[emotion] = max(

                0.0,

                values[emotion]

            )

        return EmotionBlend(

            emotions=values,

            normalize=True

        )

    def crossover(
        self,
        first: EmotionBlend,
        second: EmotionBlend
    ):

        values = {}

        emotions = set(

            first.emotions

        ) | set(

            second.emotions

        )

        for emotion in emotions:

            if random.random() < 0.5:

                values[emotion] = first.emotions.get(

                    emotion,

                    0.0

                )

            else:

                values[emotion] = second.emotions.get(

                    emotion,

                    0.0

                )

        return EmotionBlend(

            emotions=values,

            normalize=True

        )

    # --------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------

    def recommend_scale(
        self,
        blend: EmotionBlend
    ):

        darkness = self.emotional_darkness(
            blend
        )

        tension = self.harmonic_tension(
            blend
        )

        if darkness > 0.75:

            return "harmonic_minor"

        if tension > 0.80:

            return "phrygian"

        if tension > 0.60:

            return "minor"

        if self.emotional_warmth(
            blend
        ) > 0.75:

            return "lydian"

        return "major"

    def recommend_bpm(
        self,
        blend: EmotionBlend
    ):

        energy = self.emotional_energy(
            blend
        )

        return int(

            55 +

            energy * 115

        )

    def recommend_velocity(
        self,
        blend: EmotionBlend
    ):

        return max(

            45,

            min(

                120,

                80 +

                self.velocity_bias(
                    blend
                )

            )

        )

    def recommend_register(
        self,
        blend: EmotionBlend
    ):

        octave = self.octave_bias(
            blend
        )

        if octave <= -1:

            return "low"

        if octave >= 1:

            return "high"

        return "middle"

    def recommend_density(
        self,
        blend: EmotionBlend
    ):

        value = self.rhythmic_density(
            blend
        )

        if value < 0.35:

            return "sparse"

        if value < 0.70:

            return "medium"

        return "dense"

    # --------------------------------------------------
    # COMPLETE REPORT
    # --------------------------------------------------

    def report(
        self,
        blend: EmotionBlend
    ):

        analysis = self.analyse_blend(
            blend
        )

        analysis.update({

            "energy":

                self.emotional_energy(
                    blend
                ),

            "warmth":

                self.emotional_warmth(
                    blend
                ),

            "darkness":

                self.emotional_darkness(
                    blend
                ),

            "motion":

                self.emotional_motion(
                    blend
                ),

            "recommended_scale":

                self.recommend_scale(
                    blend
                ),

            "recommended_bpm":

                self.recommend_bpm(
                    blend
                ),

            "recommended_velocity":

                self.recommend_velocity(
                    blend
                ),

            "recommended_register":

                self.recommend_register(
                    blend
                ),

            "recommended_density":

                self.recommend_density(
                    blend
                ),

            "closest_profile":

                self.closest_profile(
                    blend
                )

        })

        return analysis

    # --------------------------------------------------
    # DEFAULT BLENDS
    # --------------------------------------------------

    def default_blends(
        self
    ):

        return {

            "Adventure":

                self.create_blend(

                    epic=0.45,

                    hopeful=0.35,

                    cinematic=0.20

                ),

            "Dream":

                self.create_blend(

                    ambient=0.55,

                    cinematic=0.25,

                    hopeful=0.20

                ),

            "Horror":

                self.create_blend(

                    dark=0.70,

                    ambient=0.20,

                    cinematic=0.10

                ),

            "Drama":

                self.create_blend(

                    cinematic=0.45,

                    sad=0.35,

                    hopeful=0.20

                ),

            "Fantasy":

                self.create_blend(

                    cinematic=0.40,

                    hopeful=0.35,

                    ambient=0.25

                ),

            "Trailer":

                self.trailer()

        }
            # --------------------------------------------------
    # STYLE PRESETS
    # --------------------------------------------------

    def film_score(
        self
    ):

        return self.create_blend(

            cinematic=0.55,

            epic=0.20,

            ambient=0.15,

            hopeful=0.10

        )

    def piano_solo(
        self
    ):

        return self.create_blend(

            sad=0.35,

            hopeful=0.35,

            ambient=0.30

        )

    def emotional_orchestra(
        self
    ):

        return self.create_blend(

            cinematic=0.45,

            epic=0.30,

            hopeful=0.25

        )

    def mystery(
        self
    ):

        return self.create_blend(

            dark=0.50,

            ambient=0.30,

            cinematic=0.20

        )

    def victory(
        self
    ):

        return self.create_blend(

            epic=0.55,

            happy=0.30,

            hopeful=0.15

        )

    def melancholy(
        self
    ):

        return self.create_blend(

            sad=0.60,

            ambient=0.25,

            cinematic=0.15

        )

    # --------------------------------------------------
    # BATCH ANALYSIS
    # --------------------------------------------------

    def analyse_many(
        self,
        blends: Iterable[EmotionBlend]
    ):

        return [

            self.report(
                blend
            )

            for blend

            in blends

        ]

    def strongest(
        self,
        blends
    ):

        best = None

        score = -1.0

        for blend in blends:

            energy = self.emotional_energy(
                blend
            )

            if energy > score:

                score = energy

                best = blend

        return best

    def calmest(
        self,
        blends
    ):

        best = None

        score = 10**9

        for blend in blends:

            energy = self.emotional_energy(
                blend
            )

            if energy < score:

                score = energy

                best = blend

        return best

    # --------------------------------------------------
    # PIPELINE HELPERS
    # --------------------------------------------------

    def apply_to_settings(
        self,
        settings,
        blend: EmotionBlend
    ):

        settings.metadata = (

            settings.metadata

            or

            {}

        )

        settings.metadata[
            "emotion_blend"
        ] = blend

        settings.metadata[
            "emotion_report"
        ] = self.report(
            blend
        )

        return settings

    def apply_to_metadata(
        self,
        metadata,
        blend: EmotionBlend
    ):

        metadata[
            "emotion_blend"
        ] = blend

        metadata[
            "emotion_report"
        ] = self.report(
            blend
        )

        return metadata

    # --------------------------------------------------
    # IMPORT / EXPORT
    # --------------------------------------------------

    def export_blend(
        self,
        blend: EmotionBlend
    ):

        return dict(

            blend.normalized()

        )

    def import_blend(
        self,
        values
    ):

        return EmotionBlend(

            emotions=dict(
                values
            ),

            normalize=True

        )

    # --------------------------------------------------
    # UTILITIES
    # --------------------------------------------------

    def copy_blend(
        self,
        blend: EmotionBlend
    ):

        return EmotionBlend(

            emotions=dict(
                blend.emotions
            ),

            normalize=blend.normalize,

            evolution=blend.evolution,

            seed=blend.seed

        )

    def equal(
        self,
        first,
        second
    ):

        return (

            first.normalized()

            ==

            second.normalized()

        )

    def empty_blend(
        self
    ):

        return EmotionBlend()

    # --------------------------------------------------
    # FACTORY METHODS
    # --------------------------------------------------

    @classmethod
    def create_default(
        cls
    ):

        return cls()

    @classmethod
    def create_with_seed(
        cls,
        seed: int
    ):

        engine = cls()

        random.seed(
            seed
        )

        return engine

    # --------------------------------------------------
    # ENGINE CAPABILITIES
    # --------------------------------------------------

    def capabilities(
        self
    ):

        return {

            "multi_emotion": True,

            "weighted_blending": True,

            "timeline": True,

            "emotion_evolution": True,

            "adaptive_sections": True,

            "style_presets": True,

            "recommendations": True,

            "metadata_generation": True,

            "project_processing": True,

            "emotion_reports": True,

            "comparison": True,

            "mutation": True,

            "genetic_crossover": True,

            "serialization": True,

            "batch_analysis": True

        }

    # --------------------------------------------------
    # END OF ENGINE
    # --------------------------------------------------