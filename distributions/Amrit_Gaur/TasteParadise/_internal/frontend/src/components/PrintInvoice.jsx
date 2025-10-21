import React from 'react';

const PrintInvoice = ({ orderData }) => {
  const handlePrint = async () => {
    try {
      // Call backend print-thermal API
      const response = await fetch('http://localhost:8002/api/print-thermal', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(orderData),
      });

      const result = await response.json();
      
      if (result.status === 'success') {
        alert(`✅ ${result.message}`);
      } else {
        alert(`❌ Print failed: ${result.message}`);
      }
    } catch (error) {
      console.error('Print error:', error);
      alert('❌ Print error: ' + error.message);
    }
  };

  return (
    <button
      onClick={handlePrint}
      className="bg-orange-600 hover:bg-orange-700 text-white px-6 py-2 rounded-lg flex items-center gap-2"
    >
      <span>🖨️</span>
      Print Invoice
    </button>
  );
};

export default PrintInvoice;
