<script lang="ts">
	import { onMount } from 'svelte';
	import { fly } from 'svelte/transition';
	import { goto } from '$app/navigation';
	import BackToTop from '$lib/components/BackToTop.svelte';
	import PillarNav from '$lib/components/PillarNav.svelte';
	import SemanticScale from '$lib/components/SemanticScale.svelte';
	import { PILLARS } from '$lib/config/pillars';
	import {
		activePillar,
		currentEntry,
		entryActions,
		entryApiActions,
		pillarMauriStates,
		type EntryData
	} from '$lib/stores/entry';
	import { authActions, currentUser } from '$lib/stores/auth';

	async function handleLogout() {
		await authActions.logout();
		goto('/app/login');
	}

	// State
	let loading = $state(true);
	let saving = $state(false);
	let error = $state<string | null>(null);
	let showSavedToast = $state(false);
	let showClearedToast = $state(false);
	let showClearConfirm = $state(false);
	let entryLoaded = $state(false);
	let slideDirection = $state<'left' | 'right' | null>(null);
	let previousPillarIndex = $state(0);

	// Format date for display
	const formatDateDisplay = (dateStr: string) => {
		const date = new Date(dateStr + 'T00:00:00');
		return date.toLocaleDateString('en-NZ', {
			weekday: 'long',
			day: 'numeric',
			month: 'long'
		});
	};

	// Get current pillar config and index
	let currentPillarConfig = $derived(PILLARS.find((p) => p.id === $activePillar));
	let currentPillarIndex = $derived(PILLARS.findIndex((p) => p.id === $activePillar));

	// Handle pillar navigation with direction tracking
	function handlePillarSelect(id: string) {
		const newIndex = PILLARS.findIndex((p) => p.id === id);
		if (newIndex > currentPillarIndex) {
			slideDirection = 'right';
		} else if (newIndex < currentPillarIndex) {
			slideDirection = 'left';
		}
		previousPillarIndex = currentPillarIndex;
		entryActions.navigateToPillar(id);
		setTimeout(() => {
			slideDirection = null;
		}, 300);
	}

	// Prev/Next pillar navigation
	let isFirstPillar = $derived(currentPillarIndex === 0);
	let isLastPillar = $derived(currentPillarIndex === PILLARS.length - 1);

	function goToPrevPillar() {
		if (!isFirstPillar) {
			handlePillarSelect(PILLARS[currentPillarIndex - 1].id);
		}
	}

	function goToNextPillar() {
		if (!isLastPillar) {
			handlePillarSelect(PILLARS[currentPillarIndex + 1].id);
		}
	}

	// Load today's entry on mount
	onMount(async () => {
		try {
			await entryApiActions.loadToday();
		} catch (e: unknown) {
			console.error('Load error:', e);
			if (e && typeof e === 'object' && 'detail' in e) {
				error = String((e as { detail: string }).detail);
			} else if (e instanceof Error) {
				error = e.message;
			} else {
				error = 'Failed to load entry';
			}
		} finally {
			loading = false;
		}
	});

	// Save handler
	async function handleSave() {
		saving = true;
		error = null;
		try {
			await entryApiActions.saveEntry();
			showSavedToast = true;
			setTimeout(() => {
				showSavedToast = false;
			}, 3000);
		} catch (e: unknown) {
			console.error('Save error:', e);
			if (e && typeof e === 'object' && 'detail' in e) {
				error = String((e as { detail: string }).detail);
			} else if (e instanceof Error) {
				error = e.message;
			} else {
				error = 'Failed to save entry';
			}
		} finally {
			saving = false;
		}
	}

	// Type-safe field setter
	function setField<K extends keyof EntryData>(field: K, value: EntryData[K]) {
		entryActions.setField(field, value);
	}

	// Clear confirmation handlers
	function handleClearClick() {
		showClearConfirm = true;
	}

	function confirmClear() {
		entryActions.reset();
		showClearConfirm = false;
		showClearedToast = true;
		setTimeout(() => {
			showClearedToast = false;
		}, 3000);
	}

	function cancelClear() {
		showClearConfirm = false;
	}

	// Handle date change - load entry for that date
	async function handleDateChange(newDate: string) {
		loading = true;
		error = null;
		try {
			await entryApiActions.loadByDate(newDate);
			entryLoaded = true;
			setTimeout(() => {
				entryLoaded = false;
			}, 600);
		} catch (e: unknown) {
			console.error('Load error:', e);
			if (e && typeof e === 'object' && 'detail' in e) {
				error = String((e as { detail: string }).detail);
			} else if (e instanceof Error) {
				error = e.message;
			} else {
				error = 'Failed to load entry';
			}
		} finally {
			loading = false;
		}
	}
</script>

