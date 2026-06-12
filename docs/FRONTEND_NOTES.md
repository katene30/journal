# Frontend Notes

Notes for future frontend improvements - moving from Bootstrap to custom SCSS + Svelte.

## Planned Stack

- **SvelteKit** - Progressive enhancement, transitions, form handling
- **TypeScript** - Type safety for pillar data structures
- **SCSS** - Following Springload patterns
- **Chart.js** - Keep for data visualization

### Why Svelte + TypeScript?

| Requirement | Svelte | Preact | Vanilla TS |
|-------------|--------|--------|------------|
| Smooth pillar transitions | Built-in (`transition:slide`) | Need library | Manual |
| Swipe gestures | Easy with libs | Easy with libs | Manual |
| State per pillar | Reactive by default | useState hooks | Manual |
| Small bundle | ~2kb compiled | ~3kb | 0kb (but more code) |
| Learning curve | Gentle (HTML-like) | React knowledge needed | None |
| Team exploring | Yes (Sam) | No | Yes (crfnz) |

Svelte transitions are trivial:
```svelte
{#if activePillar === 'hinengaro'}
  <div transition:slide>
    <HinenaroPillar />
  </div>
{/if}
```

---

## Entry Flow Design Spec

### Core Philosophy

This app is a **guided daily journal structured around Te Whare Tapa Whā**.

Key principles:
- **Reflection first, data second**
- **No "completion pressure"**
- Each pillar holds its own **mauri (presence/energy)**
- User can stop at any time after reflection
- Navigation is fluid, not linear obligation

The user is not "filling out a form" — they are "recording a state of being".

---

### Entry Flow (High Level)

#### Step 1: Entry Cover
```
Friday, 12th of June
```
- Human-first date format
- Calendar icon opens date picker

#### Step 2: Daily Reflection Gate (Entry Point)

Components:
- Overall semantic differential scales (bipolar)
- Journal text area (free writing)
- "Save & Exit" option

Example scales:
```
Calm ←――――●―――――→ Overwhelmed
Low energy ←―――●――――→ Energised
Disconnected ←――●―――→ Grounded
```

**User can stop here and still have a complete entry.**

#### Step 3: Pillar Navigation (Optional Deeper Reflection)

After reflection, user can optionally explore pillars.

---

### Pillar Navigation UI

Horizontal pill navigator (sticky):

```
📝  🧠  💪  💛  🌿
```

| Icon | Pillar | Domain |
|------|--------|--------|
| 📝 | Reflection | Entry base |
| 🧠 | Hinengaro | Mind |
| 💪 | Tinana | Body |
| 💛 | Whānau | Relationships |
| 🌿 | Wairua | Spirit/Meaning |

### Mauri States (Not Progress)

Instead of completion percentages:

| State | Meaning |
|-------|---------|
| ○ | Untouched |
| ◔ | Lightly engaged |
| ◕ | Meaningful reflection |
| ● | Deep presence recorded |

Example display:
```
📝● 🧠◕ 💪◔ 💛○ 🌿○
```

No progress bars. No pressure.

---

### Pillar Screen Structure

Each pillar follows consistent structure:

#### 1. Opening Statement (Bilingual)
```
"E pēhea ana tō hinengaro i tēnei rā?"
How is your mind today?
```
Te Reo Māori first, English below.

#### 2. Semantic Differential Scales
```
Calm ─────●───── Overwhelmed
Focused ───●───── Distracted
Stable ────●───── Anxious
```
- 5-7 discrete positions
- No numeric labels (unless toggled)

#### 3. Pillar-Specific Inputs

**🧠 Hinengaro (Mind)**
- Mood scales
- Stress scale
- Emotional notes

**💪 Tinana (Body)**
- Energy
- Sleep quality
- Movement/exercise
- Nutrition awareness

**💛 Whānau (Relationships)**
- Connection quality
- Social interaction presence
- Emotional closeness

**🌿 Wairua (Spirit)**
- Meaning alignment
- Groundedness
- Connection to nature/purpose

#### 4. Reflection Prompt
```
What stood out most in this space today?
```
Optional text field.

---

### Navigation Behaviour

Users can:
- Swipe left/right between pillars
- Tap pillar icons to jump directly
- Return to reflection at any time
- Exit without completing all pillars

**No lock-in flow.**

---

### Exit Options

At any point:
- Save Entry
- Continue Later
- Return to Reflection
- Close without completion

After reflection screen:
```
[Save Entry]
    or
[Continue to Hauora →]
```

---

### Visual Language

