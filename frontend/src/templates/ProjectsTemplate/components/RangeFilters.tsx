import {useState} from 'react';
import { Slider } from '@/components/ui/slider';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { ChevronDown } from 'lucide-react';

export interface RangeFilterProps {
  label: string;
  range: { min: number; max: number };
  className?: string;
}

export const RangeFilter = ({ label, range, className }: RangeFilterProps) => {
  const [value, setValue] = useState([range.min, range.max]);

  const formatCurrency = (val: number) => {
    return new Intl.NumberFormat('ru-RU', {
      style: 'currency',
      currency: 'RUB',
      maximumFractionDigits: 0,
    }).format(val);
  };

  return (
    <div className={`space-y-2 ${className}`}>
      <label className="text-sm font-medium">{label}</label>
      <Popover>
        <PopoverTrigger asChild>
          <button className="flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2">
            <span className="truncate">
              {formatCurrency(value[0])} - {formatCurrency(value[1])}
            </span>
            <ChevronDown className="h-4 w-4 opacity-50" />
          </button>
        </PopoverTrigger>
        <PopoverContent className="w-80">
          <div className="space-y-4">
            <div className="flex justify-between text-xs text-muted-foreground">
              <span>{formatCurrency(value[0])}</span>
              <span>{formatCurrency(value[1])}</span>
            </div>
            <Slider
              defaultValue={[range.min, range.max]}
              max={range.max}
              min={range.min}
              step={100000}
              value={value}
              onValueChange={setValue}
              className="py-4"
            />
          </div>
        </PopoverContent>
      </Popover>
    </div>
  );
};