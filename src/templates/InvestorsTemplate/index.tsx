import { Input } from '@/components/ui/input';
import { FilterOption, FilterSelect } from './components/FilterSelect';


import { VirtualGrid } from '@/components/VirtualGrid';
import { MOCK_INVESTORS } from './mock-investors';
import { InvestorCard } from './components/InvestorCard';

const INVESTOR_TYPES: FilterOption[] = [
  { value: 'angel', label: 'Бизнес-ангел' },
  { value: 'vc', label: 'Венчурный фонд' },
  { value: 'private', label: 'Частный инвестор' },
];

export default function InvestorsTemplate() {
  return (
    <div className="space-y-8">
      <section className="flex flex-col lg:flex-row gap-4 items-end sticky top-0 z-10 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 py-4">
        <div className="w-full lg:flex-grow space-y-2">
          <label className="text-sm font-medium">Поиск инвесторов</label>
          <Input placeholder="Введите имя или название фонда..." className="w-full" />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:flex gap-4 w-full lg:w-auto">
          <FilterSelect
            label="Тип инвестора"
            placeholder="Все типы"
            options={INVESTOR_TYPES}
            className="w-full lg:w-64"
          />

          <FilterSelect
            label="Сортировка"
            placeholder="По рейтингу"
            options={[
              { value: 'rating', label: 'По рейтингу' },
              { value: 'deals', label: 'По количеству сделок' },
            ]}
            className="w-full lg:w-64"
          />
        </div>
      </section>

      <div className="space-y-4">
        <h2 className="text-2xl font-bold">Инвесторы</h2>
        {MOCK_INVESTORS.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 text-muted-foreground">
            <p>Инвесторы не найдены</p>
          </div>
        ) : (
          <VirtualGrid
            items={MOCK_INVESTORS}
            keyExtractor={(item) => item.id}
            renderItem={(item) => <InvestorCard {...item} />}
            estimateSize={400}
          />
        )}
      </div>
    </div>
  );
}

