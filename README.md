# NeuroBot: Neuroscience RAG Assistant

NeuroBot is a sophisticated Python application that combines a local knowledge base with live web retrieval and AI to provide expert-level answers to neuroscience questions. It utilizes a **Retrieval-Augmented Generation (RAG)** architecture to ensure accuracy and educational value.

---

## Key Features
*   **Three-Tier Information Retrieval:**
    1.  **Local Knowledge Base:** Instant access to pre-defined definitions for core terms (Dopamine, Neuroplasticity, etc.).
    2.  **Wikipedia Integration:** Fetches live summaries using the Wikipedia REST API for up-to-date context.
    3.  **AI Orchestration:** Uses OpenAI's `gpt-4o-mini` to synthesize local and web data into a cohesive, educational response.
*   **Advanced GUI:** A clean, professional interface built with `scrolledtext` for long-form answers and structured input.
*   **Utility Tools:** Includes "Copy to Clipboard" functionality and "Clear" options for a seamless user experience.
*   **Educational Focus:** System prompts are optimized to deliver answers that are accessible yet technically accurate.

---

## Technical Architecture

### Retrieval-Augmented Generation (RAG)
The app follows a specific workflow to generate answers:
1.  **Query Analysis:** The user enters a neuroscience-related question.
2.  **Context Fetching:** The script searches `NEURO_KNOWLEDGE` (local) and Wikipedia (online).
3.  **Prompt Engineering:** It constructs a rich prompt containing the context from both sources.
4.  **Generative Response:** The AI generates a structured response based *only* on the provided facts and its own training.

### UI Components
*   **ScrolledText Widgets:** Used for both input and output to handle large blocks of text.
*   **Threading Simulation:** The app uses `root.update()` to provide visual feedback ("Thinking...") while waiting for API responses.

---

## Installation & Setup

### Prerequisites
*   **Python 3.x**
*   **OpenAI API Key:** You must replace `-----` in the code with a valid key.
*   **External Libraries:**
    ```bash
    pip install requests openai
    ```

### Required Dependencies
| Library | Purpose |
| :--- | :--- |
| `tkinter` | Core GUI framework and window management. |
| `requests` | Handles HTTP calls to the Wikipedia API. |
| `openai` | Connects to the GPT model for natural language processing. |

---

## How to Use
1.  **Launch:** Run the script using `python neurobot_optimized.py`.
2.  **Inquire:** Type a question (e.g., "How does dopamine affect ADHD?") into the top text area.
3.  **Ask:** Click **Ask NeuroBot**. The app will aggregate data and display a detailed report.
4.  **Manage:** Use **Copy Answer** to save the information or **Clear** to start a new session.

---

## Controls & Logic
*   **`get_local_knowledge`**: Iterates through a dictionary to find keywords in the user's query.
*   **`get_wikipedia_summary`**: Sanitizes the query and requests a summary from the Wikipedia API.
*   **`ask_neurobot`**: The central function that coordinates APIs and handles errors gracefully.
