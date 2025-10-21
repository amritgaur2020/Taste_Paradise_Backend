# Automatically fix duplicate /print-thermal endpoints

# Read main.py
with open('main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("📖 Reading main.py...")
print(f"Total lines: {len(lines)}\n")

# Find all lines with @api_router.post("/print-thermal")
thermal_lines = []
for i, line in enumerate(lines):
    if '@api_router.post("/print-thermal")' in line:
        thermal_lines.append(i + 1)  # Line numbers start at 1

print(f"Found {len(thermal_lines)} /print-thermal endpoints at lines:")
for line_num in thermal_lines:
    print(f"  Line {line_num}")

if len(thermal_lines) <= 1:
    print("\n✅ No duplicates found! File is already clean.")
else:
    print(f"\n❌ Found {len(thermal_lines) - 1} duplicate(s)!")
    print("\n🔧 Fixing by removing duplicates 2 and 3...\n")
    
    # Keep first occurrence, delete others
    # We need to delete entire functions, not just one line
    
    lines_to_delete = []
    
    # For each duplicate (skip the first one)
    for thermal_line in thermal_lines[1:]:
        # Start deleting from this line
        start_delete = thermal_line - 1  # Convert to 0-indexed
        
        # Find where this function ends (next @api_router or end of file)
        end_delete = start_delete + 1
        for i in range(start_delete + 1, len(lines)):
            if '@api_router' in lines[i]:
                end_delete = i
                break
            if i == len(lines) - 1:
                end_delete = i + 1
        
        print(f"Will delete lines {start_delete + 1} to {end_delete}")
        lines_to_delete.append((start_delete, end_delete))
    
    # Create new content by removing duplicate sections
    new_lines = []
    delete_ranges = sorted(lines_to_delete, reverse=True)
    
    current_pos = 0
    skip_until = -1
    
    for i, line in enumerate(lines):
        # Check if we should skip this line
        should_skip = False
        for start, end in lines_to_delete:
            if start <= i < end:
                should_skip = True
                break
        
        if not should_skip:
            new_lines.append(line)
    
    # Backup original
    with open('main.py.backup', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("\n💾 Backup saved as main.py.backup")
    
    # Write fixed version
    with open('main.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"✅ Fixed! Removed {len(lines) - len(new_lines)} lines")
    print(f"✅ New file has {len(new_lines)} lines (was {len(lines)})")
    print("\n🚀 Now restart: python main.py")
