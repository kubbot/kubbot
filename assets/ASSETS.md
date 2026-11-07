# Assets

## Workflow diagrams

The profile uses three original vector diagrams: `overview`, `execution`, and
`context`. Each has light/dark and desktop/mobile variants under `workflow/`.
The `<picture>` sources select the narrow layout at 600px and honor the viewer's
color scheme. The fallback is the light desktop version.

Regenerate from the repository root:

```sh
python3 scripts/render-workflow.py
python3 scripts/render-workflow.py --check
```

The generator uses Python's standard library. SVGs include accessible titles and
descriptions and contain no scripts, remote resources, animation, or embedded HTML.
The README repeats their meaning as normal text and image alternatives.

Edit the palette and layout in `scripts/render-workflow.py`, then commit both the
generator and its output. `scripts/update-readme.sh` remains a compatible entry
point for diagram generation; it no longer rewrites the README.

## Icon

| Variant | File | Usage |
|---------|------|-------|
| Blue Transparent | `icon/blue 透明.png` | Primary logo |
| Blue White BG | `icon/blue 白.png` | Light themes |
| Blue Black BG | `icon/blue 黑.png` | Dark themes |
| Red Transparent | `icon/red 透明.png` | Accent/Alert |
| Red White BG | `icon/red 白.png` | Light themes |
| Red Black BG | `icon/red 黑.png` | Dark themes |

## Logos

- `logo/openim/` - OpenIM project branding
- `logo/openkf/` - OpenKF project branding

---

**Copyright:** OpenKF logo designs by @Xx(席欣). All rights reserved.
