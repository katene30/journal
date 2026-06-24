<script lang="ts">
	import { currentUser } from '$lib/stores/auth';
</script>

<div class="home">
	<h1>Kia ora{$currentUser?.first_name ? `, ${$currentUser.first_name}` : ''}</h1>
	<p class="subtitle">Welcome to your Hauora Journal</p>

	<div class="actions">
		<a href="/app/new" class="action-card action-card--primary">
			<span class="action-icon">+</span>
			<span class="action-label">New Entry</span>
		</a>
		<a href="/app/entries" class="action-card">
			<span class="action-icon">📋</span>
			<span class="action-label">View Entries</span>
		</a>
		<a href="/app/summary" class="action-card">
			<span class="action-icon">📊</span>
			<span class="action-label">Summary</span>
		</a>
	</div>
</div>

<style lang="scss">
	.home {
		padding: var(--space-xl) var(--space-md);
		max-width: 600px;
		margin: 0 auto;
		text-align: center;
	}

	h1 {
		font-size: var(--font-size-2xl);
		color: var(--color-text);
		margin-bottom: var(--space-xs);
	}

	.subtitle {
		color: var(--color-text-muted);
		margin-bottom: var(--space-xl);
	}

	.actions {
		display: flex;
		flex-direction: column;
		gap: var(--space-md);
	}

	.action-card {
		display: flex;
		align-items: center;
		gap: var(--space-md);
		padding: var(--space-lg);
		background: var(--color-surface);
		border-radius: var(--radius-lg);
		box-shadow: var(--shadow-sm);
		text-decoration: none;
		color: var(--color-text);
		transition: box-shadow var(--transition-fast), transform var(--transition-fast);

		&:hover {
			box-shadow: var(--shadow-md);
			transform: translateY(-2px);
		}
	}

	.action-card--primary {
		background: var(--color-moana);
		color: white;
	}

	.action-icon {
		font-size: var(--font-size-xl);
		width: 48px;
		height: 48px;
		display: flex;
		align-items: center;
		justify-content: center;
		background: rgba(255, 255, 255, 0.15);
		border-radius: var(--radius-md);
	}

	.action-card:not(.action-card--primary) .action-icon {
		background: var(--color-bg);
	}

	.action-label {
		font-size: var(--font-size-lg);
		font-weight: 500;
	}
</style>
