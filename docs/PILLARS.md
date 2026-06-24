# Te Whare Tapa Whā + Te Pae Mahutonga Pillars

The journal uses two Māori health models to track wellbeing holistically.

## Te Whare Tapa Whā (The Four Walls)

A model developed by Sir Mason Durie representing health as a wharenui (meeting house) with four walls. All walls must be strong for the house to stand.

| Pillar | Symbol | Te Reo | English | What it tracks |
|--------|--------|--------|---------|----------------|
| **Hinengaro** | Koru | Mind | Mental/Emotional | Mood, anxiety, stress |
| **Tinana** | Mangopare | Body | Physical | Sleep, energy, exercise, diet |
| **Whānau** | Poutama | Family | Social/Relationships | Connection, interaction quality |
| **Wairua** | Koru Spiral | Spirit | Spiritual | Sense of meaning/purpose |

## Te Pae Mahutonga (The Southern Cross)

A model by Sir Mason Durie using the Southern Cross constellation. We use two of its stars:

| Pillar | Symbol | Te Reo | English | What it tracks |
|--------|--------|--------|---------|----------------|
| **Mauriora** | Puhoro | Life force | Identity | Feeling like yourself |
| **Waiora** | Ngutukākā | Environment | Physical environment | Is your space supportive? |

## Reflection

| Pillar | Symbol | Purpose |
|--------|--------|---------|
| **Reflection** | Koiri | Overall day rating + journal text fields |

## Mauri States

Each pillar shows a mauri (life force/presence) indicator based on how much you've engaged:

| Symbol | State | Meaning |
|--------|-------|---------|
| ○ | Untouched | Nothing filled in |
| ◔ | Light | Started (some fields) |
| ◕ | Meaningful | Good progress |
| ● | Deep | Fully engaged |

The mauri indicators are not judgmental - they simply show presence, not completion. There's no pressure to fill everything.

## Design Philosophy

- **Reflection first** - Start with how your day was, dive deeper if you want
- **No completion pressure** - Partial entries are valid
- **Bilingual prompts** - Questions shown in Te Reo Māori and English
- **Semantic scales** - Bipolar scales (e.g., "Calm ↔ Anxious") rather than numeric ratings

---

## Pillar Symbols (Māori Design Icons)

Custom SVG icons rooted in traditional Māori carving and weaving patterns. Each pillar has its own colour and symbol.

| Pillar | Symbol | Core Meaning |
|--------|--------|--------------|
| **Hinengaro** | Koru | Growth, learning, adaptation |
| **Tinana** | Mangopare | Strength, resilience, determination |
| **Whānau** | Poutama | Ascension, growth together, support |
| **Wairua** | Koru Spiral | Spiritual depth, inward journey |
| **Mauriora** | Puhoro | Speed, agility, life force in motion |
| **Waiora** | Ngutukākā | Environment, guardianship of nature, flourishing |
| **Reflection** | Koiri | Reflection, integration, self-awareness |

### Symbol Descriptions

- **Koru** — Unfurling fern frond. Internal growth, new beginnings, renewal of mind.
- **Mangopare** — Hammerhead shark pattern. Capability, determination, tenacity of body.
- **Poutama** — Stepped pattern (stairway to heaven). Ascending levels of learning and growth together.
- **Koru Spiral** — Deepening koru. Inward spiritual journey, connection to deeper self.
- **Puhoro** — Speed and agility pattern. Life force in motion, vitality, forward momentum.
- **Ngutukākā** — Kākā beak flower pattern. Relationship with living environment.
- **Koiri** — Double koru reflecting each other. Self-reflection, inward movement.

### Implementation

Icons are Svelte components at `frontend/src/lib/icons/`:
- `KoruIcon.svelte` (Hinengaro)
- `MangopareIcon.svelte` (Tinana)
- `PoutamaIcon.svelte` (Whānau)
- `KoruSpiralIcon.svelte` (Wairua)
- `PuhoroIcon.svelte` (Mauriora)
- `NgutukukaIcon.svelte` (Waiora)
- `KoiriIcon.svelte` (Reflection)

Source SVGs are in `frontend/src/lib/icons/source/`.

### Adjective Sets (for UI language/prompts)

**Hinengaro (Koru)**
Reflective, Curious, Calm, Aware, Open, Learning, Adaptable, Thoughtful

**Tinana (Mangopare)**
Strong, Active, Energised, Resilient, Determined, Enduring, Capable, Robust

**Whānau (Poutama)**
Connected, Supported, Trusted, Loyal, Caring, Included, Compassionate, Present

**Wairua (Koru Spiral)**
Grounded, Purposeful, Peaceful, Aligned, Guided, Sacred, Balanced, Connected

**Mauriora (Puhoro)**
Authentic, Proud, Rooted, Confident, True, Self-aware, Secure, Expressive

**Waiora (Ngutukākā)**
Harmonious, Natural, Nurturing, Healthy, Balanced, Restorative, Safe, Flourishing

**Reflection (Koiri)**
Insightful, Honest, Intentional, Grateful, Observant, Self-aware, Integrative, Evolving

---

## Ngāpuhi Visual Identity

Rather than pan-Māori, the app can express a distinctly Ngāpuhi identity through visual language.

### Colour Palette

Draw from Te Tai Tokerau landscapes and traditional Ngāpuhi aesthetics:

| Colour | Inspiration | Usage |
|--------|-------------|-------|
| **Deep blue** | Hokianga harbour, Te Tai Tokerau seas | Primary accent |
| **Teal/greenstone** | Pounamu, native bush | Secondary accent |
| **Black** | Te pō, traditional carving | Text, strong elements |
| **Warm white/cream** | Bone, harakeke | Backgrounds |
| **Earth browns** | Whenua, carved wood | Warm accents |
| **Muted green** | Kauri forests, native flora | Nature elements |

### Kōwhaiwhai Patterns

Te Tai Tokerau carving traditions have distinctive styles:

- **Linework** — Flowing, often asymmetrical, with strong curves
- **Rauponga** — Parallel ridges used in backgrounds
- **Negative space** — Important in Ngāpuhi carving; let elements breathe
- **Manaia styling** — Te Tai Tokerau manaia often have distinctive head shapes

### Visual Elements

- Subtle kōwhaiwhai borders or dividers
- Manaia as decorative guardians (corners, headers)
- Wave/water motifs (Hokianga, Bay of Islands)
- Kauri tree references (strength, longevity)

### References

- **Te Whare Tapu o Ngāpuhi** — Wharenui styling
- **Harbours and waterways** — Hokianga, Waitangi, Bay of Islands
- **Carving houses** — Study traditional Te Tai Tokerau whakairo

### Implementation Status

- [x] **Pillar icons** — Custom SVG symbols in pillar colours
- [x] **Colour palette** — Ngāpuhi-inspired (moana blue, pounamu, whenua, etc.)
- [ ] **Card backgrounds** — Subtle kōwhaiwhai texture or border
- [ ] **Navigation** — Wave-inspired curves
- [ ] **Loading states** — Koru unfurling animation
- [ ] **Empty states** — Manaia illustration
- [ ] **Mauri indicators** — Styled as carved circles
