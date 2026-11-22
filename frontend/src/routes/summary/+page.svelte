<script lang="ts">
	import { entriesApi, type EntryRange, type ScaleField } from '$lib/api/entries';
	import { PILLARS, getPillarById, describeScaleValue } from '$lib/config/pillars';
	import PillarNav from '$lib/components/PillarNav.svelte';
	import TrendChart from '$lib/components/TrendChart.svelte';
	import ArrowRightIcon from '$lib/icons/ArrowRightIcon.svelte';
	import type { PillarId } from '$lib/types';
	import { addDays, daysBetween, formatLongDate, formatShortDate, localISODate } from '$lib/utils/dates';

	type Preset = 7 | 30 | 90 | 'custom';
	const PRESETS: { value: Preset; label: string }[] = [
		{ value: 7, label: '7 days' },
		{ value: 30, label: '30 days' },
		{ value: 90, label: '90 days' },
		{ value: 'custom', label: 'Custom' }
	];
	const MAX_DAYS = 366; // matches the API limit

	const today = localISODate();

	let preset = $state<Preset>(30);
	let customStart = $state(addDays(today, -29));
	let customEnd = $state(today);
	let pillarId = $state<PillarId>('reflection');

	let data = $state<EntryRange | null>(null);
	let loading = $state(false);
	let error = $state<string | null>(null);

	const rangeError = $derived.by(() => {
		if (preset !== 'custom') return null;
		if (!customStart || !customEnd) return 'Choose a start and end date.';
		if (customStart > customEnd) return 'The start date needs to be before the end date.';
		if (daysBetween(customStart, customEnd) + 1 > MAX_DAYS) return `Choose ${MAX_DAYS} days or fewer.`;
		return null;
	});

	const range = $derived(
		preset === 'custom'
			? { start: customStart, end: customEnd }
			: { start: addDays(today, -(preset - 1)), end: today }
	);

	// Refetch whenever the range changes. Older responses are ignored if a newer
	// request has started, and the previous charts stay on screen (dimmed) meanwhile.
	let requestId = 0;
	$effect(() => {
		if (rangeError) return;
		const { start, end } = range;
		const id = ++requestId;
		loading = true;
		error = null;
		entriesApi
			.range(start, end)
			.then((result) => {
				if (id === requestId) data = result;
			})
			.catch(() => {
				if (id === requestId) error = "Couldn't load your entries. Please try again.";
			})
			.finally(() => {
				if (id === requestId) loading = false;
			});
	});

	function selectPreset(value: Preset) {
		if (value === 'custom' && preset !== 'custom') {
			// Start the custom inputs from whatever is showing now
			customStart = range.start;
			customEnd = range.end;
		}
		preset = value;
	}

	const pillar = $derived(getPillarById(pillarId) ?? PILLARS[0]);
	const entries = $derived(data?.entries ?? []);
	const daysInRange = $derived(data ? daysBetween(data.start, data.end) + 1 : 0);

	function average(field: ScaleField): number | null {
		const values = entries.map((e) => e[field]).filter((v): v is number => v !== null);
		if (!values.length) return null;
		return values.reduce((a, b) => a + b, 0) / values.length;
	}

	const overallScale = PILLARS[0].scales[0];
	const moodScale = PILLARS.find((p) => p.id === 'hinengaro')!.scales[0];
	const avgDay = $derived(average('overall_day_rating'));
	const avgMood = $derived(average('mood'));
</script>

<svelte:head>
	<title>Summary · Hauora Journal</title>
</svelte:head>

