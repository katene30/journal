<script lang="ts">
	import { tick } from 'svelte';
	import { accountApi } from '$lib/api/account';
	import { currentUser } from '$lib/stores/auth';

	let confirming = $state(false);
	let password = $state('');
	let error = $state<string | null>(null);
	let deleting = $state(false);
	let passwordInput = $state<HTMLInputElement>();

	async function startDelete() {
		confirming = true;
		await tick(); // let the form render before focusing it
		passwordInput?.focus();
	}

	function cancelDelete() {
		confirming = false;
		password = '';
		error = null;
	}

	async function handleDelete(e: Event) {
		e.preventDefault();
		error = null;
		deleting = true;
		try {
			await accountApi.deleteAccount(password);
			// A full reload, not goto(): it drops every in-memory copy of the
			// journal, and the fresh app finds no session and shows sign-in
			window.location.assign('/app/login?deleted=1');
		} catch (err: unknown) {
			const status = (err as { status?: number })?.status;
			error =
				status === 400
					? "That password isn't right."
					: status === 429
						? 'Too many attempts. Please wait a while and try again.'
						: "Couldn't delete your account. Please try again.";
			deleting = false;
		}
	}
</script>

<svelte:head>
	<title>Account · Hauora Journal</title>
</svelte:head>

<div class="account-page">
	<h1>Account</h1>

	<section class="panel" aria-labelledby="details-heading">
		<h2 id="details-heading">Your details</h2>
		<dl class="details">
			<dt>Email</dt>
			<dd>{$currentUser?.email}</dd>
		</dl>
		<p class="muted">
			To change your password, sign out and use <strong>Forgot password?</strong> on the sign-in page.
		</p>
	</section>

	<section class="panel" aria-labelledby="export-heading">
		<h2 id="export-heading">Download your data</h2>
		<p>Get a copy of everything you've written, any time.</p>
		<div class="actions">
			<a class="btn btn--secondary" href={accountApi.exportUrl('csv')} download>
				Spreadsheet (CSV)
			</a>
			<a class="btn btn--secondary" href={accountApi.exportUrl('json')} download>
				Full export (JSON)
			</a>
		</div>
		<p class="muted">
			The spreadsheet has one row per day and opens in Excel or Google Sheets. The JSON file also
			includes your account details.
		</p>
	</section>

	<section class="panel panel--danger" aria-labelledby="delete-heading">
		<h2 id="delete-heading">Delete account</h2>
		<p>
			This permanently deletes your account and every journal entry. It can't be undone, so
			download your data first if you want to keep it.
		</p>

		{#if !confirming}
			<button type="button" class="btn btn--secondary btn--danger-outline" onclick={startDelete}>
				Delete my account…
			</button>
		{:else}
			<form class="delete-form" onsubmit={handleDelete}>
				{#if error}
					<div class="auth-error" role="alert">{error}</div>
				{/if}
				<div class="form-group">
					<label for="delete-password">Enter your password to confirm</label>
					<input
						bind:this={passwordInput}
						type="password"
						id="delete-password"
						bind:value={password}
						required
						autocomplete="current-password"
					/>
				</div>
				<div class="actions">
					<button type="submit" class="btn btn--danger" disabled={deleting || !password}>
						{deleting ? 'Deleting…' : 'Permanently delete my account'}
					</button>
					<button type="button" class="btn btn--quiet" onclick={cancelDelete} disabled={deleting}>
						Cancel
					</button>
				</div>
			</form>
		{/if}
	</section>

	<p class="footer-link"><a href="/app/privacy">Privacy policy</a></p>
</div>

<style lang="scss">
	.account-page {
		padding: var(--space-lg) var(--space-md);
		max-width: 640px;
		margin: 0 auto;

		h1 {
			font-size: var(--font-size-xl);
			margin: 0 0 var(--space-md);
		}
	}

	.panel {
		padding: var(--space-md);
		margin-bottom: var(--space-md);
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);

		h2 {
			font-size: var(--font-size-lg);
			margin: 0 0 var(--space-xs);
		}

		p {
			margin: 0 0 var(--space-sm);
		}

		> :last-child {
			margin-bottom: 0;
		}
	}

	.panel--danger {
		border-color: color-mix(in srgb, var(--color-error) 40%, var(--color-border));
	}

	.details {
		display: grid;
		grid-template-columns: auto 1fr;
		gap: var(--space-xxs) var(--space-sm);
		margin: 0 0 var(--space-sm);

		dt {
			color: var(--color-text-muted);
		}

		dd {
			margin: 0;
			overflow-wrap: anywhere;
		}
	}

	.muted {
		font-size: var(--font-size-sm);
		color: var(--color-text-muted);
	}

	.actions {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-xs);
		margin-bottom: var(--space-sm);
	}

	.btn--danger-outline {
		color: var(--color-error);
		border-color: var(--color-error);

		&:hover:not(:disabled) {
			border-color: var(--color-error);
			background: color-mix(in srgb, var(--color-error) 8%, transparent);
		}
	}

	.delete-form {
		.form-group {
			display: flex;
			flex-direction: column;
			gap: var(--space-xxs);
			margin-bottom: var(--space-sm);
		}

		input {
			padding: var(--space-xs) var(--space-sm);
			font: inherit;
			border: 1px solid var(--color-border);
			border-radius: var(--radius-sm);
			background: var(--color-bg);
			max-width: 320px;

			&:focus-visible {
				outline: 2px solid var(--color-focus);
				outline-offset: 2px;
			}
		}

		.btn--danger:disabled {
			opacity: 0.6;
			cursor: not-allowed;
		}
	}

	.footer-link {
		font-size: var(--font-size-sm);
		text-align: center;
	}
</style>
