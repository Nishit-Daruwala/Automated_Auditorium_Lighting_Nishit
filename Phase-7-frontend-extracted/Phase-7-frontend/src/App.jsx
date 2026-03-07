import { useState, useEffect } from 'react'
import OverviewDashboard from './components/OverviewDashboard'
import SceneTimeline from './components/SceneTimeline'
import LightingCueViewer from './components/LightingCueViewer'

const SCRIPTS = [
    { id: 'Script-8', label: 'Script 8 (16 scenes)' },
    { id: 'Script-5', label: 'Script 5 (18 scenes)' },
    { id: 'Script-1', label: 'Script 1 (5 scenes)' },
]

const TABS = [
    { id: 'overview', icon: '📊', label: 'Overview' },
    { id: 'timeline', icon: '🎬', label: 'Scene Timeline' },
    { id: 'cues', icon: '💡', label: 'Lighting Cues' },
]

export default function App() {
    const [activeTab, setActiveTab] = useState('overview')
    const [selectedScript, setSelectedScript] = useState('Script-8')
    const [evalData, setEvalData] = useState(null)
    const [cueData, setCueData] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        setLoading(true)
        Promise.all([
            fetch(`/data/${selectedScript}_evaluation.json`).then(r => r.json()),
            fetch(`/data/${selectedScript}_cues.json`).then(r => r.json()),
        ])
            .then(([evalJson, cueJson]) => {
                setEvalData(evalJson)
                setCueData(cueJson)
                setLoading(false)
            })
            .catch(err => {
                console.error('Failed to load data:', err)
                setLoading(false)
            })
    }, [selectedScript])

    const renderContent = () => {
        if (loading) {
            return (
                <div className="loading">
                    <div className="spinner" />
                </div>
            )
        }

        if (!evalData) {
            return (
                <div className="empty-state">
                    <div className="empty-icon">⚠️</div>
                    <p>Failed to load evaluation data</p>
                </div>
            )
        }

        switch (activeTab) {
            case 'overview':
                return <OverviewDashboard data={evalData} />
            case 'timeline':
                return <SceneTimeline data={evalData} />
            case 'cues':
                return <LightingCueViewer data={cueData} />
            default:
                return null
        }
    }

    const tabInfo = TABS.find(t => t.id === activeTab)

    return (
        <div className="app-layout">
            {/* Sidebar */}
            <aside className="sidebar">
                <div className="sidebar-brand">
                    <div className="brand-icon">🎭</div>
                    <h1>
                        Phase 7
                        <span>Evaluation Dashboard</span>
                    </h1>
                </div>

                {TABS.map(tab => (
                    <div
                        key={tab.id}
                        className={`nav-item ${activeTab === tab.id ? 'active' : ''}`}
                        onClick={() => setActiveTab(tab.id)}
                    >
                        <span className="nav-icon">{tab.icon}</span>
                        {tab.label}
                    </div>
                ))}

                <div className="script-selector">
                    <label>Report Source</label>
                    <select
                        value={selectedScript}
                        onChange={e => setSelectedScript(e.target.value)}
                    >
                        {SCRIPTS.map(s => (
                            <option key={s.id} value={s.id}>{s.label}</option>
                        ))}
                    </select>
                </div>
            </aside>

            {/* Main */}
            <main className="main-content">
                <div className="page-header">
                    <h2>{tabInfo?.icon} {tabInfo?.label}</h2>
                    <p>
                        Viewing <strong>{selectedScript.replace('-', ' ')}</strong> evaluation report
                        {evalData && ` • ${evalData.total_scenes} scenes • ${evalData.timestamp?.split('T')[0]}`}
                    </p>
                </div>
                {renderContent()}
            </main>
        </div>
    )
}