<div class="summary-page">
	<header class="page-header">
		<h1>Summary</h1>
		{#if data}
			<p class="page-header__range">{formatLongDate(data.start)} – {formatLongDate(data.end)}</p>
		{/if}
	</header>

	<!-- Filters: one row, above everything they scope -->
	<div class="filters">
		<div class="presets" role="radiogroup" aria-label="Date range">
			{#each PRESETS as p}
				<button
					type="button"
					role="radio"
					aria-checked={preset === p.value}
					class="presets__option"
					class:presets__option--active={preset === p.value}
					onclick={() => selectPreset(p.value)}
				>
					{p.label}
				</button>
			{/each}
		</div>

		{#if preset === 'custom'}
			<div class="custom-range">
				<label>
					<span>From</span>
					<input type="date" bind:value={customStart} max={customEnd || today} />
				</label>
				<label>
					<span>To</span>
					<input type="date" bind:value={customEnd} min={customStart} max={today} />
				</label>
			</div>
			{#if rangeError}
				<p class="field-error" role="alert">{rangeError}</p>
			{/if}
		{/if}
	</div>

	{#if error}
		<p class="error" role="alert">{error}</p>
	{:else if !data}
		<p class="loading">Loading your summary…</p>
	{:else}
		<div class="results" class:results--refreshing={loading} aria-busy={loading}>
			{#if entries.length === 0}
				<div class="empty-state">
					<p>No entries between {formatShortDate(data.start)} and {formatShortDate(data.end)}.</p>
					<a href="/app/new" class="btn btn--primary">New entry <ArrowRightIcon /></a>
				</div>
			{:else}
				<section class="stats" aria-label="Overview">
					<div class="stat">
						<span class="stat__label">Days logged</span>
						<span class="stat__value">{entries.length}<span class="stat__unit"> of {daysInRange}</span></span>
					</div>
					<div class="stat">
						<span class="stat__label">Average day</span>
						{#if avgDay !== null}
							<span class="stat__value">{avgDay.toFixed(1)}</span>
							<span class="stat__note">{describeScaleValue(avgDay, overallScale)}</span>
						{:else}
							<span class="stat__value stat__value--none">–</span>
						{/if}
					</div>
					<div class="stat">
						<span class="stat__label">Average mood</span>
						{#if avgMood !== null}
							<span class="stat__value">{avgMood.toFixed(1)}</span>
							<span class="stat__note">{describeScaleValue(avgMood, moodScale)}</span>
						{:else}
							<span class="stat__value stat__value--none">–</span>
						{/if}
					</div>
				</section>

				<section class="pillar-section" aria-labelledby="pillar-heading">
					<PillarNav activePillar={pillarId} onselect={(id) => (pillarId = id)} />

					<h2 id="pillar-heading" class="pillar-heading">
						{pillar.name}
						<span class="pillar-heading__en">{pillar.question.english}</span>
					</h2>

					<div class="charts" class:charts--single={pillar.scales.length === 1}>
						{#each pillar.scales as scale (scale.id)}
							<TrendChart
								title={scale.title}
								leftLabel={scale.leftLabel}
								rightLabel={scale.rightLabel}
								color={pillar.chartColor ?? pillar.color}
								start={data.start}
								end={data.end}
								points={entries.map((e) => ({ date: e.date, value: e[scale.id as ScaleField] }))}
							/>
						{/each}
					</div>

					<details class="data-table">
						<summary>Show {pillar.name} as a table</summary>
						<div class="data-table__scroll">
							<table>
								<caption class="visually-hidden">{pillar.name} ratings by day, 1 to 5</caption>
								<thead>
									<tr>
										<th scope="col">Date</th>
										{#each pillar.scales as scale}
											<th scope="col">{scale.title}</th>
										{/each}
									</tr>
								</thead>
								<tbody>
									{#each [...entries].reverse() as entry (entry.id)}
										<tr>
											<th scope="row"><a href="/app/entries/{entry.id}">{formatLongDate(entry.date)}</a></th>
											{#each pillar.scales as scale}
												{@const v = entry[scale.id as ScaleField]}
												<td>
													{#if v === null}
														<span class="muted">–</span>
													{:else}
														{v} <span class="muted">{describeScaleValue(v, scale)}</span>
													{/if}
												</td>
											{/each}
										</tr>
									{/each}
								</tbody>
							</table>
						</div>
					</details>
				</section>
			{/if}
		</div>
	{/if}
</div>

<style lang="scss">
	.summary-page {
		padding: var(--space-lg) var(--space-md);
		max-width: 1000px;
		margin: 0 auto;
	}

	.page-header {
		margin-bottom: var(--space-md);

		h1 {
			font-size: var(--font-size-xl);
			color: var(--color-text);
			margin: 0;
		}
	}

	.page-header__range {
		margin: var(--space-xxs) 0 0;
		color: var(--color-text-muted);
		font-size: var(--font-size-sm);
	}

	/* Filters */
	.filters {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: var(--space-sm);
		margin-bottom: var(--space-md);
	}

	.presets {
		display: flex;
		width: 100%;
		padding: var(--space-xxs);
		gap: var(--space-xxs);
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
	}

	.presets__option {
		flex: 1;
		white-space: nowrap;
		min-height: 40px;
		padding: 0 var(--space-sm);
		border: none;
		border-radius: var(--radius-sm);
		background: transparent;
		color: var(--color-text-muted);
		font: inherit;
		font-size: var(--font-size-sm);
		cursor: pointer;
		transition: background var(--transition-fast);

		&:hover {
			background: var(--color-bg);
			color: var(--color-text);
		}

		&:focus-visible {
			outline: 2px solid var(--color-focus);
			outline-offset: 2px;
		}
	}

	@media (min-width: 500px) {
		.presets {
			display: inline-flex;
			width: auto;
		}
	}

	.presets__option--active,
	.presets__option--active:hover {
		background: var(--color-moana);
		color: white;
		font-weight: 600;
	}

	.custom-range {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-sm);

		label {
			display: flex;
			align-items: center;
			gap: var(--space-xs);
			font-size: var(--font-size-sm);
			color: var(--color-text-muted);
		}

		input {
			min-height: 40px;
			padding: 0 var(--space-xs);
			border: 1px solid var(--color-border);
			border-radius: var(--radius-sm);
			background: var(--color-surface);
			color: var(--color-text);
			font: inherit;

			&:focus-visible {
				outline: 2px solid var(--color-focus);
				outline-offset: 1px;
			}
		}
	}

	.field-error {
		flex-basis: 100%;
		margin: 0;
		color: var(--color-error);
		font-size: var(--font-size-sm);
	}

	/* States */
	.loading,
	.error {
		text-align: center;
		padding: var(--space-xl);
		color: var(--color-text-muted);
	}

	.error {
		color: var(--color-error);
	}

	.results {
		transition: opacity var(--transition-base);
	}

	.results--refreshing {
		opacity: 0.5;
	}

	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: var(--space-sm);
		text-align: center;
		padding: var(--space-xl);
		background: var(--color-surface);
		border-radius: var(--radius-lg);

		p {
			margin: 0;
			color: var(--color-text-muted);
		}
	}

	/* Stat tiles */
	.stats {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: var(--space-xs);

		@media (min-width: 500px) {
			gap: var(--space-sm);
		}
		margin-bottom: var(--space-lg);
	}

	.stat {
		display: flex;
		flex-direction: column;
		gap: var(--space-xxs);
		min-width: 0;
		padding: var(--space-xs);

		@media (min-width: 500px) {
			padding: var(--space-sm);
		}
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
	}

	.stat__label {
		font-size: var(--font-size-xs);

		@media (min-width: 500px) {
			font-size: var(--font-size-sm);
		}
		color: var(--color-text-muted);
	}

	.stat__value {
		font-size: var(--font-size-xl);

		@media (min-width: 500px) {
			font-size: var(--font-size-xxl);
		}
		font-weight: 600;
		line-height: var(--line-height-tight);
		color: var(--color-text);
	}

	.stat__value--none {
		color: var(--color-text-muted);
	}

	.stat__unit {
		font-size: var(--font-size-sm);
		font-weight: 400;
		color: var(--color-text-muted);
	}

	.stat__note {
		font-size: var(--font-size-xs);

		@media (min-width: 500px) {
			font-size: var(--font-size-sm);
		}
		color: var(--color-text-muted);
	}

	/* Pillar charts */
	.pillar-heading {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		gap: var(--space-xxs) var(--space-sm);
		margin: var(--space-md) 0 var(--space-sm);
		font-size: var(--font-size-lg);
		color: var(--color-text);
	}

	.pillar-heading__en {
		font-size: var(--font-size-sm);
		font-weight: 400;
		color: var(--color-text-muted);
	}

	.charts {
		display: grid;
		grid-template-columns: 1fr;
		gap: var(--space-sm);

		@media (min-width: 768px) {
			grid-template-columns: repeat(2, 1fr);
		}
	}

	.charts--single {
		@media (min-width: 768px) {
			grid-template-columns: 1fr;
		}
	}

	/* Table view */
	.data-table {
		margin-top: var(--space-md);

		summary {
			cursor: pointer;
			color: var(--color-moana);
			font-weight: 500;
			min-height: 44px;
			display: flex;
			align-items: center;

			&:focus-visible {
				outline: 2px solid var(--color-focus);
				outline-offset: 2px;
			}
		}
	}

	.data-table__scroll {
		overflow-x: auto;
		margin-top: var(--space-xs);
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
	}

	table {
		width: 100%;
		border-collapse: collapse;
		font-size: var(--font-size-sm);
		font-variant-numeric: tabular-nums;
	}

	th,
	td {
		padding: var(--space-xs) var(--space-sm);
		text-align: left;
		border-bottom: 1px solid var(--color-border);
		white-space: nowrap;
	}

	thead th {
		color: var(--color-text-muted);
		font-weight: 500;
	}

	tbody tr:last-child > * {
		border-bottom: none;
	}

	tbody th {
		font-weight: 400;

		a {
			color: var(--color-moana);
		}
	}

	.muted {
		color: var(--color-text-muted);
	}

	.visually-hidden {
		position: absolute;
		width: 1px;
		height: 1px;
		overflow: hidden;
		clip: rect(0 0 0 0);
		white-space: nowrap;
	}
</style>
