import type { PillarConfig } from '$lib/types';

export const SCALE_MIN = 1;
export const SCALE_MAX = 5;

export interface PillarScore {
	/** Mean of the rated scales on the 1-5 scale, higher = more well; null if none rated */
	score: number | null;
	rated: number;
	total: number;
}

/**
 * One indicator per pillar: the average of that day's ratings, with
 * reversed scales (anxiety, stress) flipped so higher always means more well.
 *
 * Unrated scales are left out, never counted as zero. This is a personal
 * snapshot of how the day felt, not a validated measure of hauora.
 */
export function pillarScore(
	pillar: Pick<PillarConfig, 'scales'>,
	values: object
): PillarScore {
	const oriented = pillar.scales.flatMap((scale) => {
		const v = (values as Record<string, unknown>)[scale.id];
		if (typeof v !== 'number') return [];
		return [scale.reversed ? SCALE_MIN + SCALE_MAX - v : v];
	});

	return {
		score: oriented.length ? oriented.reduce((a, b) => a + b, 0) / oriented.length : null,
		rated: oriented.length,
		total: pillar.scales.length
	};
}

/** "3.7" for averages, "4" for whole numbers */
export const formatScore = (score: number) =>
	Number.isInteger(score) ? String(score) : score.toFixed(1);
