<script lang="ts">
	import { describeScaleValue } from '$lib/config/pillars';
	import { daysBetween, formatLongDate, formatShortDate, addDays } from '$lib/utils/dates';

	interface Point {
		date: string;
		value: number | null;
	}

	interface Props {
		title: string;
		leftLabel: string;
		rightLabel: string;
		color: string;
		/** First and last day of the range, YYYY-MM-DD */
		start: string;
		end: string;
		/** One per logged day, oldest first; null = day logged but this scale left blank */
		points: Point[];
	}

	let { title, leftLabel, rightLabel, color, start, end, points }: Props = $props();

	// Geometry: the height includes the x-axis band so nothing is clipped
	const MIN = 1;
	const MAX = 5;
	const M = { top: 12, right: 32, bottom: 28, left: 28 };
	const PLOT_H = 140;
	const HEIGHT = M.top + PLOT_H + M.bottom;
	const DOTS_UP_TO = 31; // past this many points, per-day dots crowd the line

	let width = $state(320);
	let activeIndex = $state<number | null>(null);

	const plotW = $derived(Math.max(width - M.left - M.right, 40));
	const dayCount = $derived(daysBetween(start, end) + 1);

	const plotted = $derived(
		points
			.filter((p): p is { date: string; value: number } => p.value !== null)
			.map((p) => ({ ...p, day: daysBetween(start, p.date) }))
	);

	const x = (day: number) =>
		M.left + (dayCount <= 1 ? plotW / 2 : (day / (dayCount - 1)) * plotW);
	const y = (value: number) => M.top + ((MAX - value) / (MAX - MIN)) * PLOT_H;

	const linePath = $derived(
		plotted.map((p, i) => `${i === 0 ? 'M' : 'L'}${x(p.day)},${y(p.value)}`).join(' ')
	);

	const xTicks = $derived.by(() => {
		const count = Math.min(dayCount, width < 480 ? 4 : 6);
		if (count <= 1) return [0];
		return Array.from({ length: count }, (_, i) => Math.round((i * (dayCount - 1)) / (count - 1)));
	});

	const active = $derived(activeIndex === null ? null : plotted[activeIndex]);
	const last = $derived(plotted.at(-1));

	function nearestIndex(clientX: number, rect: DOMRect): number {
		const day = ((clientX - rect.left - M.left) / plotW) * (dayCount - 1);
		let best = 0;
		for (let i = 1; i < plotted.length; i++) {
			if (Math.abs(plotted[i].day - day) < Math.abs(plotted[best].day - day)) best = i;
		}
		return best;
	}

	function onpointermove(e: PointerEvent) {
		if (!plotted.length) return;
		activeIndex = nearestIndex(e.clientX, (e.currentTarget as SVGElement).getBoundingClientRect());
	}

	function onkeydown(e: KeyboardEvent) {
		if (!plotted.length) return;
		const lastIdx = plotted.length - 1;
		const moves: Record<string, number> = {
			ArrowRight: Math.min((activeIndex ?? -1) + 1, lastIdx),
			ArrowLeft: Math.max((activeIndex ?? lastIdx + 1) - 1, 0),
			Home: 0,
			End: lastIdx
		};
		if (e.key in moves) {
			e.preventDefault();
			activeIndex = moves[e.key];
		} else if (e.key === 'Escape') {
			activeIndex = null;
		}
	}

	const describe = (value: number) => describeScaleValue(value, { leftLabel, rightLabel });

	// Keep the tooltip inside the chart horizontally
	const tooltipLeft = $derived(active ? Math.min(Math.max(x(active.day), 70), width - 70) : 0);

	// What a screen reader announces as the user arrows through the days
	const valueText = $derived.by(() => {
		const p = active ?? last;
		return p ? `${formatLongDate(p.date)}: ${p.value}, ${describe(p.value)}` : '';
	});

	const summary = $derived(
		plotted.length
			? `${title} from ${formatLongDate(start)} to ${formatLongDate(end)}, ${plotted.length} ratings. ` +
					`1 is ${leftLabel}, 5 is ${rightLabel}.`
			: ''
	);
</script>

