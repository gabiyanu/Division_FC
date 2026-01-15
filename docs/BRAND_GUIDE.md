# 🎨 YOUR UNIQUE BRAND IDENTITY

## "Midnight Aurora" Theme

A distinctive, sophisticated visual identity designed exclusively for your soccer analytics content.

---

## 🎨 Color Palette

### Background Colors
| Name | Hex | Usage |
|------|-----|-------|
| Deep Space Black | `#0D1117` | Primary background |
| Charcoal | `#161B22` | Secondary background, cards |
| Slate Gray | `#21262D` | Tertiary, borders |

### Aurora Accent Colors (Your Signature!)
| Name | Hex | Usage |
|------|-----|-------|
| **Aurora Cyan** | `#58D9C4` | Primary accent, headlines, links |
| **Aurora Magenta** | `#E056A0` | Secondary accent, highlights |
| **Aurora Purple** | `#A371F7` | Tertiary accent, gradients |
| **Aurora Gold** | `#F5C344` | Special highlights, goals |

### Functional Colors
| Name | Hex | Usage |
|------|-----|-------|
| Success Green | `#3FB950` | Positive metrics, goals |
| Danger Red | `#F85149` | Negative metrics, misses |
| Warning Amber | `#D29922` | Caution states |

### Text Colors
| Name | Hex | Usage |
|------|-----|-------|
| Primary Text | `#F0F6FC` | Headlines, important text |
| Secondary Text | `#8B949E` | Body text, labels |
| Muted Text | `#484F58` | Captions, footnotes |

---

## 🔤 Typography

### Font Stack
- **Primary:** Inter (clean, modern)
- **Monospace:** JetBrains Mono (stats/numbers)
- **Fallback:** DejaVu Sans

### Size Scale
| Level | Size | Usage |
|-------|------|-------|
| Hero | 32pt | Main titles |
| Title | 24pt | Section headers |
| Subtitle | 18pt | Subtitles |
| Body | 14pt | Body text |
| Caption | 11pt | Labels, captions |
| Micro | 9pt | Annotations |

---

## ✨ Signature Elements

### 1. Accent Underline
A thin cyan line under titles marks your content instantly:
```
┌─────────────────────────┐
│   YOUR TITLE HERE       │
│   ═══════════════       │  ← Aurora Cyan underline
└─────────────────────────┘
```

### 2. Corner Accent Bar
A magenta bar in the bottom-left corner:
```
┌─────────────────────────┐
│                         │
│                         │
│ ████                    │  ← Aurora Magenta bar
└─────────────────────────┘
```

### 3. Watermark Style
Your handle in Aurora Cyan, bottom-right corner:
```
┌─────────────────────────┐
│                         │
│                         │
│               @HANDLE   │  ← Aurora Cyan text
└─────────────────────────┘
```

### 4. Aurora Gradient
Use for heatmaps and intensity scales:
```
Cyan → Purple → Magenta → Gold
#58D9C4 → #A371F7 → #E056A0 → #F5C344
```

---

## 📊 The 7 Chart Types

### 1. Progressive Passes Grid
- Dark background with team mini-pitches
- Green/red zones for improvement/decline
- Cyan accent underline on title

### 2. Player Stats Table
- Cyan header row with dark text
- Alternating row colors (charcoal/slate)
- Magenta progress bars

### 3. Crossing Zones Grid
- Purple-magenta-gold heatmap gradient
- Clean mini-pitch outlines
- Team badges/names below

### 4. Scatter Plot
- Cyan dots with dark edges
- Purple highlights for top performers
- Subtle grid lines

### 5. Histogram/Distribution
- Cyan bars on dark background
- Gold vertical line for actual values
- Clean axis styling

### 6. Zone Control Maps
- Green = team control
- Red = opponent control  
- Purple = contested
- Varying alpha for intensity

### 7. Shot Maps
- Dark pitch with green field
- Goal = green, Saved = cyan
- xG-sized markers
- Hexbin density optional

---

## 📐 Layout Guidelines

### Instagram Post (1080x1080)
```
┌──────────────────────────────┐
│         Title Area           │  12% top margin
│   ═════════════════════      │
├──────────────────────────────┤
│                              │
│        Main Content          │  80% content area
│                              │
├──────────────────────────────┤
│ ████  Data Source   @HANDLE  │  8% bottom margin
└──────────────────────────────┘
```

### Instagram Story (1080x1920)
```
┌──────────────────────────────┐
│                              │
│         Title Area           │
│   ═════════════════════      │
│                              │
│                              │
│        Main Content          │
│                              │
│                              │
│                              │
│ ████  Data Source   @HANDLE  │
└──────────────────────────────┘
```

---

## 🚀 Quick Usage

```python
from src.branding import COLORS, create_branded_charts

# Initialize
charts = create_branded_charts()

# Create any of the 7 chart types
fig = charts.scatter_plot(data, x='xG', y='Goals', ...)
fig = charts.shot_map(shots, player_name='Mbappe')
fig = charts.progressive_passes_grid(data, teams)
# ... etc

# Save with brand settings
charts.save(fig, 'my_chart.png')
```

---

## 🎯 What Makes This Unique

1. **Color Palette**: The Aurora colors (cyan, magenta, purple, gold) are NOT commonly used in soccer viz
2. **Dark Theme**: Professional, modern look that stands out on Instagram
3. **Consistent Signatures**: Accent bars, underlines, and watermarks create instant recognition
4. **Typography**: Clean, modern fonts differentiate from typical sports graphics

---

## 📝 Brand Checklist

Before posting, ensure:
- [ ] Aurora Cyan accent underline present
- [ ] Magenta accent bar in corner
- [ ] Your handle watermark visible
- [ ] Dark background applied
- [ ] Data source credited
- [ ] Consistent font usage

---

*Your exclusive "Midnight Aurora" brand identity. Make it yours! ⚽*
