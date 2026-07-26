import { useState } from 'react'
import { askQuestion } from './api'
import RiskBadge from './components/RiskBadge'
import QualityBadge from './components/QualityBadge'
import EvidencePanel from './components/EvidencePanel'
import TrustGauge from './components/TrustGauge'
import TrustRadar from './components/TrustRadar'
import Recommendations from './components/Recommendations'
import Timing from './components/Timing'

export default function App() {
  const [question, setQuestion] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleAsk() {
    if (!question.trim()) return
    setLoading(true)
    setError(null)
    try {
      const data = await askQuestion(question)
      setResult(data)
    } catch (err) {
      setError(err.message)
      setResult(null)
    } finally {
      setLoading(false)
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter') handleAsk()
  }

  return (
    <div className="app">
      <header>
        <h1>TrustShield AI</h1>
        <p className="subtitle">
          A hybrid trust layer for retrieval-augmented LLM answers — prompt risk, retrieval
          quality, and a composite Trust Score with explainable recommendations.
        </p>
      </header>

      <div className="ask-bar">
        <input
          type="text"
          placeholder="Ask a question about the documents in docs/"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button onClick={handleAsk} disabled={loading}>
          {loading ? 'Thinking…' : 'Ask'}
        </button>
      </div>

      {error && <div className="error-box">{error}</div>}

      {result && (
        <>
          <div className="columns">
            <section className="panel">
              <h2>Answer</h2>
              <p className="answer-text">{result.answer}</p>
              <RiskBadge promptRisk={result.prompt_risk} />
            </section>

            <section className="panel">
              <h2>Retrieved Evidence</h2>
              <QualityBadge retrievalQuality={result.retrieval_quality} />
              <EvidencePanel chunks={result.chunks} />
            </section>
          </div>

          <section className="panel">
            <h2>Trust Score</h2>
            <div className="columns">
              <TrustGauge score={result.trust_score} level={result.trust_level} />
              <TrustRadar radar={result.radar} />
            </div>
          </section>

          <section className="panel">
            <h2>Recommendations</h2>
            <Recommendations recommendations={result.recommendations} />
          </section>

          <section className="panel">
            <h2>Timing</h2>
            <Timing timings={result.timings} />
          </section>
        </>
      )}
    </div>
  )
}
