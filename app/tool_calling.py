from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from rag import get_retriever
from guardrails import validate_member_id
from guardrails import validate_plan_id
from guardrails import sanitize_member_data
from guardrails import (
    validate_member_id,
    check_member_access
)
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

from insurance_tools import (
    get_member_plan,
    get_provider_network_status,
    get_claim_details,
    get_authorization_details,
    get_policy_details,
)

CURRENT_USER_ID = "user_001"
@tool
def member_plan_tool(member_id: str):
    """
    Get the insurance plan associated with a specific MEMBER.

    REQUIRED INPUT:
    - member_id such as M1001

    USE ONLY when the user asks about a specific member's
    insurance plan.

    DO NOT use this tool for general insurance policy questions,
    referrals, deductibles, coverage rules, MRI requirements,
    physical therapy rules, appeals, or other policy questions.
    """
    is_valid, message = validate_member_id(member_id)

    if not is_valid:
        return {
            "success": False,
            "error": message
        }

    authorized, message = check_member_access(
        CURRENT_USER_ID,
        member_id
    )

    if not authorized:
        return {
            "success": False,
            "error": message
        }

    result = get_member_plan(member_id)

    # 1. Handle case where member is not found
    if not result:
        return {"success": False, "error": f"Member ID {member_id} not found."}

    # 2. Handle errors returned as dictionaries from backend
    if isinstance(result, dict) and "error" in result:
        return result

    # 3. Sanitize and return valid data
    return sanitize_member_data(result)


@tool
def provider_network_tool(provider_name: str):
    """
    Check whether a healthcare provider is in the insurance network.
    Use this tool when the user asks about provider network status.
    """
    return get_provider_network_status(provider_name)


@tool
def claim_status_tool(claim_id: str):
    """
    Retrieve the current status and details of an insurance claim.
    Use this tool when the user asks about a claim.
    """
    return get_claim_details(claim_id)


@tool
def authorization_status_tool(authorization_id: str):
    """
    Retrieve the status of a healthcare authorization.
    Use this tool when the user asks about an authorization.
    """
    return get_authorization_details(authorization_id)

@tool
def policy_details_tool(plan_id: str):
    """
    Retrieve insurance policy benefits using a PLAN ID.

    IMPORTANT:
    - plan_id must be an insurance plan identifier such as PPO100 or HMO200.
    - Do NOT pass a member ID such as M1001.
    - Use this tool for deductible, copay, out-of-pocket maximum,
      physical therapy coverage, and referral requirements.
    """
    is_valid, message = validate_plan_id(plan_id)

    if not is_valid:
        return {
            "success": False,
            "error": message
        }

    result = get_policy_details(plan_id)

    return result

@tool
def search_policy_knowledge(query: str):
    """
    Search the CarePlus insurance POLICY KNOWLEDGE BASE.

    Use this tool for general insurance policy and coverage questions,
    including referrals, MRI authorization, physical therapy,
    emergency care, out-of-network services, claims procedures,
    and appeals.

    Do not use this tool for specific member, claim, authorization,
    provider, or structured plan lookups.
    
    """

    retriever = get_retriever()

    results = retriever.invoke(query)

    if not results:
        return {
            "found": False,
            "message": "No relevant policy information was found."
        }

    sources = []

    for result in results:
        sources.append({
            "content": result.page_content,
            "source": result.metadata.get("source", "careplus_policy.txt")
        })

    return {
        "found": True,
        "sources": sources
    }


@tool
def prepare_claim_appeal(claim_id: str):
    """
    Prepare an appeal for a denied insurance claim.

    This tool only prepares the appeal.
    It does NOT submit the appeal.
    """

    return {
        "success": True,
        "claim_id": claim_id,
        "status": "ready_for_approval",
        "message": f"Appeal for claim {claim_id} is ready for human approval."
    }

@tool
def submit_claim_appeal(claim_id: str) -> str:
    """
    Submit an appeal for a healthcare insurance claim.
    This is a mock tool for demonstration purposes.
    """

    return (
        f"Claim appeal for {claim_id} has been successfully submitted."
    )

def safe_tool_call(tool_function, **kwargs):

    try:
        result = tool_function.invoke(kwargs)
        return result

    except Exception as e:
        return {
            "success": False,
            "error": "Unable to process the request at this time.",
            "details": str(e)
        }
#Binding the tools to the LLM
tools = [
    member_plan_tool,
    provider_network_tool,
    claim_status_tool,
    authorization_status_tool,
    policy_details_tool,
    search_policy_knowledge,
    prepare_claim_appeal,
    submit_claim_appeal
]

llm_with_tools = llm.bind_tools(tools)
#testing
response = llm_with_tools.invoke(
    "What is the status of claim CLM10001 and can you prepare an appeal for it?"
)

print("\nLLM Response:")
print(response)

print("\nTool Calls:")

for tool_call in response.tool_calls:
    print(tool_call)

for tool_call in response.tool_calls:

    if tool_call["name"] == "claim_status_tool":

        result = claim_status_tool.invoke(
            tool_call["args"]
        )

        print("\nTool Result:")
        print(result)