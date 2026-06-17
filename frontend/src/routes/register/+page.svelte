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

			<button type="submit" class="auth-button" disabled={loading}>
				{loading ? 'Creating account...' : 'Create Account'}
			</button>
		</form>

		<p class="auth-footer">
			Already have an account? <a href="/app/login">Sign in</a>
		</p>
	</div>
</div>

<style lang="scss">
	.auth-page {
		min-height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: var(--space-md);
	}

	.auth-card {
		background: var(--color-surface);
		border-radius: var(--radius-lg);
		padding: var(--space-xl);
		width: 100%;
		max-width: 400px;
		box-shadow: var(--shadow-lg);
	}

	.auth-title {
		text-align: center;
		margin-bottom: var(--space-lg);
		font-size: var(--font-size-xl);
	}

	.auth-error {
		background: #fee;
		border: 1px solid var(--color-error);
		color: var(--color-error);
		padding: var(--space-sm);
		border-radius: var(--radius-md);
		margin-bottom: var(--space-md);
		font-size: var(--font-size-sm);
	}

	.auth-form {
		display: flex;
		flex-direction: column;
		gap: var(--space-md);
	}

	.form-group {
		display: flex;
		flex-direction: column;
		gap: var(--space-xs);

		label {
			font-size: var(--font-size-sm);
			font-weight: 500;
		}

		input {
			padding: var(--space-sm);
			border: 1px solid var(--color-border);
			border-radius: var(--radius-md);
			font-size: var(--font-size-base);

			&:focus {
				outline: none;
				border-color: var(--color-focus);
			}
		}
	}

	.auth-button {
		background: var(--color-hinengaro);
		color: white;
		border: none;
		padding: var(--space-sm) var(--space-md);
		border-radius: var(--radius-md);
		font-size: var(--font-size-base);
		font-weight: 500;
		cursor: pointer;
		transition: background var(--transition-fast);

		&:hover:not(:disabled) {
			background: color-mix(in srgb, var(--color-hinengaro) 85%, black);
		}

		&:disabled {
			opacity: 0.6;
			cursor: not-allowed;
		}
	}

	.auth-footer {
		text-align: center;
		margin-top: var(--space-lg);
		font-size: var(--font-size-sm);
		color: var(--color-text-muted);

		a {
			color: var(--color-hinengaro);
			font-weight: 500;
		}
	}
</style>
