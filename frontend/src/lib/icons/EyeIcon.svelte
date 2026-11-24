<script lang="ts">
	/** An eye, struck through when `off` */
	let { size = '1em', off = false }: { size?: number | string; off?: boolean } = $props();
</script>

<svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
	stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
	<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z" />
	<circle cx="12" cy="12" r="3" />
	{#if off}<path d="M3 3l18 18" />{/if}
</svg>
