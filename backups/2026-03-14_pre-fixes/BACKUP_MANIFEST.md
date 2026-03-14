# Backup Manifest - 2026-03-14 Pre-Fixes

## Backup Purpose
Full project backup before implementing Priority 1 fixes:
- Remove CSS duplication (dropdown.css)
- Consolidate conflicting CSS rules in style.css
- Add mobile navigation toggle to glossary.js

## Files Backed Up

### Critical Assets
- assets/style.css (1204 lines - MASTER stylesheet)
- assets/dropdown.css (149 lines - to be deleted)
- assets/glossary.js (174 lines - will be modified)
- assets/media/ (all media files)

### Root HTML Files
- index.html
- glossary.html
- video_gallery.html
- references.html

## Restoration Instructions
If rollback needed:
```powershell
Copy-Item -Path "backups\2026-03-14_pre-fixes\assets\*" -Destination "assets\" -Recurse -Force
Copy-Item -Path "backups\2026-03-14_pre-fixes\*.html" -Destination "." -Force
```

## Changes Planned
1. DELETE: assets/dropdown.css (verified no HTML references)
2. MODIFY: assets/style.css (remove duplicate/conflicting rules)
3. MODIFY: assets/glossary.js (append mobile nav toggle)

## Content Preservation Verification
- Zero text content changes
- Zero academic content modifications
- All 69 glossary terms preserved
- All citations and quotes unchanged
- All video URLs preserved
