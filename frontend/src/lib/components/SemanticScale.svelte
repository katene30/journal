<script lang="ts">
	import type { SemanticScale } from '$lib/types';

	interface Props {
		scale: Omit<SemanticScale, 'value'>;
		value?: number | null;
		segments?: number;
		onchange?: (value: number) => void;
	}

	let { scale, value = null, segments = 5, onchange }: Props = $props();

	const handleChange = (newValue: number) => {
		onchange?.(newValue);
	};
</script>

<fieldset class="semantic-scale">
	<legend class="semantic-scale__title">{scale.title}</legend>

	<div class="semantic-scale__row">
		<span class="semantic-scale__label semantic-scale__label--left">{scale.leftLabel}</span>

		<div class="semantic-scale__options">
			{#each Array(segments) as _, i}
				{@const optionValue = i + 1}
				<label class="semantic-scale__option">
					<input
						type="radio"
						name={scale.id}
						value={optionValue}
						checked={value === optionValue}
						onchange={() => handleChange(optionValue)}
					/>
					<span class="semantic-scale__radio"></span>
					<span class="visually-hidden">{optionValue}</span>
				</label>
			{/each}
		</div>

		<span class="semantic-scale__label semantic-scale__label--right">{scale.rightLabel}</span>
	</div>

	{#if scale.helpText}
		<p class="semantic-scale__help">{scale.helpText}</p>
	{/if}
</fieldset>

<style lang="scss">
	.semantic-scale {
		border: none;
		padding: 0;
		margin: 0 0 var(--space-md) 0;
	}

	.semantic-scale__title {
		font-size: var(--font-size-base);
		font-weight: 500;
		color: var(--color-text);
		margin-bottom: var(--space-xs);
	}

	.semantic-scale__row {
		display: flex;
		align-items: center;
		gap: var(--space-xs);

		@media (min-width: 500px) {
			gap: var(--space-sm);
		}
	}

	.semantic-scale__label {
		font-size: var(--font-size-xs);
		color: var(--color-text-muted);
		flex: 0 1 60px;
		min-width: 0;

		@media (min-width: 500px) {
			font-size: var(--font-size-sm);
			flex: 0 0 80px;
		}

		&--left {
			text-align: right;
		}

		&--right {
			text-align: left;
		}
	}

	.semantic-scale__options {
		display: flex;
		gap: 4px;
		flex: 1;
		justify-content: center;

		@media (min-width: 500px) {
			gap: var(--space-xs);
		}
	}

	.semantic-scale__option {
		position: relative;
		cursor: pointer;

		input {
			position: absolute;
			opacity: 0;
			width: 0;
			height: 0;

			&:checked + .semantic-scale__radio {
				background: var(--pillar-color, var(--color-hinengaro));
				border-color: var(--pillar-color, var(--color-hinengaro));
			}

			&:focus-visible + .semantic-scale__radio {
				outline: 2px solid var(--color-focus);
				outline-offset: 2px;
			}
		}
	}

	.semantic-scale__radio {
		display: block;
		width: 24px;
		height: 24px;
		border: 2px solid var(--color-border);
		border-radius: 50%;
		background: var(--color-surface);
		transition: all var(--transition-fast);

		@media (min-width: 500px) {
			width: 28px;
			height: 28px;
		}

		&:hover {
			border-color: var(--pillar-color, var(--color-hinengaro));
			background: color-mix(in srgb, var(--pillar-color, var(--color-hinengaro)) 10%, white);
		}
	}

	.semantic-scale__help {
		font-size: var(--font-size-xs);
		color: var(--color-text-muted);
		margin: var(--space-xs) 0 0;
		font-style: italic;
	}

	.visually-hidden {
		position: absolute;
		width: 1px;
		height: 1px;
		padding: 0;
		margin: -1px;
		overflow: hidden;
		clip: rect(0, 0, 0, 0);
		white-space: nowrap;
		border: 0;
	}
</style>
