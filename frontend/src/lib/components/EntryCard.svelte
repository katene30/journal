<script lang="ts">
	import type { EntryListItem } from '$lib/api/entries';

	interface Props {
		entry: EntryListItem & { log?: string };
		href?: string;
	}

	let { entry, href = `/app/entries/${entry.id}` }: Props = $props();

	function formatDate(dateStr: string): string {
		const date = new Date(dateStr + 'T00:00:00');
		const today = new Date();
		const yesterday = new Date(today);
		yesterday.setDate(yesterday.getDate() - 1);

		if (dateStr === today.toISOString().split('T')[0]) {
			return 'Today';
		}
		if (dateStr === yesterday.toISOString().split('T')[0]) {
			return 'Yesterday';
		}

		return date.toLocaleDateString('en-NZ', {
			weekday: 'long',
			day: 'numeric',
			month: 'long'
		});
	}

	function truncateLog(log: string | undefined, maxLength = 120): string {
		if (!log) return '';
		if (log.length <= maxLength) return log;
		return log.slice(0, maxLength).trim() + '…';
	}

</script>

<article class="entry-card">
	<header class="entry-card__header">
		<time class="entry-card__date" datetime={entry.date}>
			{formatDate(entry.date)}
		</time>
	</header>

	{#if entry.log}
		<p class="entry-card__log">
			{truncateLog(entry.log)}
		</p>
	{:else}
		<p class="entry-card__log entry-card__log--muted">
			No log entry
		</p>
	{/if}

	<footer class="entry-card__footer">
		<a {href} class="entry-card__link">
			View entry
			<span aria-hidden="true">→</span>
		</a>
	</footer>
</article>

<style lang="scss">
	.entry-card {
		background: var(--color-surface);
		border-radius: var(--radius-lg);
		padding: var(--space-md);
		box-shadow: var(--shadow-sm);
		display: flex;
		flex-direction: column;
		gap: var(--space-sm);
		transition: box-shadow var(--transition-fast), transform var(--transition-fast);

		&:hover {
			box-shadow: var(--shadow-md);
			transform: translateY(-2px);
		}
	}

	.entry-card__header {
		display: flex;
		align-items: center;
		gap: var(--space-sm);
	}

	.entry-card__date {
		font-weight: 600;
		color: var(--color-text);
	}

	.entry-card__log {
		color: var(--color-text);
		line-height: 1.5;
		flex: 1;
	}

	.entry-card__log--muted {
		color: var(--color-text-muted);
		font-style: italic;
	}

	.entry-card__footer {
		display: flex;
		justify-content: flex-end;
		padding-top: var(--space-sm);
		border-top: 1px solid var(--color-border);
	}

	.entry-card__link {
		color: var(--color-moana);
		text-decoration: none;
		font-size: var(--font-size-sm);
		font-weight: 500;
		display: flex;
		align-items: center;
		gap: var(--space-xs);
		transition: color var(--transition-fast);

		&:hover {
			color: var(--color-pounamu);
		}
	}
</style>
