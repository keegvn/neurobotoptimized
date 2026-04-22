#neurobot_optimized.py
#optimized for learning

import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
from openai import OpenAI

#api key
API_KEY = "-----"

client = OpenAI(api_key=API_KEY)

#expanded built-in neuroscience knowledge base
NEURO_KNOWLEDGE = {
    "dopamine": "Dopamine is a neurotransmitter involved in reward, motivation, pleasure, and motor control. Dysfunction is linked to Parkinson's disease, addiction, and ADHD.",
    "serotonin": "Serotonin regulates mood, sleep, appetite, and digestion. Low levels are strongly associated with depression and anxiety disorders.",
    "adhd": "ADHD (Attention-Deficit/Hyperactivity Disorder) is a neurodevelopmental disorder characterized by inattention, hyperactivity, and impulsivity. It involves dysregulation of dopamine and norepinephrine pathways.",
    "autism": "Autism Spectrum Disorder (ASD) is a developmental disorder affecting communication, behavior, and social interaction. It has strong genetic and neurological components.",
    "alzheimer": "Alzheimer's disease is a progressive neurodegenerative disorder marked by memory loss, cognitive decline, amyloid plaques, and tau tangles.",
    "parkinson": "Parkinson's disease results from the loss of dopamine-producing neurons in the substantia nigra, causing tremors, rigidity, and bradykinesia.",
    "hippocampus": "The hippocampus is essential for forming new memories and spatial navigation. It is one of the first areas affected in Alzheimer's.",
    "neuroplasticity": "Neuroplasticity is the brain's ability to reorganize synaptic connections in response to learning, experience, or injury.",
    "amygdala": "The amygdala processes emotions such as fear, anger, and pleasure. It plays a central role in emotional memory and the fight-or-flight response.",
    "prefrontal cortex": "The prefrontal cortex is responsible for executive functions including decision-making, planning, self-control, and social behavior.",
}

def get_wikipedia_summary(topic):
    """Retrieve live information from Wikipedia"""
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
        response = requests.get(url, timeout=12)
        if response.status_code == 200:
            data = response.json()
            return data.get("extract", "")
        return ""
    except:
        return ""

def get_local_knowledge(query):
    """Search built-in knowledge base"""
    query_lower = query.lower()
    for key, info in NEURO_KNOWLEDGE.items():
        if key in query_lower:
            return info
    return ""

def build_prompt(query, wiki_info, local_info):
    context = ""
    if wiki_info:
        context += f"Wikipedia Summary:\n{wiki_info}\n\n"
    if local_info:
        context += f"Neuroscience Knowledge Base:\n{local_info}\n\n"

    return f"""You are NeuroBot, a knowledgeable and professional neuroscience assistant.

Use ALL the information provided below to answer the user's question accurately and clearly.
Explain concepts in an educational but accessible way. Use simple language when possible.

{context}
User Question: {query}

Answer in a well-structured, helpful, and engaging manner."""

def ask_neurobot(query):
    local_info = get_local_knowledge(query)
    wiki_info = get_wikipedia_summary(query)

    prompt = build_prompt(query, wiki_info, local_info)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Sorry, I couldn't generate a response right now.\nError: {str(e)}"

class NeuroBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NeuroBot - Neuroscience RAG Assistant")
        self.root.geometry("950x760")
        self.root.configure(bg="#f0f4f8")

        #title
        tk.Label(self.root, text="NeuroBot", font=("Arial", 24, "bold"),
                 bg="#f0f4f8", fg="#1e3a8a").pack(pady=15)
        tk.Label(self.root, text="Ask me anything about neuroscience",
                 font=("Arial", 12), bg="#f0f4f8").pack()

        #input
        self.input_area = scrolledtext.ScrolledText(self.root, height=7, font=("Arial", 11))
        self.input_area.pack(fill="x", padx=25, pady=15)

        #buttons
        btn_frame = tk.Frame(self.root, bg="#f0f4f8")
        btn_frame.pack(pady=8)

        tk.Button(btn_frame, text="Ask NeuroBot", font=("Arial", 12, "bold"),
                  bg="#2563eb", fg="white", width=18, height=2,
                  command=self.get_answer).pack(side="left", padx=8)

        tk.Button(btn_frame, text="Clear", font=("Arial", 11), bg="#6b7280", fg="white",
                  width=10, command=self.clear_all).pack(side="left", padx=8)

        tk.Button(btn_frame, text="Copy Answer", font=("Arial", 11), bg="#10b981", fg="white",
                  width=12, command=self.copy_answer).pack(side="left", padx=8)

        #output Label
        tk.Label(self.root, text="NeuroBot's Answer:", font=("Arial", 12, "bold"),
                 bg="#f0f4f8").pack(anchor="w", padx=25, pady=(10,5))

        #output Area
        self.output_area = scrolledtext.ScrolledText(self.root, height=20, font=("Arial", 11))
        self.output_area.pack(fill="both", expand=True, padx=25, pady=5)

    def get_answer(self):
        query = self.input_area.get("1.0", tk.END).strip()
        if not query:
            messagebox.showwarning("Input Required", "Please ask a neuroscience question.")
            return

        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, "Thinking... Retrieving information from multiple sources...\n\n")
        self.root.update()

        answer = ask_neurobot(query)

        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, answer)

    def clear_all(self):
        self.input_area.delete(1.0, tk.END)
        self.output_area.delete(1.0, tk.END)

    def copy_answer(self):
        answer = self.output_area.get("1.0", tk.END).strip()
        if answer:
            self.root.clipboard_clear()
            self.root.clipboard_append(answer)
            messagebox.showinfo("Copied", "Answer copied to clipboard!")


if __name__ == "__main__":
    root = tk.Tk()
    app = NeuroBotApp(root)
    root.mainloop()