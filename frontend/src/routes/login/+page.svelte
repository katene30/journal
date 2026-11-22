<script lang="ts">
	import { goto } from '$app/navigation';
	import { authActions } from '$lib/stores/auth';

	let email = $state('');
	let password = $state('');
	let error = $state<string | null>(null);
	let loading = $state(false);

	async function handleSubmit(e: Event) {
		e.preventDefault();
		error = null;
		loading = true;

		try {
			await authActions.login(email, password);
			goto('/app');
		} catch (err: unknown) {
			if (err && typeof err === 'object' && 'detail' in err) {
				const detail = (err as { detail: string }).detail;
				try {
					const parsed = JSON.parse(detail);
					if (parsed.non_field_errors) {
						error = parsed.non_field_errors.join(', ');
					} else {
						error = detail;
					}
				} catch {
					error = detail;
				}
			} else {
				error = 'Invalid email or password';
			}
		} finally {
			loading = false;
		}
	}
</script>

<div class="auth-page">
	<div class="auth-card">
		<h1 class="auth-title">Sign In</h1>

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
				<div class="form-group__label-row">
					<label for="password">Password</label>
					<a href="/app/forgot-password">Forgot password?</a>
				</div>
				<input
					type="password"
					id="password"
					bind:value={password}
					required
					autocomplete="current-password"
				/>
			</div>

			<button type="submit" class="auth-button" disabled={loading}>
				{loading ? 'Signing in...' : 'Sign In'}
			</button>
		</form>

		<p class="auth-footer">
			Don't have an account? <a href="/app/register">Sign up</a>
		</p>
	</div>
</div>
