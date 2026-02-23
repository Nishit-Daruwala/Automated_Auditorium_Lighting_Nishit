"""
Scene segmentation module with context-aware splitting
Handles: Screenplay, Dialogue, Act Structure, Timestamped, and Generic scripts
"""

import re
from config import MAX_WORDS_PER_SCENE, MIN_WORDS_PER_SCENE, SCENE_MARKERS

def segment_scenes(text, format_info):
    """
    Context-aware scene segmentation based on format
    
    Args:
        text (str): Cleaned script text
        format_info (dict): Format information from detect_format()
        
    Returns:
        list: List of scene dictionaries with content and metadata
    """
    # Priority 1: If timestamps like "00:00 – 03:00" are found, segment by timestamp blocks
    if format_info.get("timestamped"):
        result = _segment_by_timestamps(text)  
        if result:
            return result

    # Priority 2: Screenplay format (INT./EXT.)
    if format_info.get("screenplay"):
        result = _segment_screenplay(text)
        if result:
            return result

    # Priority 3: Act/Scene structure
    if format_info.get("act_structure"):
        result = _segment_by_acts(text) 
        if result:
            return result

    # Priority 4: Dialogue-heavy format (CHARACTER:)
    if format_info.get("dialogue_format"):
        result = _segment_dialogue(text)
        if result:
            return result

    # Fallback: Generic word-count segmentation
    return _segment_generic(text)


def _segment_by_timestamps(text):
    """
    Segment script by timestamp markers like '00:00 – 03:00' or '[00:30]'
    This is the most reliable segmentation for scripts like Script-2.txt
    
    Args:
        text (str): Script text with timestamps
        
    Returns:
        list: Segmented scenes or None if no timestamps found
    """
    # Pattern: "Scene N" followed by optional subtitle, then timestamp range
    # Matches: "Scene 1 — The Locked Room\n00:00 – 03:00"
    # Also matches standalone timestamps: "00:00 – 03:00" or "00:00 - 03:00"
    scene_pattern = r'(?:Scene\s+\d+[^\n]*\n)?\s*(\d{1,2}:\d{2})\s*(?:–|-)\s*(\d{1,2}:\d{2})'
    
    matches = list(re.finditer(scene_pattern, text, re.IGNORECASE))
    
    if len(matches) < 2:
        return None  # Not enough timestamps, fallback
    
    scenes = []
    
    for i, match in enumerate(matches):
        start_time = match.group(1)
        end_time = match.group(2)
        
        # Find where this scene's content starts (after the timestamp line)
        content_start = match.end()
        
        # Find where this scene's content ends (at the next timestamp or end of text)
        if i < len(matches) - 1:
            # Content ends where the next scene header begins
            # Look backwards from next match to find the Scene header line
            next_match_start = matches[i + 1].start()
            # Check if there's a "Scene N" header before the next timestamp
            preceding_text = text[content_start:next_match_start]
            scene_header_match = re.search(r'\nScene\s+\d+', preceding_text, re.IGNORECASE)
            if scene_header_match:
                content_end = content_start + scene_header_match.start()
            else:
                content_end = next_match_start
        else:
            content_end = len(text)
        
        content = text[content_start:content_end].strip()
        
        # Extract scene title if present (look backwards from timestamp)
        scene_title = ""
        # Look for "Scene N — Title" pattern before the timestamp
        pre_text = text[max(0, match.start() - 100):match.start()]
        title_match = re.search(r'Scene\s+(\d+)\s*(?:—|-)\s*([^\n]+)', pre_text, re.IGNORECASE)
        if title_match:
            scene_title = f"Scene {title_match.group(1)} — {title_match.group(2).strip()}"
        
        if content:
            # Further split very long scenes by dialogue exchanges
            if len(content.split()) > MAX_WORDS_PER_SCENE * 3:
                subscenes = _split_long_scene_by_speakers(content, scene_title, start_time, end_time)
                scenes.extend(subscenes)
            else:
                scenes.append({
                    "content": content,
                    "type": "timestamped_scene",
                    "header": scene_title if scene_title else f"Scene ({start_time} – {end_time})",
                    "time_range": f"{start_time} – {end_time}",
                    "speakers": _extract_speakers_from_content(content)
                })
    
    return scenes if scenes else None


