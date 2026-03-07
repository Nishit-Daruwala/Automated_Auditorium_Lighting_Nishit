export default function OverviewDashboard({ data }) {
    if (!data) return null

    const { total_scenes, pass_count, warn_count, fail_count, overall_verdict, can_proceed, timestamp } = data

    // Donut chart calculations
    const total = pass_count + warn_count + fail_count
    const radius = 62
    const circumference = 2 * Math.PI * radius
    const passArc = (pass_count / total) * circumference
    const warnArc = (warn_count / total) * circumference
    const failArc = (fail_count / total) * circumference

    // Compute aggregate stats from verdicts
    const avgCoherence = data.verdicts && data.verdicts.length > 0
        ? (data.verdicts.reduce((sum, v) => sum + (v.coherence_score || 0), 0) / data.verdicts.length).toFixed(2)
        : 'N/A'

    const avgDrift = data.verdicts && data.verdicts.length > 0
        ? (data.verdicts.reduce((sum, v) => sum + (v.details?.drift_score || 0), 0) / data.verdicts.length).toFixed(4)
        : 'N/A'

    const totalConflicts = data.verdicts
        ? data.verdicts.reduce((sum, v) => sum + (v.details?.conflict_details?.total_conflicts || 0), 0)
        : 0

    return (
        <div>
            {/* Verdict hero */}
            <div className={`glass-card verdict-hero verdict-${overall_verdict}`}>
                <div className={`verdict-badge ${overall_verdict}`}>
                    {overall_verdict === 'PASS' && '✅'}
                    {overall_verdict === 'WARN' && '⚠️'}
                    {overall_verdict === 'FAIL' && '❌'}
                    {' '}{overall_verdict}
                </div>
                <div className="verdict-sub">
                    Overall evaluation verdict for {total_scenes} scenes
                </div>
                <div className={`can-proceed ${can_proceed ? 'yes' : 'no'}`}>
                    {can_proceed ? '🟢 Pipeline Can Proceed' : '🔴 Pipeline Blocked'}
                </div>
            </div>

            {/* Stats grid */}
            <div className="overview-grid" style={{ marginTop: 20 }}>
                <div className="glass-card stat-card">
                    <div className="stat-label">Total Scenes</div>
                    <div className="stat-value">{total_scenes}</div>
                    <div className="stat-sub">Evaluated in this run</div>
                </div>
                <div className="glass-card stat-card">
                    <div className="stat-label">Passed</div>
                    <div className="stat-value" style={{ color: 'var(--pass)' }}>{pass_count}</div>
                    <div className="stat-sub">{total > 0 ? ((pass_count / total) * 100).toFixed(0) : 0}% of scenes</div>
                </div>
                <div className="glass-card stat-card">
                    <div className="stat-label">Warnings</div>
                    <div className="stat-value" style={{ color: 'var(--warn)' }}>{warn_count}</div>
                    <div className="stat-sub">{total > 0 ? ((warn_count / total) * 100).toFixed(0) : 0}% of scenes</div>
                </div>
                <div className="glass-card stat-card">
                    <div className="stat-label">Failed</div>
                    <div className="stat-value" style={{ color: 'var(--fail)' }}>{fail_count}</div>
                    <div className="stat-sub">{total > 0 ? ((fail_count / total) * 100).toFixed(0) : 0}% of scenes</div>
                </div>
            </div>

            {/* Donut + Aggregates row */}
            <div className="glass-card donut-section">
                <div className="donut-wrapper">
                    <svg viewBox="0 0 140 140">
                        {/* Pass arc */}
                        <circle
                            cx="70" cy="70" r={radius}
                            fill="none"
                            stroke="var(--pass)"
                            strokeWidth="14"
                            strokeDasharray={`${passArc} ${circumference - passArc}`}
                            strokeDashoffset="0"
                            strokeLinecap="round"
                        />
                        {/* Warn arc */}
                        <circle
                            cx="70" cy="70" r={radius}
                            fill="none"
                            stroke="var(--warn)"
                            strokeWidth="14"
                            strokeDasharray={`${warnArc} ${circumference - warnArc}`}
                            strokeDashoffset={`${-passArc}`}
                            strokeLinecap="round"
                        />
                        {/* Fail arc */}
                        <circle
                            cx="70" cy="70" r={radius}
                            fill="none"
                            stroke="var(--fail)"
                            strokeWidth="14"
                            strokeDasharray={`${failArc} ${circumference - failArc}`}
                            strokeDashoffset={`${-(passArc + warnArc)}`}
                            strokeLinecap="round"
                        />
                        {/* Background ring for zero-count edge case */}
                        {total === 0 && (
                            <circle
                                cx="70" cy="70" r={radius}
                                fill="none"
                                stroke="rgba(255,255,255,0.06)"
                                strokeWidth="14"
                            />
                        )}
                    </svg>
                    <div className="donut-center">
                        <div className="donut-total">{total}</div>
                        <div className="donut-label">Scenes</div>
                    </div>
                </div>

                <div className="donut-legend">
                    <div className="legend-item">
                        <span className="legend-dot pass" />
                        Pass
                        <span className="legend-count">{pass_count}</span>
                    </div>
                    <div className="legend-item">
                        <span className="legend-dot warn" />
                        Warning
                        <span className="legend-count">{warn_count}</span>
                    </div>
                    <div className="legend-item">
                        <span className="legend-dot fail" />
                        Fail
                        <span className="legend-count">{fail_count}</span>
                    </div>
                </div>
            </div>

            {/* Aggregate metrics */}
            <div className="overview-grid" style={{ marginTop: 20 }}>
                <div className="glass-card stat-card">
                    <div className="stat-label">Avg. Coherence</div>
                    <div className="stat-value" style={{ fontSize: '1.6rem' }}>{avgCoherence}</div>
                    <div className="coherence-gauge">
                        <div className="gauge-bar">
                            <div
                                className={`gauge-fill ${avgCoherence >= 0.8 ? 'high' : avgCoherence >= 0.5 ? 'medium' : 'low'}`}
                                style={{ width: `${(parseFloat(avgCoherence) || 0) * 100}%` }}
                            />
                        </div>
                    </div>
                </div>
                <div className="glass-card stat-card">
                    <div className="stat-label">Avg. Drift Score</div>
                    <div className="stat-value" style={{ fontSize: '1.6rem' }}>{avgDrift}</div>
                    <div className="stat-sub">Lower is better (0 = no drift)</div>
                </div>
                <div className="glass-card stat-card">
                    <div className="stat-label">Total Conflicts</div>
                    <div className="stat-value" style={{ fontSize: '1.6rem', color: totalConflicts > 0 ? 'var(--warn)' : 'var(--pass)' }}>
                        {totalConflicts}
                    </div>
                    <div className="stat-sub">Across all scenes</div>
                </div>
                <div className="glass-card stat-card">
                    <div className="stat-label">Report Time</div>
                    <div className="stat-value" style={{ fontSize: '1rem' }}>
                        {timestamp ? new Date(timestamp).toLocaleString() : 'N/A'}
                    </div>
                    <div className="stat-sub">Evaluation run timestamp</div>
                </div>
            </div>
        </div>
    )
}
