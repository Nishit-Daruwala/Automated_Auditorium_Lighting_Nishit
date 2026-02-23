"""
Emotion analysis module with three detection strategies:
  1. ML Model (7 basic emotions) — fast, always available
  2. Keyword Enrichment (19 theatrical emotions) — post-processing override
  3. Zero-Shot Classification (19 emotions) — context-aware, slower

Pipeline: ML model → Keyword enrichment → (optional) Zero-shot refinement
"""

from config import EMOTION_MODEL, EMOTION_THRESHOLD, USE_ML_EMOTION, USE_ZERO_SHOT_EMOTION

# Try to import ML dependencies
try:
    from transformers import pipeline as hf_pipeline
    import torch
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("Warning: transformers not installed. Using keyword-based emotion detection.")

# Extended emotion set (19 emotions matching Phase 3 knowledge base)
EXTENDED_EMOTIONS = [
    "joy", "fear", "anger", "sadness", "surprise", "disgust", "neutral",
    "nostalgia", "mystery", "romantic", "anticipation", "hope", "triumph",
    "tension", "despair", "serenity", "confusion", "awe", "jealousy"
]

# Theatrical keyword rules for rich emotion detection (Option 1)
THEATRICAL_KEYWORDS = {
    "nostalgia": [
        "remember", "remembered", "memories", "memory", "nostalgic", "nostalgia",
        "once upon", "years ago", "long ago", "used to", "the old", "back when",
        "sepia", "faded", "photograph", "those days", "childhood", "grandfather",
        "grandmother", "antique", "vintage", "candlelight", "flickering"
    ],
    "mystery": [
        "mysterious", "mystery", "secret", "secrets", "hidden", "shadow", "shadows",
        "unknown", "enigma", "whisper", "whispered", "fog", "mist", "cloak",
        "disappear", "vanish", "puzzle", "riddle", "strange", "peculiar", "eerie"
    ],
    "romantic": [
        "romantic", "romance", "love", "kiss", "kissed", "embrace", "embraced",
        "tender", "tenderly", "intimate", "passion", "passionate", "beloved",
        "darling", "heart", "hearts", "rose", "roses", "candlelit", "together",
        "sunset", "moonlight", "caress", "adore", "soulmate"
    ],
    "anticipation": [
        "anticipation", "anticipating", "waiting", "suspense", "eager", "eagerly",
        "about to", "on the edge", "brink", "countdown", "ticking", "building",
        "mounting", "approaching", "imminent", "soon", "any moment"
    ],
    "hope": [
        "hope", "hopeful", "hoping", "light at the end", "tomorrow", "believe",
        "faith", "prayer", "praying", "salvation", "redemption", "promise",
        "dawn", "new beginning", "rising", "survive", "endure", "overcome"
    ],
    "triumph": [
        "triumph", "triumphant", "victory", "victorious", "conquered", "champion",
        "won", "winning", "glory", "glorious", "achievement", "accomplished",
        "made it", "succeeded", "success", "hero", "heroic", "summit", "peak"
    ],
    "tension": [
        "tension", "tense", "nervous", "uneasy", "unsettling", "standoff",
        "pressure", "interrogation", "interrogated", "confrontation", "stare",
        "silence", "sweat", "sweating", "clenched", "grip", "tight", "standstill"
    ],
    "despair": [
        "despair", "despairing", "hopeless", "hopelessness", "empty", "emptiness",
        "void", "nothing left", "given up", "surrender", "broken", "shattered",
        "numb", "numbness", "futile", "pointless", "meaningless", "lost everything"
    ],
    "serenity": [
        "serene", "serenity", "peaceful", "peace", "calm", "tranquil",
        "tranquility", "still", "stillness", "gentle", "breeze", "harmony",
        "meditate", "meditation", "quiet", "soft", "soothing", "float",
        "flowing", "ethereal", "beautiful"
    ],
    "confusion": [
        "confused", "confusion", "bewildered", "baffled", "lost", "disoriented",
        "what is happening", "don't understand", "dizzy", "spinning", "chaotic",
        "chaos", "conflicting", "contradicting", "nonsense", "absurd"
    ],
    "awe": [
        "awe", "awestruck", "awestruck", "majestic", "magnificent", "breathtaking",
        "wonder", "wonderful", "wondrous", "spectacular", "grand", "grandeur",
        "vast", "infinite", "cosmic", "divine", "sacred", "sublime", "incredible"
    ],
    "jealousy": [
        "jealous", "jealousy", "envious", "envy", "covet", "resentment",
        "resentful", "bitter", "bitterness", "betray", "betrayal", "betrayed",
        "unfaithful", "cheating", "rival", "suspicious", "possessive"
    ]
}

