<script lang="ts">
	import type { SemanticScale } from '$lib/types';

	interface Props {
		scale: Omit<SemanticScale, 'value'>;
		value?: number | null;
		segments?: number;
		onchange?: (value: number) => void;
	}

	let { scale, value = null, segments = 7, onchange }: Props = $props();

	const handleChange = (newValue: number) => {
		onchange?.(newValue);
	};
</script>

<fieldset class="semantic-scale">
	<legend class="visually-hidden">{scale.leftLabel} to {scale.rightLabel}</legend>

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
</fieldset>

<style lang="scss">
	.semantic-scale {
		display: flex;
		align-items: center;
		gap: var(--space-sm);
		border: none;
		padding: 0;
		margin: 0;
	}

	.semantic-scale__label {
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

	.semantic-scale__options {
		display: flex;
		gap: var(--space-xs);
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
		width: 32px;
		height: 32px;
		border: 2px solid var(--color-border);
		border-radius: 50%;
		background: var(--color-surface);
		transition: all var(--transition-fast);

		&:hover {
			border-color: var(--pillar-color, var(--color-hinengaro));
			background: color-mix(in srgb, var(--pillar-color, var(--color-hinengaro)) 10%, white);
		}
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
