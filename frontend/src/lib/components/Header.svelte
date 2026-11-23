<script lang="ts">
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { isAuthenticated, currentUser, authActions } from '$lib/stores/auth';

	let menuOpen = $state(false);

	function toggleMenu() {
		menuOpen = !menuOpen;
	}

	function closeMenu() {
		menuOpen = false;
	}

	async function handleLogout() {
		await authActions.logout();
		closeMenu();
		goto('/app/login');
	}

	function isActive(path: string): boolean {
		const currentPath: string = $page.url.pathname;
		if (path === '/app') {
			return currentPath === '/app' || currentPath === '/app/';
		}
		return currentPath.startsWith(path);
	}
</script>

<header class="header">
	<div class="header__container">
		<a href="/app" class="header__brand" onclick={closeMenu}>
			Hauora Journal
		</a>

		{#if $isAuthenticated}
			<button
				class="header__toggle"
				type="button"
				aria-expanded={menuOpen}
				aria-controls="nav-menu"
				aria-label="Toggle navigation"
				onclick={toggleMenu}
			>
				<span class="header__toggle-bar"></span>
				<span class="header__toggle-bar"></span>
				<span class="header__toggle-bar"></span>
			</button>

			<nav
				id="nav-menu"
				class="header__nav"
				class:header__nav--open={menuOpen}
			>
				<ul class="header__nav-list">
					<li>
						<a
							href="/app"
							class="header__nav-link"
							class:header__nav-link--active={isActive('/app') && !isActive('/app/entries') && !isActive('/app/new') && !isActive('/app/summary')}
							onclick={closeMenu}
						>
							Home
						</a>
					</li>
					<li>
						<a
							href="/app/entries"
							class="header__nav-link"
							class:header__nav-link--active={isActive('/app/entries')}
							aria-current={isActive('/app/entries') ? 'page' : undefined}
							onclick={closeMenu}
						>
							Entries
						</a>
					</li>
					<li>
						<a
							href="/app/new"
							class="header__nav-link"
							class:header__nav-link--active={isActive('/app/new')}
							aria-current={isActive('/app/new') ? 'page' : undefined}
							onclick={closeMenu}
						>
							New Entry
						</a>
					</li>
					<li>
						<a
							href="/app/summary"
							class="header__nav-link"
							class:header__nav-link--active={isActive('/app/summary')}
							aria-current={isActive('/app/summary') ? 'page' : undefined}
							onclick={closeMenu}
						>
							Summary
						</a>
					</li>
				</ul>

				<div class="header__user">
					<a
						href="/app/account"
						class="header__account"
						class:header__account--active={isActive('/app/account')}
						aria-current={isActive('/app/account') ? 'page' : undefined}
						onclick={closeMenu}
					>
						Account
					</a>
					<button
						type="button"
						class="header__logout"
						onclick={handleLogout}
					>
						Logout
					</button>
				</div>
			</nav>
		{:else}
			<a href="/app/login" class="header__login">Login</a>
		{/if}
	</div>
</header>

<style lang="scss">
	/* Warm paper bar, ink text; the current page is marked in plum */
	.header {
		background: var(--color-bg);
		color: var(--color-text);
		border-bottom: 1px solid var(--color-border);
		position: relative;
		z-index: 100;
	}

	.header__container {
		display: flex;
		align-items: center;
		gap: var(--space-lg);
		padding: var(--space-sm) var(--space-md);
		max-width: 1200px;
		margin: 0 auto;
	}

	.header__brand {
		font-size: var(--font-size-lg);
		font-weight: 600;
		color: var(--color-text);
		text-decoration: none;

		&:hover,
		&:visited {
			color: var(--color-text);
		}

		&:hover {
			color: var(--color-primary);
		}
	}

	.header__toggle {
		display: flex;
		flex-direction: column;
		gap: 4px;
		padding: var(--space-xs);
		background: none;
		border: none;
		border-radius: var(--radius-sm);
		cursor: pointer;
		margin-left: auto;

		&:hover {
			background: var(--color-primary-tint);
		}

		&:focus-visible {
			outline: 2px solid var(--color-focus);
			outline-offset: 2px;
		}

		@media (min-width: 768px) {
			display: none;
		}
	}

	.header__toggle-bar {
		display: block;
		width: 24px;
		height: 2px;
		background: var(--color-text);
		border-radius: 1px;
		transition: transform var(--transition-fast), opacity var(--transition-fast);
	}

	.header__toggle[aria-expanded='true'] {
		.header__toggle-bar:nth-child(1) {
			transform: translateY(6px) rotate(45deg);
		}
		.header__toggle-bar:nth-child(2) {
			opacity: 0;
		}
		.header__toggle-bar:nth-child(3) {
			transform: translateY(-6px) rotate(-45deg);
		}
	}

	.header__nav {
		display: none;
		position: absolute;
		top: 100%;
		left: 0;
		right: 0;
		background: var(--color-bg);
		border-bottom: 1px solid var(--color-border);
		padding: var(--space-md);
		box-shadow: var(--shadow-md);

		@media (min-width: 768px) {
			display: flex;
			align-items: center;
			gap: var(--space-lg);
			position: static;
			padding: 0;
			border-bottom: none;
			box-shadow: none;
			flex: 1;
		}
	}

	.header__nav--open {
		display: block;

		@media (min-width: 768px) {
			display: flex;
		}
	}

	.header__nav-list {
		list-style: none;
		margin: 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: var(--space-xxs);

		@media (min-width: 768px) {
			flex-direction: row;
			gap: var(--space-xs);
		}
	}

	/* Shared by the page links and the Account link */
	.header__nav-link,
	.header__account {
		position: relative;
		display: block;
		padding: var(--space-xs) var(--space-sm);
		border-radius: var(--radius-sm);
		color: var(--color-text);
		text-decoration: none;
		transition: background-color var(--transition-fast), color var(--transition-fast);

		&:visited {
			color: var(--color-text);
		}

		&:hover {
			background: var(--color-primary-tint);
			color: var(--color-primary);
		}

		&:focus-visible {
			outline: 2px solid var(--color-focus);
			outline-offset: 2px;
		}

		/* Plum underline marks the current page */
		&::after {
			content: '';
			position: absolute;
			left: var(--space-sm);
			right: var(--space-sm);
			bottom: 2px;
			height: 2px;
			border-radius: 1px;
			background: var(--color-primary);
			transform: scaleX(0);
			transition: transform var(--transition-fast);
		}
	}

	.header__account {
		font-size: var(--font-size-sm);
	}

	.header__nav-link--active,
	.header__account--active {
		&,
		&:visited {
			color: var(--color-primary);
			font-weight: 600;
		}

		&::after {
			transform: scaleX(1);
		}
	}

	.header__user {
		display: flex;
		align-items: center;
		gap: var(--space-xs);
		margin-top: var(--space-sm);
		padding-top: var(--space-sm);
		border-top: 1px solid var(--color-border);

		@media (min-width: 768px) {
			margin-top: 0;
			padding-top: 0;
			border-top: none;
			margin-left: auto;
		}
	}

	.header__logout {
		padding: var(--space-xs) var(--space-sm);
		background: transparent;
		border: none;
		border-radius: var(--radius-sm);
		color: var(--color-text-muted);
		font: inherit;
		font-size: var(--font-size-sm);
		cursor: pointer;
		transition: background-color var(--transition-fast), color var(--transition-fast);

		&:hover {
			background: var(--color-primary-tint);
			color: var(--color-primary);
		}

		&:focus-visible {
			outline: 2px solid var(--color-focus);
			outline-offset: 2px;
		}
	}

	.header__login {
		margin-left: auto;
		color: var(--color-link);
	}
</style>
