'use client'
// Import necessary hooks and components
import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Pie } from 'react-chartjs-2';
import Chart, { registerables } from 'chart.js/auto';
Chart.register(...registerables);

const ResultsPage = () => {
  const router = useRouter();
  const [resultData, setResultData] = useState(null);

  useEffect(() => {
    // Assume resultData is stored in localStorage
    const data = JSON.parse(localStorage.getItem('resultData'));
    if (!data) {
      router.push('/'); // Redirect to home if no data is found
      return;
    }
    setResultData(data);
  }, [router]);

  // Define the pie chart data and options
  const pieData = {
    labels: resultData?.summary_data?.labels,
    datasets: [
      {
        data: resultData?.summary_data?.values,
        backgroundColor: resultData?.summary_data?.colors,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Quiz Summary',
      },
    },
  };

  return (
    <div>
      <h1>Quiz Results</h1>
      {resultData && (
        <>
          <div>
            {resultData.cor_ans.map((qa, index) => (
              <div key={index}>
                <h3>{qa[0]}</h3>
                <ul>
                  {qa[1].map((option, optionIndex) => (
                    <li key={optionIndex}>{option}</li>
                  ))}
                </ul>
                <p>Correct Answer: {qa[2]}</p>
                <p>Topic to Improve: {resultData.topic[index]}</p>
              </div>
            ))}
          </div>
          <div>
            <Pie data={pieData} options={options} />
          </div>
        </>
      )}
    </div>
  );
};

export default ResultsPage;
