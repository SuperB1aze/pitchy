import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Heart, Briefcase, DollarSign, Star, ShieldCheck } from 'lucide-react';
import { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';

import { Investor } from '../mock-investors';

type InvestorCardProps = Investor;

export const InvestorCard = ({
  name,
  type,
  description,
  minCheck,
  maxCheck,
  imageUrl,
  interests,
}: InvestorCardProps) => {
  const [isFavorite, setIsFavorite] = useState(false);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('ru-RU', {
      style: 'currency',
      currency: 'RUB',
      maximumFractionDigits: 0,
    }).format(value);
  };

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Card className="overflow-hidden flex flex-col h-full group relative cursor-pointer">
          <div className="aspect-square w-full overflow-hidden relative">
            <img
              src={imageUrl}
              alt={name}
              className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
            />
            <button
              onClick={(e) => {
                e.stopPropagation();
                setIsFavorite(!isFavorite);
              }}
              className="absolute top-3 right-3 p-2 rounded-full bg-white/80 backdrop-blur-sm hover:bg-white transition-colors shadow-sm z-10"
            >
              <Heart
                className={`w-5 h-5 transition-colors ${isFavorite ? 'fill-red-500 stroke-red-500' : 'stroke-slate-600'}`}
              />
            </button>
          </div>
          <div className="flex flex-col flex-grow relative">
            <div className="absolute inset-0 bg-gradient-to-t from-primary/[0.05] to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />
            <CardHeader className="space-y-1">
              <div className="flex justify-between items-start gap-2">
                <CardTitle className="text-xl line-clamp-1">{name}</CardTitle>
                <Badge variant="secondary" className="shrink-0">
                  {type}
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="flex-grow">
              <p className="text-sm text-muted-foreground line-clamp-2 mb-4">
                {description}
              </p>
              <div className="flex flex-wrap gap-1">
                {interests.slice(0, 3).map((interest) => (
                  <Badge key={interest} variant="outline" className="text-[10px] text-bg py-0">
                    {interest}
                  </Badge>
                ))}
                {interests.length > 3 && (
                  <span className="text-[10px] text-muted-foreground">+{interests.length - 3}</span>
                )}
              </div>
            </CardContent>
            <CardFooter className="border-t pt-4 bg-muted/20">
              <div className="flex justify-between items-center w-full">
                <div className="flex flex-col">
                  <span className="text-[10px] text-muted-foreground uppercase font-semibold">Чек:</span>
                  <span className="text-sm font-bold text-primary">
                    {formatCurrency(minCheck)} — {formatCurrency(maxCheck)}
                  </span>
                </div>
              </div>
            </CardFooter>
          </div>
        </Card>
      </DialogTrigger>
      <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <div className="flex justify-between items-start pr-8">
            <div className="space-y-1">
              <Badge variant="outline" className="mb-2">{type}</Badge>
              <DialogTitle className="text-3xl">{name}</DialogTitle>
            </div>
          </div>
        </DialogHeader>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-6">
          <div className="space-y-6">
            <div className="aspect-square rounded-xl overflow-hidden">
              <img src={imageUrl} alt={name} className="w-full h-full object-cover" />
            </div>
            
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Об инвесторе</h3>
              <p className="text-muted-foreground leading-relaxed">
                {description}
              </p>
            </div>
          </div>

          <div className="space-y-8">
            <div className="p-6 rounded-xl border space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-primary/10 text-primary">
                    <Briefcase className="w-4 h-4" />
                  </div>
                  <div className="flex flex-col">
                    <span className="text-[10px] text-muted-foreground uppercase">Сделок</span>
                    <span className="text-sm font-bold">42</span>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-primary/10 text-primary">
                    <DollarSign className="w-4 h-4" />
                  </div>
                  <div className="flex flex-col">
                    <span className="text-[10px] text-muted-foreground uppercase">Капитал</span>
                    <span className="text-sm font-bold">500M+ ₽</span>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-primary/10 text-primary">
                    <Star className="w-4 h-4" />
                  </div>
                  <div className="flex flex-col">
                    <span className="text-[10px] text-muted-foreground uppercase">Рейтинг</span>
                    <span className="text-sm font-bold">4.9/5.0</span>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-primary/10 text-primary">
                    <ShieldCheck className="w-4 h-4" />
                  </div>
                  <div className="flex flex-col">
                    <span className="text-[10px] text-muted-foreground uppercase">Статус</span>
                    <span className="text-sm font-bold">Верифицирован</span>
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                <h4 className="text-sm font-semibold">Интересы:</h4>
                <div className="flex flex-wrap gap-2">
                  {interests.map((interest) => (
                    <Badge key={interest} variant="secondary" className='text-background'>{interest}</Badge>
                  ))}
                </div>
              </div>

              <Button className="w-full py-6 text-lg font-bold shadow-lg shadow-primary/20">
                Предложить проект
              </Button>
            </div>

            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Предпочтения</h3>
              <ul className="space-y-3">
                {['Стадия: Seed, Series A', 'География: РФ и СНГ', 'Доля: 5-15%', 'Активное участие в совете'].map((item, i) => (
                  <li key={i} className="flex items-center gap-3 text-sm text-muted-foreground">
                    <div className="w-1.5 h-1.5 rounded-full bg-primary" />
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};
