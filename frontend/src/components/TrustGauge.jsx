import { RadialBar, RadialBarChart, PolarAngleAxis } from 'recharts'

const LEVEL_COLORS = {
  'High Trust': '#28a745',
  'Moderate Trust': '#fd7e14',
  'Low Trust': '#dc3545',
}

export default function TrustGauge({ score, level }) {
  const color = LEVEL_COLORS[level] || '#6c757d'
  const data = [{ name: 'trust', value: score, fill: color }]

  return (
    <div className="gauge-wrapper">
      <RadialBarChart
        width={260}
        height={180}
        cx="50%"
        cy="100%"
        innerRadius="70%"
        outerRadius="100%"
        startAngle={180}
        endAngle={0}
        data={data}
      >
        <PolarAngleAxis type="number" domain={[0, 100]} angleAxisId={0} tick={false} />
        <RadialBar background dataKey="value" cornerRadius={10} />
      </RadialBarChart>
      <div className="gauge-label">
        <div className="gauge-score">{score.toFixed(1)}</div>
        <div className="gauge-level" style={{ color }}>
          {level}
        </div>
      </div>
    </div>
  )
}
