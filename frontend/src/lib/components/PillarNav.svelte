<script lang="ts">
	import type { PillarId } from '$lib/types';
	import type { MauriState } from '$lib/stores/entry';
	import { PILLARS } from '$lib/config/pillars';

	interface Props {
		activePillar: PillarId;
		mauriStates?: Record<PillarId, MauriState>;
		onselect?: (id: PillarId) => void;
	}

	let { activePillar, mauriStates, onselect }: Props = $props();

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
			<li class="pillar-nav__item">
				<button
					type="button"
					class="pillar-nav__button"
					class:pillar-nav__button--active={activePillar === pillar.id}
					style="--pillar-color: {pillar.color}"
					aria-current={activePillar === pillar.id ? 'true' : undefined}
					aria-label="{pillar.name} - {mauriStates?.[pillar.id] ?? 'untouched'}"
					title={pillar.name}
					onclick={() => onselect?.(pillar.id)}
				>
					<span class="pillar-nav__icon">{pillar.icon}</span>
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
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: var(--space-xs);
		list-style: none;
		margin: 0;
		padding: 0;

		@media (min-width: 768px) {
			display: flex;
			justify-content: center;
		}
	}

	.pillar-nav__item {
		display: flex;
	}

	.pillar-nav__button {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 2px;
		padding: var(--space-sm);
		background: var(--color-surface);
		border: 2px solid transparent;
		border-radius: var(--radius-md);
		cursor: pointer;
		transition: all var(--transition-fast);
		flex: 1;
		min-width: 0;

		@media (min-width: 768px) {
			flex: 0 0 auto;
			width: 88px;
		}
	}

	.pillar-nav__button:hover {
		border-color: var(--pillar-color);
	}

	.pillar-nav__button:focus-visible {
		outline: 2px solid var(--color-focus);
		outline-offset: 2px;
	}

	.pillar-nav__button--active {
		background: var(--pillar-color);
		border-color: var(--pillar-color);
	}

	.pillar-nav__button--active .pillar-nav__icon,
	.pillar-nav__button--active .pillar-nav__name,
	.pillar-nav__button--active .pillar-nav__mauri {
		color: white;
	}

	.pillar-nav__icon {
		font-size: 1.25rem;
		line-height: 1;
	}

	.pillar-nav__name {
		font-size: var(--font-size-xs);
		color: var(--color-text-muted);
	}

	.pillar-nav__mauri {
		font-size: var(--font-size-sm);
		color: var(--color-text-muted);
		line-height: 1;
	}
</style>
