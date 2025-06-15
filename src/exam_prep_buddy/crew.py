from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict, Any
from .tools.pdf_utils import extract_syllabus_modules, categorize_files_by_module
import os
from pathlib import Path

@CrewBase
class ExamPrepBuddy():
    """ExamPrepBuddy crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    _shared_inputs: Dict[str, Any] = {}

    def __init__(self):
        super().__init__()
        self._shared_inputs = {}

    @agent
    def material_organizer(self) -> Agent:
        return Agent(config=self.agents_config['material_organizer'], verbose=True)

    @agent
    def material_analyst(self) -> Agent:
        return Agent(config=self.agents_config['material_analyst'], verbose=True)

    @agent
    def pyq_analyst(self) -> Agent:
        return Agent(config=self.agents_config['pyq_analyst'], verbose=True)

    @agent
    def qp_generator(self) -> Agent:
        return Agent(config=self.agents_config['qp_generator'], verbose=True)

    @agent
    def schedule_optimizer(self) -> Agent:
        return Agent(config=self.agents_config['schedule_optimizer'], verbose=True)

    @agent
    def consolidator(self) -> Agent:
        return Agent(config=self.agents_config['consolidator'], verbose=True)

    @agent
    def chat_agent(self) -> Agent:
        return Agent(config=self.agents_config['chat_agent'], verbose=True)

    def set_inputs(self, inputs: Dict[str, Any]) -> None:
        """Store inputs in the instance before creating the crew"""
        self._shared_inputs.clear()
        self._shared_inputs.update(inputs)

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

    @task
    def material_organizing_task(self) -> Task:
        def organize_materials(task_output=None):
            syllabus_pdf = self._shared_inputs['syllabus_pdf']
            materials_folder = self._shared_inputs['materials_folder_path']
            modules = extract_syllabus_modules(syllabus_pdf)
            mapping = categorize_files_by_module(materials_folder, modules)
            self._shared_inputs['modules'] = modules
            self._shared_inputs['module_file_mapping'] = mapping
            return mapping
        return Task(
            config=self.tasks_config['material_organizing_task'],
            callback=organize_materials
        )

    @task
    def material_analysis_task(self) -> Task:
        def analyze_materials(task_output=None):
            module_notes = {}
            for module, files in self._shared_inputs.get('module_file_mapping', {}).items():
                module_notes[module] = f"Notes for {module} (analyzed from {len(files)} files)"
            self._shared_inputs['module_notes'] = module_notes
            return module_notes
        return Task(
            config=self.tasks_config['material_analysis_task'],
            callback=analyze_materials
        )

    @task
    def pyq_analysis_task(self) -> Task:
        def analyze_pyqs(task_output=None):
            insights = {
                'weightage': 'Stub weightage analysis',
                'distribution': 'Stub distribution',
                'difficulty': 'Stub difficulty',
                'time_allocation': 'Stub time allocation',
            }
            self._shared_inputs['pyq_insights'] = insights
            return insights
        return Task(
            config=self.tasks_config['pyq_analysis_task'],
            callback=analyze_pyqs
        )

    @task
    def qp_generation_task(self) -> Task:
        def generate_mock_qps(task_output=None):
            mock_qps = [f"Mock QP {i+1} for {self._shared_inputs['course_code']}" for i in range(3)]
            self._shared_inputs['mock_qps'] = mock_qps
            return mock_qps
        return Task(
            config=self.tasks_config['qp_generation_task'],
            callback=generate_mock_qps
        )

    @task
    def schedule_optimization_task(self) -> Task:
        def optimize_schedule(task_output=None):
            schedule = f"Optimized schedule for {self._shared_inputs['course_code']} (stub)"
            self._shared_inputs['schedule'] = schedule
            return schedule
        return Task(
            config=self.tasks_config['schedule_optimization_task'],
            callback=optimize_schedule
        )

    @task
    def consolidation_task(self) -> Task:
        def consolidate_outputs(task_output=None):
            course_code = self._shared_inputs['course_code']
            output_dir = Path(course_code)
            output_dir.mkdir(exist_ok=True)
            
            for module, notes in self._shared_inputs.get('module_notes', {}).items():
                with open(output_dir / f"notes_{module.replace(' ', '_')}.md", 'w', encoding='utf-8') as f:
                    f.write(notes)
            
            for i, qp in enumerate(self._shared_inputs.get('mock_qps', [])):
                with open(output_dir / f"mock_qp_{i+1}.md", 'w', encoding='utf-8') as f:
                    f.write(qp)
            
            with open(output_dir / "insights.md", 'w', encoding='utf-8') as f:
                for k, v in self._shared_inputs.get('pyq_insights', {}).items():
                    f.write(f"{k}: {v}\n")
            
            if 'schedule' in self._shared_inputs:
                with open(output_dir / "schedule.md", 'w', encoding='utf-8') as f:
                    f.write(self._shared_inputs['schedule'])
            
            return f"Output files written to {output_dir}"
        return Task(
            config=self.tasks_config['consolidation_task'],
            callback=consolidate_outputs
        )

    @task
    def chat_task(self) -> Task:
        def chat(task_output=None):
            return "Chat agent ready to answer questions."
        return Task(
            config=self.tasks_config['chat_task'],
            callback=chat
        )
