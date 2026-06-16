import type { PillarConfig } from '$lib/types';

export const PILLARS: PillarConfig[] = [
	{
		id: 'reflection',
		icon: '📝',
		name: 'Reflection',
		teReo: 'Whakaaro',
		color: '#607D8B',
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
		textFields: [
			{ id: 'best_thing_today', label: 'Best thing today', placeholder: 'What went well?' },
			{ id: 'hardest_thing_today', label: 'Hardest thing today', placeholder: 'What was challenging?' },
			{ id: 'significant_events', label: 'Significant events', placeholder: 'Anything notable?' },
			{ id: 'log', label: 'Journal', placeholder: "What's on your mind?" }
		]
	},
	{
		id: 'hinengaro',
		icon: '🧠',
		name: 'Hinengaro',
		teReo: 'Mind',
		color: '#2196F3',
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
				helpText: 'How worried or on-edge do you feel?'
			},
			{
				id: 'stress_level',
				title: 'Stress',
				leftLabel: 'Relaxed',
				rightLabel: 'Stressed',
				helpText: 'How much pressure are you feeling?'
			}
		]
	},
	{
		id: 'tinana',
		icon: '💪',
		name: 'Tinana',
		teReo: 'Body',
		color: '#4CAF50',
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
		teReo: 'Relationships',
		color: '#FF9800',
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
		teReo: 'Spirit',
		color: '#9C27B0',
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
			}
		]
	},
	{
		id: 'mauriora',
		icon: '🪞',
		name: 'Mauriora',
		teReo: 'Identity',
		color: '#00BCD4',
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
		teReo: 'Environment',
		color: '#795548',
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
