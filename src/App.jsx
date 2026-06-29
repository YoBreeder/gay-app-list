import { useState } from 'react'
import { regions } from './data/apps'
import './App.css'

function AppCard({ app, onClick }) {
  return (
    <div className={`app-card ${app.status === 'defunct' ? 'defunct' : ''}`} onClick={() => onClick(app)}>
      <div className="app-card-header">
        <h3>{app.name}</h3>
        {app.status === 'defunct' && <span className="badge">Defunct</span>}
      </div>
      <div className="app-meta">
        <span>📍 {app.country}</span>
        <span>📅 {app.founded}</span>
      </div>
      <p className="audience">👥 {app.audience}</p>
      <p className="description">{app.description}</p>
      <div className="app-links">
        {app.website && <span className="link-chip">🌐 Website</span>}
        {app.appStore && <span className="link-chip">🍎 iOS</span>}
        {app.playStore && <span className="link-chip">🤖 Android</span>}
      </div>
    </div>
  )
}

function AppModal({ app, onClose }) {
  if (!app) return null
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>✕</button>
        <h2>{app.name}</h2>
        {app.status === 'defunct' && <span className="badge">Defunct</span>}
        <div className="modal-meta">
          <span>📍 {app.country}</span>
          <span>📅 Founded {app.founded}</span>
        </div>
        <p className="modal-audience">👥 {app.audience}</p>
        <p className="modal-description">{app.description}</p>
        <div className="modal-links">
          {app.website && <a href={app.website} target="_blank" rel="noopener noreferrer">🌐 Visit Website</a>}
          {app.appStore && <a href={app.appStore} target="_blank" rel="noopener noreferrer">🍎 App Store</a>}
          {app.playStore && <a href={app.playStore} target="_blank" rel="noopener noreferrer">🤖 Google Play</a>}
          {!app.website && !app.appStore && !app.playStore && (
            <p className="no-links">This app is no longer available.</p>
          )}
        </div>
      </div>
    </div>
  )
}

function App() {
  const [selectedApp, setSelectedApp] = useState(null)
  const [search, setSearch] = useState('')

  const totalApps = regions.reduce((sum, r) => sum + r.apps.length, 0)

  const filtered = regions.map(region => ({
    ...region,
    apps: region.apps.filter(app =>
      app.name.toLowerCase().includes(search.toLowerCase()) ||
      app.country.toLowerCase().includes(search.toLowerCase()) ||
      app.audience.toLowerCase().includes(search.toLowerCase()) ||
      app.description.toLowerCase().includes(search.toLowerCase())
    ),
  })).filter(region => region.apps.length > 0)

  return (
    <div className="app">
      <header className="hero-header">
        <div className="brand">
          <span className="brand-flag">🏳️‍🌈</span>
          <div className="brand-text">
            <h1><span className="brand-gay">Gay</span><span className="brand-app"> App</span><span className="brand-list"> List</span></h1>
            <p className="brand-tagline">The world's only LGBTQ+ app directory</p>
          </div>
        </div>
        <p className="count">{totalApps} apps across {regions.length} regions</p>
        <input
          className="search"
          type="text"
          placeholder="Search by name, country, or community..."
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
      </header>

      <main>
        {filtered.map(region => (
          <section key={region.name} className="region">
            <h2 className="region-title">{region.name}</h2>
            <div className="apps-grid">
              {region.apps.map(app => (
                <AppCard key={app.name} app={app} onClick={setSelectedApp} />
              ))}
            </div>
          </section>
        ))}
        {filtered.length === 0 && (
          <div className="no-results">No apps found for "{search}"</div>
        )}
      </main>

      <footer>
        <p>🏳️‍🌈 <strong>Gay App List</strong> — The most comprehensive LGBTQ+ app directory in the world</p>
      </footer>

      <AppModal app={selectedApp} onClose={() => setSelectedApp(null)} />
    </div>
  )
}

export default App