{#if loading}
	<div class="loading">Loading...</div>
{:else}
	<div class="container">
		{#if showSavedToast}
			<div class="toast toast--success" transition:fly={{ y: -20, duration: 300 }}>&#10003; Saved</div>
		{/if}

		{#if showClearedToast}
			<div class="toast toast--error" transition:fly={{ y: -20, duration: 300 }}>&#10005; Entry cleared</div>
		{/if}

		{#if error}
			<div class="error">{error}</div>
		{/if}

		<!-- User header -->
		<div class="user-header">
			<span class="user-email">{$currentUser?.email}</span>
			<button type="button" class="logout-btn" onclick={handleLogout}>Sign out</button>
		</div>

		<!-- Date Header with picker -->
		<header class="entry-header">
			<h1 class="entry-date">{formatDateDisplay($currentEntry.date)}</h1>
			<input
				type="date"
				class="date-picker"
				value={$currentEntry.date}
				onchange={(e) => handleDateChange(e.currentTarget.value)}
			/>
		</header>

		<!-- Pillar Navigation -->
		<PillarNav
			activePillar={$activePillar}
			mauriStates={$pillarMauriStates}
			onselect={handlePillarSelect}
		/>

		<!-- Pillar Content -->
		{#if currentPillarConfig}
			<section
				class="pillar-content"
				class:pillar-content--loaded={entryLoaded}
				class:pillar-content--slide-left={slideDirection === 'left'}
				class:pillar-content--slide-right={slideDirection === 'right'}
				style="--pillar-color: {currentPillarConfig.color}"
			>
				<!-- Bilingual Question -->
				<div class="pillar-question">
					<p class="pillar-question__maori">{currentPillarConfig.question.maori}</p>
					<p class="pillar-question__english">{currentPillarConfig.question.english}</p>
				</div>

				<!-- Scales -->
				<div class="pillar-scales">
					{#each currentPillarConfig.scales as scale (scale.id)}
						<SemanticScale
							{scale}
							value={$currentEntry[scale.id as keyof EntryData] as number | null}
							onchange={(v) => setField(scale.id as keyof EntryData, v)}
						/>
					{/each}
				</div>

				<!-- Extra fields (number/text inputs for Tinana) -->
				{#if currentPillarConfig.extraFields}
					<div class="extra-fields">
						{#each currentPillarConfig.extraFields as field (field.id)}
							<div class="field-group">
								<label for={field.id}>{field.label}</label>
								{#if field.type === 'number'}
									<input
										type="number"
										id={field.id}
										value={$currentEntry[field.id as keyof EntryData] ?? ''}
										placeholder={field.placeholder}
										onchange={(e) => setField(field.id as keyof EntryData, e.currentTarget.value ? Number(e.currentTarget.value) : null)}
									/>
								{:else}
									<input
										type="text"
										id={field.id}
										value={$currentEntry[field.id as keyof EntryData] ?? ''}
										placeholder={field.placeholder}
										onchange={(e) => setField(field.id as keyof EntryData, e.currentTarget.value)}
									/>
								{/if}
							</div>
						{/each}
					</div>
				{/if}

				<!-- Text fields (for Reflection pillar) -->
				{#if currentPillarConfig.textFields}
					<div class="text-fields">
						{#each currentPillarConfig.textFields as field (field.id)}
							<div class="field-group">
								<label for={field.id}>{field.label}</label>
								<textarea
									id={field.id}
									value={$currentEntry[field.id as keyof EntryData] ?? ''}
									placeholder={field.placeholder}
									rows={field.id === 'log' ? 6 : 2}
									onchange={(e) => setField(field.id as keyof EntryData, e.currentTarget.value)}
								></textarea>
							</div>
						{/each}
					</div>
				{/if}
			</section>
		{/if}

		<!-- Pillar Navigation -->
		<nav class="pillar-nav-buttons" aria-label="Pillar navigation">
			<button
				type="button"
				class="btn btn--secondary btn--nav"
				onclick={goToPrevPillar}
				disabled={isFirstPillar}
			>
				&#8592; Back
			</button>
			<button
				type="button"
				class="btn btn--secondary btn--nav"
				onclick={goToNextPillar}
				disabled={isLastPillar}
			>
				Next &#8594;
			</button>
		</nav>

		<!-- Actions -->
		<footer class="entry-actions">
			<button type="button" class="btn btn--secondary" onclick={handleClearClick}>
				Clear
			</button>
			<button type="button" class="btn btn--primary" onclick={handleSave} disabled={saving}>
				{saving ? 'Saving...' : 'Save'}
			</button>
		</footer>
	</div>

	<!-- Clear Confirmation Dialog -->
	{#if showClearConfirm}
		<div class="dialog-backdrop" onclick={cancelClear} role="presentation">
			<div
				class="dialog"
				role="dialog"
				aria-modal="true"
				aria-labelledby="clear-dialog-title"
				tabindex="-1"
				onclick={(e) => e.stopPropagation()}
				onkeydown={(e) => e.key === 'Escape' && cancelClear()}
			>
				<h2 id="clear-dialog-title" class="dialog__title">Clear entry?</h2>
				<p class="dialog__body">This will remove all unsaved changes for today's entry.</p>
				<div class="dialog__actions">
					<button type="button" class="btn btn--secondary" onclick={cancelClear}>
						Cancel
					</button>
					<button type="button" class="btn btn--danger" onclick={confirmClear}>
						Clear
					</button>
				</div>
			</div>
		</div>
	{/if}

	<BackToTop />
{/if}

<style lang="scss">
	@use '$lib/scss/mixins' as mx;

	.loading {
		text-align: center;
		padding: var(--space-xl);
		color: var(--color-text-muted);
	}

	.error {
		background: #fee;
		border: 1px solid var(--color-error);
		color: var(--color-error);
		padding: var(--space-sm);
		border-radius: var(--radius-md);
		margin-bottom: var(--space-md);
	}

	.user-header {
		display: flex;
		justify-content: flex-end;
		align-items: center;
		gap: var(--space-sm);
		padding: var(--space-sm) 0;
	}

	.user-email {
		font-size: var(--font-size-sm);
		color: var(--color-text-muted);
	}

	.logout-btn {
		font-size: var(--font-size-sm);
		color: var(--color-text-muted);
		background: none;
		border: none;
		cursor: pointer;
		padding: var(--space-xs) var(--space-sm);
		border-radius: var(--radius-sm);

		&:hover {
			background: var(--color-bg);
			color: var(--color-text);
		}
	}

	.entry-header {
		text-align: center;
		padding: var(--space-lg) 0;
	}

	.entry-date {
		font-size: var(--font-size-xl);
		font-weight: 400;
		margin: 0 0 var(--space-sm);
	}

	.date-picker {
		font-family: var(--font-family);
		font-size: var(--font-size-sm);
		padding: var(--space-xs) var(--space-sm);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-sm);
		cursor: pointer;

		&:focus {
			outline: none;
			border-color: var(--color-focus);
		}
	}

	.pillar-content {
		padding: var(--space-lg);
		@include mx.flex-column(var(--space-lg));
		border-radius: var(--radius-md);
	}

	.pillar-content--loaded {
		animation: highlight-pulse 0.6s ease-out;
	}

	@keyframes highlight-pulse {
		0% {
			background-color: color-mix(in srgb, var(--pillar-color) 20%, transparent);
		}
		100% {
			background-color: transparent;
		}
	}

	.pillar-content--slide-left {
		animation: slide-from-left 0.3s ease-out;
	}

	.pillar-content--slide-right {
		animation: slide-from-right 0.3s ease-out;
	}

	@keyframes slide-from-left {
		from {
			opacity: 0;
			transform: translateX(-30px);
		}
		to {
			opacity: 1;
			transform: translateX(0);
		}
	}

	@keyframes slide-from-right {
		from {
			opacity: 0;
			transform: translateX(30px);
		}
		to {
			opacity: 1;
			transform: translateX(0);
		}
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

	.extra-fields,
	.text-fields {
		@include mx.flex-column(var(--space-md));
		margin-top: var(--space-md);
	}

	.field-group {
		display: flex;
		flex-direction: column;
		gap: var(--space-xs);
		margin-bottom: var(--space-md);

		label {
			font-size: var(--font-size-sm);
			font-weight: 500;
			color: var(--color-text);
		}

		input,
		textarea {
			width: 100%;
			padding: var(--space-sm);
			border: 1px solid var(--color-border);
			border-radius: var(--radius-md);
			font-family: var(--font-family);
			font-size: var(--font-size-base);
			line-height: var(--line-height-base);

			&:focus {
				outline: none;
				border-color: var(--color-focus);
				box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2);
			}

			&::placeholder {
				color: var(--color-text-muted);
			}
		}

		textarea {
			resize: vertical;
		}

		input[type='number'] {
			max-width: 120px;
		}
	}

	.pillar-nav-buttons {
		display: flex;
		justify-content: space-between;
		gap: var(--space-md);
		margin-top: var(--space-lg);

		.btn--nav {
			min-width: 100px;

			&:disabled {
				opacity: 0.4;
				cursor: not-allowed;
			}
		}
	}

	.entry-actions {
		display: flex;
		justify-content: center;
		gap: var(--space-sm);
		padding: var(--space-lg) 0;
		border-top: 1px solid var(--color-border);
		margin-top: var(--space-md);
	}
</style>
