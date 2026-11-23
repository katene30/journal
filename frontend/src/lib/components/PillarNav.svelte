<script lang="ts">
	import type { PillarId } from '$lib/types';
	import type { MauriState } from '$lib/stores/entry';
	import { PILLARS } from '$lib/config/pillars';
	import KoruIcon from '$lib/icons/KoruIcon.svelte';
	import KoiriIcon from '$lib/icons/KoiriIcon.svelte';
	import KoruSpiralIcon from '$lib/icons/KoruSpiralIcon.svelte';
	import MangopareIcon from '$lib/icons/MangopareIcon.svelte';
	import NgutukukaIcon from '$lib/icons/NgutukukaIcon.svelte';
	import PoutamaIcon from '$lib/icons/PoutamaIcon.svelte';
	import PuhoroIcon from '$lib/icons/PuhoroIcon.svelte';

	interface Props {
		activePillar: PillarId;
		mauriStates?: Record<PillarId, MauriState>;
		onselect?: (id: PillarId) => void;
	}

	let { activePillar, mauriStates, onselect }: Props = $props();

	const ICON_SIZE = 42;

	const mauriSymbols: Record<MauriState, string> = {
		untouched: '○',
		light: '◔',
		meaningful: '◕',
		deep: '●'
	};
</script>

<nav class="pillar-nav" aria-label="Journal pillars">
	<ul class="pillar-nav__list">
		{#each PILLARS as pillar}
			{@const iconColor = pillar.color}
			<li class="pillar-nav__item">
				<button
					type="button"
					class="pillar-nav__button"
					class:pillar-nav__button--active={activePillar === pillar.id}
					style="--pillar-color: {pillar.color}; --pillar-tint: {pillar.tint}"
					aria-current={activePillar === pillar.id ? 'true' : undefined}
					aria-label="{pillar.name} - {mauriStates?.[pillar.id] ?? 'untouched'}"
					title={pillar.name}
					onclick={() => onselect?.(pillar.id)}
				>
					<span class="pillar-nav__icon">
						{#if pillar.id === 'hinengaro'}
							<KoruIcon size={ICON_SIZE} color={iconColor} />
						{:else if pillar.id === 'reflection'}
							<KoiriIcon size={ICON_SIZE} color={iconColor} />
						{:else if pillar.id === 'tinana'}
							<MangopareIcon size={ICON_SIZE} color={iconColor} />
						{:else if pillar.id === 'waiora'}
							<NgutukukaIcon size={ICON_SIZE} color={iconColor} />
						{:else if pillar.id === 'whanau'}
							<PoutamaIcon size={ICON_SIZE} color={iconColor} />
						{:else if pillar.id === 'wairua'}
							<KoruSpiralIcon size={ICON_SIZE} color={iconColor} />
						{:else if pillar.id === 'mauriora'}
							<PuhoroIcon size={ICON_SIZE} color={iconColor} />
						{:else}
							{pillar.icon}
						{/if}
					</span>
					<span class="pillar-nav__name">{pillar.name}</span>
					{#if mauriStates}
						<span class="pillar-nav__mauri" aria-hidden="true">
							{mauriSymbols[mauriStates[pillar.id] ?? 'untouched']}
						</span>
					{/if}
				</button>
			</li>
		{/each}
	</ul>
</nav>

<style lang="scss">
	.pillar-nav {
		padding: var(--space-sm) 0;
		overflow-x: auto;
		-webkit-overflow-scrolling: touch;
	}

	.pillar-nav__list {
		display: flex;
		gap: var(--space-xs);
		list-style: none;
		margin: 0;
		padding: 0;
		width: max-content;
		min-width: 100%;
		justify-content: center;

		@media (min-width: 768px) {
			width: auto;
		}
	}

	.pillar-nav__item {
		flex: 1 1 0;
		min-width: 70px;

		@media (min-width: 768px) {
			flex: 0 0 auto;
		}
	}

	.pillar-nav__button {
		position: relative;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 2px;
		padding: var(--space-sm);
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		overflow: hidden;
		cursor: pointer;
		transition: background-color var(--transition-fast), border-color var(--transition-fast);
		width: 100%;
		white-space: nowrap;

		@media (min-width: 768px) {
			width: 88px;
		}

		/* Selection marker: the same 3px accent underline on every tab */
		&::after {
			content: '';
			position: absolute;
			left: 0;
			right: 0;
			bottom: 0;
			height: 3px;
			background: var(--pillar-color);
			transform: scaleY(0);
			transform-origin: bottom;
			transition: transform var(--transition-fast);
		}
	}

	.pillar-nav__button:hover {
		background: var(--color-hover);
	}

	.pillar-nav__button:focus-visible {
		outline: 2px solid var(--color-focus);
		outline-offset: 2px;
	}

	.pillar-nav__button--active,
	.pillar-nav__button--active:hover {
		background: var(--pillar-tint);
		border-color: color-mix(in srgb, var(--pillar-color) 35%, var(--color-border));

		&::after {
			transform: scaleY(1);
		}
	}

	.pillar-nav__button--active .pillar-nav__name {
		color: var(--color-text);
		font-weight: 600;
	}

	.pillar-nav__icon {
		font-size: 1.25rem;
		line-height: 1;
		display: flex;
		align-items: center;
		justify-content: center;
		height: 2rem;

		:global(svg) {
			max-height: 100%;
			width: auto;
		}
	}

	.pillar-nav__name {
		font-size: var(--font-size-xs);
		color: var(--color-text);
	}

	.pillar-nav__mauri {
		font-size: var(--font-size-sm);
		color: var(--color-text-muted);
		line-height: 1;
	}
</style>
