import os

# Read the JavaScript file
js_path = 'static/static/js/main.8670ff2c.js'

print(f"📂 Reading {js_path}...")
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"📊 File size: {len(content)} characters")

# Multiple possible variations of the print code
replacements = [
    ('const t=window.open("","","height=600,width=800");t&&(t.document.write(e),t.document.close(),t.focus(),setTimeout((()=>{t.print(),t.close()}),250))', 'window.print()'),
    ('window.open("","","height=600,width=800")', 'window.print();return'),
    ('window.open(""', 'window.print();return;void(""'),
]

replaced = False
for old, new in replacements:
    if old in content:
        print(f"✅ Found: {old[:50]}...")
        content = content.replace(old, new)
        replaced = True
        print(f"✅ Replaced with: {new}")

if not replaced:
    print("❌ Could not find the print code to replace!")
    print("Searching for 'window.open'...")
    index = content.find('window.open')
    if index != -1:
        print(f"Found at position {index}:")
        print(content[index:index+200])
    else:
        print("No window.open found!")
else:
    # Write back
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ File updated successfully!")
    
    # Clear WebView2 cache
    cache_path = os.path.expanduser('~\\AppData\\Local\\Temp\\TasteParadise')
    if os.path.exists(cache_path):
        print(f"🗑️ Clearing cache at {cache_path}...")
        try:
            import shutil
            shutil.rmtree(cache_path, ignore_errors=True)
            print("✅ Cache cleared!")
        except:
            print("⚠️ Could not clear cache (not critical)")

print("\n✅ Done! Now restart the app with: python main.py")
