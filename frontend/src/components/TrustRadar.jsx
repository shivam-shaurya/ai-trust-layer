import {
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  ResponsiveContainer,
} from 'recharts'

export default function TrustRadar({ radar }) {
  const data = radar.categories.map((category, i) => ({
    category,
    value: radar.values[i],
    pending: radar.pending[i],
  }))

  const pendingLabels = data.filter((d) => d.pending).map((d) => d.category)

  return (
    <div className="radar-wrapper">
      <ResponsiveContainer width="100%" height={320}>
        <RadarChart data={data}>
          <PolarGrid />
          <PolarAngleAxis dataKey="category" tick={{ fontSize: 12 }} />
          <PolarRadiusAxis angle={90} domain={[0, 1]} tick={false} />
          <Radar
            name="Trust Signals"
            dataKey="value"
            stroke="#4a6cf7"
            fill="#4a6cf7"
            fillOpacity={0.4}
          />
        </RadarChart>
      </ResponsiveContainer>
      {pendingLabels.length > 0 && (
        <p className="radar-caption">
          Pending Milestone 3 (shown as neutral placeholders): {pendingLabels.join(', ')}.
        </p>
      )}
    </div>
  )
}
