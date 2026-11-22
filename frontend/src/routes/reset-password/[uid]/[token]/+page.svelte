<script lang="ts">
	import { page } from '$app/stores';
	import { authApi } from '$lib/api/auth';

	let password1 = $state('');
	let password2 = $state('');
	let error = $state<string | null>(null);
	let linkInvalid = $state(false);
	let loading = $state(false);
	let done = $state(false);

	async function handleSubmit(e: Event) {
		e.preventDefault();
		error = null;

		if (password1 !== password2) {
			error = "The passwords don't match.";
			return;
		}

		loading = true;
		try {
			await authApi.confirmPasswordReset({
				uid: $page.params.uid ?? '',
				token: $page.params.token ?? '',
				new_password1: password1,
				new_password2: password2
			});
			done = true;
		} catch (err: unknown) {
			let fields: Record<string, string[]> = {};
			try {
				fields = JSON.parse((err as { detail?: string })?.detail ?? '{}');
			} catch {
				// not JSON
			}
			if (fields.token || fields.uid) {
				// Expired, already used, or mangled by an email client
				linkInvalid = true;
			} else {
				const messages = [...(fields.new_password1 ?? []), ...(fields.new_password2 ?? [])];
				error = messages.length ? messages.join(' ') : "Couldn't reset your password. Please try again.";
			}
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Choose a new password · Hauora Journal</title>
</svelte:head>

<div class="auth-page">
	<div class="auth-card">
		<h1 class="auth-title">Choose a new password</h1>

		{#if done}
			<div class="auth-success" role="status">Your password has been changed.</div>
			<a href="/app/login" class="auth-button auth-button--link">Sign in</a>
		{:else if linkInvalid}
			<div class="auth-error" role="alert">
				This reset link has expired or has already been used.
			</div>
			<a href="/app/forgot-password" class="auth-button auth-button--link">Send a new link</a>
		{:else}
			{#if error}
				<div class="auth-error" role="alert">{error}</div>
			{/if}

			<form onsubmit={handleSubmit} class="auth-form">
				<div class="form-group">
					<label for="password1">New password</label>
					<input
						type="password"
						id="password1"
						bind:value={password1}
						required
						minlength="8"
						autocomplete="new-password"
						aria-describedby="password-hint"
					/>
					<p id="password-hint" class="auth-hint">At least 8 characters, and not a common password.</p>
				</div>

				<div class="form-group">
					<label for="password2">Confirm new password</label>
					<input
						type="password"
						id="password2"
						bind:value={password2}
						required
						autocomplete="new-password"
					/>
				</div>

				<button type="submit" class="auth-button" disabled={loading}>
					{loading ? 'Saving…' : 'Change password'}
				</button>
			</form>
		{/if}
	</div>
</div>
