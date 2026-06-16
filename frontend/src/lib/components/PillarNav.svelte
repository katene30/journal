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
		display: flex;
		justify-content: center;
		gap: var(--space-xs);
		list-style: none;
		margin: 0;
		padding: 0;
		min-width: min-content;
	}

	.pillar-nav__item {
		flex-shrink: 0;
	}

	.pillar-nav__button {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 2px;
		padding: var(--space-sm);
		background: var(--color-surface);
		border: 2px solid transparent;
		border-radius: var(--radius-md);
		cursor: pointer;
		transition: all var(--transition-fast);
		min-width: 56px;

		&:hover {
			background: var(--color-bg);
		}

		&:focus-visible {
			outline: 2px solid var(--color-focus);
			outline-offset: 2px;
		}

		&--active {
			border-color: var(--pillar-color);
			background: color-mix(in srgb, var(--pillar-color) 10%, white);
		}
	}

	.pillar-nav__icon {
		font-size: 1.25rem;
		line-height: 1;
	}

	.pillar-nav__name {
		font-size: var(--font-size-xs);
		color: var(--color-text-muted);
		white-space: nowrap;

		.pillar-nav__button--active & {
			color: var(--pillar-color);
			font-weight: 500;
		}
	}

	.pillar-nav__mauri {
		font-size: var(--font-size-sm);
		color: var(--color-text-muted);
		line-height: 1;

		.pillar-nav__button--active & {
			color: var(--pillar-color);
		}
	}
</style>
