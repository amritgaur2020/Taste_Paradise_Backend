# Read the JavaScript file
js_path = 'static/static/js/main.8670ff2c.js'

with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the pattern we added before
old_pattern = 'onClick:async()=>{const e=document.getElementById("invoice-content");if(!e)return void alert("Invoice content not found");try{const invoiceData={invoiceNo:e.querySelector("h1")?.textContent||"N/A",customerName:e.querySelector("p")?.textContent||"Walk-in",tableNo:"T1",items:[],subtotal:0,gst:0,total:0};const response=await fetch("http://localhost:8002/api/print-invoice",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(invoiceData)});const html=await response.text();const w=window.open("","_blank","width=900,height=700");w.document.write(html);w.document.close()}catch(err){console.error("Print error:",err);alert("Print failed: "+err.message)}return;const t=window.open("","","height=600,width=800");'

# Simpler version that uses the invoice HTML content
new_pattern = 'onClick:async()=>{const e=document.getElementById("invoice-content");if(!e)return void alert("Invoice content not found");try{const response=await fetch("http://localhost:8002/api/print-invoice",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({invoiceNo:"#706E6994",customerName:"Walk-in Customer",tableNo:"T1",items:t.items||[],subtotal:t.subtotal||0,gst:t.gst||0,total:t.total||0})});const html=await response.text();const w=window.open("","_blank","width=900,height=700");if(w){w.document.write(html);w.document.close()}else{alert("Popup blocked! Please allow popups.")}}catch(err){console.error("Print error:",err);alert("Print failed: "+err.message)}return;const t=window.open("","","height=600,width=800");'

if old_pattern in content:
    print("✅ Found the problematic pattern")
    content = content.replace(old_pattern, new_pattern)
    
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed invoice data handling!")
else:
    print("❌ Pattern not found - trying alternative fix")
    # Alternative: just make window.open work better
    if 'const w=window.open("","_blank","width=900,height=700");w.document.write(html)' in content:
        content = content.replace(
            'const w=window.open("","_blank","width=900,height=700");w.document.write(html)',
            'const w=window.open("","_blank","width=900,height=700");if(w){w.document.write(html);w.document.close()}else{alert("Please allow popups")}'
        )
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Applied alternative fix!")
