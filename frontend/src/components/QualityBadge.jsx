function colorFor(score) {
  if (score >= 0.6) return '#28a745'
  if (score >= 0.35) return '#fd7e14'
  return '#dc3545'
}

export default function QualityBadge({ retrievalQuality }) {
  const color = colorFor(retrievalQuality.score)

  return (
    <div className="badge-block">
      <span className="badge" style={{ backgroundColor: color }}>
        Retrieval Quality: {retrievalQuality.score.toFixed(2)}
      </span>
      <details>
        <summary>Quality breakdown</summary>
        <pre>{JSON.stringify(retrievalQuality, null, 2)}</pre>
      </details>
    </div>
  )
}
