<script lang="ts">
	import { onMount } from 'svelte';
	import { currentUser } from '$lib/stores/auth';
	import { entriesApi, type EntryListItem } from '$lib/api/entries';
	import EntryCard from '$lib/components/EntryCard.svelte';
	import ArrowRightIcon from '$lib/icons/ArrowRightIcon.svelte';

	let recentEntries = $state<EntryListItem[]>([]);
	let loading = $state(true);

	onMount(async () => {
		try {
			recentEntries = await entriesApi.recent();
		} catch (e) {
			console.error('Failed to load recent entries:', e);
		} finally {
			loading = false;
		}
	});
</script>

<div class="home">
	<h1>Kia ora{$currentUser?.first_name ? `, ${$currentUser.first_name}` : ''}</h1>
	<p class="subtitle">Welcome to your Hauora Journal</p>

	<div class="actions">
		<a href="/app/new" class="btn btn--primary">
			New Entry
			<ArrowRightIcon />
		</a>
	</div>

	<section class="recent">
		<h2>Recent Entries</h2>
		{#if loading}
			<p class="loading">Loading...</p>
		{:else if recentEntries.length === 0}
			<p class="empty">No entries yet. Start journaling!</p>
		{:else}
			<div class="entries-grid">
				{#each recentEntries.slice(0, 5) as entry}
					<EntryCard {entry} />
				{/each}
			</div>
		{/if}
		{#if recentEntries.length > 0}
			<a href="/app/entries" class="view-all">View all entries →</a>
		{/if}
	</section>
</div>

<style lang="scss">
	.home {
		padding: var(--space-xl) var(--space-md);
		max-width: 600px;
		margin: 0 auto;
	}

	h1 {
		font-size: var(--font-size-2xl);
		color: var(--color-text);
		margin-bottom: var(--space-xs);
		text-align: center;
	}

	.subtitle {
		color: var(--color-text-muted);
		margin-bottom: var(--space-xl);
		text-align: center;
	}

	.actions {
		display: flex;
		flex-direction: column;
		gap: var(--space-md);
		margin-bottom: var(--space-xl);
	}

	.recent {
		margin-top: var(--space-lg);
	}

	.recent h2 {
		font-size: var(--font-size-lg);
		color: var(--color-text);
		margin-bottom: var(--space-md);
	}

	.loading,
	.empty {
		color: var(--color-text-muted);
		text-align: center;
		padding: var(--space-lg);
	}

	.entries-grid {
		display: flex;
		flex-direction: column;
		gap: var(--space-md);
	}

	.view-all {
		display: block;
		text-align: center;
		margin-top: var(--space-md);
		color: var(--color-moana);
		text-decoration: none;
		font-weight: 500;

		&:hover {
			text-decoration: underline;
		}
	}
</style>
