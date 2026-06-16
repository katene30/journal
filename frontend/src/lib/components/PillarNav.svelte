<script lang="ts">
	import type { PillarId, MauriState } from '$lib/types';
	import { PILLARS } from '$lib/config/pillars';

	interface Props {
		activePillar: PillarId;
		pillarStates: Record<PillarId, MauriState>;
	}

	let { activePillar = $bindable('reflection'), pillarStates = {
		reflection: 'untouched',
		hinengaro: 'untouched',
		tinana: 'untouched',
		whanau: 'untouched',
		wairua: 'untouched'
	} }: Props = $props();

	const mauriSymbols: Record<MauriState, string> = {
		untouched: '○',
		light: '◔',
		meaningful: '◕',
		deep: '●'
	};

	const handleSelect = (id: PillarId) => {
		activePillar = id;
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
					aria-label="{pillar.name} - {pillarStates[pillar.id]}"
					onclick={() => handleSelect(pillar.id)}
				>
					<span class="pillar-nav__icon">{pillar.icon}</span>
					<span class="pillar-nav__mauri" aria-hidden="true">
						{mauriSymbols[pillarStates[pillar.id]]}
					</span>
				</button>
			</li>
		{/each}
	</ul>
</nav>

<style lang="scss">
	@use '$lib/scss/mixins' as mx;

	.pillar-nav {
		position: sticky;
		top: 0;
		z-index: 10;
		background: var(--color-surface);
		border-bottom: 1px solid var(--color-border);
		padding: var(--space-sm) 0;

		&__list {
			display: flex;
			justify-content: center;
			gap: var(--space-sm);
			list-style: none;
			margin: 0;
			padding: 0;
		}

		&__item {
			margin: 0;
		}

		&__button {
			@include mx.touch-target;
			@include mx.focus-visible;

			display: flex;
			flex-direction: column;
			align-items: center;
			gap: 2px;
			padding: var(--space-xs);
			border: 2px solid transparent;
			border-radius: var(--radius-md);
			background: transparent;
			cursor: pointer;
			transition:
				border-color var(--transition-fast),
				background-color var(--transition-fast);

			&:hover {
				background: var(--color-bg);
			}

			&--active {
				border-color: var(--pillar-color);
				background: var(--color-bg);
			}
		}

		&__icon {
			font-size: 1.5rem;
			line-height: 1;
		}

		&__mauri {
			font-size: var(--font-size-xs);
			color: var(--color-text-muted);
		}
	}
</style>
