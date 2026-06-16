<script lang="ts">
	import PillarNav from '$lib/components/PillarNav.svelte';
	import SemanticScale from '$lib/components/SemanticScale.svelte';
	import { PILLARS } from '$lib/config/pillars';
	import { activePillar, pillarMauriStates, currentEntry, entryActions } from '$lib/stores/entry';
	import type { PillarId } from '$lib/types';

	// Format date nicely
	const formatDate = (date: Date) => {
		return date.toLocaleDateString('en-NZ', {
			weekday: 'long',
			day: 'numeric',
			month: 'long'
		});
	};

	// Get current pillar config - use $derived for reactive values in Svelte 5
	let currentPillarConfig = $derived(PILLARS.find((p) => p.id === $activePillar));

	// Scale values for current pillar
	let scaleValues: Record<string, number | null> = $state({});
</script>

<div class="container">
	<!-- Date Header -->
	<header class="entry-header">
		<h1 class="entry-date">{formatDate($currentEntry.date)}</h1>
	</header>

	<!-- Pillar Navigation -->
	<PillarNav bind:activePillar={$activePillar} pillarStates={$pillarMauriStates} />

	<!-- Pillar Content -->
	{#if currentPillarConfig}
		<section class="pillar-content" style="--pillar-color: {currentPillarConfig.color}">
			<!-- Bilingual Question -->
			<div class="pillar-question">
				<p class="pillar-question__maori">{currentPillarConfig.question.maori}</p>
				<p class="pillar-question__english">{currentPillarConfig.question.english}</p>
			</div>

			<!-- Scales -->
			<div class="pillar-scales">
				{#each currentPillarConfig.scales as scale (scale.id)}
					<SemanticScale {scale} bind:value={scaleValues[scale.id]} />
				{/each}
			</div>

			<!-- Reflection (on reflection pillar) -->
			{#if $activePillar === 'reflection'}
				<div class="journal-input">
					<label for="journal-text" class="visually-hidden">Journal entry</label>
					<textarea
						id="journal-text"
						class="journal-textarea"
						placeholder="What's on your mind today?"
						bind:value={$currentEntry.journalText}
						rows="6"
					></textarea>
				</div>
			{/if}

			<!-- Pillar reflection prompt -->
			{#if $activePillar !== 'reflection'}
				<div class="pillar-reflection">
					<label for="pillar-reflection" class="pillar-reflection__label">
						What stood out most in this space today?
					</label>
					<textarea
						id="pillar-reflection"
						class="pillar-reflection__input"
						placeholder="Optional reflection..."
						rows="3"
					></textarea>
				</div>
			{/if}
		</section>
	{/if}

	<!-- Actions -->
	<footer class="entry-actions">
		<button type="button" class="btn btn--secondary" onclick={() => entryActions.reset()}>
			Clear
		</button>
		<button type="button" class="btn btn--primary">
			{$activePillar === 'reflection' ? 'Save & Exit' : 'Save Entry'}
		</button>
	</footer>
</div>

<style lang="scss">
	@use '$lib/scss/mixins' as mx;

	.entry-header {
		text-align: center;
		padding: var(--space-lg) 0;
	}

	.entry-date {
		font-size: var(--font-size-xl);
		font-weight: 400;
		margin: 0;
	}

	.pillar-content {
		padding: var(--space-lg) 0;
		@include mx.flex-column(var(--space-lg));
	}

	.pillar-question {
		text-align: center;
		margin-bottom: var(--space-md);

		&__maori {
			font-size: var(--font-size-lg);
			font-style: italic;
			color: var(--pillar-color);
			margin-bottom: var(--space-xs);
		}

		&__english {
			font-size: var(--font-size-base);
			color: var(--color-text-muted);
			margin: 0;
		}
	}

	.pillar-scales {
		@include mx.flex-column(var(--space-md));
	}

	.journal-input,
	.pillar-reflection {
		margin-top: var(--space-md);
	}

	.journal-textarea,
	.pillar-reflection__input {
		width: 100%;
		padding: var(--space-sm);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		font-family: var(--font-family);
		font-size: var(--font-size-base);
		line-height: var(--line-height-base);
		resize: vertical;

		&:focus {
			outline: none;
			border-color: var(--color-focus);
			box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2);
		}

		&::placeholder {
			color: var(--color-text-muted);
		}
	}

	.pillar-reflection__label {
		display: block;
		margin-bottom: var(--space-xs);
		font-size: var(--font-size-sm);
		color: var(--color-text-muted);
	}

	.entry-actions {
		display: flex;
		justify-content: center;
		gap: var(--space-sm);
		padding: var(--space-lg) 0;
		border-top: 1px solid var(--color-border);
		margin-top: var(--space-lg);
	}

	.btn {
		@include mx.button-base;

		&--primary {
			background: var(--color-hinengaro);
			color: white;

			&:hover {
				background: darken(#2196f3, 10%);
			}
		}

		&--secondary {
			background: var(--color-bg);
			color: var(--color-text);
			border: 1px solid var(--color-border);

			&:hover {
				background: var(--color-border);
			}
		}
	}
</style>
