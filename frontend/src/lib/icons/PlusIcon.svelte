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
	xmlns="http://www.w3.org/2000/svg"
	aria-hidden="true"
>
	<path d="M12 5v14M5 12h14" />
</svg>
