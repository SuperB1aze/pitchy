import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Heart, Calendar, Users, Target, TrendingUp } from 'lucide-react';
import { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';

import { Project } from '../mock-projects';

interface ProjectCardProps extends Project {}

export const ProjectCard = ({
  title,
  type,
  description,
  investmentAmount,
  collectedAmount,
  imageUrl,
}: ProjectCardProps) => {
  const [isFavorite, setIsFavorite] = useState(false);
  const progress = Math.min(Math.round((collectedAmount / investmentAmount) * 100), 100);

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
          <div className="aspect-video w-full overflow-hidden relative">
            <img
              src={imageUrl}
              alt={title}
              className="h-full w-full object-cover"
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
            <div className="absolute inset-0 bg-gradient-to-t from-blue-400/[0.08] to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />
            <CardHeader className="space-y-1">
              <div className="flex justify-between items-start gap-2">
                <CardTitle className="text-xl line-clamp-1">{title}</CardTitle>
                <Badge variant="secondary" className="shrink-0">
                  {type}
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="flex-grow">
              <p className="text-sm text-muted-foreground line-clamp-3">
                {description}
              </p>
            </CardContent>
            <CardFooter className="border-t pt-4">
              <div className="flex flex-col w-full gap-2">
                <div className="flex justify-between text-xs text-muted-foreground">
                  <span>Собрано: {formatCurrency(collectedAmount)}</span>
                  <span>{progress}%</span>
                </div>
                <Progress value={progress} className="h-2" />
                <div className="flex justify-between items-end">
                  <div className="flex flex-col">
                    <span className="text-[10px] text-muted-foreground uppercase font-semibold">Цель:</span>
                    <span className="text-sm font-bold text-primary">
                      {formatCurrency(investmentAmount)}
                    </span>
                  </div>
                  <div className="flex flex-col items-end">
                    <span className="text-[10px] text-muted-foreground uppercase font-semibold">Осталось:</span>
                    <span className="text-sm font-medium">
                      {formatCurrency(Math.max(0, investmentAmount - collectedAmount))}
                    </span>
                  </div>
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
              <DialogTitle className="text-3xl">{title}</DialogTitle>
            </div>
          </div>
        </DialogHeader>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-6">
          <div className="space-y-6">
            <div className="aspect-video rounded-xl overflow-hidden">
              <img src={imageUrl} alt={title} className="w-full h-full object-cover" />
            </div>
            
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">О проекте</h3>
              <p className="text-muted-foreground leading-relaxed">
                {description}
                <br /><br />
                Этот проект направлен на решение ключевых проблем в своей индустрии. Мы используем передовые технологии и инновационный подход для достижения поставленных целей. Наша команда экспертов работает над тем, чтобы сделать этот продукт лучшим на рынке.
              </p>
            </div>
          </div>

          <div className="space-y-8">
            <div className="p-6 rounded-xl bg-secondary/30 border space-y-6">
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="font-medium">Прогресс сбора</span>
                  <span className="text-primary font-bold">{progress}%</span>
                </div>
                <Progress value={progress} className="h-3" />
                <div className="flex justify-between text-xs text-muted-foreground">
                  <span>{formatCurrency(collectedAmount)} собрано</span>
                  <span>цель {formatCurrency(investmentAmount)}</span>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-primary/10 text-primary">
                    <Users className="w-4 h-4" />
                  </div>
                  <div className="flex flex-col">
                    <span className="text-[10px] text-muted-foreground uppercase">Инвесторов</span>
                    <span className="text-sm font-bold">124</span>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-primary/10 text-primary">
                    <Calendar className="w-4 h-4" />
                  </div>
                  <div className="flex flex-col">
                    <span className="text-[10px] text-muted-foreground uppercase">Дней осталось</span>
                    <span className="text-sm font-bold">18</span>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-primary/10 text-primary">
                    <Target className="w-4 h-4" />
                  </div>
                  <div className="flex flex-col">
                    <span className="text-[10px] text-muted-foreground uppercase">Стадия</span>
                    <span className="text-sm font-bold">MVP</span>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-primary/10 text-primary">
                    <TrendingUp className="w-4 h-4" />
                  </div>
                  <div className="flex flex-col">
                    <span className="text-[10px] text-muted-foreground uppercase">Доходность</span>
                    <span className="text-sm font-bold">15-20%</span>
                  </div>
                </div>
              </div>

              <Button className="w-full py-6 text-lg font-bold shadow-lg shadow-primary/20">
                Инвестировать в проект
              </Button>
            </div>

            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Ключевые показатели</h3>
              <ul className="space-y-3">
                {['Инновационная технология', 'Опытная команда основателей', 'Растущий рынок', 'Подтвержденный спрос'].map((item, i) => (
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
