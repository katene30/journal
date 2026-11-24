<script lang="ts">
	import { untrack } from 'svelte';
	import { entriesApi, type Entry, type EntryListItem } from '$lib/api/entries';
	import { PILLARS, describeScaleValue, getPillarById } from '$lib/config/pillars';
	import { SCALE_MAX, formatScore, pillarScore } from '$lib/utils/hauora';
	import { addDays, localISODate } from '$lib/utils/dates';
	import EyeIcon from '$lib/icons/EyeIcon.svelte';
	import LockIcon from '$lib/icons/LockIcon.svelte';

	interface Props {
		entry: EntryListItem;
		/** Show the six pillar meters */
		showIndicators?: boolean;
		href?: string;
	}

	let { entry, showIndicators = true, href = `/app/entries/${entry.id}` }: Props = $props();

	const INDICATOR_PILLARS = PILLARS.filter((p) => p.id !== 'reflection');
	const reflection = getPillarById('reflection')!;
	const overallScale = reflection.scales[0];
	const PREVIEW_LENGTH = 120;

	// Starts revealed only when the list came with previews (the "show by
	// default" setting). Otherwise the text is fetched on the first tap and
	// stays in this card until the page is left.
	// Deliberately the starting value: after that the eye is in charge
	const initialPreview = untrack(() => entry.preview);
	let preview = $state<string | null>(initialPreview);
	let revealed = $state(Boolean(initialPreview));
	let loadingPreview = $state(false);
	let previewError = $state(false);
	const previewId = $derived(`entry-preview-${entry.id}`);
	const labelId = $derived(`entry-reflection-${entry.id}`);

	/** Same rule as the server: the start of the first Reflection box written in */
	function previewOf(full: Entry): string {
		const text =
			(reflection.textFields ?? [])
				.map((f) => String(full[f.id as keyof Entry] ?? '').trim())
				.find(Boolean) ?? '';
		return text.length <= PREVIEW_LENGTH ? text : text.slice(0, PREVIEW_LENGTH).trimEnd() + '…';
	}

	async function toggleReveal() {
		// Not disabled while loading: a disabled button would drop keyboard focus
		if (loadingPreview) return;
		if (revealed) {
			revealed = false;
			return;
		}
		if (preview === null) {
			loadingPreview = true;
			previewError = false;
			try {
				preview = previewOf(await entriesApi.get(entry.id));
			} catch (e) {
				console.error('Failed to load preview:', e);
				previewError = true;
				return;
			} finally {
				loadingPreview = false;
			}
		}
		revealed = true;
	}

	const day = $derived(new Date(entry.date + 'T00:00:00'));
	const dayLabel = $derived.by(() => {
		const today = localISODate();
		if (entry.date === today) return 'Today';
		if (entry.date === addDays(today, -1)) return 'Yesterday';
		return day.toLocaleDateString('en-NZ', { weekday: 'long' });
	});
	const fullDate = $derived(
		day.toLocaleDateString('en-NZ', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
	);
	const indicators = $derived(
		INDICATOR_PILLARS.map((pillar) => ({ pillar, ...pillarScore(pillar, entry) }))
	);
</script>

<article class="entry-card">
	<header class="entry-card__header">
		<time class="entry-card__datebox" datetime={entry.date} aria-label={fullDate}>
			<span class="entry-card__day">{day.getDate()}</span>
			<span class="entry-card__month">{day.toLocaleDateString('en-NZ', { month: 'short' })}</span>
		</time>
		<div>
			<p class="entry-card__weekday">{dayLabel}</p>
			{#if entry.overall_day_rating}
				<p class="entry-card__rating">
					<strong>{entry.overall_day_rating}</strong>/{SCALE_MAX}
					· {describeScaleValue(entry.overall_day_rating, overallScale)}
				</p>
			{:else}
				<p class="entry-card__rating entry-card__rating--none">Day not rated</p>
			{/if}
		</div>
	</header>

	{#if showIndicators}
		<ul class="entry-card__pillars" aria-label="Hauora indicators">
			{#each indicators as { pillar, score } (pillar.id)}
				<li style="--pillar-color: {pillar.color}; --pillar-tint: {pillar.tint}">
					<span class="entry-card__pillar-name">{pillar.name}</span>
					<span class="entry-card__meter" aria-hidden="true">
						{#if score !== null}
							<span style="width: {(score / SCALE_MAX) * 100}%"></span>
						{/if}
					</span>
					<span class="visually-hidden">
						{score === null ? 'not rated' : `${formatScore(score)} out of ${SCALE_MAX}`}
					</span>
				</li>
			{/each}
		</ul>
	{/if}

	<!-- Same size on every card, hidden or shown, so tapping the eye never
	     moves anything. The button comes before the text it reveals. -->
	<div class="entry-card__reflection" class:entry-card__reflection--empty={!entry.has_reflection}>
		<div class="entry-card__reflection-bar">
			{#if entry.has_reflection}
				<span class="entry-card__reflection-label" id={labelId}>
					<!-- Short label so it never wraps on narrow cards; the lock marks hidden -->
					{#if !revealed}<LockIcon /><span class="visually-hidden">Hidden:</span>{/if}
					Reflection
				</span>
				<button
					type="button"
					class="entry-card__reveal"
					aria-expanded={revealed}
					aria-controls={previewId}
					aria-describedby={labelId}
					aria-busy={loadingPreview}
					onclick={toggleReveal}
				>
					<EyeIcon off={revealed} />
					{revealed ? 'Hide' : 'Show'}<span class="visually-hidden">{` reflection for ${fullDate}`}</span>
				</button>
			{:else}
				<span class="entry-card__reflection-label">Nothing written</span>
			{/if}
		</div>
		<div class="entry-card__reflection-body" id={previewId}>
			{#if revealed && preview}
				<p class="entry-card__preview">{preview}</p>
			{:else if previewError}
				<p class="entry-card__preview entry-card__preview--error" role="status">
					Couldn't load the preview. Try again.
				</p>
			{:else if entry.has_reflection}
				<!-- Redaction bars: a hint of hidden text, never the text itself -->
				<span class="entry-card__redacted" aria-hidden="true"><span></span><span></span><span></span></span>
			{/if}
		</div>
	</div>

	<footer class="entry-card__footer">
		<a {href} class="entry-card__link">
			View entry
			<span aria-hidden="true">→</span>
		</a>
	</footer>
</article>

<style lang="scss">
	.entry-card {
		background: var(--color-surface);
		border-radius: var(--radius-lg);
		padding: var(--space-md);
		box-shadow: var(--shadow-sm);
		display: flex;
		flex-direction: column;
		gap: var(--space-sm);
		transition: box-shadow var(--transition-fast), transform var(--transition-fast);

		&:hover {
			box-shadow: var(--shadow-md);
			transform: translateY(-2px);
		}
	}

	.entry-card__header {
		display: flex;
		align-items: center;
		gap: var(--space-sm);

		p {
			margin: 0;
		}
	}

	/* A small calendar leaf: day number over the month */
	.entry-card__datebox {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		flex: none;
		width: 3.25rem;
		height: 3.25rem;
		border-radius: var(--radius-md);
		background: var(--color-primary-tint);
		color: var(--color-primary);
		line-height: 1;
	}

	.entry-card__day {
		font-family: var(--font-family-display);
		font-size: var(--font-size-xl);
		font-weight: 500;
	}

	.entry-card__month {
		font-size: var(--font-size-xs);
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		margin-top: 2px;
	}

	.entry-card__weekday {
		font-weight: 600;
		color: var(--color-text);
	}

	.entry-card__rating {
		font-size: var(--font-size-sm);
		color: var(--color-text-muted);

		strong {
			color: var(--color-text);
			font-size: var(--font-size-base);
		}
	}

	.entry-card__rating--none {
		font-style: italic;
	}

	.entry-card__pillars {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: var(--space-xs) var(--space-sm);

		li {
			display: flex;
			flex-direction: column;
			gap: 3px;
			min-width: 0;
		}
	}

	.entry-card__pillar-name {
		font-size: var(--font-size-xs);
		color: var(--color-text-muted);
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.entry-card__meter {
		display: block;
		height: 6px;
		border-radius: 3px;
		background: var(--pillar-tint);
		box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--pillar-color) 20%, transparent);
		overflow: hidden;

		span {
			display: block;
			height: 100%;
			border-radius: 3px;
			background: var(--pillar-color);
		}
	}

	/* Three lines of text plus the bar, on every card */
	.entry-card__reflection {
		--preview-lines: 3;
		--preview-line-height: 1.5;
		display: flex;
		flex-direction: column;
		gap: var(--space-xxs);
		padding: var(--space-xs) var(--space-sm) var(--space-sm);
		background: var(--color-bg);
		border-radius: var(--radius-md);
	}

	/* Fixed height and no wrapping, so the bar is the same in every state */
	.entry-card__reflection-bar {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: var(--space-xs);
		height: 2rem;
	}

	.entry-card__reflection-label {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		min-width: 0;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		font-size: var(--font-size-sm);
		color: var(--color-text-muted);
	}

	.entry-card__reflection--empty .entry-card__reflection-label {
		font-style: italic;
	}

	.entry-card__reflection-body {
		height: calc(var(--preview-lines) * var(--preview-line-height) * 1rem);
		overflow: hidden;
	}

	.entry-card__preview {
		margin: 0;
		color: var(--color-text);
		line-height: var(--preview-line-height);
		display: -webkit-box;
		-webkit-box-orient: vertical;
		-webkit-line-clamp: var(--preview-lines);
		line-clamp: var(--preview-lines);
		overflow: hidden;
	}

	@media (prefers-reduced-motion: no-preference) {
		.entry-card__preview {
			animation: preview-in 150ms ease-out;
		}
	}

	@keyframes preview-in {
		from {
			opacity: 0;
		}
	}

	.entry-card__preview--error {
		font-size: var(--font-size-sm);
		color: var(--color-error);
	}

	/* Soft bars standing in for the hidden lines */
	.entry-card__redacted {
		display: flex;
		flex-direction: column;
		justify-content: space-around;
		height: 100%;

		span {
			display: block;
			height: 0.5rem;
			border-radius: 0.25rem;
			background: var(--color-border);
			opacity: 0.6;
		}

		span:nth-child(2) {
			width: 85%;
		}

		span:nth-child(3) {
			width: 55%;
		}
	}

	/* Quiet text button that stays in the same spot in both states */
	.entry-card__reveal {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		justify-content: center;
		min-height: 2rem;
		min-width: 4.75rem; /* fits Show and Hide, so it doesn't shift */
		padding: 0 var(--space-xs);
		margin-right: calc(-1 * var(--space-xs));
		background: none;
		border: none;
		border-radius: var(--radius-sm);
		color: var(--color-link);
		font-size: var(--font-size-sm);
		font-weight: 500;
		white-space: nowrap;
		cursor: pointer;

		&:hover {
			background: var(--color-primary-tint);
			color: var(--color-primary);
		}

		&:focus-visible {
			outline: 2px solid var(--color-focus);
			outline-offset: 2px;
		}

		&[aria-busy='true'] {
			cursor: progress;
		}
	}

	.entry-card__footer {
		display: flex;
		justify-content: flex-end;
		margin-top: auto;
	}

	.entry-card__link {
		margin-left: auto;
		white-space: nowrap;
		color: var(--color-link);
		text-decoration: none;
		font-size: var(--font-size-sm);
		font-weight: 500;
		display: flex;
		align-items: center;
		gap: var(--space-xs);
		transition: color var(--transition-fast);

		&:hover {
			color: var(--color-link-hover);
		}
	}
</style>
