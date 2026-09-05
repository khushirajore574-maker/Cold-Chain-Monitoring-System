import React, { useState, useEffect } from 'react';

function App() {
  const [data, setData] = useState({
    temperature: '--',
    humidity: '--',
    status: 'LOADING',
    sensor_type: 'DHT11'
  });
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMetrics = () => {
      // हर 2 सेकंड में Flask API से लेटेस्ट रिकॉर्ड लाना
      fetch('http://localhost:5000/latest')
        .then((res) => {
          if (!res.ok) throw new Error('Server not responding');
          return res.json();
        })
        .then((incomingData) => {
          setData(incomingData);
          setError(null);
        })
        .catch((err) => {
          setError('Connecting to Flask Server...');
        });
    };

    fetchMetrics(); // पहली बार तुरंत चलाने के लिए
    
    // 🟢 यहाँ हमने इंटरवल को 2000ms (2 सेकंड) पर सेट कर दिया है
    const interval = setInterval(fetchMetrics, 2000); 
    return () => clearInterval(interval);
  }, []);

  const isAlert = data.status === 'ALERT';

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: isAlert ? '#fff5f5' : '#f8fafc',
      fontFamily: 'Segoe UI, Geneva, Verdana, sans-serif',
      padding: '40px 20px',
      transition: 'background-color 0.4s ease'
    }}>
      <div style={{ maxWidth: '600px', margin: '0 auto', textAlign: 'center' }}>
        <h1 style={{ color: '#0f172a', marginBottom: '5px' }}>❄️ Cold Chain Monitor</h1>
        <p style={{ color: '#64748b', fontSize: '15px', marginTop: '0' }}>Real-Time IoT Storage Dashboard (Updates every 2s)</p>

        {error && (
          <div style={{ padding: '12px', backgroundColor: '#fffbeb', color: '#b45309', borderRadius: '8px', margin: '20px 0', fontSize: '14px', fontWeight: '500' }}>
            ⚠️ {error}
          </div>
        )}

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', margin: '30px 0' }}>
          <div style={{ background: '#ffffff', padding: '25px', borderRadius: '16px', border: isAlert ? '2px solid #ef4444' : '1px solid #e2e8f0' }}>
            <span style={{ fontSize: '13px', color: '#64748b', fontWeight: '600' }}>TEMPERATURE</span>
            <h2 style={{ fontSize: '38px', margin: '12px 0 0 0', color: isAlert ? '#dc2626' : '#0f172a' }}>{data.temperature} °C</h2>
          </div>

          <div style={{ background: '#ffffff', padding: '25px', borderRadius: '16px', border: '1px solid #e2e8f0' }}>
            <span style={{ fontSize: '13px', color: '#64748b', fontWeight: '600' }}>HUMIDITY</span>
            <h2 style={{ fontSize: '38px', margin: '12px 0 0 0', color: '#0284c7' }}>{data.humidity} %</h2>
          </div>
        </div>

        <div style={{ padding: '20px', borderRadius: '12px', fontSize: '22px', fontWeight: 'bold', backgroundColor: isAlert ? '#ef4444' : '#22c55e', color: '#ffffff' }}>
          {isAlert ? '🚨 TEMPERATURE ALERT 🚨' : '🟢 SYSTEM STABLE'}
        </div>
      </div>
    </div>
  );
}

export default App;
