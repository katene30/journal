import { api } from './client';

export type ExportFormat = 'json' | 'csv';

export const accountApi = {
	/** A plain link: the browser downloads the file with the session cookie. */
	exportUrl: (format: ExportFormat) => `/api/account/export/?file=${format}`,

	/** Permanently deletes the account and every entry. Ends the session. */
	deleteAccount: (password: string) => api.post<void>('/account/delete/', { password })
};
