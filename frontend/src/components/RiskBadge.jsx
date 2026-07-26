function colorFor(score) {
  if (score >= 0.7) return '#dc3545'
  if (score >= 0.3) return '#fd7e14'
  return '#28a745'
}

export default function RiskBadge({ promptRisk }) {
  const color = colorFor(promptRisk.risk_score)

  return (
    <div className="badge-block">
      <span className="badge" style={{ backgroundColor: color }}>
        Prompt Risk: {promptRisk.risk_score.toFixed(2)} ({promptRisk.category})
      </span>
      <p className="reason">{promptRisk.reason}</p>
      <details>
        <summary>Signal breakdown</summary>
        <pre>{JSON.stringify(promptRisk.signals, null, 2)}</pre>
      </details>
    </div>
  )
}
