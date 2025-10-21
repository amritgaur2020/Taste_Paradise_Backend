import React, { useRef } from "react";
import "./InvoicePrint.css";
import PrintInvoice from "./PrintInvoice";

const InvoiceTemplate = (props) => {
  const invoiceRef = useRef();
  const orderData = props.orderData || {};

  const handlePrint = () => {
    const printContents = invoiceRef.current.outerHTML;
    const printWindow = window.open("", "", "width=400,height=600,left=200,top=200");
    printWindow.document.write(`
      <html>
      <head>
        <title>Print Invoice</title>
        <link rel="stylesheet" type="text/css" href="InvoicePrint.css" />
        <style>
          @page { size: 80mm auto; margin: 0; }
          body { background: #fff; margin: 0; }
        </style>
      </head>
      <body>${printContents}</body>
      </html>
    `);
    printWindow.document.close();
    printWindow.focus();
    setTimeout(() => {
      printWindow.print();
      printWindow.close();
    }, 500);
  };

  return (
    <div>
      <div className="invoice-container" ref={invoiceRef}>
        <div className="invoice-header">
          <h2 style={{ margin: "5px 0", color: "#d97706", fontSize: "18px" }}>Taste Paradise</h2>
          <p style={{ margin: "2px 0", fontSize: "11px" }}>Restaurant & Billing Service</p>
          <p style={{ margin: "2px 0", fontSize: "10px" }}>123 Food Street, Flavor City, FC 12345</p>
          <p style={{ margin: "2px 0", fontSize: "10px" }}>Phone: +91 98765 43210</p>
        </div>
        <hr style={{ border: "1px dashed #000", margin: "10px 0" }} />
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "10px", fontSize: "11px" }}>
          <div>
            <p style={{ margin: "3px 0" }}><strong>Bill To:</strong></p>
            <p style={{ margin: "3px 0" }}>{orderData.customerName || "Walk-in Customer"}</p>
            {orderData.tableNo && <p style={{ margin: "3px 0" }}>Table: {orderData.tableNo}</p>}
          </div>
          <div style={{ textAlign: "right" }}>
            <p style={{ margin: "3px 0" }}><strong>INVOICE</strong></p>
            <p style={{ margin: "3px 0" }}>{orderData.invoiceNo || orderData.order_id || orderData.id || 'NA'}</p>
            <p style={{ margin: "3px 0" }}>{new Date().toLocaleDateString("en-IN")}</p>
            <p style={{ margin: "3px 0" }}>{new Date().toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit" })}</p>
          </div>
        </div>
        <hr style={{ border: "1px dashed #000", margin: "4px 0" }} />
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "10px", fontSize: "11px" }}>
          <div>
            <p style={{ margin: "3px 0" }}><strong>Order Details:</strong></p>
            <p style={{ margin: "3px 0" }}>Status: {orderData.status}</p>
            <p style={{ margin: "3px 0" }}>Payment: {orderData.paymentStatus}</p>
            <p style={{ margin: "3px 0" }}>Method: {orderData.paymentMethod}</p>
          </div>
        </div>
        <table className="invoice-table">
          <thead>
            <tr>
              <th>Item</th>
              <th style={{ textAlign: "center" }}>Qty</th>
              <th style={{ textAlign: "right" }}>Rate (₹)</th>
              <th style={{ textAlign: "right" }}>Amount (₹)</th>
            </tr>
          </thead>
          <tbody>
            {orderData.items && orderData.items.map((item, idx) => (
              <tr key={idx}>
                <td>{item.name}</td>
                <td style={{ textAlign: "center" }}>{item.quantity}</td>
                <td style={{ textAlign: "right" }}>{item.rate.toFixed(2)}</td>
                <td style={{ textAlign: "right" }}>{(item.rate * item.quantity).toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="invoice-total">
          <div className="subtotal-row">Subtotal: ₹{orderData.subtotal?.toFixed(2) || "0.00"}</div>
          <div className="gst-row">GST (5%): ₹{orderData.gst?.toFixed(2) || "0.00"}</div>
          <div className="total-amount-row">Total Amount: ₹{orderData.total?.toFixed(2) || "0.00"}</div>
        </div>
        <div className="invoice-footer">
          <div className="thank-you">Thank you for dining with us at Taste Paradise!</div>
          <div className="footer-info">
            GST No: 27AAAAA0000A1Z5 | FSSAI Lic: 12345678901234<br />
            This is a computer generated invoice.
          </div>
        </div>
      </div>
      <PrintInvoice onPrint={handlePrint} />
    </div>
  );
};

export default InvoiceTemplate;
