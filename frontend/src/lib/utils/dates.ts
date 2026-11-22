// Date helpers that work in the user's *local* calendar.
//
// Avoid `new Date().toISOString().split('T')[0]` for "today": toISOString is UTC,
// so in Aotearoa it returns yesterday's date until midday (NZDT is UTC+13).

/** YYYY-MM-DD for a Date, in local time. */
export function localISODate(d: Date = new Date()): string {
	const y = d.getFullYear();
	const m = String(d.getMonth() + 1).padStart(2, '0');
	const day = String(d.getDate()).padStart(2, '0');
	return `${y}-${m}-${day}`;
}

/** Parse YYYY-MM-DD as a local-time Date (new Date('2026-01-01') would be UTC). */
export function parseISODate(iso: string): Date {
	const [y, m, d] = iso.split('-').map(Number);
	return new Date(y, m - 1, d);
}

/** Shift a YYYY-MM-DD date by a number of days. */
export function addDays(iso: string, days: number): string {
	const d = parseISODate(iso);
	d.setDate(d.getDate() + days);
	return localISODate(d);
}

/** Whole days from a to b (b - a), for YYYY-MM-DD dates. */
export function daysBetween(a: string, b: string): number {
	// Date.UTC sidesteps daylight-saving days that are 23 or 25 hours long
	const [ay, am, ad] = a.split('-').map(Number);
	const [by, bm, bd] = b.split('-').map(Number);
	return Math.round((Date.UTC(by, bm - 1, bd) - Date.UTC(ay, am - 1, ad)) / 86_400_000);
}

/** "3 Nov" */
export function formatShortDate(iso: string): string {
	return parseISODate(iso).toLocaleDateString('en-NZ', { day: 'numeric', month: 'short' });
}

/** "Tue 3 Nov 2026" */
export function formatLongDate(iso: string): string {
	return parseISODate(iso).toLocaleDateString('en-NZ', {
		weekday: 'short',
		day: 'numeric',
		month: 'short',
		year: 'numeric'
	});
}
