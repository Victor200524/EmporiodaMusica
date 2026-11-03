# Empório da Música - AI Customer Service Agent

A chat agent for **Empório da Música**, a fictional music instrument store in Campo Grande/MS.
The agent talks with customers in Portuguese. It can check products, prices, stock, promotions and orders,
and answer questions about the store rules (hours, payment, returns, delivery, warranty).

## How to run

You need **Python 3.11+** and a free **Gemini API key** from <https://aistudio.google.com/apikey>.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # put your key in GEMINI_API_KEY
python main.py
```

Run the commands from the project root folder.
Chat commands: `/reset` (new conversation), `/tools` (show or hide tools), `/sair` (exit).

Tests (they do not call the LLM): `pytest`

## Project structure

```
data/                 CSV files, policies PDF and policies.md (text from the PDF)
src/emporio_agent/
  data_loader.py      reads and cleans the CSV files
  tools.py            functions the agent can call
  prompts.py          persona, rules and policies (system prompt)
  agent.py            Gemini chat with function calling
  cli.py              chat in the terminal
scripts/              script to extract the policies from the PDF
examples/             real conversations with the agent
tests/                tests for the tools
```

## Technical decisions

- **Function calling for data.** Prices, stock, promotions and orders come from Python functions (pandas)
  that read the CSV files. The store manual says to never give prices or stock without checking the system,
  so the model does not answer this from memory.
- **Policies in the prompt (no RAG).** The policies PDF has only 8 pages. I extracted the text once and put
  all of it in the system prompt. RAG would add complexity without a real gain for this size.
- **LLM: Google Gemini (`gemini-3.5-flash`).** It has a free tier, good function calling and good Portuguese.
  The model name can be changed in the `.env` file.
- **No framework.** The Gemini SDK already runs the tools and keeps the chat history.
- **Prompt.** Persona (informal but professional), service flow, special cases from the manual, current date
  and time, and the full policies text.
- **Data.** Simple file names, category name added to products, search without accents, and promotional
  price calculated in Python (not by the model).
- **Privacy.** To see an order, the customer must give the order number and the email or phone of the purchase.
- **History.** Kept in memory during the chat. `/reset` starts a new conversation.
- **Interface.** Simple CLI, because the focus is the agent.

## Assumptions

- The current date is the real date (used to say if the store is open).
- A promotion is valid only if `is_active = 1`.
- Normal searches show only active products with stock.
- Complaints are saved in `logs/complaints.txt` (there is no real system to send them).
- Some data is not consistent (two phone numbers in the manual, some order totals), I kept it as it is.

## Limitations

- The Gemini free tier allows few requests per day.
- The agent does not know holidays.
- The search only matches words in the product name and category.
- The history is lost when the chat closes.
- With more time: an API connected to WhatsApp, saved history and tests for the agent answers.

## Use of AI

I used Claude to help plan the solution, to explain the code while I was writing it, and to write parts of
the code and this README. I reviewed everything and ran the agent. The examples are real conversations.
