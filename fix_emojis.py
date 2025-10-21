import re

# Backup first
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Save backup
with open('main_backup.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Remove ALL emojis
emoji_pattern = re.compile(
    "[\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251]+",
    flags=re.UNICODE
)

cleaned = emoji_pattern.sub('', content)

# Save cleaned version
with open('main.py', 'w', encoding='utf-8') as f:
    f.write(cleaned)

print("✅ ALL EMOJIS REMOVED!")
print("✅ Backup saved as: main_backup.py")
print("✅ Now run: pyinstaller TasteParadise.spec")
