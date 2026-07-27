import { useState } from 'react'

export default function Header() {
  const [logoFailed, setLogoFailed] = useState(false)

  return (
    <header className="navbar">
      <div className="navbar-inner">
        <div className="brand">
          <span className="brand-mark" aria-hidden="true">TS</span>
          <div className="brand-text">
            <span className="brand-name">TrustShield AI</span>
            <span className="brand-tag">Hybrid Trust Layer for RAG</span>
          </div>
        </div>

        <div className="college-block">
          <div className="college-text">
            <span className="college-name">Rajiv Gandhi Institute of Petroleum Technology</span>
            <span className="college-tag">B.Tech Project Demo</span>
          </div>
          {!logoFailed && (
            <img
              src="/rgipt-logo.png"
              alt="RGIPT logo"
              className="college-logo"
              onError={() => setLogoFailed(true)}
            />
          )}
        </div>
      </div>
    </header>
  )
}
