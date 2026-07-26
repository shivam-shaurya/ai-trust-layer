export default function Timing({ timings }) {
  const stages = Object.entries(timings).filter(([key]) => key !== 'total')
  const maxSeconds = Math.max(...stages.map(([, seconds]) => seconds))

  return (
    <div className="timing">
      {stages.map(([stage, seconds]) => (
        <div className="timing-row" key={stage}>
          <span className="timing-label">{stage}</span>
          <div className="timing-bar-track">
            <div
              className="timing-bar-fill"
              style={{ width: `${(seconds / maxSeconds) * 100}%` }}
            />
          </div>
          <span className="timing-value">{seconds.toFixed(2)}s</span>
        </div>
      ))}
      <div className="timing-total">Total: {timings.total.toFixed(2)}s</div>
    </div>
  )
}
