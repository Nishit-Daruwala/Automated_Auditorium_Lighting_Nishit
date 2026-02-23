"""
Lighting Decision Engine (Phase 4)

Converts scene emotions → lighting INTENT (not execution details).

Key design principles:
- Outputs groups, not individual fixtures
- Uses semantic parameters (intensity, color, focus_area)
- NO DMX channels here — that's adapter/Phase 8 responsibility
- LangChain for prompt formatting and structured output
- NO direct dependency on Phase 3 schemas (uses interface)
"""

import os
from typing import Dict, List, Any, Optional, Protocol
from enum import Enum
from pydantic import BaseModel, Field

# Import config
from config import (
    LLM_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS,
    LANGCHAIN_VERBOSE,
    FALLBACK_TO_RULES
)

# Try to import LangChain libraries
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import PydanticOutputParser
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("Warning: langchain-openai not installed. Using rule-based generation only.")


# =============================================================================
# RETRIEVER PROTOCOL (Interface for Phase 3 — we don't own Phase 3)
# =============================================================================

class RetrieverProtocol(Protocol):
    """Protocol for knowledge retriever — Phase 3 implements this"""
    def retrieve_palette(self, emotion: str) -> Dict: ...
    def build_context_for_llm(self, emotion: str, scene_text: str) -> str: ...


class SimpleRetriever:
    """Fallback retriever when Phase 3 is not available"""
    
    DEFAULT_PALETTES = {
        "joy": {
            "primary_colors": [{"name": "warm_amber", "rgb": [255, 191, 0]}],
            "intensity": {"default": 80},
            "transition": {"type": "fade", "duration": 2.0},
            "color_temperature": "warm"
        },
        "sadness": {
            "primary_colors": [{"name": "steel_blue", "rgb": [70, 130, 180]}],
            "intensity": {"default": 40},
            "transition": {"type": "fade", "duration": 4.0},
            "color_temperature": "cool"
        },
        "fear": {
            "primary_colors": [{"name": "dark_red", "rgb": [139, 0, 0]}],
            "intensity": {"default": 25},
            "transition": {"type": "flicker", "duration": 1.0},
            "effects": ["flicker"],
            "color_temperature": "cool"
        },
        "anger": {
            "primary_colors": [{"name": "deep_red", "rgb": [150, 0, 50]}],
            "intensity": {"default": 90},
            "transition": {"type": "snap", "duration": 0.5},
            "color_temperature": "warm"
        },
        "neutral": {
            "primary_colors": [{"name": "white", "rgb": [255, 255, 255]}],
            "intensity": {"default": 60},
            "transition": {"type": "fade", "duration": 2.0},
            "color_temperature": "neutral"
        },
        "surprise": {
            "primary_colors": [{"name": "bright_white", "rgb": [255, 255, 255]}, {"name": "cyan", "rgb": [0, 255, 255]}],
            "intensity": {"default": 100},
            "transition": {"type": "snap", "duration": 0.1},
            "effects": ["strobe"],
            "color_temperature": "cool"
        },
        "disgust": {
            "primary_colors": [{"name": "sickly_green", "rgb": [173, 255, 47]}, {"name": "yellow_green", "rgb": [154, 205, 50]}],
            "intensity": {"default": 35},
            "transition": {"type": "smooth", "duration": 3.0},
            "color_temperature": "cool"
        }
    }
    
    def retrieve_palette(self, emotion: str) -> Dict:
        return self.DEFAULT_PALETTES.get(emotion.lower(), self.DEFAULT_PALETTES["neutral"])
    
    def build_context_for_llm(self, emotion: str, scene_text: str) -> str:
        palette = self.retrieve_palette(emotion)
        return f"Emotion: {emotion}, Suggested colors: {palette.get('primary_colors', [])}"


def get_retriever() -> RetrieverProtocol:
    """
    Get the knowledge retriever.
    Attempts to use Phase 3 retriever if available, otherwise uses simple fallback.
    """
    try:
        from phase_3.rag_retriever import get_retriever as get_rag_retriever
        return get_rag_retriever()
    except ImportError:
        print("Phase 3 retriever not available. Using simple fallback.")
        return SimpleRetriever()


# =============================================================================
# ENUMS
# =============================================================================

