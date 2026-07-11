import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { VirtualGrid } from '@/components/VirtualGrid';
import { ProjectCard } from '@/templates/ProjectsTemplate/components/ProjectCard';

import { MOCK_PROJECTS } from '@/templates/ProjectsTemplate/mock-projects';
import { InvestorCard } from '../InvestorsTemplate/components/InvestorCard';
import { MOCK_INVESTORS } from '../InvestorsTemplate/mock-investors';


export default function FavoritesTemplate() {
  // В реальном приложении здесь была бы логика фильтрации только избранных элементов
  // Для демонстрации возьмем первые несколько элементов из моков
  const favoriteProjects = MOCK_PROJECTS.slice(0, 5);
  const favoriteInvestors = MOCK_INVESTORS.slice(0, 3);

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">Избранное</h1>

      <Tabs defaultValue="projects" className="w-full">
        <TabsList className="grid w-full max-w-md grid-cols-2 mb-8">
          <TabsTrigger value="projects">Проекты</TabsTrigger>
          <TabsTrigger value="investors">Инвесторы</TabsTrigger>
        </TabsList>

        <TabsContent value="projects" className="space-y-4">
          {favoriteProjects.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-20 text-muted-foreground">
              <p>У вас пока нет избранных проектов</p>
            </div>
          ) : (
            <VirtualGrid
              items={favoriteProjects}
              keyExtractor={(p) => p.id}
              renderItem={(p) => <ProjectCard {...p} />}
            />
          )}
        </TabsContent>

        <TabsContent value="investors" className="space-y-4">
          {favoriteInvestors.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-20 text-muted-foreground">
              <p>У вас пока нет избранных инвесторов</p>
            </div>
          ) : (
            <VirtualGrid
              items={favoriteInvestors}
              keyExtractor={(i) => i.id}
              renderItem={(i) => <InvestorCard {...i} />}
              estimateSize={400}
            />
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}
