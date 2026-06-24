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
							onclick={closeMenu}
						>
							Summary
						</a>
					</li>
				</ul>

				<div class="header__user">
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
	.header {
		background: var(--color-moana);
		color: white;
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
		color: white;
		text-decoration: none;

		&:hover {
			color: var(--color-kowhai);
		}
	}

	.header__toggle {
		display: flex;
		flex-direction: column;
		gap: 4px;
		padding: var(--space-xs);
		background: none;
		border: none;
		cursor: pointer;
		margin-left: auto;

		@media (min-width: 768px) {
			display: none;
		}
	}

	.header__toggle-bar {
		display: block;
		width: 24px;
		height: 2px;
		background: white;
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
		background: var(--color-moana);
		padding: var(--space-md);
		box-shadow: var(--shadow-lg);

		@media (min-width: 768px) {
			display: flex;
			align-items: center;
			gap: var(--space-lg);
			position: static;
			padding: 0;
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
		gap: var(--space-xs);

		@media (min-width: 768px) {
			flex-direction: row;
			gap: var(--space-md);
		}
	}

	.header__nav-link {
		display: block;
		padding: var(--space-sm) 0;
		color: rgba(255, 255, 255, 0.8);
		text-decoration: none;
		position: relative;
		transition: color var(--transition-fast);

		&:hover {
			color: white;
		}

		@media (min-width: 768px) {
			padding: var(--space-xs) 0;

			&::after {
				content: '';
				position: absolute;
				bottom: 0;
				left: 0;
				right: 0;
				height: 2px;
				background: var(--color-kowhai);
				transform: scaleX(0);
				transition: transform var(--transition-fast);
			}

			&:hover::after {
				transform: scaleX(1);
			}
		}
	}

	.header__nav-link--active {
		color: white;

		@media (min-width: 768px) {
			&::after {
				transform: scaleX(1);
			}
		}
	}

	.header__user {
		display: flex;
		align-items: center;
		gap: var(--space-sm);
		margin-top: var(--space-md);
		padding-top: var(--space-md);
		border-top: 1px solid rgba(255, 255, 255, 0.2);

		@media (min-width: 768px) {
			margin-top: 0;
			padding-top: 0;
			border-top: none;
			margin-left: auto;
		}
	}

	.header__logout {
		padding: var(--space-xs) 0;
		background: transparent;
		border: none;
		color: rgba(255, 255, 255, 0.8);
		font-size: var(--font-size-sm);
		cursor: pointer;
		transition: color var(--transition-fast);

		&:hover {
			color: white;
		}
	}

	.header__login {
		margin-left: auto;
		color: rgba(255, 255, 255, 0.8);
		text-decoration: none;
		transition: color var(--transition-fast);

		&:hover {
			color: white;
		}
	}
</style>
