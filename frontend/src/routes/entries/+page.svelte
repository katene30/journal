<script lang="ts">
	import { entriesApi, type EntryListItem } from '$lib/api/entries';
	import { privacyPrefs } from '$lib/stores/privacy';
	import EntryCard from '$lib/components/EntryCard.svelte';
	import ArrowRightIcon from '$lib/icons/ArrowRightIcon.svelte';

	let entries = $state<EntryListItem[]>([]);
	let loading = $state(true);
	let error = $state<string | null>(null);

	const showPreviews = $derived($privacyPrefs.showPreviews);

	// Previews only come from the server when "show by default" is on in Account
	$effect(() => {
		const preview = showPreviews;
		let stale = false;
		entriesApi
			.list(preview)
			.then((list) => {
				if (!stale) entries = list;
			})
			.catch((e) => {
				console.error('Failed to load entries:', e);
				if (!stale) error = 'Failed to load entries';
			})
			.finally(() => {
				if (!stale) loading = false;
			});
		return () => {
			stale = true;
		};
	});
</script>

<div class="entries-page reading-column">
	<header class="page-header">
		<h1>All Entries</h1>
		<div class="page-header__actions">
			<a href="/app/new" class="btn btn--primary">New Entry <ArrowRightIcon /></a>
		</div>
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
			{#each entries as entry (entry.id)}
				<EntryCard {entry} showIndicators={$privacyPrefs.showIndicators} />
			{/each}
		</div>
	{/if}
</div>

<style lang="scss">
	.entries-page {
		--reading-max: 1000px;
		padding-block: var(--space-lg);
	}

	.page-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: var(--space-lg);
		gap: var(--space-md);
		flex-wrap: wrap;
	}

	.page-header__actions {
		display: flex;
		align-items: center;
		gap: var(--space-xs);
		flex-wrap: wrap;
	}

	h1 {
		font-size: var(--font-size-xl);
		color: var(--color-text);
		margin: 0;
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
		color: var(--color-link);
		text-decoration: none;
		font-weight: 500;

		&:hover {
			text-decoration: underline;
		}
	}

	.entries-grid {
		display: grid;
		gap: var(--space-md);
		/* As many columns as fit with the six pillar names readable */
		grid-template-columns: repeat(auto-fill, minmax(min(100%, 270px), 1fr));
	}
</style>