class TransitionType(str, Enum):
    """Supported transition types"""
    FADE = "fade"
    SNAP = "snap"
    SMOOTH = "smooth"
    PULSE = "pulse"
    FLICKER = "flicker"
    STROBE = "strobe"
    CUT = "cut"
    CROSSFADE = "crossfade"
    FLASH = "flash"
    BLINK = "blink"


class FocusArea(str, Enum):
    """Stage focus areas"""
    CENTER_STAGE = "center_stage"
    STAGE_LEFT = "stage_left"
    STAGE_RIGHT = "stage_right"
    UPSTAGE = "upstage"
    DOWNSTAGE = "downstage"
    FULL_STAGE = "full_stage"
    AUDIENCE = "audience"


# =============================================================================
# PYDANTIC OUTPUT MODELS (Architecturally Correct)
# =============================================================================

class Transition(BaseModel):
    """Transition specification"""
    type: TransitionType = Field(default=TransitionType.FADE)
    duration_seconds: float = Field(default=2.0, ge=0.0, le=30.0)


class LightingParameters(BaseModel):
    """Semantic lighting parameters — NO DMX here"""
    intensity: float = Field(
        description="Intensity level 0.0-100.0 percent",
        ge=0.0, le=100.0
    )
    color: str = Field(
        description="Color name or hex code, e.g. 'warm_amber', 'deep_red', '#FF5500'"
    )
    focus_area: Optional[FocusArea] = Field(
        default=None,
        description="Where light is focused on stage"
    )
    color_temperature: Optional[str] = Field(
        default=None,
        description="warm, neutral, cool"
    )


class GroupLightingInstruction(BaseModel):
    """Lighting instruction for a fixture GROUP (not individual fixtures)"""
    group_id: str = Field(
        description="Group identifier: 'front_wash', 'back_light', 'side_fill', 'specials', 'ambient'"
    )
    parameters: LightingParameters = Field(
        description="Semantic lighting parameters"
    )
    transition: Transition = Field(
        default_factory=Transition,
        description="How to transition to this state"
    )


class TimeWindow(BaseModel):
    """Time window for the lighting instruction"""
    start_time: float = Field(ge=0.0)
    end_time: float = Field(ge=0.0)
    
    @property
    def duration(self) -> float:
        return self.end_time - self.start_time


class LightingInstruction(BaseModel):
    """Complete lighting instruction output from Phase 4
    
    This is the contract between LLM Decision Engine and downstream systems.
    Contains INTENT only — no DMX, no fixture IDs.
    """
    scene_id: str = Field(description="Scene identifier from Phase 1")
    emotion: str = Field(description="Detected emotion driving this instruction")
    time_window: TimeWindow = Field(description="When this instruction applies")
    groups: List[GroupLightingInstruction] = Field(
        description="Lighting instructions per group"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional metadata (reasoning, debug info). Stripped before Phase 5."
    )


# =============================================================================
# GROUP DEFINITIONS (These map to fixtures in adapter layer)
# =============================================================================

LIGHTING_GROUPS = {
    "front_wash": {
        "description": "Primary audience-facing illumination",
        "typical_fixtures": ["PAR", "fresnel"]
    },
    "back_light": {
        "description": "Separation from background, silhouettes",
        "typical_fixtures": ["PAR", "LED_bar"]
    },
    "side_fill": {
        "description": "Side lighting for depth and dimension",
        "typical_fixtures": ["PAR", "ellipsoidal"]
    },
    "specials": {
        "description": "Focused highlights, spotlights",
        "typical_fixtures": ["moving_head", "followspot"]
    },
    "ambient": {
        "description": "Overall wash, atmosphere",
        "typical_fixtures": ["RGB_wash", "cyclorama"]
    }
}


# =============================================================================
# PROMPT TEMPLATES
# =============================================================================

SYSTEM_PROMPT = """You are a professional lighting designer for theatre.
Your job is to specify lighting INTENT for scenes, not hardware details.

RULES:
1. Think in GROUPS: front_wash, back_light, side_fill, specials, ambient
2. Use SEMANTIC parameters: intensity (0-100), color (name or hex), focus_area
3. DO NOT specify DMX channels or fixture IDs — that happens later
4. Match lighting to emotion: warm for joy, cool for sadness, contrast for drama
5. Consider smooth transitions for most scenes

AVAILABLE GROUPS:
- front_wash: Primary audience-facing illumination
- back_light: Separation from background
- side_fill: Side lighting for depth
- specials: Focused highlights
- ambient: Overall atmosphere

{format_instructions}"""

