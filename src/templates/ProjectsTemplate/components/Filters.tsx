import { Input } from "@/components/ui/input";
import { FilterOption, FilterSelect } from "./FilterSelect";
import { RangeFilter } from "./RangeFilters";

interface FilterProps {
    categoriesData: FilterOption[],
    sortOptionsData: FilterOption[]
}

export const Filters = ({categoriesData, sortOptionsData}: FilterProps) =>  
    <section className="flex flex-col md:flex-row gap-4 items-end sticky top-14 z-10 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 py-1">
        <div className="flex-grow space-y-2">
          <label className="text-sm font-medium">Поиск проектов</label>
          <Input className='bg-background' placeholder="Введите название проекта..." />
        </div>

        <FilterSelect
          label="Категория"
          placeholder="Все категории"
          options={categoriesData}
          className="w-full md:w-48"
        />

        <RangeFilter
          label="Финансирование"
          range={{ min: 100000, max: 50000000 }}
          className="w-full md:w-64"
        />

        <FilterSelect
          label="Сортировка"
          placeholder="По дате"
          options={sortOptionsData}
          className="w-full md:w-48"
        />
      </section>