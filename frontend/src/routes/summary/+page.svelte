<script lang="ts">
	import { entriesApi, type EntryRange, type ScaleField } from '$lib/api/entries';
	import { PILLARS, getPillarById, describeScaleValue } from '$lib/config/pillars';
	import PillarNav from '$lib/components/PillarNav.svelte';
	import Sparkline from '$lib/components/Sparkline.svelte';
	import TrendChart from '$lib/components/TrendChart.svelte';
	import ArrowRightIcon from '$lib/icons/ArrowRightIcon.svelte';
	import type { PillarConfig, PillarId } from '$lib/types';
	import { SCALE_MAX, formatScore, pillarScore } from '$lib/utils/hauora';
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

	// Pillar scores: the same per-day calculation as the entry page
	const OVERVIEW_PILLARS = PILLARS.filter((p) => p.id !== 'reflection');
	const SCORE_LABELS = { leftLabel: 'Low', rightLabel: 'High' };

	const scoreSeries = (p: PillarConfig) =>
		entries.map((e) => ({ date: e.date, value: pillarScore(p, e).score }));

	const pillarSummaries = $derived(
		OVERVIEW_PILLARS.map((p) => {
			const series = scoreSeries(p);
			const values = series.map((d) => d.value).filter((v): v is number => v !== null);
			return {
				pillar: p,
				series,
				days: values.length,
				average: values.length ? values.reduce((a, b) => a + b, 0) / values.length : null
			};
		})
	);

	// A combined score only adds anything when a pillar has more than one scale
	const showScore = $derived(pillar.id !== 'reflection' && pillar.scales.length > 1);
	const hasReversed = $derived(pillar.scales.some((s) => s.reversed));

	let pillarHeading = $state<HTMLElement>();

	function openPillar(id: PillarId) {
		pillarId = id;
		const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
		pillarHeading?.focus({ preventScroll: true });
		pillarHeading?.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
	}
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

				<section class="glance" aria-labelledby="glance-heading">
					<h2 id="glance-heading" class="section-heading">Pillars at a glance</h2>
					<p class="section-intro">Each pillar's average score on the days you rated it. Select one to see its charts.</p>

					<ul class="glance__grid">
						{#each pillarSummaries as item (item.pillar.id)}
							{@const ink = item.pillar.chartColor ?? item.pillar.color}
							<li>
								<button
									type="button"
									class="glance-card"
									class:glance-card--active={pillarId === item.pillar.id}
									style="--pillar-color: {item.pillar.color}; --pillar-ink: {ink}"
									aria-label={item.average === null
										? `${item.pillar.name}: not rated in this range. Show charts.`
										: `${item.pillar.name}: average ${formatScore(Number(item.average.toFixed(1)))} out of ${SCALE_MAX} over ${item.days} days. Show charts.`}
									onclick={() => openPillar(item.pillar.id)}
								>
									<span class="glance-card__top">
										<span class="glance-card__heading">
											<span class="glance-card__name">{item.pillar.name}</span>
											<span class="glance-card__theme">{item.pillar.theme}</span>
										</span>
										{#if item.average !== null}
											<span class="glance-card__value">
												{item.average.toFixed(1)}<span class="glance-card__out-of">/ {SCALE_MAX}</span>
											</span>
										{/if}
									</span>
									{#if item.average !== null}
										<Sparkline color={ink} start={data.start} end={data.end} points={item.series} />
										<span class="glance-card__days">{item.days} {item.days === 1 ? 'day' : 'days'} rated</span>
									{:else}
										<span class="glance-card__days">Not rated in this range</span>
									{/if}
								</button>
							</li>
						{/each}
					</ul>

					<p class="glance__note">
						A pillar's score is the average of its ratings that day, with anxiety and stress reversed so
						higher always means more settled. It's a personal snapshot, not a measure of your hauora.
					</p>
				</section>

				<section class="pillar-section" aria-labelledby="pillar-heading">
					<PillarNav activePillar={pillarId} onselect={(id) => (pillarId = id)} />

					<h2 id="pillar-heading" class="pillar-heading" tabindex="-1" bind:this={pillarHeading}>
						{pillar.name}
						<span class="pillar-heading__en">{pillar.question.english}</span>
					</h2>

					{#if showScore}
						<div class="score-chart">
							<TrendChart
								title="{pillar.name} score"
								leftLabel={SCORE_LABELS.leftLabel}
								rightLabel={SCORE_LABELS.rightLabel}
								color={pillar.chartColor ?? pillar.color}
								start={data.start}
								end={data.end}
								points={scoreSeries(pillar)}
							/>
							<p class="score-chart__note">
								The average of the {pillar.scales.length} ratings below{hasReversed
									? ', with anxiety and stress reversed'
									: ''}.
							</p>
						</div>
					{/if}

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
										{#if showScore}
											<th scope="col">{pillar.name} score</th>
										{/if}
										{#each pillar.scales as scale}
											<th scope="col">{scale.title}</th>
										{/each}
									</tr>
								</thead>
								<tbody>
									{#each [...entries].reverse() as entry (entry.id)}
										<tr>
											<th scope="row"><a href="/app/entries/{entry.id}">{formatLongDate(entry.date)}</a></th>
											{#if showScore}
												{@const score = pillarScore(pillar, entry).score}
												<td>
													{#if score === null}
														<span class="muted">–</span>
													{:else}
														<strong>{formatScore(Number(score.toFixed(1)))}</strong>
													{/if}
												</td>
											{/if}
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
		background: var(--color-primary);
		color: var(--color-on-primary);
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

	/* Pillars at a glance */
	.section-heading {
		margin: 0 0 var(--space-xxs);
		font-size: var(--font-size-lg);
		color: var(--color-text);
	}

	.section-intro {
		margin: 0 0 var(--space-sm);
		font-size: var(--font-size-sm);
		color: var(--color-text-muted);
	}

	.glance {
		margin-bottom: var(--space-lg);
	}

	.glance__grid {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: var(--space-xs);
		margin: 0;
		padding: 0;
		list-style: none;

		@media (min-width: 700px) {
			grid-template-columns: repeat(3, minmax(0, 1fr));
			gap: var(--space-sm);
		}
	}

	.glance-card {
		display: flex;
		flex-direction: column;
		gap: var(--space-xs);
		width: 100%;
		height: 100%;
		padding: var(--space-sm);
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-left: 4px solid var(--pillar-color);
		border-radius: var(--radius-md);
		color: var(--color-text);
		font: inherit;
		text-align: left;
		cursor: pointer;
		transition: border-color var(--transition-fast), background-color var(--transition-fast);

		&:hover {
			border-color: var(--pillar-ink);
			border-left-color: var(--pillar-color);
		}

		&:focus-visible {
			outline: 2px solid var(--color-focus);
			outline-offset: 2px;
		}
	}

	.glance-card--active {
		background: color-mix(in srgb, var(--pillar-color) 8%, var(--color-surface));
		border-color: var(--pillar-ink);
		border-left-color: var(--pillar-color);
	}

	.glance-card__top {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		gap: var(--space-xs);
	}

	.glance-card__heading {
		display: flex;
		flex-direction: column;
		min-width: 0;
	}

	.glance-card__name {
		font-weight: 600;
		color: var(--pillar-ink);
	}

	.glance-card__theme {
		font-size: var(--font-size-xs);
		color: var(--color-text-muted);
	}

	.glance-card__value {
		font-size: var(--font-size-lg);
		font-weight: 600;
		font-variant-numeric: tabular-nums;
		white-space: nowrap;

		@media (min-width: 500px) {
			font-size: var(--font-size-xl);
		}
	}

	.glance-card__out-of {
		margin-left: 2px;
		font-size: var(--font-size-xs);
		font-weight: 400;
		color: var(--color-text-muted);
	}

	.glance-card__days {
		margin-top: auto;
		font-size: var(--font-size-xs);
		color: var(--color-text-muted);
	}

	.glance__note {
		margin: var(--space-sm) 0 0;
		font-size: var(--font-size-xs);
		color: var(--color-text-muted);
	}

	.score-chart {
		margin-bottom: var(--space-sm);
	}

	.score-chart__note {
		margin: var(--space-xxs) 0 0;
		font-size: var(--font-size-xs);
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
		scroll-margin-top: var(--space-md);

		&:focus {
			outline: none;
		}
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
			color: var(--color-link);
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
			color: var(--color-link);
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