def _split_long_scene_by_speakers(content, scene_title, start_time, end_time):
    """
    Split a long timestamped scene into smaller chunks by speaker dialogue blocks.
    Groups consecutive dialogue into chunks that respect MAX_WORDS_PER_SCENE.
    """
    # Split by speaker patterns (e.g., "ARIN:" at start of line)
    parts = re.split(r'(^[A-Z][A-Z\s]{1,}:\s*)', content, flags=re.MULTILINE)
    
    scenes = []
    current_text = []
    word_count = 0
    part_num = 1
    
    # parts[0] is any text before the first speaker
    if parts[0].strip():
        current_text.append(parts[0].strip())
        word_count += len(parts[0].split())
    
    for i in range(1, len(parts), 2):
        speaker_tag = parts[i] if i < len(parts) else ""
        dialogue = parts[i + 1] if i + 1 < len(parts) else ""
        block = f"{speaker_tag}{dialogue}".strip()
        block_words = len(block.split())
        
        if word_count + block_words > MAX_WORDS_PER_SCENE and word_count >= MIN_WORDS_PER_SCENE:
            # Flush current scene
            scenes.append({
                "content": "\n".join(current_text),
                "type": "timestamped_scene",
                "header": f"{scene_title} (Part {part_num})" if scene_title else f"Scene ({start_time} – {end_time}, Part {part_num})",
                "time_range": f"{start_time} – {end_time}",
                "speakers": _extract_speakers_from_content("\n".join(current_text))
            })
            current_text = [block]
            word_count = block_words
            part_num += 1
        else:
            current_text.append(block)
            word_count += block_words
    
    # Flush remaining
    if current_text:
        scenes.append({
            "content": "\n".join(current_text),
            "type": "timestamped_scene",
            "header": f"{scene_title} (Part {part_num})" if scene_title and part_num > 1 else (scene_title or f"Scene ({start_time} – {end_time})"),
            "time_range": f"{start_time} – {end_time}",
            "speakers": _extract_speakers_from_content("\n".join(current_text))
        })
    
    return scenes


def _extract_speakers_from_content(text):
    """Extract speaker names from content (ALL CAPS followed by colon)"""
    names = re.findall(r'^([A-Z][A-Z\s]{1,}):', text, re.MULTILINE)
    return list(set(name.strip() for name in names))


def _segment_screenplay(text):
    """
    Segment screenplay by scene headers (INT., EXT., etc.)
    
    Args:
        text (str): Screenplay text
        
    Returns:
        list: Segmented scenes
    """
    # Create regex pattern from scene markers
    markers_pattern = "|".join(re.escape(marker) for marker in SCENE_MARKERS)
    scene_pattern = rf"({markers_pattern}[^\n]+)"
    
    # Split by scene headers
    parts = re.split(scene_pattern, text, flags=re.IGNORECASE)
    
    scenes = []
    for i in range(1, len(parts), 2):
        if i+1 < len(parts):
            header = parts[i].strip()
            content = parts[i+1].strip()
            
            if content:  # Only add non-empty scenes
                scenes.append({
                    "header": header,
                    "content": content,
                    "type": "screenplay_scene",
                    "location": _extract_location(header)
                })
    
    # If no scenes found, fall back to generic segmentation
    if not scenes:
        return None
    
    # Filter out micro-scenes (junk from CUT TO:, FADE IN:, etc.)
    # Merge tiny scenes into the previous scene's content
    filtered = []
    for scene in scenes:
        word_count = len(scene["content"].split())
        if word_count < MIN_WORDS_PER_SCENE and filtered:
            # Merge this tiny scene into the previous one
            filtered[-1]["content"] += "\n\n" + scene["content"]
        elif word_count < 3:
            # Skip 1-2 word junk entirely (like ":" or ".")
            continue
        else:
            filtered.append(scene)
    
    return filtered if filtered else None