- Minimal UI
- Soft transitions between pillars
- No harsh progress indicators
- Icons carry meaning, not decoration
- Calm, diary-like aesthetic

---

## TypeScript Data Structures

```typescript
type MauriState = 'untouched' | 'light' | 'meaningful' | 'deep';

interface SemanticScale {
  leftLabel: string;    // e.g., "Calm"
  rightLabel: string;   // e.g., "Overwhelmed"
  value: number | null; // 1-7, null if not set
}

interface PillarState {
  mauri: MauriState;
  scales: SemanticScale[];
  reflection?: string;
}

interface EntryState {
  id?: number;
  date: Date;

  // Core reflection (always available)
  overallScales: SemanticScale[];
  journalText: string;

  // Pillar states
  hinengaro: PillarState;
  tinana: PillarState;
  whanau: PillarState;
  wairua: PillarState;

  // Metadata
  savedAt?: Date;
  isDraft: boolean;
}

// Derived pillar scores (calculated, not input)
interface DerivedScores {
  hinengaro: number;  // Average of mind scales (anxiety/stress inverted)
  tinana: number;     // Average of body scales
  whanau: number;     // Average of relationship scales
  wairua: number;     // Meaning/spirit score
}
```

---

## SvelteKit Project Structure

```
frontend/
├── src/
│   ├── lib/
│   │   ├── components/
│   │   │   ├── PillarNav.svelte
│   │   │   ├── SemanticScale.svelte
│   │   │   ├── PillarScreen.svelte
│   │   │   ├── ReflectionGate.svelte
│   │   │   └── MauriIndicator.svelte
│   │   ├── stores/
│   │   │   └── entry.ts          # Entry state store
│   │   ├── types/
│   │   │   └── index.ts          # TypeScript interfaces
│   │   └── utils/
│   │       └── derived-scores.ts # Score calculations
│   ├── routes/
│   │   ├── +page.svelte          # Home/entry list
│   │   ├── entry/
│   │   │   ├── new/+page.svelte  # New entry flow
│   │   │   └── [id]/+page.svelte # View/edit entry
│   │   └── api/                  # API routes (or call Django)
│   └── app.html
├── static/
│   └── scss/                     # SCSS files
└── svelte.config.js
```

---

## SCSS Architecture (Springload Pattern)

### File Structure
```
scss/
├── _variables.scss      # Design tokens
├── _mixins.scss         # Reusable functions
├── _layout.scss         # Container, grid patterns
├── _elements.scss       # Base element styles
├── _components.scss     # Component styles
├── _utilities.scss      # Helper classes
└── main.scss            # Entry point
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

  // Semantic scale
  --scale-segments: 7;
  --scale-height: 48px;

  @media (min-width: 768px) {
    --page-gutter: 32px;
    --space-md: 32px;
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

---

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

### Semantic Scale A11y
```svelte
<fieldset role="radiogroup" aria-label="Rate from Calm to Overwhelmed">
  {#each segments as segment, i}
    <input
      type="radio"
      name="mood-scale"
      value={i + 1}
      aria-label="Level {i + 1} of {segments.length}"
    />
  {/each}
</fieldset>
```

---

## Derived Scores (Backend)

Add to Django model:
```python
@property
def hinengaro_score(self):
    """Calculate mind pillar score (invert anxiety/stress)."""
    values = [
        self.mood,
        10 - self.anxiety_level if self.anxiety_level else None,
        10 - self.stress_level if self.stress_level else None,
    ]
    valid = [v for v in values if v is not None]
    return sum(valid) / len(valid) if valid else None

@property
def tinana_score(self):
    """Calculate body pillar score."""
    values = [self.sleep_quality, self.exercise_level, self.diet_quality, self.energy_level]
    valid = [v for v in values if v is not None]
    return sum(valid) / len(valid) if valid else None

@property
def whanau_score(self):
    """Calculate relationships pillar score."""
    values = [self.social_connection, self.social_interactions_quality]
    valid = [v for v in values if v is not None]
    return sum(valid) / len(valid) if valid else None

@property
def wairua_score(self):
    """Spirit pillar is single metric."""
    return self.sense_of_meaning
```

---

## Resources

- [Svelte Tutorial](https://svelte.dev/tutorial)
- [SvelteKit Docs](https://kit.svelte.dev/docs)
- [SvelteKit Forms](https://kit.svelte.dev/docs/form-actions)
- [Svelte Transitions](https://svelte.dev/docs#template-syntax-element-directives-transition-fn)
- [Charts.css](https://chartscss.org/) - Pure CSS charts alternative
