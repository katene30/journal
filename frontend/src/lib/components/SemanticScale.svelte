<script lang="ts">
	import type { SemanticScale } from '$lib/types';

	interface Props {
		scale: Omit<SemanticScale, 'value'>;
		value?: number | null;
		segments?: number;
		onchange?: (value: number) => void;
	}

	let { scale, value = null, segments = 7, onchange }: Props = $props();

	const handleSelect = (index: number) => {
		const newValue = index + 1;
		onchange?.(newValue);
	};

	const handleKeydown = (e: KeyboardEvent, index: number) => {
		if (e.key === 'Enter' || e.key === ' ') {
			e.preventDefault();
			handleSelect(index);
		} else if (e.key === 'ArrowRight' && value !== null && value < segments) {
			onchange?.(value + 1);
		} else if (e.key === 'ArrowLeft' && value !== null && value > 1) {
			onchange?.(value - 1);
		}
	};
</script>

<fieldset class="semantic-scale" role="radiogroup" aria-label="Rate from {scale.leftLabel} to {scale.rightLabel}">
	<legend class="visually-hidden">{scale.leftLabel} to {scale.rightLabel}</legend>

	<span class="semantic-scale__label semantic-scale__label--left">{scale.leftLabel}</span>

	<div class="semantic-scale__segments">
		{#each Array(segments) as _, i}
			<button
				type="button"
				class="semantic-scale__segment"
				class:semantic-scale__segment--selected={value === i + 1}
				class:semantic-scale__segment--filled={value !== null && i + 1 <= value}
				role="radio"
				aria-checked={value === i + 1}
				aria-label="Level {i + 1} of {segments}"
				tabindex={value === i + 1 || (value === null && i === 0) ? 0 : -1}
				onclick={() => handleSelect(i)}
				onkeydown={(e) => handleKeydown(e, i)}
			>
				<span class="visually-hidden">{i + 1}</span>
			</button>
		{/each}
	</div>

	<span class="semantic-scale__label semantic-scale__label--right">{scale.rightLabel}</span>
</fieldset>

<style lang="scss">
	@use '$lib/scss/mixins' as mx;

	.semantic-scale {
		display: flex;
		align-items: center;
		gap: var(--space-sm);
		border: none;
		padding: 0;
		margin: 0;

		&__label {
			font-size: var(--font-size-sm);
			color: var(--color-text-muted);
			min-width: 80px;

			&--left {
				text-align: right;
			}

			&--right {
				text-align: left;
			}
		}

		&__segments {
			display: flex;
			gap: 4px;
			flex: 1;
			justify-content: center;
		}

		&__segment {
			@include mx.touch-target;
			@include mx.focus-visible;

			width: 100%;
			max-width: 48px;
			height: var(--scale-height);
			border: 2px solid var(--color-border);
			border-radius: var(--radius-sm);
			background: var(--color-surface);
			cursor: pointer;
			transition:
				background-color var(--transition-fast),
				border-color var(--transition-fast),
				transform var(--transition-fast);

			&:hover {
				border-color: var(--color-focus);
			}

			&--filled {
				background: var(--color-focus);
				border-color: var(--color-focus);
				opacity: 0.3;
			}

			&--selected {
				background: var(--color-focus);
				border-color: var(--color-focus);
				opacity: 1;
				transform: scale(1.1);
			}
		}
	}

	.visually-hidden {
		@include mx.visually-hidden;
	}
</style>