<figure class="trend-chart">
	<figcaption class="trend-chart__header">
		<span class="trend-chart__title">{title}</span>
		<span class="trend-chart__scale">1 {leftLabel} · 5 {rightLabel}</span>
	</figcaption>

	{#if plotted.length === 0}
		<p class="trend-chart__empty">No {title.toLowerCase()} ratings in this range.</p>
	{:else}
		<div class="trend-chart__plot" bind:clientWidth={width}>
			<svg
				width={width}
				height={HEIGHT}
				role="slider"
				tabindex="0"
				aria-label={summary}
				aria-valuemin={1}
				aria-valuemax={plotted.length}
				aria-valuenow={(activeIndex ?? plotted.length - 1) + 1}
				aria-valuetext={valueText}
				{onpointermove}
				onpointerdown={onpointermove}
				onpointerleave={(e) => {
					// Touch fires pointerleave as the finger lifts; keep the tapped day showing until blur
					if (e.pointerType !== 'touch') activeIndex = null;
				}}
				{onkeydown}
				onblur={() => (activeIndex = null)}
			>
				<!-- Horizontal gridlines + y ticks -->
				{#each [1, 2, 3, 4, 5] as v}
					<line class="grid" x1={M.left} x2={M.left + plotW} y1={y(v)} y2={y(v)} />
					<text class="tick tick--y" x={M.left - 10} y={y(v)} dy="0.35em">{v}</text>
				{/each}

				<!-- X ticks -->
				{#each xTicks as day}
					<text class="tick tick--x" x={x(day)} y={HEIGHT - 8}>{formatShortDate(addDays(start, day))}</text>
				{/each}

				<!-- Crosshair -->
				{#if active}
					<line class="crosshair" x1={x(active.day)} x2={x(active.day)} y1={M.top} y2={M.top + PLOT_H} />
				{/if}

				<path class="line" d={linePath} stroke={color} />

				{#each plotted as p, i}
					{#if plotted.length <= DOTS_UP_TO || i === plotted.length - 1 || i === activeIndex}
						<circle
							class="dot"
							cx={x(p.day)}
							cy={y(p.value)}
							r={i === activeIndex ? 6 : 4}
							fill={color}
						/>
					{/if}
				{/each}

				<!-- End label: the latest value -->
				{#if last}
					<text class="end-label" x={x(last.day) + 10} y={y(last.value)} dy="0.35em">{last.value}</text>
				{/if}
			</svg>

			{#if active}
				<div class="trend-chart__tooltip" style="left: {tooltipLeft}px" aria-hidden="true">
					<span class="trend-chart__tooltip-value">
						<span class="trend-chart__key" style="background: {color}"></span>
						<strong>{active.value}</strong>
						{describe(active.value)}
					</span>
					<span class="trend-chart__tooltip-date">{formatLongDate(active.date)}</span>
				</div>
			{/if}
		</div>

	{/if}
</figure>

<style lang="scss">
	.trend-chart {
		margin: 0;
		padding: var(--space-sm);
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		min-width: 0;
	}

	.trend-chart__header {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		justify-content: space-between;
		gap: var(--space-xxs) var(--space-sm);
		margin-bottom: var(--space-xs);
	}

	.trend-chart__title {
		font-weight: 600;
		color: var(--color-text);
	}

	.trend-chart__scale {
		font-size: var(--font-size-xs);
		color: var(--color-text-muted);
	}

	.trend-chart__empty {
		margin: 0;
		padding: var(--space-md) 0;
		font-size: var(--font-size-sm);
		color: var(--color-text-muted);
	}

	.trend-chart__plot {
		position: relative;
	}

	svg {
		display: block;
		overflow: visible;
		touch-action: pan-y;
		border-radius: var(--radius-sm);

		&:focus-visible {
			outline: 2px solid var(--color-focus);
			outline-offset: 4px;
		}
	}

	.grid {
		stroke: var(--color-border);
		stroke-width: 1;
	}

	.tick {
		font-size: 11px;
		fill: var(--color-text-muted);
		font-variant-numeric: tabular-nums;
	}

	.tick--y {
		text-anchor: end;
	}

	.tick--x {
		text-anchor: middle;
	}

	.crosshair {
		stroke: var(--color-text-muted);
		stroke-width: 1;
	}

	.line {
		fill: none;
		stroke-width: 2;
		stroke-linejoin: round;
		stroke-linecap: round;
	}

	.dot {
		stroke: var(--color-surface);
		stroke-width: 2;
		pointer-events: none;
	}

	.end-label {
		font-size: var(--font-size-xs);
		font-weight: 600;
		fill: var(--color-text);
	}

	.trend-chart__tooltip {
		position: absolute;
		top: -8px;
		transform: translate(-50%, -100%);
		display: flex;
		flex-direction: column;
		gap: 2px;
		padding: var(--space-xs) var(--space-sm);
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-sm);
		box-shadow: var(--shadow-md);
		font-size: var(--font-size-sm);
		white-space: nowrap;
		pointer-events: none;
		z-index: 2;
	}

	.trend-chart__tooltip-value {
		display: flex;
		align-items: center;
		gap: var(--space-xs);
		color: var(--color-text-muted);

		strong {
			color: var(--color-text);
			font-size: var(--font-size-base);
		}
	}

	.trend-chart__key {
		width: 12px;
		height: 2px;
		border-radius: 1px;
	}

	.trend-chart__tooltip-date {
		font-size: var(--font-size-xs);
		color: var(--color-text-muted);
	}
</style>
