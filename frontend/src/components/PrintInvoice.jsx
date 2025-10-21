import React from 'react';

const PrintInvoice = ({ orderData, onPrint }) => {
  return (
    <button
      onClick={onPrint}
      style={{
        backgroundColor: '#d97706',
        color: 'white',
        padding: '10px 20px',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        fontSize: '16px',
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        fontWeight: '600',
        transition: 'background-color 0.3s ease'
      }}
      onMouseEnter={(e) => e.target.style.backgroundColor = '#b45309'}
      onMouseLeave={(e) => e.target.style.backgroundColor = '#d97706'}
    >
      🖨️ Print Invoice
    </button>
  );
};

export default PrintInvoice;
