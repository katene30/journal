<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { entriesApi, type Entry } from '$lib/api/entries';
	import { PILLARS, describeScaleValue, getPillarById } from '$lib/config/pillars';
	import { SCALE_MAX, formatScore, pillarScore } from '$lib/utils/hauora';
	import ArrowRightIcon from '$lib/icons/ArrowRightIcon.svelte';

	const OVERVIEW_PILLARS = PILLARS.filter((p) => p.id !== 'reflection');
	const overallScale = getPillarById('reflection')!.scales[0];
	const REFLECTION_FIELDS = getPillarById('reflection')!.textFields ?? [];

	let entry = $state<Entry | null>(null);
	let loading = $state(true);
	let error = $state<string | null>(null);

	const id = $derived(Number($page.params.id));
	const reflectionText = $derived(
		entry
			? REFLECTION_FIELDS.map((f) => ({ ...f, value: String(entry![f.id as keyof Entry] ?? '').trim() })).filter(
					(f) => f.value
				)
			: []
	);

	onMount(async () => {
		try {
			entry = await entriesApi.get(id);
		} catch (e) {
			console.error('Failed to load entry:', e);
			error = 'Entry not found';
		} finally {
			loading = false;
		}
	});

	function formatDate(dateStr: string): string {
		const date = new Date(dateStr + 'T00:00:00');
		return date.toLocaleDateString('en-NZ', {
			weekday: 'long',
			day: 'numeric',
			month: 'long',
			year: 'numeric'
		});
	}

	const scaleValue = (field: string) => (entry as Record<string, unknown> | null)?.[field] as number | null;

	// Extra Tinana details that aren't 1-5 ratings
	const tinanaExtras = $derived(
		entry
			? [
					entry.sleep_hours !== null && { label: 'Hours of sleep', value: `${entry.sleep_hours}h` },
					entry.alcohol_caffeine_consumption && {
						label: 'Alcohol/caffeine',
						value: entry.alcohol_caffeine_consumption
					}
				].filter((x): x is { label: string; value: string } => Boolean(x))
			: []
	);

	async function handleDelete() {
		if (!entry) return;
		if (!confirm('Are you sure you want to delete this entry?')) return;

		try {
			await entriesApi.delete(entry.id);
			goto('/app/entries');
		} catch (e) {
			console.error('Failed to delete entry:', e);
			alert('Failed to delete entry');
		}
	}
</script>

