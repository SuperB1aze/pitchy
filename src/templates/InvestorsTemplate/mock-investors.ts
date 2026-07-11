export type Investor = {
  id: number;
  name: string;
  type: string;
  description: string;
  minCheck: number;
  maxCheck: number;
  imageUrl: string;
  interests: string[];
};

const BASE_INVESTORS: Investor[] = [
  {
    id: 1,
    name: 'Александр Соколов',
    type: 'Бизнес-ангел',
    description:
      'Частный инвестор с фокусом на EdTech и AI стартапы. Помогаю проектам на ранних стадиях с выходом на рынок.',
    minCheck: 500000,
    maxCheck: 5000000,
    imageUrl:
      'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&q=80&w=800',
    interests: ['EdTech', 'AI', 'SaaS'],
  },
  {
    id: 2,
    name: 'Green Capital',
    type: 'Венчурный фонд',
    description:
      'Фонд, специализирующийся на экологических технологиях и устойчивом развитии. Ищем проекты с потенциалом глобального масштабирования.',
    minCheck: 10000000,
    maxCheck: 100000000,
    imageUrl:
      'https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&q=80&w=800',
    interests: ['Ecology', 'Energy', 'CleanTech'],
  },
  {
    id: 3,
    name: 'Мария Иванова',
    type: 'Частный инвестор',
    description:
      'Инвестирую в потребительские сервисы и мобильные приложения. Имею большой опыт в маркетинге и продуктовом управлении.',
    minCheck: 1000000,
    maxCheck: 10000000,
    imageUrl:
      'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&q=80&w=800',
    interests: ['B2C', 'Mobile', 'Lifestyle'],
  },
  {
    id: 4,
    name: 'TechStars Russia',
    type: 'Акселератор',
    description:
      'Поддерживаем технологические стартапы на стадии идеи и MVP. Предоставляем менторство и начальные инвестиции.',
    minCheck: 100000,
    maxCheck: 1000000,
    imageUrl:
      'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&q=80&w=800',
    interests: ['DeepTech', 'Robotics', 'IoT'],
  },
];

export const MOCK_INVESTORS: Investor[] = Array.from({ length: 25 }, (_, chunk) =>
  BASE_INVESTORS.map((investor, index) => ({
    ...investor,
    id: chunk * BASE_INVESTORS.length + index + 1,
  })),
).flat();
