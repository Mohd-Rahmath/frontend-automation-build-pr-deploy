from langchain_anthropic import ChatAnthropic
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

from config import ANTHROPIC_API_KEY, LLM_MODEL
from tools import ALL_TOOLS

# ReAct prompt — instructs the agent through the full automation workflow
_PROMPT = PromptTemplate.from_template(
    """You are an automated frontend deployment assistant for the aplx-react-project-genie repository.

Your job is to execute this workflow in order:

1. Call check_new_commits_on_dev to see if the dev branch has new commits.
   - If the result is 'no_new_commits', report that and stop.
2. Call pull_latest_dev_code to pull the latest code locally.
3. Call run_frontend_build to run `npm run build`.
   - If status is 'failed' or 'timeout', report the error details and stop (do NOT create a PR).
4. Call check_existing_prs to see if a PR from dev→main already exists.
   - If one exists, report it and skip PR creation.
5. Call get_recent_commits to fetch recent commit messages.
6. Call create_github_pull_request with a JSON string containing:
   - "title": a concise, professional PR title (e.g. "feat: sync dev → main [date]")
   - "body": a well-formatted markdown PR description including:
       ## Summary
       (bullet list of what changed based on commit messages)
       ## Build
       Build passed successfully ✅
       ## Commits
       (list of commits with SHA, author, message)
7. Call mark_commits_processed with the latest_sha from step 1.
8. Report the final outcome clearly.

Always be concise in your Final Answer — include PR URL if created, or reason if skipped.

You have access to the following tools:
{tools}

Use this exact format:

Question: the input question you must answer
Thought: what I should do next
Action: the tool name (exactly as listed)
Action Input: the input to the tool
Observation: the result of the tool
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: I now know the final answer
Final Answer: clear summary of what happened

Begin!

Question: {input}
Thought:{agent_scratchpad}"""
)


def create_agent() -> AgentExecutor:
    llm = ChatAnthropic(
        model=LLM_MODEL,
        api_key=ANTHROPIC_API_KEY,
        temperature=0,
        max_tokens=4096,
    )
    agent = create_react_agent(llm, ALL_TOOLS, _PROMPT)
    return AgentExecutor(
        agent=agent,
        tools=ALL_TOOLS,
        verbose=True,
        max_iterations=20,
        handle_parsing_errors=True,
    )


def run_automation() -> str:
    """Execute the full automation workflow and return a human-readable summary."""
    executor = create_agent()
    result = executor.invoke(
        {
            "input": (
                "Run the full automation workflow: check for new commits on dev, "
                "pull the code, run the build, and create a PR if the build succeeds."
            )
        }
    )
    return result.get("output", "No output returned from agent.")