USER_PROMPT = """Design lighting for this scene:

SCENE: {scene_text}
EMOTION: {emotion}
DURATION: {duration} seconds

CONTEXT FROM VENUE:
{context}

Specify lighting intent for appropriate groups."""


# =============================================================================
# LIGHTING DECISION ENGINE
# =============================================================================

class LightingDecisionEngine:
    """
    Phase 4: Convert scene emotions to lighting INTENT
    
    Uses LangChain for LLM-based generation with Pydantic output parsing.
    Falls back to rule-based generation if LLM fails.
    """
    
    def __init__(self, use_llm: bool = False, api_key: Optional[str] = None):
        """
        Initialize decision engine
        
        Args:
            use_llm: Whether to use LLM (requires API key)
            api_key: OpenAI API key (or set OPENAI_API_KEY env var)
        """
        self.retriever = get_retriever()
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.groq_key = os.environ.get("GROQ_API_KEY")
        self.use_llm = use_llm and LANGCHAIN_AVAILABLE and (bool(self.api_key) or bool(self.groq_key))
        
        self.chain = None
        if self.use_llm:
            self.chain = self._create_llm_chain()
    
    def _create_llm_chain(self):
        """Create LangChain chain with prompt template and output parser"""
        parser = PydanticOutputParser(pydantic_object=LightingInstruction)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("user", USER_PROMPT)
        ])
        prompt = prompt.partial(format_instructions=parser.get_format_instructions())
        
        kwargs = {
            "temperature": LLM_TEMPERATURE,
            "verbose": LANGCHAIN_VERBOSE
        }
        
        if getattr(self, "groq_key", None):
            kwargs["api_key"] = self.groq_key
            kwargs["base_url"] = "https://api.groq.com/openai/v1"
            kwargs["model"] = "llama-3.3-70b-versatile"  # Excellent Groq model for reasoning
        else:
            kwargs["api_key"] = self.api_key
            kwargs["model"] = LLM_MODEL
            kwargs["max_tokens"] = LLM_MAX_TOKENS

        llm = ChatOpenAI(**kwargs)
        
        return prompt | llm | parser
    
    def generate_instruction(self, scene_data: Dict) -> LightingInstruction:
        """
        Generate lighting instruction for a scene
        
        Args:
            scene_data: Scene dictionary from Phase 1
            
        Returns:
            LightingInstruction with semantic lighting intent
        """
        emotion = scene_data.get("emotion", {}).get("primary_emotion", "neutral")
        scene_text = scene_data.get("content", {}).get("text", "")
        scene_id = scene_data.get("scene_id", "unknown")
        timing = scene_data.get("timing", {})
        doc_type = scene_data.get("doc_type", "theatrical_script")
        
        if doc_type == "event_schedule":
            return self._generate_event_instruction(scene_id, scene_text, timing)
            
        if self.use_llm and self.chain:
            try:
                return self._generate_with_llm(scene_id, emotion, scene_text, timing)
            except Exception as e:
                print(f"LLM generation failed: {e}")
                if FALLBACK_TO_RULES:
                    print("Falling back to rule-based generation.")
                else:
                    raise
        
        return self._generate_with_rules(scene_id, emotion, scene_text, timing)
        
    def _generate_event_instruction(self, scene_id: str, scene_text: str, timing: Dict) -> LightingInstruction:
        """
        Bypass RAG/Emotion mapping and generate presets based purely on event context.
        """
        text_lower = scene_text.lower()
        
        # Simple local logic to map to event presets
        if "walk in" in text_lower or "reception" in text_lower or "break" in text_lower:
            preset = "WALK_IN_AMBIENCE"
            base_color = "warm_white"
            base_intensity = 80
            ambient_intensity = 60
        elif "panel" in text_lower or "discussion" in text_lower:
            preset = "PANEL_DISCUSSION"
            base_color = "daylight_white"
            base_intensity = 90
            ambient_intensity = 40
        elif "q&a" in text_lower or "audience" in text_lower:
            preset = "AUDIENCE_QNA"
            base_color = "warm_white"
            base_intensity = 70
            ambient_intensity = 80
        elif "award" in text_lower or "gala" in text_lower:
            preset = "AWARD_CEREMONY"
            base_color = "gold"
            base_intensity = 100
            ambient_intensity = 30
        else:
            preset = "KEYNOTE_SPEAKER"
            base_color = "cool_white"
            base_intensity = 95
            ambient_intensity = 10
            
        transition = Transition(type=TransitionType.FADE, duration_seconds=3.0)
        
        groups = [
            GroupLightingInstruction(
                group_id="front_wash",
                parameters=LightingParameters(intensity=base_intensity, color=base_color, focus_area=FocusArea.FULL_STAGE, color_temperature="neutral"),
                transition=transition
            ),
            GroupLightingInstruction(
                group_id="back_light",
                parameters=LightingParameters(intensity=int(base_intensity * 0.6), color=base_color, focus_area=FocusArea.FULL_STAGE, color_temperature="neutral"),
                transition=transition
            ),
            GroupLightingInstruction(
                group_id="side_fill",
                parameters=LightingParameters(intensity=int(base_intensity * 0.7), color=base_color, focus_area=FocusArea.CENTER_STAGE, color_temperature="neutral"),
                transition=transition
            ),
            GroupLightingInstruction(
                group_id="specials",
                parameters=LightingParameters(intensity=base_intensity if preset == "KEYNOTE_SPEAKER" else int(base_intensity*0.5), color=base_color, focus_area=FocusArea.CENTER_STAGE, color_temperature="neutral"),
                transition=transition
            ),
            GroupLightingInstruction(
                group_id="ambient",
                parameters=LightingParameters(intensity=ambient_intensity, color="white", focus_area=FocusArea.AUDIENCE, color_temperature="neutral"),
                transition=transition
            )
        ]
        
        return LightingInstruction(
            scene_id=scene_id,
            emotion="neutral",
            time_window=TimeWindow(
                start_time=timing.get("start_time", 0),
                end_time=timing.get("end_time", 0)
            ),
            groups=groups,
            metadata={"generation_method": "event_preset", "preset_applied": preset}
        )
    
    def _generate_with_llm(
        self, 
        scene_id: str, 
        emotion: str, 
        scene_text: str, 
        timing: Dict
    ) -> LightingInstruction:
        """Generate using LangChain LLM chain with Dynamic RLHF Memory Injection"""
        context = self.retriever.build_context_for_llm(emotion, scene_text)
        
        # --- RLHF MEMORY INJECTION ---
        # Look into the past experiences and fetch Human Corrections to adapt generation
        try:
            import json, os
            from pathlib import Path
            feedback_dir = Path("data/feedback_memory")
            if feedback_dir.exists():
                feedback_texts = []
                # Load the 10 most recent pieces of human feedback
                files = sorted(feedback_dir.glob("*.json"), key=os.path.getmtime, reverse=True)[:10]
                for fb_file in files:
                    try:
                        with open(fb_file, "r") as f:
                            fb_data = json.load(f)
                        correction = fb_data.get("human_correction", "")
                        if correction and len(correction.strip()) > 3:
                            feedback_texts.append(f"- DIRECTOR'S NOTE: {correction}")
                    except json.JSONDecodeError:
                        continue
                
                if feedback_texts:
                    rlhf_header = "\n\n--- CRITICAL SYSTEM MEMORY (HUMAN FEEDBACK FROM PRIOR RUNS) ---\n"
                    rlhf_header += "The following are historical corrections provided by the human director for previous simulations.\n"
                    rlhf_header += "You MUST interpret and apply these style preferences to the current scene generation wherever applicable:\n"
                    context += rlhf_header + "\n".join(feedback_texts)
                    print(f"🧠 [RLHF] Injected {len(feedback_texts)} human memories into LLM context for scene {scene_id}!")
        except Exception as e:
            print(f"⚠️ [RLHF] Error loading memory: {e}")
        
        response: LightingInstruction = self.chain.invoke({
            "scene_text": scene_text,
            "emotion": emotion,
            "duration": timing.get("duration", 0),
            "context": context
        })
        
        # Inject timing and metadata
        response.time_window = TimeWindow(
            start_time=timing.get("start_time", 0),
            end_time=timing.get("end_time", 0)
        )
        response.metadata = {"generation_method": "llm", "rlhf_applied": len(feedback_texts) if 'feedback_texts' in locals() else 0}
        
        return response
    
    def _generate_with_rules(
        self, 
        scene_id: str, 
        emotion: str, 
        scene_text: str, 
        timing: Dict
    ) -> LightingInstruction:
        """Generate using rule-based system"""
        palette = self.retriever.retrieve_palette(emotion)
        
        # Build group instructions from palette
        groups = self._build_group_instructions(palette, emotion)
        
        return LightingInstruction(
            scene_id=scene_id,
            emotion=emotion,
            time_window=TimeWindow(
                start_time=timing.get("start_time", 0),
                end_time=timing.get("end_time", 0)
            ),
            groups=groups,
            metadata={"generation_method": "rule_based"}
        )
    
    def _build_group_instructions(self, palette: Dict, emotion: str) -> List[GroupLightingInstruction]:
        """Build group instructions from RAG mood palette — ALL 5 groups."""
        instructions = []
        
        # Get palette values
        primary_colors = palette.get("primary_colors", [{"name": "white"}])
        primary_color = primary_colors[0].get("name", "white")
        secondary_color = primary_colors[1].get("name", primary_color) if len(primary_colors) > 1 else primary_color
        accent_color = primary_colors[2].get("name", secondary_color) if len(primary_colors) > 2 else secondary_color
        
        intensity_config = palette.get("intensity", {"default": 50})
        base_intensity = intensity_config.get("default", 50)
        
        color_temp = palette.get("color_temperature", "neutral")
        
        transition_config = palette.get("transition", {"type": "fade", "duration": 2.0})
        try:
            transition_type = TransitionType(transition_config.get("type", "fade"))
        except ValueError:
            transition_type = TransitionType.FADE
            
        transition = Transition(
            type=transition_type,
            duration_seconds=transition_config.get("duration", 2.0)
        )
        
        # === GROUP 1: FRONT WASH — Primary illumination ===
        instructions.append(GroupLightingInstruction(
            group_id="front_wash",
            parameters=LightingParameters(
                intensity=min(base_intensity, 100),
                color=primary_color,
                focus_area=FocusArea.FULL_STAGE,
                color_temperature=color_temp
            ),
            transition=transition
        ))
        
        # === GROUP 2: BACK LIGHT — Separation, slightly dimmer ===
        instructions.append(GroupLightingInstruction(
            group_id="back_light",
            parameters=LightingParameters(
                intensity=min(base_intensity * 0.6, 100),
                color=secondary_color,
                focus_area=FocusArea.FULL_STAGE,
                color_temperature=color_temp
            ),
            transition=transition
        ))
        
        # === GROUP 3: SIDE FILL — Moving heads + color PARs, use secondary color ===
        instructions.append(GroupLightingInstruction(
            group_id="side_fill",
            parameters=LightingParameters(
                intensity=min(base_intensity * 0.7, 100),
                color=secondary_color,
                focus_area=FocusArea.CENTER_STAGE,
                color_temperature=color_temp
            ),
            transition=transition
        ))
        
        # === GROUP 4: SPECIALS — Focused highlights with accent color ===
        instructions.append(GroupLightingInstruction(
            group_id="specials",
            parameters=LightingParameters(
                intensity=min(base_intensity * 0.5, 100),
                color=accent_color,
                focus_area=FocusArea.CENTER_STAGE,
                color_temperature=color_temp
            ),
            transition=transition
        ))
        
        # === GROUP 5: AMBIENT — Atmospheric wash ===
        instructions.append(GroupLightingInstruction(
            group_id="ambient",
            parameters=LightingParameters(
                intensity=min(base_intensity * 0.3, 100),
                color=accent_color,
                color_temperature=color_temp
            ),
            transition=transition
        ))
        
        # DEMONSTRATION LOGIC: intentionally trigger conflicts for specific colors
        if emotion == "anger":  # Trigger power draw conflict
            # Trigger power draw conflict (max_intensity_count >= 3)
            for instr in instructions:
                instr.parameters.intensity = 100.0
                
        elif emotion == "fear":  # Trigger visual timing conflict
            # Trigger visual timing conflict ("cut" mixed with "crossfade")
            instructions[0].transition.type = TransitionType.CUT
            instructions[1].transition.type = TransitionType.CROSSFADE
            
        return instructions


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def generate_lighting_instruction(scene_data: Dict, use_llm: bool = False) -> LightingInstruction:
    """Generate lighting instruction for a single scene"""
    engine = LightingDecisionEngine(use_llm=use_llm)
    return engine.generate_instruction(scene_data)


def batch_generate_instructions(scenes: List[Dict], use_llm: bool = False) -> List[LightingInstruction]:
    """Generate lighting instructions for multiple scenes"""
    engine = LightingDecisionEngine(use_llm=use_llm)
    return [engine.generate_instruction(scene) for scene in scenes]
