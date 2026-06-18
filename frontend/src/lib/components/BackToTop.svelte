<script lang="ts">
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';

	let visible = $state(false);
	const threshold = 300;

	function handleScroll() {
		visible = window.scrollY > threshold;
	}

	function scrollToTop() {
		window.scrollTo({ top: 0, behavior: 'smooth' });
	}

	onMount(() => {
		window.addEventListener('scroll', handleScroll, { passive: true });
		return () => window.removeEventListener('scroll', handleScroll);
	});
</script>

{#if visible}
	<button
		type="button"
		class="back-to-top"
		onclick={scrollToTop}
		aria-label="Back to top"
		transition:fade={{ duration: 200 }}
	>
		<svg
			width="20"
			height="20"
			viewBox="0 0 20 20"
			fill="none"
			stroke="currentColor"
			stroke-width="2"
			stroke-linecap="round"
			stroke-linejoin="round"
			aria-hidden="true"
		>
			<path d="M10 16V4M4 10l6-6 6 6" />
		</svg>
	</button>
{/if}

<style lang="scss">
	.back-to-top {
		position: fixed;
		bottom: var(--space-lg);
		right: var(--space-lg);
		z-index: 50;

		display: flex;
		align-items: center;
		justify-content: center;

		width: 44px;
		height: 44px;
		padding: 0;

		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 50%;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

		cursor: pointer;
		transition:
			border-color var(--transition-fast),
			box-shadow var(--transition-fast);

		&:hover {
			border-color: var(--color-hinengaro);
			box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
		}

		&:focus-visible {
			outline: 2px solid var(--color-hinengaro);
			outline-offset: 2px;
		}
	}
</style>
