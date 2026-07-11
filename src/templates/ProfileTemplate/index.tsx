import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { UserSettingsForm } from './components/UserSettingsForm';
import { ProjectForm } from './components/ProjectForm';
import { InvestorForm } from './components/InvestorForm';

export default function ProfileTemplate() {
  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-10">
      <h1 className="text-3xl font-bold">Профиль</h1>

      <UserSettingsForm />

      <Tabs defaultValue="project" className="w-full">
        <TabsList className="grid w-full grid-cols-2 gap-2 bg-card">
          <TabsTrigger value="project">Данные проекта</TabsTrigger>
          <TabsTrigger value="investor">Данные инвестора</TabsTrigger>
        </TabsList>

        <TabsContent value="project">
          <ProjectForm />
        </TabsContent>

        <TabsContent value="investor">
          <InvestorForm />
        </TabsContent>
      </Tabs>
    </div>
  );
}
