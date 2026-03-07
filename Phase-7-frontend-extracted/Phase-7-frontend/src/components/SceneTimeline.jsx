import { useState } from 'react'
import SceneDetail from './SceneDetail'

const CHECK_KEYS = [
    { key: 'schema_check', short: 'SCH' },
    { key: 'confidence_check', short: 'CNF' },
    { key: 'consistency_check', short: 'CNS' },
    { key: 'drift_status', short: 'DRF' },
    { key: 'conflict_check', short: 'CFT' },
    { key: 'stability_check', short: 'STB' },
    { key: 'narrative_validation', short: 'NAR' },
]

export default function SceneTimeline({ data }) {
    const [selectedScene, setSelectedScene] = useState(null)

    if (!data || !data.verdicts) return null

    const handleSelect = (scene) => {
        setSelectedScene(prev => prev?.scene_id === scene.scene_id ? null : scene)
    }

    return (
        <div>
            {/* Legend */}
            <div className="glass-card" style={{ padding: '12px 18px', marginBottom: 16, display: 'flex', gap: 16, alignItems: 'center', flexWrap: 'wrap' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>LEGEND:</span>
                {CHECK_KEYS.map(c => (
                    <span key={c.key} style={{ fontSize: '0.72rem', color: 'var(--text-secondary)' }}>
                        <strong>{c.short}</strong> = {c.key.replace(/_/g, ' ')}
                    </span>
                ))}
                <span style={{ fontSize: '0.72rem', color: 'var(--text-secondary)' }}>
                    <strong>COH</strong> = coherence
                </span>
            </div>

            {/* Timeline rows */}
            <div className="timeline-container">
                {data.verdicts.map((scene) => (
                    <div
                        key={scene.scene_id}
                        className={`timeline-row ${selectedScene?.scene_id === scene.scene_id ? 'selected' : ''}`}
                        onClick={() => handleSelect(scene)}
                    >
                        <span className="scene-id">{scene.scene_id}</span>

                        <div className="timeline-checks">
                            {CHECK_KEYS.map(c => (
                                <span
                                    key={c.key}
                                    className={`check-pill ${scene[c.key]}`}
                                    data-tooltip={`${c.key.replace(/_/g, ' ')}: ${scene[c.key]}`}
                                >
                                    {c.short}
                                </span>
                            ))}

                            {/* Coherence as a special pill */}
                            <span
                                className={`check-pill ${scene.coherence_score >= 0.8 ? 'PASS' : scene.coherence_score >= 0.5 ? 'WARN' : 'FAIL'}`}
                                data-tooltip={`coherence: ${scene.coherence_score}`}
                            >
                                COH
                            </span>
                        </div>

                        <span className="emotion-tag" style={{ fontSize: '0.68rem' }}>
                            {scene.human_alignment_trend || '—'}
                        </span>

                        <span className={`timeline-verdict ${scene.final_verdict}`}>
                            {scene.final_verdict}
                        </span>
                    </div>
                ))}
            </div>

            {/* Detail panel */}
            {selectedScene && (
                <SceneDetail
                    scene={selectedScene}
                    onClose={() => setSelectedScene(null)}
                />
            )}
        </div>
    )
}
