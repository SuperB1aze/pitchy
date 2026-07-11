import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';


export interface FilterOption {
  value: string;
  label: string;
}

export interface FilterSelectProps {
  label: string;
  placeholder: string;
  options: FilterOption[];
  className?: string;
}

export const FilterSelect = ({ label, placeholder, options, className }: FilterSelectProps) => (
  <div className={`space-y-2 ${className}`}>
    <label className="text-sm font-medium">{label}</label>
    <Select>
      <SelectTrigger>
        <SelectValue placeholder={placeholder} />
      </SelectTrigger>
      <SelectContent>
        {options.map((option) => (
          <SelectItem key={option.value} value={option.value}>
            {option.label}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  </div>
);