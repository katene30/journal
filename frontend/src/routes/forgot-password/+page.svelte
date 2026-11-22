<script lang="ts">
	import { authApi } from '$lib/api/auth';

	let email = $state('');
	let error = $state<string | null>(null);
	let loading = $state(false);
	let sentTo = $state<string | null>(null);

	async function handleSubmit(e: Event) {
		e.preventDefault();
		error = null;
		loading = true;

		try {
			await authApi.requestPasswordReset(email);
			sentTo = email;
		} catch (err: unknown) {
			const status = (err as { status?: number })?.status;
			error =
				status === 429
					? 'Too many reset requests. Please wait a while and try again.'
					: "Couldn't send the reset email. Please try again.";
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Reset password · Hauora Journal</title>
</svelte:head>

<div class="auth-page">
	<div class="auth-card">
		<h1 class="auth-title">Reset password</h1>

		{#if sentTo}
			<div class="auth-success" role="status">
				If <strong>{sentTo}</strong> has an account, we've emailed it a link to choose a new
				password. The link expires in 1 hour. Check your spam folder if it doesn't arrive.
			</div>
		{:else}
			<p class="auth-intro">Enter your account's email and we'll send you a link to choose a new password.</p>

			{#if error}
				<div class="auth-error" role="alert">{error}</div>
			{/if}

			<form onsubmit={handleSubmit} class="auth-form">
				<div class="form-group">
					<label for="email">Email</label>
					<input type="email" id="email" bind:value={email} required autocomplete="email" />
				</div>

				<button type="submit" class="auth-button" disabled={loading}>
					{loading ? 'Sending…' : 'Send reset link'}
				</button>
			</form>
		{/if}

		<p class="auth-footer">
			Remembered it? <a href="/app/login">Sign in</a>
		</p>
	</div>
</div>
