import { api } from './client';

export interface User {
	pk: number;
	email: string;
	username: string;
	first_name: string;
	last_name: string;
}

export interface LoginData {
	email: string;
	password: string;
}

export interface RegisterData {
	email: string;
	password1: string;
	password2: string;
}

export const authApi = {
	login: (data: LoginData) => api.post<void>('/auth/login/', data),

	logout: () => api.post<void>('/auth/logout/', {}),

	register: (data: RegisterData) => api.post<void>('/auth/registration/', data),

	getUser: () => api.get<User>('/auth/user/'),

	/** Emails a reset link if the address has an account; responds the same either way. */
	requestPasswordReset: (email: string) => api.post<void>('/auth/password/reset/', { email }),

	confirmPasswordReset: (data: {
		uid: string;
		token: string;
		new_password1: string;
		new_password2: string;
	}) => api.post<void>('/auth/password/reset/confirm/', data)
};
