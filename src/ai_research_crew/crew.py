from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from ai_research_crew.models import ResearchFindings,ResearchReport,VerifiedReport,AnalystFindings
from crewai_tools import TavilyExtractorTool,TavilySearchTool

search_tool = TavilySearchTool()
extract_tool = TavilyExtractorTool()

@CrewBase
class AiResearchCrew():
    """AiResearchCrew crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True,
            tools=[search_tool,extract_tool]
        )

    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['analyst'], # type: ignore[index]
            verbose=True
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def verifier(self) -> Agent:
        return Agent(
            config=self.agents_config['verifier'], #type: ignore[index]
            verbose=True 
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
            output_pydantic=ResearchFindings,
            output_file='output/research.json'
        )
    
    @task
    def analyst_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyst_task'],  # type: ignore[index]
            output_pydantic=AnalystFindings,
            output_file='output/analysis.json',
            context=[self.research_task()]  # type: ignore[reportCallIssue]
        )

    @task
    def writer_task(self) -> Task:
        return Task(
            config=self.tasks_config['writer_task'],  # type: ignore[index]
            output_file='output/research_report.json',
            output_pydantic=ResearchReport,
            context=[self.analyst_task()]  # type: ignore[reportCallIssue]
        )

    @task
    def verify_task(self) -> Task:
        return Task(
            config=self.tasks_config['verify_task'],  # type: ignore[index]
            output_file='output/complete_report.json',
            output_pydantic=VerifiedReport,
            context=[self.analyst_task(), self.writer_task()] # type: ignore[reportCallIssue]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AiResearchCrew crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            tracing=True
        )
