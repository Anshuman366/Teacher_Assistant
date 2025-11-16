import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function StudentAnalytics({ data }) {
  // data: { labels: [], scores: [] }
  const chartData = {
    labels: data.labels || [],
    datasets: [
      {
        label: 'Average Score',
        data: data.scores || [],
        fill: true,
        backgroundColor: 'rgba(102,126,234,0.15)',
        borderColor: 'rgba(102,126,234,1)'
      }
    ]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Student Performance Over Time' }
    },
    scales: {
      y: { beginAtZero: true, max: 100 }
    }
  };

  return (
    <div style={{ width: '100%', maxWidth: 900 }}>
      <Line data={chartData} options={options} />
    </div>
  );
}

export default StudentAnalytics;
