export default function SceneDetail({ scene, onClose }) {
    if (!scene) return null

    const checks = [
        { label: 'Schema', value: scene.schema_check },
        { label: 'Confidence', value: scene.confidence_check },
        { label: 'Consistency', value: scene.consistency_check },
        { label: 'Drift', value: scene.drift_status },
        { label: 'Conflict', value: scene.conflict_check },
        { label: 'Stability', value: scene.stability_check },
        { label: 'Narrative', value: scene.narrative_validation },
        { label: 'Alignment', value: scene.human_alignment_trend === 'stable' ? 'PASS' : 'WARN' },
        { label: 'Verdict', value: scene.final_verdict },
    ]

    const details = scene.details || {}
    const conflictDetails = details.conflict_details || {}
    const consistencyDetails = details.consistency_details || {}
    const groupVariances = consistencyDetails.group_variances || {}

    // Collect all issues
    const allIssues = [
        ...(details.schema_issues || []),
        ...(details.hierarchy_issues || []),
        ...(details.confidence_issues || []),
        ...(details.drift_issues || []),
        ...(conflictDetails.all_issues || []),
        ...(details.narrative_issues || []),
    ]

    const coherenceScore = scene.coherence_score ?? 0
    const coherenceClass = coherenceScore >= 0.8 ? 'high' : coherenceScore >= 0.5 ? 'medium' : 'low'

    return (
        <div className="detail-panel glass-card">
            <div className="detail-header">
                <h3>🔍 {scene.scene_id} — Detail View</h3>
                <button className="detail-close" onClick={onClose}>✕</button>
            </div>

            {/* 9-check grid */}
            <div className="checks-grid">
                {checks.map(c => (
                    <div key={c.label} className="check-card">
                        <div className="check-name">{c.label}</div>
                        <div className={`check-status ${c.value}`}>{c.value}</div>
                    </div>
                ))}
            </div>

            {/* Coherence gauge */}
            <div className="glass-card" style={{ padding: 18, marginBottom: 16 }}>
                <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--text-muted)', fontWeight: 600, marginBottom: 8 }}>
                    Coherence Score
                </div>
                <div className="coherence-gauge">
                    <div className="gauge-bar">
                        <div className={`gauge-fill ${coherenceClass}`} style={{ width: `${coherenceScore * 100}%` }} />
                    </div>
                    <span className="gauge-value">{(coherenceScore * 100).toFixed(0)}%</span>
                </div>
            </div>

            {/* Drift score */}
            {details.drift_score !== undefined && (
                <div className="glass-card" style={{ padding: 18, marginBottom: 16 }}>
                    <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--text-muted)', fontWeight: 600, marginBottom: 8 }}>
                        Drift Score
                    </div>
                    <div style={{ display: 'flex', alignItems: 'baseline', gap: 8 }}>
                        <span style={{ fontSize: '1.5rem', fontWeight: 800, color: details.drift_score <= 0.3 ? 'var(--pass)' : details.drift_score <= 0.6 ? 'var(--warn)' : 'var(--fail)' }}>
                            {details.drift_score.toFixed(4)}
                        </span>
                        <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                            {details.drift_score <= 0.3 ? '(Low — stable)' : details.drift_score <= 0.6 ? '(Moderate)' : '(High — unstable)'}
                        </span>
                    </div>
                </div>
            )}

            {/* Conflict breakdown */}
            {conflictDetails.overall && (
                <div className="glass-card" style={{ padding: 18, marginBottom: 16 }}>
                    <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--text-muted)', fontWeight: 600, marginBottom: 12 }}>
                        Conflict Breakdown
                    </div>
                    <div className="checks-grid">
                        {['color_conflict', 'intensity_conflict', 'movement_conflict', 'preset_compliance'].map(key => {
                            const sub = conflictDetails[key]
                            if (!sub) return null
                            return (
                                <div key={key} className="check-card">
                                    <div className="check-name">{key.replace(/_/g, ' ')}</div>
                                    <div className={`check-status ${sub.verdict}`}>{sub.verdict}</div>
                                    {sub.issues && sub.issues.length > 0 && (
                                        <div style={{ fontSize: '0.68rem', color: 'var(--warn)', marginTop: 6 }}>
                                            {sub.issues.length} issue(s)
                                        </div>
                                    )}
                                </div>
                            )
                        })}
                    </div>
                </div>
            )}

            {/* Emotion consistency table */}
            {Object.keys(groupVariances).length > 0 && (
                <div className="glass-card" style={{ padding: 18, marginBottom: 16 }}>
                    <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--text-muted)', fontWeight: 600, marginBottom: 8 }}>
                        Emotion Consistency ({consistencyDetails.total_emotions} emotions)
                    </div>
                    <table className="variance-table">
                        <thead>
                            <tr>
                                <th>Emotion</th>
                                <th>Variance</th>
                                <th>Mean Intensity</th>
                                <th>Count</th>
                            </tr>
                        </thead>
                        <tbody>
                            {Object.entries(groupVariances).map(([emotion, stats]) => (
                                <tr key={emotion}>
                                    <td><span className="emotion-tag">{emotion}</span></td>
                                    <td>{stats.variance?.toFixed(6) ?? '—'}</td>
                                    <td>{stats.mean_intensity?.toFixed(2) ?? '—'}</td>
                                    <td>{stats.count ?? '—'}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            {/* Issues */}
            {allIssues.length > 0 && (
                <div className="issues-section">
                    <h4>⚠️ Issues ({allIssues.length})</h4>
                    {allIssues.map((issue, i) => (
                        <div key={i} className="issue-item">{issue}</div>
                    ))}
                </div>
            )}

            {allIssues.length === 0 && (
                <div style={{ textAlign: 'center', padding: '16px 0', color: 'var(--pass)', fontSize: '0.85rem' }}>
                    ✅ No issues found for this scene
                </div>
            )}
        </div>
    )
}
