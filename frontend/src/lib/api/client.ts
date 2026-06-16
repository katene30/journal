const API_BASE = '/api';

interface ApiError {
	status: number;
	message: string;
	detail?: string;
}

function getCsrfToken(): string | null {
	const match = document.cookie.match(/csrftoken=([^;]+)/);
	return match ? match[1] : null;
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
	const url = `${API_BASE}${endpoint}`;
	const csrfToken = getCsrfToken();

	const headers: Record<string, string> = {
		'Content-Type': 'application/json',
		...(options.headers as Record<string, string>)
	};

	if (csrfToken && options.method && options.method !== 'GET') {
		headers['X-CSRFToken'] = csrfToken;
	}

	const response = await fetch(url, {
		...options,
		headers,
		credentials: 'include'
	});

	if (!response.ok) {
		const error: ApiError = {
			status: response.status,
			message: response.statusText
		};

		try {
			const data = await response.json();
			error.detail = data.detail || JSON.stringify(data);
		} catch {
			// Response wasn't JSON
		}

		throw error;
	}

	if (response.status === 204) {
		return undefined as T;
	}

	return response.json();
}

export const api = {
	get: <T>(endpoint: string) => request<T>(endpoint),

	post: <T>(endpoint: string, data: unknown) =>
		request<T>(endpoint, {
			method: 'POST',
			body: JSON.stringify(data)
		}),

	put: <T>(endpoint: string, data: unknown) =>
		request<T>(endpoint, {
			method: 'PUT',
			body: JSON.stringify(data)
		}),

	patch: <T>(endpoint: string, data: unknown) =>
		request<T>(endpoint, {
			method: 'PATCH',
			body: JSON.stringify(data)
		}),

	delete: (endpoint: string) =>
		request<void>(endpoint, {
			method: 'DELETE'
		})
};
