export type Project = {
  id: number;
  title: string;
  type: string;
  description: string;
  investmentAmount: number;
  collectedAmount: number;
  imageUrl: string;
};

const BASE_PROJECTS: Project[] = [
  {
    id: 1,
    title: 'EcoSphere AI',
    type: 'Web-сервис',
    description:
      'Платформа на базе ИИ для оптимизации энергопотребления в промышленных масштабах. Помогает снизить выбросы CO2 на 30%.',
    investmentAmount: 15000000,
    collectedAmount: 9750000,
    imageUrl:
      'https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&q=80&w=800',
  },
  {
    id: 2,
    title: 'HealthTrack Pro',
    type: 'Mobile App',
    description:
      'Мобильное приложение для мониторинга здоровья в реальном времени с интеграцией носимых устройств и телемедицины.',
    investmentAmount: 5000000,
    collectedAmount: 1200000,
    imageUrl:
      'https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&q=80&w=800',
  },
  {
    id: 3,
    title: 'UrbanGreen',
    type: 'IoT',
    description:
      'Система автоматизированных вертикальных ферм для городских условий с управлением через облачный сервис.',
    investmentAmount: 8500000,
    collectedAmount: 6800000,
    imageUrl:
      'https://images.unsplash.com/photo-1530836361253-efad5d69687d?auto=format&fit=crop&q=80&w=800',
  },
  {
    id: 4,
    title: 'FinFlow',
    type: 'FinTech',
    description:
      'Децентрализованная платежная система для малого бизнеса с минимальными комиссиями и мгновенными расчетами.',
    investmentAmount: 12000000,
    collectedAmount: 11500000,
    imageUrl:
      'https://images.unsplash.com/photo-1551288049-bbbda536339a?auto=format&fit=crop&q=80&w=800',
  },
  {
    id: 5,
    title: 'EduVR',
    type: 'EdTech',
    description:
      'Образовательная платформа в виртуальной реальности для обучения сложным техническим специальностям.',
    investmentAmount: 25000000,
    collectedAmount: 5000000,
    imageUrl:
      'https://images.unsplash.com/photo-1592478411213-6153e4ebc07d?auto=format&fit=crop&q=80&w=800',
  },
  {
    id: 6,
    title: 'SmartLogistics',
    type: 'SaaS',
    description:
      'Система управления логистическими цепочками с использованием блокчейна для обеспечения прозрачности поставок.',
    investmentAmount: 18000000,
    collectedAmount: 9000000,
    imageUrl:
      'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&q=80&w=800',
  },
];

// Многократно повторяем базовый набор, чтобы получить достаточно данных для
// демонстрации виртуализации. Уникальный id — обязательно, иначе React будет
// ругаться на одинаковые ключи.
export const MOCK_PROJECTS: Project[] = Array.from({ length: 20 }, (_, chunk) =>
  BASE_PROJECTS.map((project, index) => ({
    ...project,
    id: chunk * BASE_PROJECTS.length + index + 1,
  })),
).flat();
