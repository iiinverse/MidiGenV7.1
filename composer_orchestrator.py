# --------------------------------------------------
# COMPOSER ORCHESTRATOR
# --------------------------------------------------

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Optional
from typing import Any

from harmony_engine import HarmonyEngine
from cadence_engine import CadenceEngine
from tension_engine import TensionEngine
from voice_leading_v2 import VoiceLeadingEngine

from composer_core import ComposerCore

from structure_engine import StructureEngine
from expression_layer import ExpressionLayer
from time_layer import TimeLayer

from midi_renderer_v2 import MidiRendererV2


# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

@dataclass
class CompositionSettings:

    root: str = "C"

    scale: str = "major"

    emotion: str = "cinematic"

    bpm: int = 120

    bars: int = 32

    beats_per_bar: int = 4

    humanize: bool = True

    seed: Optional[int] = None

    metadata: Optional[Dict[str, Any]] = None


# --------------------------------------------------
# ORCHESTRATOR
# --------------------------------------------------

class ComposerOrchestrator:

    def __init__(self):

        self.harmony = HarmonyEngine()

        self.cadence = CadenceEngine()

        self.tension = TensionEngine()

        self.voice = VoiceLeadingEngine()

        self.core = ComposerCore(
            harmony_engine=self.harmony,
            cadence_engine=self.cadence,
            tension_engine=self.tension,
            voice_leading_engine=self.voice
        )

        self.structure = StructureEngine()

        self.expression = ExpressionLayer()

        self.time = TimeLayer()

        self.renderer = MidiRendererV2()

        self.last_result = None

    # --------------------------------------------------
    # BUILD STRUCTURE
    # --------------------------------------------------

    def build_structure(
        self,
        settings: CompositionSettings
    ):

        return self.structure.generate(
            bars=settings.bars,
            emotion=settings.emotion
        )

    # --------------------------------------------------
    # BUILD HARMONY
    # --------------------------------------------------

    def build_harmony(
        self,
        settings: CompositionSettings,
        structure
    ):

        return self.core.compose_progression(
            root=settings.root,
            scale=settings.scale,
            bars=settings.bars,
            emotion=settings.emotion
        )

    # --------------------------------------------------
    # VOICE LEADING
    # --------------------------------------------------

    def apply_voice_leading(
        self,
        progression
    ):

        return self.voice.optimize(
            progression
        )

    # --------------------------------------------------
    # EXPRESSION
    # --------------------------------------------------

    def apply_expression(
        self,
        voiced,
        settings
    ):

        if not settings.humanize:

            return voiced

        return self.expression.process(
            voiced
        )

    # --------------------------------------------------
    # TIMING
    # --------------------------------------------------

    def apply_timing(
        self,
        voiced,
        settings
    ):

        return self.time.process(
            voiced,
            bpm=settings.bpm
        )

    # --------------------------------------------------
    # MIDI
    # --------------------------------------------------

    def render(
        self,
        voiced,
        filename
    ):

        self.renderer.render(
            voiced,
            filename
        )

    # --------------------------------------------------
    # COMPLETE PIPELINE
    # --------------------------------------------------

    def compose(
        self,
        settings: CompositionSettings
    ):

        structure = self.build_structure(
            settings
        )

        progression = self.build_harmony(
            settings,
            structure
        )

        voiced = self.apply_voice_leading(
            progression
        )

        voiced = self.apply_expression(
            voiced,
            settings
        )

        voiced = self.apply_timing(
            voiced,
            settings
        )

        result = {

            "settings": settings,

            "structure": structure,

            "progression": progression,

            "voiced": voiced

        }

        self.last_result = result

        return result

    # --------------------------------------------------
    # EXPORT
    # --------------------------------------------------

    def compose_to_midi(
        self,
        filename,
        settings: CompositionSettings
    ):

        result = self.compose(
            settings
        )

        self.render(
            result["voiced"],
            filename
        )

        return result
            # --------------------------------------------------
    # VALIDATION
    # --------------------------------------------------

    def validate_settings(
        self,
        settings: CompositionSettings
    ):

        if settings.bars <= 0:

            raise ValueError(
                "bars must be greater than zero."
            )

        if settings.bpm <= 0:

            raise ValueError(
                "bpm must be greater than zero."
            )

        if not settings.root:

            raise ValueError(
                "root key is required."
            )

        if not settings.scale:

            raise ValueError(
                "scale is required."
            )

    # --------------------------------------------------
    # PIPELINE STAGES
    # --------------------------------------------------

    def generate_structure(
        self,
        settings: CompositionSettings
    ):

        return self.structure.generate(
            bars=settings.bars,
            emotion=settings.emotion
        )

    def generate_progression(
        self,
        settings: CompositionSettings,
        structure
    ):

        progression = self.core.compose_progression(

            root=settings.root,

            scale=settings.scale,

            bars=settings.bars,

            emotion=settings.emotion

        )

        progression = self.cadence.apply_cadences(
            progression
        )

        return progression

    def optimize_progression(
        self,
        progression
    ):

        return self.harmony.optimize_loop(
            progression
        )

    def calculate_tension(
        self,
        progression
    ):

        values = []

        for chord in progression:

            values.append(

                self.tension.chord_tension(
                    chord
                )

            )

        return values

    def build_metadata(
        self,
        settings,
        structure,
        progression,
        tension
    ):

        return {

            "root": settings.root,

            "scale": settings.scale,

            "emotion": settings.emotion,

            "tempo": settings.bpm,

            "bars": settings.bars,

            "structure": structure,

            "tension": tension,

            "chord_count": len(
                progression
            )

        }

    # --------------------------------------------------
    # MAIN GENERATION
    # --------------------------------------------------

    def generate(
        self,
        settings: CompositionSettings
    ):

        self.validate_settings(
            settings
        )

        structure = self.generate_structure(
            settings
        )

        progression = self.generate_progression(
            settings,
            structure
        )

        voiced = self.optimize_progression(
            progression
        )

        voiced = self.apply_expression(
            voiced,
            settings
        )

        voiced = self.apply_timing(
            voiced,
            settings
        )

        tension = self.calculate_tension(
            progression
        )

        metadata = self.build_metadata(

            settings,

            structure,

            progression,

            tension

        )

        result = {

            "metadata": metadata,

            "structure": structure,

            "progression": progression,

            "voiced": voiced,

            "tension": tension

        }

        self.last_result = result

        return result

    # --------------------------------------------------
    # QUICK EXPORT
    # --------------------------------------------------

    def export(
        self,
        filename,
        settings: CompositionSettings
    ):

        result = self.generate(
            settings
        )

        self.renderer.render(

            result["voiced"],

            filename

        )

        return result
            # --------------------------------------------------
    # REPORTS
    # --------------------------------------------------

    def statistics(
        self
    ):

        if self.last_result is None:

            return {}

        progression = self.last_result[
            "progression"
        ]

        voiced = self.last_result[
            "voiced"
        ]

        tension = self.last_result[
            "tension"
        ]

        report = {

            "bars": len(
                progression
            ),

            "chords": len(
                progression
            ),

            "average_tension": (
                sum(tension) / len(tension)
                if tension
                else 0
            ),

            "max_tension": (
                max(tension)
                if tension
                else 0
            ),

            "min_tension": (
                min(tension)
                if tension
                else 0
            ),

            "voices": len(
                voiced
            )

        }

        return report

    # --------------------------------------------------
    # REGENERATION
    # --------------------------------------------------

    def regenerate_harmony(
        self
    ):

        if self.last_result is None:

            return None

        settings = self.last_result[
            "metadata"
        ]

        return self.generate(

            CompositionSettings(

                root=settings["root"],

                scale=settings["scale"],

                emotion=settings["emotion"],

                bpm=settings["tempo"],

                bars=settings["bars"]

            )

        )

    # --------------------------------------------------
    # PRESETS
    # --------------------------------------------------

    @staticmethod
    def cinematic():

        return CompositionSettings(

            emotion="cinematic",

            bpm=95,

            bars=32

        )

    @staticmethod
    def epic():

        return CompositionSettings(

            emotion="epic",

            bpm=120,

            bars=48

        )

    @staticmethod
    def ambient():

        return CompositionSettings(

            emotion="ambient",

            bpm=70,

            bars=64

        )

    @staticmethod
    def piano():

        return CompositionSettings(

            emotion="hopeful",

            bpm=80,

            bars=24

        )

    @staticmethod
    def dark():

        return CompositionSettings(

            emotion="dark",

            bpm=90,

            bars=32

        )

    # --------------------------------------------------
    # MULTIPLE GENERATION
    # --------------------------------------------------

    def generate_batch(
        self,
        count: int,
        settings: CompositionSettings
    ):

        results = []

        for _ in range(count):

            results.append(

                self.generate(
                    settings
                )

            )

        return results

    # --------------------------------------------------
    # SAVE MULTIPLE MIDI
    # --------------------------------------------------

    def export_batch(
        self,
        prefix: str,
        count: int,
        settings: CompositionSettings
    ):

        results = self.generate_batch(

            count,

            settings

        )

        for index, result in enumerate(
            results,
            start=1
        ):

            filename = (

                f"{prefix}_"

                f"{index:02d}.mid"

            )

            self.renderer.render(

                result["voiced"],

                filename

            )

        return results
            # --------------------------------------------------
    # PROJECT EXPORT
    # --------------------------------------------------

    def export_project(
        self,
        directory: str,
        settings: CompositionSettings
    ):

        result = self.generate(
            settings
        )

        voiced = result["voiced"]

        self.renderer.render(
            voiced,
            f"{directory}/master.mid"
        )

        return result

    # --------------------------------------------------
    # TRACK ACCESS
    # --------------------------------------------------

    def get_progression(self):

        if self.last_result is None:

            return []

        return self.last_result[
            "progression"
        ]

    def get_voicings(self):

        if self.last_result is None:

            return []

        return self.last_result[
            "voiced"
        ]

    def get_structure(self):

        if self.last_result is None:

            return []

        return self.last_result[
            "structure"
        ]

    def get_tension(self):

        if self.last_result is None:

            return []

        return self.last_result[
            "tension"
        ]

    def metadata(self):

        if self.last_result is None:

            return {}

        return self.last_result[
            "metadata"
        ]

    # --------------------------------------------------
    # RESET
    # --------------------------------------------------

    def clear(self):

        self.last_result = None

    # --------------------------------------------------
    # REUSE SETTINGS
    # --------------------------------------------------

    def clone_settings(
        self,
        settings: CompositionSettings
    ):

        return CompositionSettings(

            root=settings.root,

            scale=settings.scale,

            emotion=settings.emotion,

            bpm=settings.bpm,

            bars=settings.bars,

            beats_per_bar=settings.beats_per_bar,

            humanize=settings.humanize,

            seed=settings.seed,

            metadata=(
                dict(settings.metadata)
                if settings.metadata
                else None
            )

        )

    # --------------------------------------------------
    # CHANGE TEMPO
    # --------------------------------------------------

    def with_bpm(
        self,
        settings: CompositionSettings,
        bpm: int
    ):

        copy = self.clone_settings(
            settings
        )

        copy.bpm = bpm

        return copy

    # --------------------------------------------------
    # CHANGE EMOTION
    # --------------------------------------------------

    def with_emotion(
        self,
        settings: CompositionSettings,
        emotion: str
    ):

        copy = self.clone_settings(
            settings
        )

        copy.emotion = emotion

        return copy

    # --------------------------------------------------
    # CHANGE KEY
    # --------------------------------------------------

    def with_key(
        self,
        settings: CompositionSettings,
        root: str,
        scale: str
    ):

        copy = self.clone_settings(
            settings
        )

        copy.root = root

        copy.scale = scale

        return copy

    # --------------------------------------------------
    # RANDOMIZE
    # --------------------------------------------------

    def randomize_seed(
        self,
        settings: CompositionSettings
    ):

        import random

        copy = self.clone_settings(
            settings
        )

        copy.seed = random.randint(
            1,
            2 ** 31
        )

        return copy

    # --------------------------------------------------
    # VERSION
    # --------------------------------------------------

    @staticmethod
    def version():

        return "MidiGenV7"
            # --------------------------------------------------
    # FUTURE ENGINE REGISTRATION
    # --------------------------------------------------

    def register_emotion_engine(
        self,
        engine
    ):

        self.emotion_engine = engine

    def register_motif_engine(
        self,
        engine
    ):

        self.motif_engine = engine

    def register_variation_engine(
        self,
        engine
    ):

        self.variation_engine = engine

    def register_bass_engine(
        self,
        engine
    ):

        self.bass_engine = engine

    def register_counterpoint_engine(
        self,
        engine
    ):

        self.counterpoint_engine = engine

    def register_arrangement_engine(
        self,
        engine
    ):

        self.arrangement_engine = engine

    def register_genre_engine(
        self,
        engine
    ):

        self.genre_engine = engine

    def register_rule_engine(
        self,
        engine
    ):

        self.rule_engine = engine

    # --------------------------------------------------
    # OPTIONAL PIPELINE
    # --------------------------------------------------

    def apply_optional_engines(
        self,
        result,
        settings
    ):

        if hasattr(
            self,
            "emotion_engine"
        ):

            result = self.emotion_engine.process(
                result,
                settings
            )

        if hasattr(
            self,
            "motif_engine"
        ):

            result = self.motif_engine.process(
                result,
                settings
            )

        if hasattr(
            self,
            "variation_engine"
        ):

            result = self.variation_engine.process(
                result,
                settings
            )

        if hasattr(
            self,
            "bass_engine"
        ):

            result = self.bass_engine.process(
                result,
                settings
            )

        if hasattr(
            self,
            "counterpoint_engine"
        ):

            result = self.counterpoint_engine.process(
                result,
                settings
            )

        if hasattr(
            self,
            "arrangement_engine"
        ):

            result = self.arrangement_engine.process(
                result,
                settings
            )

        if hasattr(
            self,
            "genre_engine"
        ):

            result = self.genre_engine.process(
                result,
                settings
            )

        if hasattr(
            self,
            "rule_engine"
        ):

            result = self.rule_engine.process(
                result,
                settings
            )

        return result

    # --------------------------------------------------
    # COMPLETE PROJECT
    # --------------------------------------------------

    def compose_project(
        self,
        settings: CompositionSettings
    ):

        result = self.generate(
            settings
        )

        result = self.apply_optional_engines(
            result,
            settings
        )

        self.last_result = result

        return result

    # --------------------------------------------------
    # MULTI EXPORT
    # --------------------------------------------------

    def export_project_tracks(
        self,
        directory,
        settings
    ):

        project = self.compose_project(
            settings
        )

        if "tracks" not in project:

            self.renderer.render(

                project["voiced"],

                f"{directory}/master.mid"

            )

            return project

        for track in project["tracks"]:

            filename = (

                f"{directory}/"

                f"{track['name']}.mid"

            )

            self.renderer.render(

                track["events"],

                filename

            )

        return project

    # --------------------------------------------------
    # INFORMATION
    # --------------------------------------------------

    def available_engines(
        self
    ):

        engines = {

            "HarmonyEngine":
                self.harmony,

            "CadenceEngine":
                self.cadence,

            "TensionEngine":
                self.tension,

            "VoiceLeadingEngine":
                self.voice,

            "ComposerCore":
                self.core,

            "StructureEngine":
                self.structure,

            "ExpressionLayer":
                self.expression,

            "TimeLayer":
                self.time,

            "MidiRendererV2":
                self.renderer

        }

        optional = [

            "emotion_engine",

            "motif_engine",

            "variation_engine",

            "bass_engine",

            "counterpoint_engine",

            "arrangement_engine",

            "genre_engine",

            "rule_engine"

        ]

        for name in optional:

            if hasattr(
                self,
                name
            ):

                engines[name] = getattr(
                    self,
                    name
                )

        return engines
            # --------------------------------------------------
    # PROFILE MANAGEMENT
    # --------------------------------------------------

    def save_profile(
        self,
        name: str,
        settings: CompositionSettings
    ):

        if not hasattr(
            self,
            "_profiles"
        ):

            self._profiles = {}

        self._profiles[name] = self.clone_settings(
            settings
        )

    def load_profile(
        self,
        name: str
    ):

        if not hasattr(
            self,
            "_profiles"
        ):

            raise KeyError(name)

        return self.clone_settings(
            self._profiles[name]
        )

    def available_profiles(
        self
    ):

        if not hasattr(
            self,
            "_profiles"
        ):

            return []

        return sorted(
            self._profiles.keys()
        )

    # --------------------------------------------------
    # COMPOSITION HISTORY
    # --------------------------------------------------

    def push_history(
        self,
        result
    ):

        if not hasattr(
            self,
            "_history"
        ):

            self._history = []

        self._history.append(
            result
        )

    def history(
        self
    ):

        if not hasattr(
            self,
            "_history"
        ):

            return []

        return list(
            self._history
        )

    def clear_history(
        self
    ):

        self._history = []

    # --------------------------------------------------
    # ENGINE STATUS
    # --------------------------------------------------

    def status(
        self
    ):

        return {

            "last_result":
                self.last_result is not None,

            "profiles":
                len(
                    getattr(
                        self,
                        "_profiles",
                        {}
                    )
                ),

            "history":
                len(
                    getattr(
                        self,
                        "_history",
                        []
                    )
                ),

            "optional_engines":
                len(
                    self.available_engines()
                ) - 9

        }

    # --------------------------------------------------
    # QUALITY SCORE
    # --------------------------------------------------

    def quality_score(
        self
    ):

        if self.last_result is None:

            return 0.0

        tension = self.last_result.get(
            "tension",
            []
        )

        if not tension:

            return 0.0

        average = sum(
            tension
        ) / len(
            tension
        )

        spread = max(
            tension
        ) - min(
            tension
        )

        score = (
            average * 0.60 +
            spread * 0.40
        )

        return round(
            score,
            3
        )

    # --------------------------------------------------
    # DUPLICATE PROJECT
    # --------------------------------------------------

    def duplicate_last(
        self
    ):

        import copy

        if self.last_result is None:

            return None

        return copy.deepcopy(
            self.last_result
        )

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    def summary(
        self
    ):

        if self.last_result is None:

            return {}

        meta = self.metadata()

        return {

            "project":

                "MidiGenV7",

            "emotion":

                meta.get(
                    "emotion"
                ),

            "root":

                meta.get(
                    "root"
                ),

            "scale":

                meta.get(
                    "scale"
                ),

            "tempo":

                meta.get(
                    "tempo"
                ),

            "bars":

                meta.get(
                    "bars"
                ),

            "quality":

                self.quality_score()

        }
            # --------------------------------------------------
    # PROJECT ANALYSIS
    # --------------------------------------------------

    def analyze(
        self
    ):

        if self.last_result is None:

            return {}

        progression = self.last_result[
            "progression"
        ]

        voiced = self.last_result[
            "voiced"
        ]

        tension = self.last_result[
            "tension"
        ]

        report = {

            "bars": len(
                progression
            ),

            "chords": len(
                progression
            ),

            "voices": len(
                voiced
            ),

            "tension_curve": tension,

            "average_tension": (
                sum(tension) / len(tension)
                if tension
                else 0
            ),

            "highest_tension": (
                max(tension)
                if tension
                else 0
            ),

            "lowest_tension": (
                min(tension)
                if tension
                else 0
            )

        }

        return report

    # --------------------------------------------------
    # PROJECT COMPARISON
    # --------------------------------------------------

    def compare_projects(
        self,
        first,
        second
    ):

        return {

            "bars":

                len(
                    first["progression"]
                ) -
                len(
                    second["progression"]
                ),

            "tension_difference":

                abs(

                    sum(
                        first["tension"]
                    ) -

                    sum(
                        second["tension"]
                    )

                ),

            "voice_difference":

                abs(

                    len(
                        first["voiced"]
                    ) -

                    len(
                        second["voiced"]
                    )

                )

        }

    # --------------------------------------------------
    # PROJECT SCORE
    # --------------------------------------------------

    def score(
        self,
        result
    ):

        score = 0.0

        score += len(
            result.get(
                "progression",
                []
            )
        )

        score += sum(
            result.get(
                "tension",
                []
            )
        )

        score += len(
            result.get(
                "voiced",
                []
            )
        )

        return score

    # --------------------------------------------------
    # BEST OF BATCH
    # --------------------------------------------------

    def generate_best(
        self,
        attempts,
        settings
    ):

        best = None

        best_score = -1

        for _ in range(
            attempts
        ):

            project = self.generate(
                settings
            )

            current = self.score(
                project
            )

            if current > best_score:

                best_score = current

                best = project

        self.last_result = best

        return best

    # --------------------------------------------------
    # PIPELINE CALLBACKS
    # --------------------------------------------------

    def before_generate(
        self,
        callback
    ):

        if not hasattr(
            self,
            "_before"
        ):

            self._before = []

        self._before.append(
            callback
        )

    def after_generate(
        self,
        callback
    ):

        if not hasattr(
            self,
            "_after"
        ):

            self._after = []

        self._after.append(
            callback
        )

    def execute_before(
        self,
        settings
    ):

        if not hasattr(
            self,
            "_before"
        ):

            return

        for callback in self._before:

            callback(
                settings
            )

    def execute_after(
        self,
        result
    ):

        if not hasattr(
            self,
            "_after"
        ):

            return

        for callback in self._after:

            callback(
                result
            )

    # --------------------------------------------------
    # PIPELINE ENTRY
    # --------------------------------------------------

    def compose(
        self,
        settings: CompositionSettings
    ):

        self.execute_before(
            settings
        )

        result = self.generate(
            settings
        )

        result = self.apply_optional_engines(
            result,
            settings
        )

        self.push_history(
            result
        )

        self.last_result = result

        self.execute_after(
            result
        )

        return result
            # --------------------------------------------------
    # EMOTION BLENDING
    # --------------------------------------------------

    def compose_with_emotions(
        self,
        emotions,
        settings: CompositionSettings
    ):

        settings = self.clone_settings(
            settings
        )

        settings.metadata = settings.metadata or {}

        settings.metadata[
            "emotion_blend"
        ] = list(
            emotions
        )

        return self.compose(
            settings
        )

    # --------------------------------------------------
    # SECTION GENERATION
    # --------------------------------------------------

    def compose_section(
        self,
        section_name,
        settings: CompositionSettings
    ):

        result = self.compose(
            settings
        )

        result["section"] = section_name

        return result

    def compose_song(
        self,
        sections,
        settings: CompositionSettings
    ):

        song = []

        for section in sections:

            part = self.compose_section(

                section,

                settings

            )

            song.append(
                part
            )

        return song

    # --------------------------------------------------
    # PROJECT CACHE
    # --------------------------------------------------

    def enable_cache(
        self
    ):

        self._cache = {}

    def cache_result(
        self,
        key,
        value
    ):

        if not hasattr(
            self,
            "_cache"
        ):

            self.enable_cache()

        self._cache[key] = value

    def cached(
        self,
        key
    ):

        if not hasattr(
            self,
            "_cache"
        ):

            return None

        return self._cache.get(
            key
        )

    def clear_cache(
        self
    ):

        self._cache = {}

    # --------------------------------------------------
    # AUTO SAVE
    # --------------------------------------------------

    def autosave(
        self,
        filename
    ):

        if self.last_result is None:

            return

        self.renderer.render(

            self.last_result[
                "voiced"
            ],

            filename

        )

    # --------------------------------------------------
    # RESET PROJECT
    # --------------------------------------------------

    def reset_project(
        self
    ):

        self.last_result = None

        self.clear_history()

        self.clear_cache()

    # --------------------------------------------------
    # ENGINE INFORMATION
    # --------------------------------------------------

    def info(
        self
    ):

        return {

            "name":

                "MidiGenV7",

            "version":

                self.version(),

            "profiles":

                self.available_profiles(),

            "engines":

                list(

                    self.available_engines().keys()

                )

        }

    # --------------------------------------------------
    # MAGIC METHODS
    # --------------------------------------------------

    def __repr__(
        self
    ):

        return (

            f"<ComposerOrchestrator "

            f"version={self.version()} "

            f"history={len(getattr(self,'_history',[]))}>"

        )

    def __len__(
        self
    ):

        if self.last_result is None:

            return 0

        return len(

            self.last_result.get(

                "progression",

                []

            )

        )

    def __bool__(
        self
    ):

        return self.last_result is not None
            # --------------------------------------------------
    # COMPOSITION EVOLUTION
    # --------------------------------------------------

    def evolve(
        self,
        settings: CompositionSettings,
        generations: int = 5
    ):

        population = []

        for _ in range(
            generations
        ):

            candidate = self.generate(
                settings
            )

            population.append(
                candidate
            )

        population.sort(

            key=self.score,

            reverse=True

        )

        self.last_result = population[0]

        return population

    # --------------------------------------------------
    # RANDOM PRESET
    # --------------------------------------------------

    def random_preset(
        self
    ):

        import random

        presets = [

            self.cinematic,

            self.epic,

            self.dark,

            self.ambient,

            self.piano

        ]

        return random.choice(
            presets
        )()

    # --------------------------------------------------
    # QUICK COMPOSE
    # --------------------------------------------------

    def quick_compose(
        self
    ):

        settings = self.random_preset()

        return self.compose(
            settings
        )

    # --------------------------------------------------
    # MULTI KEY GENERATION
    # --------------------------------------------------

    def compose_keys(
        self,
        keys,
        settings: CompositionSettings
    ):

        results = {}

        for root in keys:

            current = self.with_key(

                settings,

                root,

                settings.scale

            )

            results[root] = self.compose(
                current
            )

        return results

    # --------------------------------------------------
    # MULTI TEMPO GENERATION
    # --------------------------------------------------

    def compose_tempos(
        self,
        tempos,
        settings: CompositionSettings
    ):

        results = {}

        for bpm in tempos:

            current = self.with_bpm(

                settings,

                bpm

            )

            results[bpm] = self.compose(
                current
            )

        return results

    # --------------------------------------------------
    # MULTI EMOTION GENERATION
    # --------------------------------------------------

    def compose_emotion_set(
        self,
        emotions,
        settings: CompositionSettings
    ):

        results = {}

        for emotion in emotions:

            current = self.with_emotion(

                settings,

                emotion

            )

            results[emotion] = self.compose(
                current
            )

        return results

    # --------------------------------------------------
    # SEARCH BEST EMOTION
    # --------------------------------------------------

    def best_emotion(
        self,
        emotions,
        settings: CompositionSettings
    ):

        candidates = self.compose_emotion_set(

            emotions,

            settings

        )

        best = None

        best_score = -1

        for emotion, project in candidates.items():

            value = self.score(
                project
            )

            if value > best_score:

                best_score = value

                best = emotion

        return best, candidates[best]
            # --------------------------------------------------
    # PROJECT MERGING
    # --------------------------------------------------

    def merge_projects(
        self,
        *projects
    ):

        merged = {

            "structure": [],

            "progression": [],

            "voiced": [],

            "tension": []

        }

        for project in projects:

            merged["structure"].extend(
                project.get(
                    "structure",
                    []
                )
            )

            merged["progression"].extend(
                project.get(
                    "progression",
                    []
                )
            )

            merged["voiced"].extend(
                project.get(
                    "voiced",
                    []
                )
            )

            merged["tension"].extend(
                project.get(
                    "tension",
                    []
                )
            )

        self.last_result = merged

        return merged

    # --------------------------------------------------
    # PROJECT CONCATENATION
    # --------------------------------------------------

    def concatenate(
        self,
        projects
    ):

        return self.merge_projects(
            *projects
        )

    # --------------------------------------------------
    # PROJECT DUPLICATION
    # --------------------------------------------------

    def repeat_project(
        self,
        project,
        repeats=2
    ):

        result = {

            "structure": [],

            "progression": [],

            "voiced": [],

            "tension": []

        }

        for _ in range(repeats):

            result["structure"].extend(
                project["structure"]
            )

            result["progression"].extend(
                project["progression"]
            )

            result["voiced"].extend(
                project["voiced"]
            )

            result["tension"].extend(
                project["tension"]
            )

        return result

    # --------------------------------------------------
    # TRANSPOSITION
    # --------------------------------------------------

    def transpose_project(
        self,
        project,
        semitones
    ):

        import copy

        project = copy.deepcopy(
            project
        )

        for chord in project["voiced"]:

            for note in chord:

                note.midi += semitones

        return project

    # --------------------------------------------------
    # OCTAVE SHIFT
    # --------------------------------------------------

    def octave_up(
        self,
        project
    ):

        return self.transpose_project(
            project,
            12
        )

    def octave_down(
        self,
        project
    ):

        return self.transpose_project(
            project,
            -12
        )

    # --------------------------------------------------
    # VELOCITY
    # --------------------------------------------------

    def scale_velocity(
        self,
        project,
        factor
    ):

        import copy

        project = copy.deepcopy(
            project
        )

        for chord in project["voiced"]:

            for note in chord:

                note.velocity = int(

                    max(

                        1,

                        min(

                            127,

                            note.velocity * factor

                        )

                    )

                )

        return project

    # --------------------------------------------------
    # HUMANIZATION
    # --------------------------------------------------

    def humanize_project(
        self,
        project
    ):

        import copy

        project = copy.deepcopy(
            project
        )

        project["voiced"] = self.expression.process(

            project["voiced"]

        )

        return project

    # --------------------------------------------------
    # TIMING
    # --------------------------------------------------

    def retime_project(
        self,
        project,
        bpm
    ):

        import copy

        project = copy.deepcopy(
            project
        )

        project["voiced"] = self.time.process(

            project["voiced"],

            bpm=bpm

        )

        return project

    # --------------------------------------------------
    # NORMALIZATION
    # --------------------------------------------------

    def normalize_project(
        self,
        project
    ):

        import copy

        project = copy.deepcopy(
            project
        )

        for chord in project["voiced"]:

            for note in chord:

                note.velocity = max(

                    40,

                    min(

                        110,

                        note.velocity

                    )

                )

                note.midi = max(

                    21,

                    min(

                        108,

                        note.midi

                    )

                )

        return project

    # --------------------------------------------------
    # VALIDATION
    # --------------------------------------------------

    def validate_project(
        self,
        project
    ):

        required = (

            "progression",

            "voiced",

            "structure",

            "tension"

        )

        for key in required:

            if key not in project:

                raise ValueError(

                    f"Missing '{key}'"

                )

        return True

    # --------------------------------------------------
    # CLONE
    # --------------------------------------------------

    def clone_project(
        self,
        project
    ):

        import copy

        return copy.deepcopy(
            project
        )

    # --------------------------------------------------
    # CURRENT PROJECT
    # --------------------------------------------------

    def current(
        self
    ):

        return self.last_result

    # --------------------------------------------------
    # IS EMPTY
    # --------------------------------------------------

    def empty(
        self
    ):

        return self.last_result is None

    # --------------------------------------------------
    # PROJECT NAME
    # --------------------------------------------------

    def project_name(
        self
    ):

        return "MidiGenV7 Composition"

    # --------------------------------------------------
    # ENGINE NAME
    # --------------------------------------------------

    @staticmethod
    def engine_name():

        return "MidiGenV7 Composer Orchestrator"
            # --------------------------------------------------
    # EXPORT HELPERS
    # --------------------------------------------------

    def export_master(
        self,
        filename: str
    ):

        if self.last_result is None:

            raise RuntimeError(
                "Nothing to export."
            )

        self.renderer.render(

            self.last_result[
                "voiced"
            ],

            filename

        )

        return filename

    def export_variations(
        self,
        prefix: str,
        count: int,
        settings: CompositionSettings
    ):

        exported = []

        projects = self.generate_batch(

            count,

            settings

        )

        for index, project in enumerate(

            projects,

            start=1

        ):

            filename = (

                f"{prefix}_"

                f"{index:03d}.mid"

            )

            self.renderer.render(

                project["voiced"],

                filename

            )

            exported.append(
                filename
            )

        return exported

    # --------------------------------------------------
    # PREVIEW
    # --------------------------------------------------

    def preview(
        self
    ):

        if self.last_result is None:

            return {}

        progression = [

            str(chord)

            for chord

            in self.last_result[
                "progression"
            ]

        ]

        return {

            "progression":

                progression,

            "bars":

                len(
                    progression
                ),

            "tempo":

                self.last_result[
                    "metadata"
                ][
                    "tempo"
                ]

        }

    # --------------------------------------------------
    # GENERATOR OPTIONS
    # --------------------------------------------------

    def supported_emotions(
        self
    ):

        return [

            "happy",

            "sad",

            "dark",

            "hopeful",

            "cinematic",

            "epic",

            "ambient"

        ]

    def supported_scales(
        self
    ):

        return [

            "major",

            "minor",

            "harmonic_minor",

            "melodic_minor",

            "dorian",

            "phrygian",

            "lydian",

            "mixolydian"

        ]

    def supported_keys(
        self
    ):

        return [

            "C",

            "Db",

            "D",

            "Eb",

            "E",

            "F",

            "Gb",

            "G",

            "Ab",

            "A",

            "Bb",

            "B"

        ]

    # --------------------------------------------------
    # CONFIGURATION
    # --------------------------------------------------

    def configure(

        self,

        **kwargs

    ):

        if not hasattr(

            self,

            "_config"

        ):

            self._config = {}

        self._config.update(

            kwargs

        )

        return self._config

    def configuration(
        self
    ):

        return getattr(

            self,

            "_config",

            {}

        )

    # --------------------------------------------------
    # RANDOM SETTINGS
    # --------------------------------------------------

    def random_settings(
        self
    ):

        import random

        settings = CompositionSettings()

        settings.root = random.choice(

            self.supported_keys()

        )

        settings.scale = random.choice(

            self.supported_scales()

        )

        settings.emotion = random.choice(

            self.supported_emotions()

        )

        settings.bpm = random.randint(

            60,

            170

        )

        settings.bars = random.choice(

            [

                8,

                16,

                24,

                32,

                48,

                64

            ]

        )

        return settings

    # --------------------------------------------------
    # STRESS TEST
    # --------------------------------------------------

    def benchmark(

        self,

        iterations=25

    ):

        import time

        start = time.time()

        for _ in range(

            iterations

        ):

            settings = self.random_settings()

            self.generate(

                settings

            )

        elapsed = time.time() - start

        return {

            "iterations":

                iterations,

            "seconds":

                elapsed,

            "per_project":

                elapsed / iterations

        }

    # --------------------------------------------------
    # FINAL CLEANUP
    # --------------------------------------------------

    def shutdown(
        self
    ):

        self.last_result = None

        if hasattr(

            self,

            "_history"

        ):

            self._history.clear()

        if hasattr(

            self,

            "_cache"

        ):

            self._cache.clear()

        return True
            # --------------------------------------------------
    # PUBLIC API
    # --------------------------------------------------

    def __call__(
        self,
        settings: CompositionSettings
    ):

        return self.compose(
            settings
        )

    def __getitem__(
        self,
        key
    ):

        if self.last_result is None:

            raise KeyError(
                key
            )

        return self.last_result[
            key
        ]

    def keys(
        self
    ):

        if self.last_result is None:

            return []

        return list(
            self.last_result.keys()
        )

    def values(
        self
    ):

        if self.last_result is None:

            return []

        return list(
            self.last_result.values()
        )

    def items(
        self
    ):

        if self.last_result is None:

            return []

        return list(
            self.last_result.items()
        )

    # --------------------------------------------------
    # SERIALIZATION
    # --------------------------------------------------

    def to_dict(
        self
    ):

        if self.last_result is None:

            return {}

        return dict(
            self.last_result
        )

    def from_dict(
        self,
        project
    ):

        self.validate_project(
            project
        )

        self.last_result = project

        return self.last_result

    # --------------------------------------------------
    # METADATA
    # --------------------------------------------------

    def set_metadata(
        self,
        **kwargs
    ):

        if self.last_result is None:

            return

        metadata = self.last_result.setdefault(
            "metadata",
            {}
        )

        metadata.update(
            kwargs
        )

    def metadata_value(
        self,
        key,
        default=None
    ):

        if self.last_result is None:

            return default

        return self.last_result.get(
            "metadata",
            {}
        ).get(
            key,
            default
        )

    # --------------------------------------------------
    # CUSTOM PIPELINES
    # --------------------------------------------------

    def register_stage(
        self,
        callback
    ):

        if not hasattr(
            self,
            "_stages"
        ):

            self._stages = []

        self._stages.append(
            callback
        )

    def execute_stages(
        self,
        project,
        settings
    ):

        if not hasattr(
            self,
            "_stages"
        ):

            return project

        current = project

        for stage in self._stages:

            current = stage(
                current,
                settings
            )

        return current

    # --------------------------------------------------
    # ADVANCED GENERATION
    # --------------------------------------------------

    def compose_advanced(
        self,
        settings: CompositionSettings
    ):

        project = self.compose(
            settings
        )

        project = self.execute_stages(
            project,
            settings
        )

        self.last_result = project

        return project

    # --------------------------------------------------
    # SAFE GENERATION
    # --------------------------------------------------

    def try_compose(
        self,
        settings: CompositionSettings
    ):

        try:

            return self.compose(
                settings
            )

        except Exception as exc:

            return {

                "success": False,

                "error": str(
                    exc
                )

            }

    # --------------------------------------------------
    # HEALTH CHECK
    # --------------------------------------------------

    def health_check(
        self
    ):

        report = {

            "harmony":
                self.harmony is not None,

            "cadence":
                self.cadence is not None,

            "tension":
                self.tension is not None,

            "voice":
                self.voice is not None,

            "composer":
                self.core is not None,

            "structure":
                self.structure is not None,

            "expression":
                self.expression is not None,

            "time":
                self.time is not None,

            "renderer":
                self.renderer is not None

        }

        report["ready"] = all(
            report.values()
        )

        return report

    # --------------------------------------------------
    # DEFAULT INSTANCE
    # --------------------------------------------------

    @classmethod
    def create(
        cls
    ):

        return cls()

    @classmethod
    def default(
        cls
    ):

        return cls()

    # --------------------------------------------------
    # END OF FILE
    # --------------------------------------------------