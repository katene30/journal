import { writable } from 'svelte/store';
import { authApi, type User } from '$lib/api/auth';

export const currentUser = writable<User | null>(null);
export const isAuthenticated = writable(false);
export const authLoading = writable(true);

export const authActions = {
	async login(email: string, password: string) {
		await authApi.login({ email, password });
		const user = await authApi.getUser();
		currentUser.set(user);
		isAuthenticated.set(true);
	},

	async logout() {
		await authApi.logout();
		currentUser.set(null);
		isAuthenticated.set(false);
	},

	async register(email: string, password: string) {
		await authApi.register({ email, password1: password, password2: password });
		// Auto-login after registration (dj-rest-auth does this automatically)
		const user = await authApi.getUser();
		currentUser.set(user);
		isAuthenticated.set(true);
	},

	async checkAuth() {
		authLoading.set(true);
		try {
			const user = await authApi.getUser();
			currentUser.set(user);
			isAuthenticated.set(true);
		} catch {
			currentUser.set(null);
			isAuthenticated.set(false);
		} finally {
			authLoading.set(false);
		}
	},
};
