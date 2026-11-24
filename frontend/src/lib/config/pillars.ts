import type { PillarConfig } from '$lib/types';

export const PILLARS: PillarConfig[] = [
	{
		id: 'reflection',
		icon: '📝',
		name: 'Reflection',
		teReo: 'Koiri',
		theme: 'Your day',
		color: '#52636d',
		tint: '#edf0f1',
		question: {
			maori: 'He pēhea tō rā i tēnei rā?',
			english: 'How was your day today?'
		},
		scales: [
			{
				id: 'overall_day_rating',
				title: 'Overall Day',
				leftLabel: 'Difficult',
				rightLabel: 'Great',
				helpText: 'How would you rate your day overall?'
			}
		],
		// Journal comes first so a busy day can still be a score and a quick note
		textFields: [
			{ id: 'log', label: 'Journal', placeholder: "What's on your mind?" },
			{
				id: 'gratitude',
				label: "Things I'm grateful for",
				placeholder: 'Big or small, what are you thankful for today?'
			},
			{ id: 'best_thing_today', label: 'Best thing today', placeholder: 'What went well?' },
			{ id: 'hardest_thing_today', label: 'Hardest thing today', placeholder: 'What was challenging?' },
			{ id: 'significant_events', label: 'Significant events', placeholder: 'Anything notable?' }
		]
	},
	{
		id: 'hinengaro',
		icon: '🧠',
		name: 'Hinengaro',
		teReo: 'Koru',
		theme: 'Mind & emotions',
		color: '#20566d',
		tint: '#e8f0f4',
		question: {
			maori: 'E pēhea ana tō hinengaro i tēnei rā?',
			english: 'How is your mind today?'
		},
		scales: [
			{
				id: 'mood',
				title: 'Mood',
				leftLabel: 'Low',
				rightLabel: 'Positive',
				helpText: 'Your overall emotional state'
			},
			{
				id: 'anxiety_level',
				title: 'Anxiety',
				leftLabel: 'Calm',
				rightLabel: 'Anxious',
				helpText: 'How worried or on-edge do you feel?',
				reversed: true
			},
			{
				id: 'stress_level',
				title: 'Stress',
				leftLabel: 'Relaxed',
				rightLabel: 'Stressed',
				helpText: 'How much pressure are you feeling?',
				reversed: true
			}
		]
	},
	{
		id: 'tinana',
		icon: '💪',
		name: 'Tinana',
		teReo: 'Mangopare',
		theme: 'Physical wellbeing',
		color: '#276757',
		tint: '#e8f2ed',
		question: {
			maori: 'E pēhea ana tō tinana i tēnei rā?',
			english: 'How is your body today?'
		},
		scales: [
			{
				id: 'sleep_quality',
				title: 'Sleep Quality',
				leftLabel: 'Poor',
				rightLabel: 'Great',
				helpText: 'How well did you sleep?'
			},
			{
				id: 'energy_level',
				title: 'Energy',
				leftLabel: 'Exhausted',
				rightLabel: 'Energetic',
				helpText: 'Your physical energy level'
			},
			{
				id: 'exercise_level',
				title: 'Movement',
				leftLabel: 'Sedentary',
				rightLabel: 'Active',
				helpText: 'How much did you move today?'
			},
			{
				id: 'diet_quality',
				title: 'Nourishment',
				leftLabel: 'Poor',
				rightLabel: 'Well fed',
				helpText: 'How well did you eat?'
			}
		],
		extraFields: [
			{ id: 'sleep_hours', type: 'number', label: 'Hours of sleep', placeholder: '8' },
			{ id: 'alcohol_caffeine_consumption', type: 'text', label: 'Alcohol/caffeine', placeholder: 'e.g., 2 coffees' }
		]
	},
	{
		id: 'whanau',
		icon: '💛',
		name: 'Whānau',
		teReo: 'Pikorua',
		theme: 'Connection & belonging',
		color: '#94600e',
		tint: '#faefd8',
		question: {
			maori: 'E pēhea ana ō hononga i tēnei rā?',
			english: 'How are your connections today?'
		},
		scales: [
			{
				id: 'social_connection',
				title: 'Connection',
				leftLabel: 'Isolated',
				rightLabel: 'Connected',
				helpText: 'How connected do you feel to others?'
			},
			{
				id: 'social_interactions_quality',
				title: 'Interaction Quality',
				leftLabel: 'Draining',
				rightLabel: 'Nourishing',
				helpText: 'Were your interactions positive?'
			}
		]
	},
	{
		id: 'wairua',
		icon: '🌿',
		name: 'Wairua',
		teReo: 'Manaia',
		theme: 'Spirit & meaning',
		color: '#69466f',
		tint: '#f1eaf2',
		question: {
			maori: 'E pēhea ana tō wairua i tēnei rā?',
			english: 'How is your spirit today?'
		},
		scales: [
			{
				id: 'sense_of_meaning',
				title: 'Meaning',
				leftLabel: 'Lacking',
				rightLabel: 'Purposeful',
				helpText: 'Do you feel a sense of purpose?'
			},
			{
				id: 'spiritual_connection',
				title: 'Spiritual Connection',
				leftLabel: 'Disconnected',
				rightLabel: 'Connected',
				helpText: 'Through faith, karakia, nature, whakapapa, or whatever feeds your spirit'
			}
		]
	},
	{
		id: 'mauriora',
		icon: '🪞',
		name: 'Mauriora',
		teReo: 'Hei Tiki',
		theme: 'Identity',
		color: '#84523d',
		tint: '#f5ebe5',
		question: {
			maori: 'I rongo koe i a koe anō i tēnei rā?',
			english: 'Did you feel like yourself today?'
		},
		scales: [
			{
				id: 'felt_like_myself',
				title: 'Authenticity',
				leftLabel: 'Not myself',
				rightLabel: 'Fully myself',
				helpText: 'How true to yourself did you feel?'
			}
		]
	},
	{
		id: 'waiora',
		icon: '🏡',
		name: 'Waiora',
		teReo: 'Ngutukākā',
		theme: 'Environment',
		color: '#52652b',
		tint: '#eef2e4',
		question: {
			maori: 'E pēhea ana tō taiao i tēnei rā?',
			english: 'How is your environment today?'
		},
		scales: [
			{
				id: 'environment_quality',
				title: 'Environment',
				leftLabel: 'Unsupportive',
				rightLabel: 'Supportive',
				helpText: 'Is your space helping or hindering you?'
			}
		]
	}
];

export const getPillarById = (id: string): PillarConfig | undefined => {
	return PILLARS.find((p) => p.id === id);
};

export const getPillarColor = (id: string): string => {
	return getPillarById(id)?.color ?? '#607D8B';
};

/** Describe a 1-5 scale value in the scale's own words, e.g. 4 -> "Leaning positive". */
export const describeScaleValue = (
	value: number,
	scale: { leftLabel: string; rightLabel: string }
): string => {
	const step = Math.round(value);
	if (step <= 1) return scale.leftLabel;
	if (step === 2) return `Leaning ${scale.leftLabel.toLowerCase()}`;
	if (step === 3) return 'In between';
	if (step === 4) return `Leaning ${scale.rightLabel.toLowerCase()}`;
	return scale.rightLabel;
};
