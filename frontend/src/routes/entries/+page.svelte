<script lang="ts">
	import { onMount } from 'svelte';
	import { entriesApi, type EntryListItem } from '$lib/api/entries';
	import EntryCard from '$lib/components/EntryCard.svelte';
	import ArrowRightIcon from '$lib/icons/ArrowRightIcon.svelte';

	let entries = $state<EntryListItem[]>([]);
	let loading = $state(true);
	let error = $state<string | null>(null);

	onMount(async () => {
		try {
			entries = await entriesApi.list();
		} catch (e) {
			console.error('Failed to load entries:', e);
			error = 'Failed to load entries';
		} finally {
			loading = false;
		}
	});
</script>

<div class="entries-page">
	<header class="page-header">
		<h1>All Entries</h1>
		<a href="/app/new" class="new-entry-btn">New Entry <ArrowRightIcon /></a>
	</header>

	{#if loading}
		<p class="loading">Loading entries...</p>
	{:else if error}
		<p class="error">{error}</p>
	{:else if entries.length === 0}
		<div class="empty-state">
			<p>No entries yet.</p>
			<a href="/app/new" class="start-link">Create your first entry →</a>
		</div>
	{:else}
		<div class="entries-grid">
			{#each entries as entry}
				<EntryCard {entry} />
			{/each}
		</div>
	{/if}
</div>

<style lang="scss">
	.entries-page {
		padding: var(--space-lg) var(--space-md);
		max-width: 1000px;
		margin: 0 auto;
	}

	.page-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: var(--space-lg);
		gap: var(--space-md);
		flex-wrap: wrap;
	}

	h1 {
		font-size: var(--font-size-xl);
		color: var(--color-text);
		margin: 0;
	}

	.new-entry-btn {
		display: inline-flex;
		align-items: center;
		gap: var(--space-xs);
		padding: var(--space-sm) var(--space-md);
		background: var(--color-moana);
		color: white;
		text-decoration: none;
		border-radius: var(--radius-md);
		font-weight: 500;
		transition: background var(--transition-fast);

		&:hover {
			background: var(--color-pounamu);
		}
	}

	.loading,
	.error {
		text-align: center;
		padding: var(--space-xl);
		color: var(--color-text-muted);
	}

	.error {
		color: var(--color-error);
	}

	.empty-state {
		text-align: center;
		padding: var(--space-xl);
		background: var(--color-surface);
		border-radius: var(--radius-lg);

		p {
			color: var(--color-text-muted);
			margin-bottom: var(--space-md);
		}
	}

	.start-link {
		color: var(--color-moana);
		text-decoration: none;
		font-weight: 500;

		&:hover {
			text-decoration: underline;
		}
	}

	.entries-grid {
		display: grid;
		gap: var(--space-md);
		grid-template-columns: 1fr;

		@media (min-width: 640px) {
			grid-template-columns: repeat(2, 1fr);
		}

		@media (min-width: 900px) {
			grid-template-columns: repeat(3, 1fr);
		}
	}
</style>
