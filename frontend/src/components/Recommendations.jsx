export default function Recommendations({ recommendations }) {
  return (
    <ul className="recommendations">
      {recommendations.map((rec) => (
        <li key={rec}>{rec}</li>
      ))}
    </ul>
  )
}
