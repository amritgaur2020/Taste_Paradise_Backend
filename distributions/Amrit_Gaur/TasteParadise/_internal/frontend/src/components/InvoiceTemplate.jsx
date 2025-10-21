import React from 'react';

const InvoiceTemplate = React.forwardRef((props, ref) => {
  const { orderData } = props;
  
  return (
    <div ref={ref} style={{ padding: '20px', fontFamily: 'Arial', backgroundColor: 'white' }}>
      {/* Restaurant Header */}
      <div style={{ textAlign: 'center', marginBottom: '20px' }}>
        <h1 style={{ margin: 0, color: '#ea580c' }}>Taste Paradise</h1>
        <p style={{ margin: '5px 0' }}>Restaurant Billing Service</p>
        <p style={{ margin: '5px 0', fontSize: '12px' }}>123 Food Street, Flavor City, FC 12345</p>
        <p style={{ margin: '5px 0', fontSize: '12px' }}>Phone: +91 98765 43210</p>
      </div>

      <hr style={{ border: '1px solid #ddd' }} />

      {/* Invoice Details */}
      <div style={{ marginTop: '20px' }}>
        <p><strong>Invoice No:</strong> {orderData.invoiceNo}</p>
        <p><strong>Date:</strong> {new Date().toLocaleDateString('en-IN')}</p>
        <p><strong>Time:</strong> {new Date().toLocaleTimeString('en-IN')}</p>
        <p><strong>Table No:</strong> {orderData.tableNo || 'N/A'}</p>
        <p><strong>Customer:</strong> {orderData.customerName || 'Walk-in Customer'}</p>
      </div>

      <hr style={{ border: '1px solid #ddd', margin: '15px 0' }} />

      {/* Items Table */}
      <table style={{ width: '100%', marginTop: '20px', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '2px solid #000', backgroundColor: '#f5f5f5' }}>
            <th style={{ textAlign: 'left', padding: '10px', border: '1px solid #ddd' }}>Item</th>
            <th style={{ textAlign: 'center', padding: '10px', border: '1px solid #ddd' }}>Qty</th>
            <th style={{ textAlign: 'right', padding: '10px', border: '1px solid #ddd' }}>Price</th>
            <th style={{ textAlign: 'right', padding: '10px', border: '1px solid #ddd' }}>Total</th>
          </tr>
        </thead>
        <tbody>
          {orderData.items && orderData.items.map((item, index) => (
            <tr key={index} style={{ borderBottom: '1px solid #ddd' }}>
              <td style={{ padding: '8px', border: '1px solid #ddd' }}>
                {item.menuitemname || item.name}
              </td>
              <td style={{ textAlign: 'center', padding: '8px', border: '1px solid #ddd' }}>
                {item.quantity}
              </td>
              <td style={{ textAlign: 'right', padding: '8px', border: '1px solid #ddd' }}>
                ₹{item.price.toFixed(2)}
              </td>
              <td style={{ textAlign: 'right', padding: '8px', border: '1px solid #ddd' }}>
                ₹{(item.quantity * item.price).toFixed(2)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <hr style={{ border: '1px solid #ddd', margin: '15px 0' }} />

      {/* Totals */}
      <div style={{ marginTop: '20px', textAlign: 'right' }}>
        <p><strong>Subtotal:</strong> ₹{orderData.subtotal.toFixed(2)}</p>
        <p><strong>GST ({orderData.gstRate || 5}%):</strong> ₹{orderData.gst.toFixed(2)}</p>
        {orderData.serviceCharge > 0 && (
          <p><strong>Service Charge:</strong> ₹{orderData.serviceCharge.toFixed(2)}</p>
        )}
        <h2 style={{ marginTop: '10px', color: '#ea580c' }}>
          Total: ₹{orderData.total.toFixed(2)}
        </h2>
      </div>

      <hr style={{ border: '1px solid #ddd', margin: '20px 0' }} />

      {/* Footer */}
      <div style={{ textAlign: 'center', marginTop: '30px', fontSize: '12px', color: '#666' }}>
        <p>Thank you for dining with us at Taste Paradise!</p>
        <p style={{ marginTop: '10px' }}>GST No: 27AAAAA0000A1Z5 | FSSAI Lic: 12345678901234</p>
        <p>This is a computer generated invoice.</p>
      </div>
    </div>
  );
});

InvoiceTemplate.displayName = 'InvoiceTemplate';

export default InvoiceTemplate;
