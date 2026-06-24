<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { entriesApi, type Entry } from '$lib/api/entries';
	import ArrowRightIcon from '$lib/icons/ArrowRightIcon.svelte';

	let entry = $state<Entry | null>(null);
	let loading = $state(true);
	let error = $state<string | null>(null);

	const id = $derived(Number($page.params.id));

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

	function getRatingLabel(value: number | null): string {
		if (value === null) return '—';
		return `${value}/10`;
	}

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

<div class="entry-detail">
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
				<span class="overall-rating">Overall: {entry.overall_day_rating}/10</span>
			{/if}
		</header>

		<!-- Reflection Section -->
		{#if entry.log || entry.best_thing_today || entry.hardest_thing_today || entry.significant_events}
			<section class="section">
				<h2>Reflection</h2>

				{#if entry.best_thing_today}
					<div class="field">
						<h3>Best thing today</h3>
						<p>{entry.best_thing_today}</p>
					</div>
				{/if}

				{#if entry.hardest_thing_today}
					<div class="field">
						<h3>Hardest thing today</h3>
						<p>{entry.hardest_thing_today}</p>
					</div>
				{/if}

				{#if entry.significant_events}
					<div class="field">
						<h3>Significant events</h3>
						<p>{entry.significant_events}</p>
					</div>
				{/if}

				{#if entry.log}
					<div class="field">
						<h3>Journal</h3>
						<p class="log">{entry.log}</p>
					</div>
				{/if}
			</section>
		{/if}

		<!-- Hauora Overview -->
		<section class="section">
			<h2>Hauora Overview</h2>
			<div class="pillars-grid">
				<div class="pillar-card" style="--pillar-color: var(--color-hinengaro)">
					<h3>Hinengaro</h3>
					<dl>
						<div><dt>Mood</dt><dd>{getRatingLabel(entry.mood)}</dd></div>
						<div><dt>Anxiety</dt><dd>{getRatingLabel(entry.anxiety_level)}</dd></div>
						<div><dt>Stress</dt><dd>{getRatingLabel(entry.stress_level)}</dd></div>
					</dl>
				</div>

				<div class="pillar-card" style="--pillar-color: var(--color-tinana)">
					<h3>Tinana</h3>
					<dl>
						<div><dt>Sleep</dt><dd>{entry.sleep_hours ? `${entry.sleep_hours}h` : '—'}</dd></div>
						<div><dt>Sleep quality</dt><dd>{getRatingLabel(entry.sleep_quality)}</dd></div>
						<div><dt>Exercise</dt><dd>{getRatingLabel(entry.exercise_level)}</dd></div>
						<div><dt>Diet</dt><dd>{getRatingLabel(entry.diet_quality)}</dd></div>
						<div><dt>Energy</dt><dd>{getRatingLabel(entry.energy_level)}</dd></div>
					</dl>
				</div>

				<div class="pillar-card" style="--pillar-color: var(--color-whanau)">
					<h3>Whānau</h3>
					<dl>
						<div><dt>Connection</dt><dd>{getRatingLabel(entry.social_connection)}</dd></div>
						<div><dt>Quality</dt><dd>{getRatingLabel(entry.social_interactions_quality)}</dd></div>
					</dl>
				</div>

				<div class="pillar-card" style="--pillar-color: var(--color-wairua)">
					<h3>Wairua</h3>
					<dl>
						<div><dt>Sense of meaning</dt><dd>{getRatingLabel(entry.sense_of_meaning)}</dd></div>
					</dl>
				</div>

				<div class="pillar-card" style="--pillar-color: var(--color-mauriora)">
					<h3>Mauriora</h3>
					<dl>
						<div><dt>Felt like myself</dt><dd>{getRatingLabel(entry.felt_like_myself)}</dd></div>
					</dl>
				</div>

				<div class="pillar-card" style="--pillar-color: var(--color-waiora)">
					<h3>Waiora</h3>
					<dl>
						<div><dt>Environment</dt><dd>{getRatingLabel(entry.environment_quality)}</dd></div>
					</dl>
				</div>
			</div>
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
		padding: var(--space-lg) var(--space-md);
		max-width: 800px;
		margin: 0 auto;
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
		color: var(--color-moana);
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
		display: inline-block;
		padding: var(--space-xs) var(--space-sm);
		background: var(--color-bg);
		border-radius: var(--radius-md);
		font-size: var(--font-size-sm);
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

	.log {
		white-space: pre-wrap;
	}

	.pillars-grid {
		display: grid;
		gap: var(--space-md);
		grid-template-columns: 1fr;

		@media (min-width: 500px) {
			grid-template-columns: repeat(2, 1fr);
		}

		@media (min-width: 700px) {
			grid-template-columns: repeat(3, 1fr);
		}
	}

	.pillar-card {
		background: var(--color-surface);
		border-radius: var(--radius-md);
		padding: var(--space-md);
		border-left: 3px solid var(--pillar-color);

		h3 {
			font-size: var(--font-size-base);
			color: var(--pillar-color);
			margin-bottom: var(--space-sm);
		}

		dl {
			display: flex;
			flex-direction: column;
			gap: var(--space-xs);
		}

		dl > div {
			display: flex;
			justify-content: space-between;
			font-size: var(--font-size-sm);
		}

		dt {
			color: var(--color-text-muted);
		}

		dd {
			color: var(--color-text);
			font-weight: 500;
		}
	}

	.actions {
		display: flex;
		gap: var(--space-sm);
		padding-top: var(--space-lg);
		border-top: 1px solid var(--color-border);
	}
</style>
