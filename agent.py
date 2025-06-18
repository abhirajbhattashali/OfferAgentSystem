from google.adk.agents import LlmAgent
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService,Session
from google.adk.runners import Runner
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from google.genai import types
import datetime
from google.adk.models.lite_llm import LiteLlm


OpenAI_Model = "openai/gpt-4o-mini"

APP_NAME = "open_ai_multimodal_agent"
USER_ID = "1234"
SESSION_ID = "1233"

offer_choice_agent = LlmAgent(
    name="offer_choice_agent",
    model=LiteLlm(model=OpenAI_Model),
    description="Offer Choice Agent which collects asks the User to select the type of offer from the options provided.",
    instruction="""You are the Offer Choice Agent whose main task is to first enquire the User regarding which type of Offers he/she wishes to seek:
     1. Flight Offers 
     2. Hotel Offers  
     3. Tour Offers


     Only ask user specifically for the offer he/she wishes to find only once, store it in [choice].
     Store it in a JSON object containing the [choice].
     """,
    output_key="offer_choice"

)

collect_user_card_details_agent = LlmAgent(
    name="collect_user_card_details_agent",
    model=LiteLlm(model=OpenAI_Model),
    description="Agent which collects collects specific user card details based on the [choice] received",
    instruction=""" 

    Ask the user to specifically Enter :
    • Card type (Credit or Debit)  
    • Bank name (e.g., HDFC, SBI)  
    • Card network (e.g., VISA, RuPay, Mastercard, Amex)
    •  Ask only Once.
    •  No other info should be asked.
    Use the 'offer_choice' tool to fetch the user choice and based on the [choice] fetched :
    Display it in a proper format.
    Store it in a  JSON object containing the user_card_details.
     """,
    tools=[AgentTool(agent=offer_choice_agent)],
    output_key="user_card_details"

)

agent_search = LlmAgent(
    model=LiteLlm(model=OpenAI_Model),
    name='SearchAgent',
    description="Search Agent which uses openai/gpt-4o-mini model to fetch the search query and always returns the desired search results",
    instruction=
    """
    Search the internet based on the search query.
    Construct a single search query using this template:
    Search the internet for the current date's live active offers based on all [choice] websites, available for users booking with a [Credit/Debit] card from [BANK_NAME], issued under the [VISA/RUPAY/MASTERCARD/AMEX] network.

    Only Respond  with this format.
    Format-
    . [choice] Offer Platform Name.
    . Offer details (e.g., percentage off, max discount, min booking amount).
    . Promo Code.
    . Offer Validity.
    . Source URL.
    
    Note - Do not display the search results.
    Store it in a JSON object containing 'offer_search_results'.
    """,
    output_key='offer_search_results'
)

def get_current_datetime():
  """
  Returns the current date and time in a human-readable format.

  This tool does not require any arguments.

  Returns:
      str: A string representing the current date and time.
  """
  now = datetime.datetime.now()
  return now.strftime("%Y-%m-%d %H:%M:%S")

search_response_formatter_agent = LlmAgent(
    model=LiteLlm(model=OpenAI_Model),
    name="search_response_formatter_agent",

    description="Agent which modifies, formats and displays the responses from 'Search Agent' tool",
    instruction="""
    
    • Use 'Search Agent' tool to fetch the 'offer_search_results'.
    • Use 'get_current_datetime' tool to fetch the CURRENT DATE and TIME.
    
    Format -
    • Refrain from Mentioning those offers which only include Card Details without belonging to any user choice category.
    • In the Offer Validity Section, display only the ACTIVE offers whose validity ends after CURRENT DATE and TIME label them as ACTIVE , else label those offers as 'EXPIRED' and don't mention their Validity Duration.
    • Display the curated details clearly with labels.
    • Use a 'source_name' label for the URL provided.
    
    Note-
    . If there are no search results return 'No Matching Offer Found for this Card'
    . Do not display JSON object even if there are no search results.
    
    Display and Return the formatted response as formatted_search_response.
     """,
    tools=[AgentTool(agent=agent_search),get_current_datetime],
    output_key="formatted_search_response"

)

root_agent = LlmAgent(
    name="coordinator_agent",
    model=LiteLlm(model=OpenAI_Model),
    description="Multi Agent Coordinator that coordinates between 'collect_user_card_details_agent','offer_choice_agent', search_agent' and 'search_response_formatter_agent' in order",
    instruction=
    """
    1. Directly call 'collect_user_card_details_agent' tool right after user message to manually collect [user_card_details] from user.
    2. Call 'offer_choice_agent' tool to manually collect the offer_choice [choice] from user.
    3. Use 'agent_search' tool to automatically retrieve the [offer_search_results] but do not display the results pass it to 'search_response_formatter_agent' tool.
    4. Call 'search_response_formatter_agent' tool and  display the [formatted_search_response] to the user.
    
    
    Note - 
     Call the agent tools in the order mentioned.
    """,

    tools=[AgentTool(agent=offer_choice_agent), AgentTool(agent=collect_user_card_details_agent),
           AgentTool(agent=agent_search),AgentTool(agent=search_response_formatter_agent)]
)




#
#
# # Session and Runner
# session_service = InMemorySessionService()
# session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
# runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
#
#
# # Agent Interaction
# def call_agent(query):
#     content = types.Content(role='user', parts=[types.Part(text=query)])
#     events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
#
#     for event in events:
#         if event.is_final_response():
#             final_response = event.content.parts[0].text
#             print("Agent Response: ", final_response)
#
#
# call_agent("Start.")