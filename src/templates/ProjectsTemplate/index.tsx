import { Input } from '@/components/ui/input';
import { FilterOption, FilterSelect } from './components/FilterSelect';
import { RangeFilter } from './components/RangeFilters';
import { ProjectCard } from './components/ProjectCard';
import { MOCK_PROJECTS } from './mock-projects';
import { VirtualGrid } from '@/components/VirtualGrid';

const CATEGORIES: FilterOption[] = [
  { value: 'web', label: 'Веб-разработка' },
  { value: 'mobile', label: 'Мобильные приложения' },
  { value: 'design', label: 'Дизайн' },
];

const SORT_OPTIONS: FilterOption[] = [
  { value: 'newest', label: 'Сначала новые' },
  { value: 'oldest', label: 'Сначала старые' },
  { value: 'popular', label: 'Популярные' },
];

export default function ProjectsTemplate() {
  return (
    <div className="space-y-8">
      <section className="flex flex-col lg:flex-row gap-4 items-end sticky top-0 z-10 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 py-4">
        <div className="w-full lg:flex-grow space-y-2">
          <label className="text-sm font-medium">Поиск проектов</label>
          <Input placeholder="Введите название проекта..." className="w-full" />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:flex gap-4 w-full lg:w-auto">
          <FilterSelect
            label="Категория"
            placeholder="Все категории"
            options={CATEGORIES}
            className="w-full lg:w-48"
          />

          <RangeFilter
            label="Финансирование"
            range={{ min: 100000, max: 50000000 }}
            className="w-full lg:w-64"
          />

          <FilterSelect
            label="Сортировка"
            placeholder="По дате"
            options={SORT_OPTIONS}
            className="w-full lg:w-48"
          />
        </div>
      </section>

      <div className="space-y-4">
        <h2 className="text-2xl font-bold">Проекты</h2>
        {MOCK_PROJECTS.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 text-muted-foreground">
            <p>Проекты не найдены</p>
          </div>
        ) : (
          <VirtualGrid
            items={MOCK_PROJECTS}
            keyExtractor={(p) => p.id}
            renderItem={(p) => <ProjectCard {...p} />}
          />
        )}
      </div>
    </div>
  );
}

