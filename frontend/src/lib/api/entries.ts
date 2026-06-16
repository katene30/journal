import { api } from './client';

export interface EntryListItem {
	id: number;
	date: string;
	header: string;
	overall_day_rating: number | null;
	mood: number | null;
}

export interface Entry {
	id: number;
	date: string;
	created_at: string;
	updated_at: string;
	// Hinengaro
	mood: number | null;
	anxiety_level: number | null;
	stress_level: number | null;
	// Tinana
	sleep_hours: number | null;
	sleep_quality: number | null;
	exercise_level: number | null;
	diet_quality: number | null;
	energy_level: number | null;
	alcohol_caffeine_consumption: string;
	// Whanau
	social_connection: number | null;
	social_interactions_quality: number | null;
	// Wairua
	sense_of_meaning: number | null;
	// Mauriora
	felt_like_myself: number | null;
	// Waiora
	environment_quality: number | null;
	// Reflection
	overall_day_rating: number | null;
	best_thing_today: string;
	hardest_thing_today: string;
	significant_events: string;
	log: string;
}

export type EntryCreate = Omit<Entry, 'id' | 'created_at' | 'updated_at'>;
export type EntryUpdate = Partial<EntryCreate>;

export const entriesApi = {
	list: () => api.get<EntryListItem[]>('/entries/'),

	get: (id: number) => api.get<Entry>(`/entries/${id}/`),

	create: (data: EntryCreate) => api.post<Entry>('/entries/', data),

	update: (id: number, data: EntryUpdate) => api.patch<Entry>(`/entries/${id}/`, data),

	delete: (id: number) => api.delete(`/entries/${id}/`),

	today: () => api.get<Entry>('/entries/today/'),

	byDate: (date: string) => api.get<Entry>(`/entries/by-date/${date}/`),

	recent: () => api.get<EntryListItem[]>('/entries/recent/')
};
