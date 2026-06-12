# Frontend Notes

Notes for future frontend improvements - moving from Bootstrap to custom SCSS + Svelte.

## Planned Stack

- **Svelte/SvelteKit** - Progressive enhancement, form handling
- **SCSS** - Following Springload patterns
- **HTMX** - For simple AJAX interactions (optional alongside Svelte)
- **Chart.js** - Keep for data visualization

## SCSS Architecture (Springload Pattern)

### File Structure
```
static_src/
├── scss/
│   ├── _variables.scss      # Design tokens
│   ├── _mixins.scss         # Reusable functions
│   ├── _layout.scss         # Container, grid patterns
│   ├── _elements.scss       # Base element styles
│   ├── _components.scss     # Component styles
│   ├── _utilities.scss      # Helper classes
│   └── main.scss            # Entry point
```

### Design Tokens
```scss
:root {
  // Spacing scale (responsive)
  --space-xs: 8px;
  --space-sm: 16px;
  --space-md: 24px;
  --space-lg: 32px;
  --space-xl: 48px;

  // Layout
  --content-max-width: 800px;
  --page-gutter: 16px;

  // Pillar colors (Te Whare Tapa Whā)
  --color-hinengaro: #2196F3;  // Mind - blue
  --color-tinana: #4CAF50;     // Body - green
  --color-whanau: #FF9800;     // Family - orange
  --color-wairua: #9C27B0;     // Spirit - purple
  --color-mauriora: #E91E63;   // Identity - pink
  --color-waiora: #00BCD4;     // Environment - teal

  @media (min-width: 768px) {
    --page-gutter: 32px;
    --space-md: 32px;
  }

  @media (min-width: 1024px) {
    --page-gutter: 48px;
  }
}
```

### Container Mixin (Replaces Bootstrap .container)
```scss
@mixin content-width {
  width: 100%;
  max-width: calc(var(--content-max-width) + var(--page-gutter) * 2);
  margin-inline: auto;
  padding-inline: var(--page-gutter);
}
```

### Breakpoint Mixins
```scss
$bp-sm: 500px;
$bp-md: 768px;
$bp-lg: 1024px;
$bp-xl: 1440px;

@mixin sm { @media (min-width: $bp-sm) { @content; } }
@mixin md { @media (min-width: $bp-md) { @content; } }
@mixin lg { @media (min-width: $bp-lg) { @content; } }
@mixin xl { @media (min-width: $bp-xl) { @content; } }
```

### Grid Patterns
```scss
// Standard grid
@mixin grid($cols: 12, $gap: 20px) {
  display: grid;
  grid-template-columns: repeat($cols, minmax(0, 1fr));
  gap: $gap;
}

// Auto-fit responsive grid (for cards)
.pillar-grid {
  display: grid;
  gap: var(--space-md);
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}
```

## Layout Philosophy

### Bootstrap vs Custom
```
Bootstrap:  HTML controls layout (classes everywhere)
            <div class="container"><div class="row"><div class="col-md-6">

Custom:     CSS controls layout (clean HTML)
            <div class="content-page">
```

### Key Principle
Define layout in CSS with grid-template-areas, not scattered col classes:

```scss
.entry-detail {
  @include content-width;
  display: grid;
  grid-template-areas:
    "header"
    "chart"
    "pillars"
    "reflection";
  gap: var(--space-lg);

  @include lg {
    grid-template-areas:
      "header header"
      "chart pillars"
      "reflection reflection";
    grid-template-columns: 1fr 1fr;
  }
}

.entry-header { grid-area: header; }
.entry-chart { grid-area: chart; }
.entry-pillars { grid-area: pillars; }
.entry-reflection { grid-area: reflection; }
```

## Accessibility Patterns

### Skip Link
```scss
.skip-link {
  position: absolute;
  transform: translateY(-100%);

  &:focus {
    transform: translateY(0);
  }
}
```

### Focus Visible
```scss
button:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

### Minimum Touch Target (48px)
```scss
@mixin touch-target {
  min-height: 48px;
  min-width: 48px;
}
```

### Visually Hidden (Screen Reader Only)
```scss
@mixin visually-hidden {
  position: absolute !important;
  width: 1px !important;
  height: 1px !important;
  margin: -1px !important;
  padding: 0 !important;
  overflow: hidden !important;
  clip: rect(0, 0, 0, 0) !important;
  border: 0 !important;
}
```

## Form UX Ideas

### Simplify Entry Form
1. **Quick mode** - Overall rating + journal only (daily habit)
2. **Full mode** - All pillars (weekly reflection)
3. **Pillar-by-pillar wizard** - One screen per pillar, swipe through

### Visual Whare Metaphor
Display pillars as walls of a house - tap to expand/rate each one.
Makes the framework tangible, not just a form.

### Derived Scores (Calculate, Don't Ask)
```python
# In model
@property
def hinengaro_score(self):
    return (self.mood + (10 - self.anxiety_level) + (10 - self.stress_level)) / 3

@property
def tinana_score(self):
    return mean([self.sleep_quality, self.exercise_level, self.diet_quality, self.energy_level])
```

Show pillar scores on dashboard, raw metrics only in detail view.

## Resources

- [Svelte Tutorial](https://svelte.dev/tutorial)
- [SvelteKit Forms](https://kit.svelte.dev/docs/form-actions)
- [HTMX](https://htmx.org/) - If needed for simple AJAX
- [Charts.css](https://chartscss.org/) - Pure CSS charts alternative
