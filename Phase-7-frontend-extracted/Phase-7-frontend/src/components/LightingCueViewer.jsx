import { useState } from 'react'

export default function LightingCueViewer({ data }) {
    const [expandedScene, setExpandedScene] = useState(null)

    if (!data || !data.instructions) {
        return (
            <div className="empty-state">
                <div className="empty-icon">💡</div>
                <p>No lighting cue data available</p>
            </div>
        )
    }

    const toggleExpand = (sceneId) => {
        setExpandedScene(prev => prev === sceneId ? null : sceneId)
    }

    return (
        <div className="cue-cards">
            {data.instructions.map((instruction) => {
                const meta = instruction.metadata || {}
                const graphMeta = meta.graph_metadata || {}
                const isExpanded = expandedScene === instruction.scene_id

                return (
                    <div key={instruction.scene_id} className="glass-card cue-card">
                        {/* Header */}
                        <div className="cue-card-header">
                            <span className="cue-scene-id">🎬 {instruction.scene_id}</span>
                            <div className="cue-meta-tags">
                                {meta.emotion && (
                                    <span className="cue-tag emotion">{meta.emotion}</span>
                                )}
                                {meta.technique && (
                                    <span className="cue-tag technique">{meta.technique.replace(/_/g, ' ')}</span>
                                )}
                                {meta.generation_method && (
                                    <span className="cue-tag method">{meta.generation_method.replace(/_/g, ' ')}</span>
                                )}
                            </div>
                        </div>

                        {/* Time window */}
                        {instruction.time_window && (
                            <div className="time-window">
                                🕐 {formatTime(instruction.time_window.start)} → {formatTime(instruction.time_window.end)}
                                <span style={{ marginLeft: 8, color: 'var(--text-secondary)' }}>
                                    ({(instruction.time_window.end - instruction.time_window.start).toFixed(0)}s)
                                </span>
                            </div>
                        )}

                        {/* Strategy summary */}
                        {meta.strategy_summary && (
                            <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: 16, fontStyle: 'italic' }}>
                                "{meta.strategy_summary}"
                            </p>
                        )}

                        {/* Fixture groups */}
                        <div className="fixture-groups">
                            {(instruction.groups || []).map((group, gi) => (
                                <div key={gi} className="fixture-group">
                                    <div className="fixture-group-id">{group.group_id}</div>

                                    {/* Intensity bar */}
                                    <div className="intensity-bar-wrapper">
                                        <span className="intensity-bar-label">Intensity</span>
                                        <div className="intensity-bar">
                                            <div
                                                className="intensity-bar-fill"
                                                style={{ width: `${(group.parameters?.intensity || 0) * 100}%` }}
                                            />
                                        </div>
                                        <span className="intensity-bar-value">
                                            {((group.parameters?.intensity || 0) * 100).toFixed(0)}%
                                        </span>
                                    </div>

                                    {/* Params */}
                                    <div className="fixture-params">
                                        {group.parameters?.color && (
                                            <span className="param-chip">
                                                🎨 {group.parameters.color.replace(/_/g, ' ')}
                                            </span>
                                        )}
                                        {group.parameters?.focus_area && (
                                            <span className="param-chip">
                                                🎯 {group.parameters.focus_area.replace(/_/g, ' ')}
                                            </span>
                                        )}
                                        {group.transition && (
                                            <span className="param-chip">
                                                ⏱ {group.transition.type} ({group.transition.duration}s)
                                            </span>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>

                        {/* Expand/collapse toggle for graph details */}
                        <button
                            onClick={() => toggleExpand(instruction.scene_id)}
                            style={{
                                background: 'none',
                                border: '1px solid var(--glass-border)',
                                color: 'var(--text-secondary)',
                                padding: '6px 14px',
                                borderRadius: 'var(--radius-sm)',
                                fontSize: '0.78rem',
                                cursor: 'pointer',
                                fontFamily: 'inherit',
                                fontWeight: 500,
                                transition: 'all 0.15s ease',
                                marginBottom: isExpanded ? 14 : 0,
                            }}
                        >
                            {isExpanded ? '▾ Hide' : '▸ Show'} Graph RAG Details
                        </button>

                        {/* Graph RAG details (collapsible) */}
                        {isExpanded && graphMeta.path_nodes && (
                            <div className="graph-path-section">
                                <h5>Graph Path</h5>

                                {/* Path chain */}
                                <div className="path-chain">
                                    {graphMeta.path_nodes.map((node, ni) => (
                                        <span key={ni} style={{ display: 'contents' }}>
                                            <span className="path-node">{node.replace(/_/g, ' ')}</span>
                                            {ni < graphMeta.path_nodes.length - 1 && (
                                                <span className="path-arrow">→</span>
                                            )}
                                        </span>
                                    ))}
                                </div>

                                {/* Score & alternatives */}
                                <div style={{ display: 'flex', gap: 20, flexWrap: 'wrap', marginTop: 8 }}>
                                    <div className="path-score">
                                        Path Score: <strong>{graphMeta.path_score}</strong>
                                    </div>
                                    {graphMeta.alternatives_count !== undefined && (
                                        <div className="path-score">
                                            Alternatives: <strong>{graphMeta.alternatives_count}</strong>
                                        </div>
                                    )}
                                    {graphMeta.fallback_used !== undefined && (
                                        <div className="path-score">
                                            Fallback: <strong style={{ color: graphMeta.fallback_used ? 'var(--warn)' : 'var(--pass)' }}>
                                                {graphMeta.fallback_used ? 'Yes' : 'No'}
                                            </strong>
                                        </div>
                                    )}
                                </div>

                                {/* Safety checks */}
                                {graphMeta.safety_checks && graphMeta.safety_checks.length > 0 && (
                                    <div className="safety-badges">
                                        {graphMeta.safety_checks.map((check, ci) => {
                                            const isPassing = check.includes(':PASS')
                                            const label = check.split(':')[0]
                                            return (
                                                <span key={ci} className={`safety-badge ${isPassing ? 'pass' : 'fail'}`}>
                                                    {isPassing ? '✓' : '✕'} {label}
                                                </span>
                                            )
                                        })}
                                    </div>
                                )}

                                {/* Fixture types */}
                                {graphMeta.fixture_types_required && graphMeta.fixture_types_required.length > 0 && (
                                    <div style={{ marginTop: 10, display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                                        <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 600 }}>Fixtures:</span>
                                        {graphMeta.fixture_types_required.map((ft, fi) => (
                                            <span key={fi} className="param-chip">{ft}</span>
                                        ))}
                                    </div>
                                )}

                                {/* Provenance */}
                                {meta.provenance && meta.provenance.length > 0 && (
                                    <div style={{ marginTop: 12, fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                                        <strong>Provenance:</strong>
                                        {meta.provenance.map((p, pi) => (
                                            <div key={pi} style={{ marginTop: 3, paddingLeft: 12, color: 'var(--text-secondary)' }}>
                                                • {p}
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                )
            })}
        </div>
    )
}

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60)
    const secs = (seconds % 60).toFixed(0)
    return `${mins}:${secs.padStart(2, '0')}`
}
