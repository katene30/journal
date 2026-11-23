<script lang="ts">
	import { goto } from '$app/navigation';
	import { authActions } from '$lib/stores/auth';

	let email = $state('');
	let password = $state('');
	let confirmPassword = $state('');
	let error = $state<string | null>(null);
	let loading = $state(false);

	async function handleSubmit(e: Event) {
		e.preventDefault();
		error = null;

		if (password !== confirmPassword) {
			error = 'Passwords do not match';
			return;
		}

		if (password.length < 8) {
			error = 'Password must be at least 8 characters';
			return;
		}

		loading = true;

		try {
			await authActions.register(email, password);
			goto('/app');
		} catch (err: unknown) {
			if (err && typeof err === 'object' && 'detail' in err) {
				const detail = (err as { detail: string }).detail;
				try {
					const parsed = JSON.parse(detail);
					if (parsed.non_field_errors) {
						error = parsed.non_field_errors.join(', ');
					} else if (parsed.email) {
						error = parsed.email.join(', ');
					} else if (parsed.password1) {
						error = parsed.password1.join(', ');
					} else {
						error = detail;
					}
				} catch {
					error = detail;
				}
			} else {
				error = 'Registration failed. Please try again.';
			}
		} finally {
			loading = false;
		}
	}
</script>

<div class="auth-page">
	<div class="auth-card">
		<h1 class="auth-title">Create Account</h1>

		{#if error}
			<div class="auth-error">{error}</div>
		{/if}

		<form onsubmit={handleSubmit} class="auth-form">
			<div class="form-group">
				<label for="email">Email</label>
				<input
					type="email"
					id="email"
					bind:value={email}
					required
					autocomplete="email"
				/>
			</div>

			<div class="form-group">
				<label for="password">Password</label>
				<input
					type="password"
					id="password"
					bind:value={password}
					required
					autocomplete="new-password"
					minlength="8"
				/>
			</div>

			<div class="form-group">
				<label for="confirmPassword">Confirm Password</label>
				<input
					type="password"
					id="confirmPassword"
					bind:value={confirmPassword}
					required
					autocomplete="new-password"
				/>
			</div>

			<p class="auth-hint">
				Your journal is private to you. Read how it's stored and protected in the
				<a href="/app/privacy">privacy policy</a>.
			</p>

			<button type="submit" class="auth-button" disabled={loading}>
				{loading ? 'Creating account...' : 'Create Account'}
			</button>
		</form>

		<p class="auth-footer">
			Already have an account? <a href="/app/login">Sign in</a>
		</p>
	</div>
</div>
