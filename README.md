# Multi-Modal Offer Search Agent System

Developed a multi-agent conversational system using Google ADK and GPT-4o-mini to fetch personalized, real-time offers based on user-selected categories (Flight, Hotel, Tour) and card details.
The system coordinates multiple LLM agents to collect user preferences, perform live Google searches, and filter only active, valid offers.
Integrated tools for agent orchestration, search query generation, and date-based result validation using a fully modular architecture.

---

## 🔁 Agent System Overview

This system is composed of the following interconnected agents:

### 1. `offer_choice_agent`
- Asks the user which type of offer they are looking for:  
  _Flight_, _Hotel_, or _Tour_.
- Stores the selected choice in a JSON object.

### 2. `collect_user_card_details_agent`
- Collects specific card-related details from the user:
  - Card Type (Credit/Debit)
  - Bank Name (e.g., HDFC, SBI)
  - Card Network (e.g., VISA, RuPay, Mastercard, Amex)
- Uses the selected `offer_choice` to contextualize the data.

### 3. `agent_search`
- Builds a search query using both the `offer_choice` and `user_card_details`.
- Searches online for current offers and stores results in `offer_search_results`.

### 4. `search_response_formatter_agent`
- Filters out expired or unrelated offers.
- Labels results clearly with:
  - Offer Type, Discount Details, Promo Code, Validity, Source Name
- Ensures only active offers (based on current datetime) are shown.

### 5. `coordinator_agent` *(Root Agent)*
- Orchestrates the flow between all agents in the correct order:
  1. Collect card details
  2. Ask for offer choice
  3. Search for relevant offers
  4. Format and return the final output to the user

---

## ✅ Features

- Collects user preferences and card information  
- Performs real-time web search for card-based offers  
- Filters and formats results into a user-friendly response  
- Ignores expired or irrelevant entries  
- Fully modular and tool-augmented LLM design

---

## 🛠️ Tech Stack

- Python  
- Google ADK (Agent Development Kit)  
- OpenAI GPT-4o-mini (`LiteLlm`)  
- InMemorySessionService  
- Google Search Tool  
- DateTime Utility Tool

---

## ▶️ Usage

```python
call_agent("Start.")
