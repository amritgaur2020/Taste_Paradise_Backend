# Read the JavaScript file
js_path = 'static/static/js/main.8670ff2c.js'

print(f"📂 Reading {js_path}...")
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"📊 Original file size: {len(content)} characters")

# Replace window.print() with backend API call
old_code = 'window.print()'
new_code = '''fetch("http://localhost:8002/api/print-invoice",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(e)}).then(r=>r.text()).then(html=>{const w=window.open("","_blank","width=800,height=600");w.document.write(html);w.document.close()}).catch(err=>alert("Print error: "+err))'''

if old_code in content:
    print(f"✅ Found window.print()")
    content = content.replace(old_code, new_code)
    print(f"✅ Replaced with backend API call")
    
    # Write back
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ File updated successfully!")
    print(f"📊 New file size: {len(content)} characters")
else:
    print("❌ Could not find window.print() in the file")

print("\n✅ Done! Now:")
print("1. Restart the app: python main.py")
print("2. Click Print Invoice - it will open a new window with the invoice!")
