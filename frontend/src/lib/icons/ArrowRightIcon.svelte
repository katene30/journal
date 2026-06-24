<script lang="ts">
	interface Props {
		size?: number | string;
		color?: string;
	}

	let { size = '1em', color = 'currentColor' }: Props = $props();
</script>

<svg
	width={size}
	height={size}
	viewBox="0 0 24 24"
	fill="none"
	stroke={color}
	stroke-width="2.5"
	stroke-linecap="round"
	stroke-linejoin="round"
	xmlns="http://www.w3.org/2000/svg"
	aria-hidden="true"
>
	<path d="M5 12h14M13 5l7 7-7 7" />
</svg>