<div class="entry-detail reading-column">
	{#if loading}
		<p class="loading">Loading...</p>
	{:else if error || !entry}
		<p class="error">{error || 'Entry not found'}</p>
		<a href="/app/entries" class="back-link">← Back to entries</a>
	{:else}
		<a href="/app/entries" class="back-link">← Back to entries</a>

		<header class="entry-header">
			<h1>{formatDate(entry.date)}</h1>
			{#if entry.overall_day_rating !== null}
				<p class="overall-rating">
					Overall day <strong>{entry.overall_day_rating}</strong><span class="out-of">/ {SCALE_MAX}</span>
					· {describeScaleValue(entry.overall_day_rating, overallScale)}
				</p>
			{/if}
		</header>

		<!-- Reflection Section: same fields, same order as the New Entry form -->
		{#if reflectionText.length}
			<section class="section">
				<h2>Reflection</h2>

				{#each reflectionText as field (field.id)}
					<div class="field">
						<h3>{field.label}</h3>
						<p class="field__text">{field.value}</p>
					</div>
				{/each}
			</section>
		{/if}

		<!-- Hauora Overview: one indicator per pillar, details on request -->
		<section class="section" aria-labelledby="overview-heading">
			<h2 id="overview-heading">Hauora overview</h2>
			<p class="section__intro">Select a pillar to see what went into it.</p>

			<div class="pillars-grid">
				{#each OVERVIEW_PILLARS as pillar (pillar.id)}
					{@const result = pillarScore(pillar, entry)}
					<details
						class="pillar"
						style="--pillar-color: {pillar.color}; --pillar-ink: {pillar.chartColor ?? pillar.color}"
					>
						<summary>
							<span class="pillar__heading">
								<span class="pillar__name">{pillar.name}</span>
								<span class="pillar__theme">{pillar.theme}</span>
							</span>
							{#if result.score !== null}
								<span class="pillar__score">
									<strong>{formatScore(result.score)}</strong><span class="out-of">/ {SCALE_MAX}</span>
								</span>
								<span class="pillar__meter" aria-hidden="true">
									<span style="width: {(result.score / SCALE_MAX) * 100}%"></span>
								</span>
								{#if result.rated < result.total}
									<span class="pillar__note">{result.rated} of {result.total} rated</span>
								{/if}
							{:else}
								<span class="pillar__score pillar__score--empty">Not rated</span>
							{/if}
						</summary>

						<dl class="pillar__details">
							{#each pillar.scales as scale (scale.id)}
								{@const value = scaleValue(scale.id)}
								<div>
									<dt>{scale.title}</dt>
									<dd>
										{#if value !== null}
											<strong>{value}</strong> {describeScaleValue(value, scale)}
										{:else}
											<span class="muted">Not rated</span>
										{/if}
									</dd>
								</div>
							{/each}
							{#if pillar.id === 'tinana'}
								{#each tinanaExtras as extra (extra.label)}
									<div>
										<dt>{extra.label}</dt>
										<dd>{extra.value}</dd>
									</div>
								{/each}
							{/if}
						</dl>
						{#if pillar.scales.some((s) => s.reversed)}
							<p class="pillar__hint">Calmer and more relaxed raise this score.</p>
						{/if}
					</details>
				{/each}
			</div>

			<p class="overview-note">
				Each score is the average of that pillar's ratings for the day, from 1 to 5. It's a personal
				snapshot of how the day felt, not a measure of your hauora.
			</p>
		</section>

		<!-- Actions -->
		<footer class="actions">
			<a href="/app/new?date={entry.date}" class="btn btn--primary">
				Edit Entry <ArrowRightIcon />
			</a>
			<button type="button" class="btn btn--danger" onclick={handleDelete}>
				Delete
			</button>
		</footer>
	{/if}
</div>

<style lang="scss">
	.entry-detail {
		--reading-max: 800px;
		padding-block: var(--space-lg);
	}

	.loading,
	.error {
		text-align: center;
		padding: var(--space-xl);
		color: var(--color-text-muted);
	}

	.error {
		color: var(--color-error);
	}

	.back-link {
		display: inline-block;
		color: var(--color-link);
		text-decoration: none;
		margin-bottom: var(--space-md);

		&:hover {
			text-decoration: underline;
		}
	}

	.entry-header {
		margin-bottom: var(--space-xl);

		h1 {
			font-size: var(--font-size-xl);
			color: var(--color-text);
			margin-bottom: var(--space-xs);
		}
	}

	.overall-rating {
		margin: 0;
		color: var(--color-text-muted);

		strong {
			color: var(--color-text);
			font-size: var(--font-size-lg);
		}
	}

	.out-of {
		margin-left: 2px;
		font-size: var(--font-size-sm);
		color: var(--color-text-muted);
	}

	.muted {
		color: var(--color-text-muted);
	}

	.section {
		margin-bottom: var(--space-xl);

		h2 {
			font-size: var(--font-size-lg);
			color: var(--color-text);
			margin-bottom: var(--space-md);
			padding-bottom: var(--space-xs);
			border-bottom: 1px solid var(--color-border);
		}
	}

	.section__intro {
		margin: calc(var(--space-xs) - var(--space-md)) 0 var(--space-sm);
		font-size: var(--font-size-sm);
		color: var(--color-text-muted);
	}

	.field {
		margin-bottom: var(--space-md);

		h3 {
			font-size: var(--font-size-sm);
			color: var(--color-text-muted);
			font-weight: 500;
			margin-bottom: var(--space-xs);
		}

		p {
			color: var(--color-text);
			line-height: 1.6;
		}
	}

	.field__text {
		white-space: pre-wrap;
	}

	.pillars-grid {
		display: grid;
		gap: var(--space-sm);
		grid-template-columns: 1fr;
		align-items: start;

		@media (min-width: 500px) {
			grid-template-columns: repeat(2, 1fr);
		}

		@media (min-width: 700px) {
			grid-template-columns: repeat(3, 1fr);
		}
	}

	.pillar {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-left: 4px solid var(--pillar-color);
		border-radius: var(--radius-md);

		&[open] summary::after {
			transform: translateY(4px) rotate(-135deg);
		}
	}

	summary {
		position: relative;
		display: grid;
		grid-template-columns: 1fr auto;
		align-items: baseline;
		gap: var(--space-xs) var(--space-sm);
		padding: var(--space-sm) calc(var(--space-sm) + 20px) var(--space-sm) var(--space-sm);
		cursor: pointer;
		list-style: none;
		border-radius: var(--radius-md);

		&::-webkit-details-marker {
			display: none;
		}

		/* Chevron */
		&::after {
			content: '';
			position: absolute;
			top: calc(var(--space-sm) + 6px);
			right: var(--space-sm);
			width: 8px;
			height: 8px;
			border-right: 2px solid var(--color-text-muted);
			border-bottom: 2px solid var(--color-text-muted);
			transform: rotate(45deg);
			transform-origin: 60% 60%;
			transition: transform var(--transition-fast);
		}

		&:hover::after {
			border-color: var(--color-text);
		}

		&:focus-visible {
			outline: 2px solid var(--color-focus);
			outline-offset: 2px;
		}
	}

	.pillar__heading {
		display: flex;
		flex-direction: column;
		min-width: 0;
	}

	.pillar__name {
		font-weight: 600;
		color: var(--pillar-ink);
	}

	.pillar__theme {
		font-size: var(--font-size-xs);
		color: var(--color-text-muted);
	}

	.pillar__score {
		white-space: nowrap;

		strong {
			font-size: var(--font-size-xl);
			font-variant-numeric: tabular-nums;
			color: var(--color-text);
		}
	}

	.pillar__score--empty {
		font-size: var(--font-size-sm);
		color: var(--color-text-muted);
	}

	.pillar__meter {
		grid-column: 1 / -1;
		height: 6px;
		border-radius: var(--radius-full);
		background: color-mix(in srgb, var(--pillar-color) 15%, var(--color-surface));
		overflow: hidden;

		span {
			display: block;
			height: 100%;
			border-radius: var(--radius-full);
			background: var(--pillar-ink);
		}
	}

	.pillar__note {
		grid-column: 1 / -1;
		font-size: var(--font-size-xs);
		color: var(--color-text-muted);
	}

	.pillar__details {
		display: flex;
		flex-direction: column;
		gap: var(--space-xs);
		margin: 0;
		padding: var(--space-sm);
		border-top: 1px solid var(--color-border);

		> div {
			display: flex;
			justify-content: space-between;
			gap: var(--space-sm);
			font-size: var(--font-size-sm);
		}

		dt {
			color: var(--color-text-muted);
		}

		dd {
			margin: 0;
			text-align: right;
			color: var(--color-text);
		}
	}

	.pillar__hint {
		margin: 0;
		padding: 0 var(--space-sm) var(--space-sm);
		font-size: var(--font-size-xs);
		color: var(--color-text-muted);
	}

	.overview-note {
		margin: var(--space-sm) 0 0;
		font-size: var(--font-size-xs);
		color: var(--color-text-muted);
	}

	.actions {
		display: flex;
		gap: var(--space-sm);
		padding-top: var(--space-lg);
		border-top: 1px solid var(--color-border);
	}
</style>