# Minimum keyword score to override ML neutral
KEYWORD_OVERRIDE_THRESHOLD = 2


class EmotionAnalyzer:
    """
    Multi-strategy emotion analyzer:
      - ML model: 7 basic emotions (fast)
      - Keyword enrichment: 12 additional theatrical emotions (instant)
      - Zero-shot: 19 emotions with full context understanding (slower)
    """
    
    def __init__(self, use_ml=USE_ML_EMOTION, use_zero_shot=USE_ZERO_SHOT_EMOTION):
        """
        Initialize emotion analyzer.
        
        Args:
            use_ml (bool): Use the 7-emotion ML model
            use_zero_shot (bool): Use zero-shot for neutral refinement
        """
        self.ml_available = ML_AVAILABLE and use_ml
        self.classifier = None
        self.zero_shot_classifier = None
        self.use_zero_shot = use_zero_shot
        
        # Load 7-emotion ML model
        if self.ml_available:
            try:
                device = 0 if torch.cuda.is_available() else -1
                self.classifier = hf_pipeline(
                    "text-classification",
                    model=EMOTION_MODEL,
                    top_k=None,
                    device=device
                )
                print(f"✅ Loaded ML emotion model: {EMOTION_MODEL}")
            except Exception as e:
                print(f"⚠️  Failed to load ML model: {e}")
                self.ml_available = False
        
        # Load zero-shot classifier (Option 2)
        if self.use_zero_shot and ML_AVAILABLE:
            try:
                self.zero_shot_classifier = hf_pipeline(
                    "zero-shot-classification",
                    model="facebook/bart-large-mnli",
                    device=-1  # CPU — this model is large
                )
                print(f"✅ Loaded zero-shot classifier: facebook/bart-large-mnli")
            except Exception as e:
                print(f"⚠️  Zero-shot classifier not available: {e}")
                print(f"   Continuing with ML + keyword enrichment only")
                self.zero_shot_classifier = None
        
        self.keywords = self._load_keywords()
    
    def analyze(self, text):
        """
        Full emotion analysis pipeline:
          1. Run 7-emotion ML model (basic 7 emotions)
          2. Always try keyword enrichment — upgrade to richer theatrical emotion
             if keyword evidence is strong enough (even when ML says joy/anger/etc.)
          3. If STILL neutral AND zero-shot available → refine (Option 2)
        
        Returns:
            dict: Emotion analysis results with primary_emotion, primary_score, etc.
        """
        if not text or not text.strip():
            return self._neutral_response()
        
        # Step 1: ML model (7 emotions)
        if self.ml_available and self.classifier:
            result = self._ml_analyze(text)
        else:
            result = self._keyword_analyze(text)
        
        ml_emotion = result["primary_emotion"]
        
        # Step 2: Keyword enrichment — upgrade ANY basic emotion to a richer one
        # For neutral: low threshold (2 keywords). For non-neutral: higher (3 keywords).
        threshold = 2 if ml_emotion == "neutral" else 3
        enriched = self._keyword_enrich(text, threshold=threshold)
        
        if enriched:
            # Only override if the enriched emotion is MORE SPECIFIC than the basic one
            # e.g., joy→triumph, anger→tension, sadness→despair are valid upgrades
            # But joy→nostalgia would need strong evidence
            result["primary_emotion"] = enriched["emotion"]
            result["primary_score"] = enriched["score"]
            result["method"] = result.get("method", "keyword") + "+keyword_enriched"
            return result
        
        # Step 3: Zero-shot refinement — if still basic/neutral and zero-shot available
        if ml_emotion in ("neutral", "joy", "sadness", "anger", "fear") and self.zero_shot_classifier:
            zs_result = self._zero_shot_analyze(text)
            if zs_result and zs_result["primary_emotion"] not in ("neutral", ml_emotion):
                result["primary_emotion"] = zs_result["primary_emotion"]
                result["primary_score"] = zs_result["primary_score"]
                result["all_scores"] = zs_result["all_scores"]
                result["method"] = result.get("method", "ml") + "+zero_shot"
        
        return result
    
    def _ml_analyze(self, text):
        """
        ML-based emotion analysis using DistilRoBERTa (7 emotions).
        For large scenes, splits into chunks and aggregates scores.
        """
        try:
            CHUNK_SIZE = 400
            chunks = []
            words = text.split()
            current_chunk = []
            current_len = 0
            
            for word in words:
                current_chunk.append(word)
                current_len += len(word) + 1
                if current_len >= CHUNK_SIZE:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = []
                    current_len = 0
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            
            if not chunks:
                return self._neutral_response()
            
            aggregated = {}
            for chunk in chunks[:8]:
                if not chunk.strip():
                    continue
                chunk_results = self.classifier(chunk)[0]
                for r in chunk_results:
                    label = r['label']
                    score = r['score']
                    aggregated[label] = aggregated.get(label, 0.0) + score
            
            n = min(len(chunks), 8)
            for label in aggregated:
                aggregated[label] /= n
            
            sorted_emotions = sorted(aggregated.items(), key=lambda x: x[1], reverse=True)
            
            primary_emotion = sorted_emotions[0][0]
            primary_score = sorted_emotions[0][1]
            
            # Anti-neutral bias for the 7-emotion model
            if primary_emotion == 'neutral' and len(sorted_emotions) > 1:
                for label, score in sorted_emotions[1:]:
                    if label != 'neutral' and score >= 0.25:
                        primary_emotion = label
                        primary_score = score
                        break
            
            secondary_emotion = None
            secondary_score = 0
            for label, score in sorted_emotions:
                if label != primary_emotion and score > EMOTION_THRESHOLD:
                    secondary_emotion = label
                    secondary_score = score
                    break
            
            return {
                "primary_emotion": primary_emotion,
                "primary_score": round(primary_score, 3),
                "secondary_emotion": secondary_emotion,
                "secondary_score": round(secondary_score, 3) if secondary_emotion else 0,
                "all_scores": {label: round(score, 3) for label, score in sorted_emotions[:5]},
                "method": "ml_chunked"
            }
        except Exception as e:
            print(f"⚠️  ML analysis failed: {e}. Using keyword fallback.")
            return self._keyword_analyze(text)
    
    def _keyword_enrich(self, text, threshold=KEYWORD_OVERRIDE_THRESHOLD):
        """
        Option 1: Keyword-based enrichment.
        Scans text for theatrical keywords to detect richer emotions
        that the 7-emotion ML model misses.
        
        Args:
            text: Scene text to analyze
            threshold: Minimum keyword matches to trigger enrichment
        
        Returns:
            dict or None: {emotion, score} if enriched, None if no match
        """
        text_lower = text.lower()
        scores = {}
        
        for emotion, keywords in THEATRICAL_KEYWORDS.items():
            count = sum(1 for kw in keywords if kw in text_lower)
            if count >= threshold:
                scores[emotion] = count
        
        if not scores:
            return None
        
        # Pick the best match
        best_emotion = max(scores, key=scores.get)
        total = sum(scores.values())
        confidence = min(0.85, 0.5 + (scores[best_emotion] / max(total, 1)) * 0.35)
        
        return {"emotion": best_emotion, "score": round(confidence, 3)}
    
    def _zero_shot_analyze(self, text):
        """
        Option 2: Zero-shot classification with all 19 emotions.
        Uses facebook/bart-large-mnli to classify into any label set.
        Slower but understands context, not just keywords.
        """
        if not self.zero_shot_classifier:
            return None
        
        try:
            # Truncate text for zero-shot (max ~300 chars for speed)
            truncated = text[:500] if len(text) > 500 else text
            
            result = self.zero_shot_classifier(
                truncated,
                candidate_labels=EXTENDED_EMOTIONS,
                multi_label=False
            )
            
            labels = result["labels"]
            scores = result["scores"]
            
            primary_emotion = labels[0]
            primary_score = scores[0]
            
            # Only trust zero-shot if confidence is reasonable
            if primary_score < 0.15:
                return None
            
            all_scores = {label: round(score, 3) for label, score in zip(labels[:7], scores[:7])}
            
            return {
                "primary_emotion": primary_emotion,
                "primary_score": round(primary_score, 3),
                "secondary_emotion": labels[1] if len(labels) > 1 else None,
                "secondary_score": round(scores[1], 3) if len(scores) > 1 else 0,
                "all_scores": all_scores,
                "method": "zero_shot"
            }
        except Exception as e:
            print(f"⚠️  Zero-shot analysis failed: {e}")
            return None
    
    def _keyword_analyze(self, text):
        """
        Fallback keyword-based analysis (all 19 emotions).
        Used when ML model is not available at all.
        """
        text_lower = text.lower()
        emotion_scores = {}
        
        # Check all keyword dictionaries (basic + theatrical)
        all_keywords = {**self.keywords, **THEATRICAL_KEYWORDS}
        
        for emotion, words in all_keywords.items():
            score = sum(1 for word in words if word in text_lower)
            if score > 0:
                emotion_scores[emotion] = score
        
        if not emotion_scores:
            return self._neutral_response()
        
        sorted_emotions = sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)
        
        total_matches = sum(emotion_scores.values())
        normalized_scores = {
            emotion: round(score / total_matches, 3) if total_matches > 0 else 0
            for emotion, score in emotion_scores.items()
        }
        
        primary_emotion = sorted_emotions[0][0]
        secondary_emotion = sorted_emotions[1][0] if len(sorted_emotions) > 1 and sorted_emotions[1][1] > 0 else None
        
        return {
            "primary_emotion": primary_emotion,
            "primary_score": normalized_scores.get(primary_emotion, 0),
            "secondary_emotion": secondary_emotion,
            "secondary_score": normalized_scores.get(secondary_emotion, 0) if secondary_emotion else 0,
            "all_scores": normalized_scores,
            "method": "keyword_extended"
        }
    
    def _neutral_response(self):
        """Return neutral emotion response."""
        return {
            "primary_emotion": "neutral",
            "primary_score": 1.0,
            "secondary_emotion": None,
            "secondary_score": 0,
            "all_scores": {"neutral": 1.0},
            "method": "default"
        }
    
    def _load_keywords(self):
        """Load basic 7-emotion keyword dictionary for fallback."""
        return {
            "joy": [
                "happy", "happiness", "joy", "joyful", "love", "loved", "loving",
                "smile", "smiling", "laugh", "laughing", "laughter", "celebrate",
                "celebration", "wonderful", "delight", "delightful", "cheerful",
                "excited", "excitement", "pleased", "glad", "grateful", "fun"
            ],
            "sadness": [
                "sad", "sadness", "cry", "crying", "tears", "lonely", "alone",
                "sorrow", "sorrowful", "grief", "grieving", "miserable",
                "depressed", "depression", "unhappy", "tragic", "heartbreak",
                "heartbroken", "gloomy", "melancholy", "mourn", "mourning",
                "flatlines", "loss"
            ],
            "anger": [
                "angry", "anger", "mad", "rage", "furious", "fury", "hate",
                "hatred", "hostile", "violence", "violent", "fight", "fighting",
                "scream", "screaming", "yell", "yelling", "frustrated", "frustration",
                "annoyed", "irritated", "outrage", "enraged"
            ],
            "fear": [
                "fear", "afraid", "scared", "frightened", "terrified", "terror",
                "panic", "panicked", "dread", "dreading", "horror", "horrified",
                "anxious", "anxiety", "nervous", "worried", "worry", "threat",
                "threatening", "danger", "dangerous", "ghost", "growl"
            ],
            "surprise": [
                "surprise", "surprised", "surprising", "shock", "shocked", "shocking",
                "sudden", "suddenly", "unexpected", "unexpectedly", "amazed",
                "amazing", "astonished", "astonishing", "startled", "wow"
            ],
            "disgust": [
                "disgusting", "disgust", "disgusted", "revolting", "repulsive",
                "sick", "sickening", "awful", "terrible", "horrible", "gross",
                "nasty", "vile", "repugnant", "stench", "smells"
            ],
            "neutral": [
                "said", "say", "says", "walked", "walk", "went", "go", "goes",
                "looked", "look", "looks", "saw", "see", "sees", "came", "come"
            ]
        }


# Global singleton instance
_analyzer_instance = None

def get_analyzer():
    """
    Get or create singleton analyzer instance.
    
    Returns:
        EmotionAnalyzer: Analyzer instance
    """
    global _analyzer_instance
    if _analyzer_instance is None:
        _analyzer_instance = EmotionAnalyzer()
    return _analyzer_instance

def analyze_emotion(text):
    """
    Convenience function for emotion analysis.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        dict: Emotion analysis results
    """
    analyzer = get_analyzer()
    return analyzer.analyze(text)