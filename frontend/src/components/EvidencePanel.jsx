export default function EvidencePanel({ chunks }) {
  return (
    <div className="evidence-panel">
      {chunks.map((chunk) => (
        <details key={`${chunk.source}-${chunk.chunk_id}`} className="evidence-item">
          <summary>
            {chunk.source} #{chunk.chunk_id} — similarity {chunk.score.toFixed(3)}
          </summary>
          <p>{chunk.text}</p>
        </details>
      ))}
    </div>
  )
}
