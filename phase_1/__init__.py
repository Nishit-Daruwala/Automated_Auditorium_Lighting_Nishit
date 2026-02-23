"""
Phase 1: Parsing Module
Script → Scene structure processing
"""

from .format_detector import detect_format
from .text_cleaner import clean_text, extract_stage_directions
from .scene_segmenter import segment_scenes
from .timestamp_generator import generate_timestamps, extract_timestamps
from .json_builder import build_scene_json, build_complete_output
from .document_classifier import classify_document


def process_script(raw_text: str, filename: str = "script.txt"):
    """
    Convenience function: runs the full Phase 1 pipeline in one call.
    Returns a list of scene dicts ready for Phase 2.
    """
    fmt = detect_format(raw_text)
    doc_type = classify_document(raw_text)
    cleaned = clean_text(raw_text)
    scenes = segment_scenes(cleaned, fmt)
    timestamps = generate_timestamps(scenes)
    
    # Merge timestamps + generate scene_ids
    result = []
    for i, scene in enumerate(scenes):
        scene_id = f"scene_{i+1:03d}"
        text = scene.get("content", "")
        ts = timestamps[i] if i < len(timestamps) else {"start": 0, "end": 0, "duration": 0}
        
        result.append({
            "scene_id": scene_id,
            "timing": {
                "start_time": ts.get("start", 0),
                "end_time": ts.get("end", 0),
                "duration": ts.get("duration", 0),
            },
            "content": {
                "text": text,
                "word_count": len(text.split()),
                "type": scene.get("type", "generic"),
                "header": scene.get("header", ""),
                "location": scene.get("location", ""),
            },
        })
    
    return result


__all__ = [
    'detect_format',
    'clean_text',
    'extract_stage_directions',
    'segment_scenes',
    'generate_timestamps',
    'extract_timestamps',
    'build_scene_json',
    'build_complete_output',
    'process_script',
    'classify_document',
]
