<script lang="ts">
	import { SCALE_MAX, SCALE_MIN } from '$lib/utils/hauora';
	import { daysBetween } from '$lib/utils/dates';

	interface Props {
		color: string;
		/** First and last day of the range, YYYY-MM-DD */
		start: string;
		end: string;
		/** Oldest first; null values are skipped */
		points: { date: string; value: number | null }[];
	}

	let { color, start, end, points }: Props = $props();

	// A glance, not a reading: no axes. The y-range is always 1-5 so cards compare fairly.
	const HEIGHT = 48;
	const PAD = 4; // room for the end dot

	let width = $state(160);

	const dayCount = $derived(daysBetween(start, end) + 1);
	const plotted = $derived(
		points
			.filter((p): p is { date: string; value: number } => p.value !== null)
			.map((p) => ({ day: daysBetween(start, p.date), value: p.value }))
	);

	const x = (day: number) =>
		PAD + (dayCount <= 1 ? (width - 2 * PAD) / 2 : (day / (dayCount - 1)) * (width - 2 * PAD));
	const y = (value: number) =>
		PAD + ((SCALE_MAX - value) / (SCALE_MAX - SCALE_MIN)) * (HEIGHT - 2 * PAD);

	const path = $derived(plotted.map((p, i) => `${i ? 'L' : 'M'}${x(p.day)},${y(p.value)}`).join(' '));
	const last = $derived(plotted.at(-1));
</script>

<div class="sparkline" bind:clientWidth={width} aria-hidden="true">
	<svg {width} height={HEIGHT}>
		<line class="mid" x1={PAD} x2={width - PAD} y1={y(3)} y2={y(3)} />
		{#if plotted.length > 1}
			<path d={path} stroke={color} />
		{/if}
		{#if last}
			<circle cx={x(last.day)} cy={y(last.value)} r="3" fill={color} />
		{/if}
	</svg>
</div>

<style>
	.sparkline {
		width: 100%;
		min-width: 0;
	}

	svg {
		display: block;
		overflow: visible;
	}

	.mid {
		stroke: var(--color-border);
		stroke-width: 1;
		stroke-dasharray: 2 3;
	}

	path {
		fill: none;
		stroke-width: 2;
		stroke-linejoin: round;
		stroke-linecap: round;
	}

	circle {
		stroke: var(--color-surface);
		stroke-width: 1.5;
	}
</style>
