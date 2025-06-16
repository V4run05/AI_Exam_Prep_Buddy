from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from .tools.pdf_utils import extract_text_from_pdf
from .tools.docx_utils import extract_text_from_docx
from .tools.pptx_utils import extract_text_from_pptx
import os

@CrewBase
class ExamPrepBuddy():
    """ExamPrepBuddy crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def syllabus_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['syllabus_analyzer'], # type: ignore[index]
            verbose=True
        )

    @agent
    def material_extractor(self) -> Agent:
        return Agent(
            config=self.agents_config['material_extractor'], # type: ignore[index]
            verbose=True
        )

    @agent
    def material_categorizer(self) -> Agent:
        return Agent(
            config=self.agents_config['material_categorizer'], # type: ignore[index]
            verbose=True
        )

    @task
    def extract_modules_and_topics(self) -> Task:
        return Task(
            config=self.tasks_config['extract_modules_and_topics'],
        )

    @task
    def extract_material_content(self) -> Task:
        return Task(
            config=self.tasks_config['extract_material_content'],
        )

    @task
    def categorize_materials_by_module(self) -> Task:
        return Task(
            config=self.tasks_config['categorize_materials_by_module'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ExamPrepBuddy crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True
        )
