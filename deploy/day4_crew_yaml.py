import os
import yaml
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, task, crew

# Disable IPython logging warning if not using a Jupyter notebook
os.environ["CREWAI_DISABLE_IPYTHON"] = "true"

# Load environment variables from .env file
load_dotenv()

# Initialize Gemini 3.1 Flash model using CrewAI's LLM class
GEMINI_MODEL = "gemini/gemini-3.1-flash-lite"
gemini_llm = LLM(
    model=GEMINI_MODEL,
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

@CrewBase
class AiTrendCrew:
    """AiTrendCrew system orchestration using YAML files"""
    
    # Paths relative to where this script is executed
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True,
            allow_delegation=False,
            llm=gemini_llm
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'],
            verbose=True,
            allow_delegation=False,
            llm=gemini_llm
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task']
        )

    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['writing_task']
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,       # Automatically collected from @agent decorators
            tasks=self.tasks,         # Automatically collected from @task decorators
            process=Process.sequential,  
            verbose=True
        )  

# --- FastAPI App Setup ---
app = FastAPI(title="CrewAI Azure Service")

@app.get("/")
def health_check():
    """Endpoint to check if the API server is up and running"""
    return {"status": "healthy", "service": "CrewAI Runner"}

@app.post("/run-crew")
def run_crew():
    """Endpoint to trigger the CrewAI execution pipeline via an API call"""
    try:
        # Instantiate your crew system and kick it off
        result = AiTrendCrew().crew().kickoff()
        return {"status": "success", "result": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Local testing block
if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI Development Server locally...")
    # This automatically boots up your server on http://127.0.0.1:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)