def _extract_location(header):
    """Extract location from scene header"""
    # Remove common prefixes
    location = re.sub(r"^(INT\.|EXT\.|INTERIOR|EXTERIOR)\s*", "", header, flags=re.IGNORECASE)
    # Extract first part before dash or period
    location = re.split(r"[-\.]", location)[0].strip()
    return location if location else "UNKNOWN"

def _segment_dialogue(text):
    """
    Segment by speaker changes (for dialogue-heavy scripts)
    
    Args:
        text (str): Dialogue script text
        
    Returns:
        list: Segmented dialogue blocks
    """
    # Split by character names (ALL CAPS followed by colon)
    dialogue_pattern = r"(^[A-Z][A-Z\s]{1,}:)"
    parts = re.split(dialogue_pattern, text, flags=re.MULTILINE)
    
    scenes = []
    current_scene = []
    current_speakers = []
    word_count = 0
    
    # Handle preamble text (before first speaker)
    if parts[0].strip() and len(parts[0].strip().split()) > MIN_WORDS_PER_SCENE:
        scenes.append({
            "content": parts[0].strip(),
            "type": "preamble",
            "speakers": [],
            "speaker_count": 0
        })
    
    for i in range(1, len(parts), 2):
        if i+1 < len(parts):
            speaker = parts[i].strip().rstrip(':')
            dialogue = parts[i+1].strip()
            
            current_scene.append(f"{speaker}: {dialogue}")
            current_speakers.append(speaker)
            word_count += len(dialogue.split())
            
            # Create scene if word limit reached
            if word_count >= MAX_WORDS_PER_SCENE:
                scenes.append({
                    "content": "\n".join(current_scene),
                    "type": "dialogue_block",
                    "speakers": list(set(current_speakers)),
                    "speaker_count": len(set(current_speakers))
                })
                current_scene = []
                current_speakers = []
                word_count = 0
    
    # Add remaining content
    if current_scene:
        scenes.append({
            "content": "\n".join(current_scene),
            "type": "dialogue_block",
            "speakers": list(set(current_speakers)),
            "speaker_count": len(set(current_speakers))
        })
    
    return scenes if scenes else None

def _segment_by_acts(text):
    """
    Segment by acts and scenes
    
    Args:
        text (str): Script with act structure
        
    Returns:
        list: Segmented by acts/scenes
    """
    # Split by ACT or SCENE markers
    act_pattern = r"((?:ACT|SCENE)\s+[IVX\d]+[^\n]*)"
    parts = re.split(act_pattern, text, flags=re.IGNORECASE)
    
    scenes = []
    for i in range(1, len(parts), 2):
        if i+1 < len(parts):
            header = parts[i].strip()
            content = parts[i+1].strip()
            
            # Further segment long acts into smaller scenes
            if len(content.split()) > MAX_WORDS_PER_SCENE * 2:
                subscenes = _segment_generic(content)
                for j, subscene in enumerate(subscenes):
                    scenes.append({
                        "header": f"{header} - Part {j+1}",
                        "content": subscene["content"],
                        "type": "act_segment"
                    })
            else:
                scenes.append({
                    "header": header,
                    "content": content,
                    "type": "act_segment"
                })
    
    return scenes if scenes else None

def _segment_generic(text, max_words=MAX_WORDS_PER_SCENE):
    """
    Generic segmentation by word count with sentence awareness
    
    Args:
        text (str): Text to segment
        max_words (int): Maximum words per scene
        
    Returns:
        list: Segmented scenes
    """
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    scenes = []
    current_scene = []
    word_count = 0
    
    for sentence in sentences:
        if not sentence.strip():
            continue
            
        sentence_words = len(sentence.split())
        
        # Check if adding this sentence would exceed limit
        if word_count + sentence_words > max_words and word_count >= MIN_WORDS_PER_SCENE:
            scenes.append({
                "content": " ".join(current_scene),
                "type": "segment",
                "word_count": word_count
            })
            current_scene = [sentence]
            word_count = sentence_words
        else:
            current_scene.append(sentence)
            word_count += sentence_words
    
    # Add remaining content
    if current_scene:
        scenes.append({
            "content": " ".join(current_scene),
            "type": "segment",
            "word_count": word_count
        })
    
    return scenes