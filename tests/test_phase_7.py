"""
Phase 7 unit tests.
IMPORTANT: Tests use PRE-GENERATED fixtures, never Phase 4 calls.
"""
import json
import pytest
from pathlib import Path
from uuid import UUID

from phase_7.trace_logger import TraceLogger
from phase_7.metrics import MetricsEngine
from phase_7.schemas import TraceEntry, RAGContextRef
from phase_7.evaluation.consistency import (
    compute_determinism_score,
    compute_jaccard_similarity,
    compute_drift_score,
    extract_group_ids
)
from phase_7.evaluation.coverage import (
    compute_group_coverage,
    compute_parameter_diversity
)

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "phase_7"


class TestTraceLogger:
    def test_hash_consistency(self):
        data = {"scene_id": "test", "intensity": 0.8}
        hash1 = TraceLogger.compute_hash(data)
        hash2 = TraceLogger.compute_hash(data)
        assert hash1 == hash2
    
    def test_hash_order_independence(self):
        data1 = {"a": 1, "b": 2}
        data2 = {"b": 2, "a": 1}
        assert TraceLogger.compute_hash(data1) == TraceLogger.compute_hash(data2)
    
    def test_log_decision(self, tmp_path):
        logger = TraceLogger(tmp_path, seed=42)
        scene = {"scene_id": "scene_001", "text": "Test"}
        instruction = {"scene_id": "scene_001", "groups": []}
        entry = logger.log_decision(scene, instruction)
        assert entry.scene_id == "scene_001"
        assert entry.seed == 42
        assert isinstance(entry.run_id, UUID)
    
    def test_log_with_rag_context(self, tmp_path):
        logger = TraceLogger(tmp_path)
        scene = {"scene_id": "scene_001", "text": "Test"}
        instruction = {"scene_id": "scene_001", "groups": []}
        rag_ctx = [{"document_id": "doc_001", "chunk_id": "chunk_003"}]
        entry = logger.log_decision(scene, instruction, rag_context_ids=rag_ctx)
        assert len(entry.rag_context_ids) == 1
        assert entry.rag_context_ids[0].document_id == "doc_001"
    
    def test_save_trace(self, tmp_path):
        logger = TraceLogger(tmp_path, seed=42)
        scene = {"scene_id": "scene_001", "text": "Test"}
        instruction = {"scene_id": "scene_001", "groups": []}
        logger.log_decision(scene, instruction)
        output_file = logger.save()
        assert output_file.exists()
        with open(output_file) as f:
            data = json.load(f)
        assert len(data["entries"]) == 1


class TestConsistencyMetrics:
    def test_identical_instructions(self):
        instr = {"groups": [{"group_id": "G1", "parameters": {"intensity": 0.8}}]}
        score, breakdown = compute_determinism_score(instr, instr)
        assert score == 1.0
        assert breakdown["group_match"] == 1.0
    
    def test_within_epsilon(self):
        instr_a = {"groups": [{"group_id": "G1", "parameters": {"intensity": 0.80}}]}
        instr_b = {"groups": [{"group_id": "G1", "parameters": {"intensity": 0.82}}]}
        score, breakdown = compute_determinism_score(instr_a, instr_b, epsilon=0.05)
        assert breakdown["intensity_matches"] == 1
    
    def test_outside_epsilon(self):
        instr_a = {"groups": [{"group_id": "G1", "parameters": {"intensity": 0.80}}]}
        instr_b = {"groups": [{"group_id": "G1", "parameters": {"intensity": 0.90}}]}
        score, breakdown = compute_determinism_score(instr_a, instr_b, epsilon=0.05)
        assert breakdown["intensity_matches"] == 0
    
    def test_jaccard_empty_sets(self):
        assert compute_jaccard_similarity(set(), set()) == 1.0
    
    def test_jaccard_identical_sets(self):
        s = {"a", "b", "c"}
        assert compute_jaccard_similarity(s, s) == 1.0
    
    def test_jaccard_disjoint_sets(self):
        s1 = {"a", "b"}
        s2 = {"c", "d"}
        assert compute_jaccard_similarity(s1, s2) == 0.0
    
    def test_drift_single_instruction(self):
        assert compute_drift_score([{"groups": []}]) == 0.0
    
    def test_extract_group_ids(self):
        instr = {"groups": [{"group_id": "G1"}, {"group_id": "G2"}]}
        ids = extract_group_ids(instr)
        assert ids == {"G1", "G2"}


class TestCoverageMetrics:
    def test_full_coverage(self):
        available = {"G1", "G2"}
        instr = {"groups": [{"group_id": "G1"}, {"group_id": "G2"}]}
        assert compute_group_coverage(instr, available) == 1.0
    
    def test_partial_coverage(self):
        available = {"G1", "G2", "G3"}
        instr = {"groups": [{"group_id": "G1"}, {"group_id": "G2"}]}
        assert compute_group_coverage(instr, available) == 2/3
    
    def test_empty_groups(self):
        available = {"G1", "G2"}
        instr = {"groups": []}
        assert compute_group_coverage(instr, available) == 0.0
    
    def test_parameter_diversity(self):
        instr = {
            "groups": [
                {"group_id": "G1", "parameters": {"intensity": 0.2, "color": "red"}, "transition": {"type": "fade"}},
                {"group_id": "G2", "parameters": {"intensity": 0.8, "color": "blue"}, "transition": {"type": "cut"}}
            ]
        }
        diversity = compute_parameter_diversity(instr)
        assert diversity["intensity_range"] == pytest.approx(0.6)
        assert diversity["transition_types"] == 2
        assert diversity["colors_used"] == 2


class TestMetricsEngine:
    def test_evaluate_instruction(self):
        engine = MetricsEngine(available_groups={"G1", "G2", "G3"})
        instruction = {"groups": [{"group_id": "G1"}, {"group_id": "G2"}]}
        result = engine.evaluate_instruction(instruction)
        assert result["coverage"] == 2/3
        assert "diversity" in result
    
    def test_evaluate_pair(self):
        engine = MetricsEngine()
        instr_a = {"groups": [{"group_id": "G1", "parameters": {"intensity": 0.5}}]}
        instr_b = {"groups": [{"group_id": "G1", "parameters": {"intensity": 0.5}}]}
        result = engine.evaluate_pair(instr_a, instr_b)
        assert result["determinism_score"] == 1.0


class TestFixtureLoading:
    def test_load_sample_scene(self):
        scene_file = FIXTURES_DIR / "sample_scene.json"
        if scene_file.exists():
            with open(scene_file) as f:
                scene = json.load(f)
            assert "scene_id" in scene
            assert "text" in scene
    
    def test_load_sample_instruction(self):
        instr_file = FIXTURES_DIR / "sample_instruction.json"
        if instr_file.exists():
            with open(instr_file) as f:
                instr = json.load(f)
            assert "groups" in instr
            assert len(instr["groups"]) > 0
