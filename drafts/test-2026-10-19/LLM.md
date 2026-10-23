# 📰 LLM Research Weekly Papers | 4th Week of October 2026

Use the heading above as the newsletter title.

![cover](https://raw.githubusercontent.com/hyunhp/technical-newletter/main/99.%20Image/llm/llm-curated-cover.png)

Cover image: https://raw.githubusercontent.com/hyunhp/technical-newletter/main/99.%20Image/llm/llm-curated-cover.png

---

## 1) POST TEXT

Copy everything inside the box into the LinkedIn post (plain text).

```text
Start Your Week Informed — Explore 6 Key Papers Driving the Future of LLMs and Generative AI!

Your agent's "forget this" mostly doesn't work
Stay ahead with insights that matter.

(1) Can Agents Forget When Asked? A Benchmark for Memory Unlearning in LLM Agents
(2) MemCut: Every Secret Leaves a Trail in the Long-Term Memory of LLM Agents
(3) New Model, Old Habits: Behavior Transfer under Model Swapping in Multi-Session LLM Agents
(4) Lost in Implicit Routing: How LLM Agents Fail to Load Relevant Skills at Scale
(5) When Code Becomes an LLM Call: An Empirical Study of Call-Site Contracts in Agentic Systems
(6) The Window Is in the Reasoning: When LLM Agents Decide to Follow Prompt Injections

#LLMResearch #GenAI #AIInnovation #ResearchDigest #WeeklyUpdate
```

---

## 2) NEWSLETTER ARTICLE

Copy the part below the line **from the rendered preview**, not from the raw text, so bold and links keep their formatting.

---

Top Papers in Large Language Models (12 October - 18 October)

Ask an agent with long-term memory to forget something, and it probably won't. Researchers tested six mainstream memory systems on three backbone LLMs, and none of them passed more than 1.5% of forget requests end to end. Most passed none.

**🔎 What happened**  
Three papers look at what agent memory holds on to. Bemula has 50 multi-session dialogues with 135 forget requests and 1,742 test questions. Each dialogue has a control version, so a system only gets credit for forgetting a fact it actually stored. The systems failed in one of two ways: the data could still be pulled out with simple attacks, or they deleted far more than was asked. MemCut traces 456 hand-designed secrets through annotated evidence trails, including messages that never state the secret directly. Removing the message that disclosed a secret lowered recovery through the system's own retrieval much more than recovery from the objects left in storage. Even LLM-guided deletion of ten extra turns left 39-76% residual recovery. A third paper finds that when an agent switches to a new model, the new model picks up reasoning and action habits from the old model's history.

**🛠 Why it matters**  
If your product promises to delete things on request, today's memory layers probably can't keep that promise. Deleting the message that stated a fact doesn't delete the fact. Related turns and other stored objects still point to it. MemCut found that searching a wider pool of candidates helps more than deleting every original candidate, so the real bottleneck is finding every trace. If you route between cheap and strong models, the history you hand over also carries behavior, not just context. Summarize it instead of passing along raw transcripts.

**🌱 In plain words**  
Picture asking a friend to forget an embarrassing story. They promise never to repeat it. But the old group chat is still there, along with the photo captions and the follow-up jokes, and anyone reading them can piece it back together. Agent memory has the same problem. Deleting the one note that stated a secret leaves the clues around it. And when a new assistant takes over by reading the old one's notes, it starts copying the old one's habits too.

**⚠️ Reality check**  
These are benchmarks built on constructed dialogues and hand-designed secrets. MemCut's deletion methods are reference baselines, not the best anyone could build. The abstracts don't say which memory systems were tested or how much the results vary between them. The model-swap finding comes from controlled multi-session tasks, not production traffic.

**💭 Editor's Take**  
Today, "we delete on request" is a claim almost no agent memory system can back up. The weak point isn't the delete call. It's that these systems don't know everywhere a fact has spread. Until a system shows a meaningful pass rate on an end-to-end suite like Bemula's, I'd treat that claim as unverified. The thing to watch is whether memory designs start recording, at write time, which stored objects came from which turn. MemCut's coverage finding points there, and a system with that tracking that cut residual recovery sharply would change my view.

**(1) Can Agents Forget When Asked? A Benchmark for Memory Unlearning in LLM Agents** – Lead: the Bemula benchmark shows that no tested memory system passes more than 1.5% of forget requests end to end; failures either leave data extractable or delete too much.

Read More : <https://arxiv.org/abs/2610.18052>

**(2) MemCut: Every Secret Leaves a Trail in the Long-Term Memory of LLM Agents** – Explains why deletion fails: secrets leave evidence trails, and residual recovery stays at 39-76% even after LLM-guided deletion of extra turns.

Read More : <https://arxiv.org/abs/2610.21405>

**(3) New Model, Old Habits: Behavior Transfer under Model Swapping in Multi-Session LLM Agents** – Widens the story: transferred history carries the previous model's reasoning and action habits into the new one, and summarization (including the proposed DASH) reduces this.

Read More : <https://arxiv.org/abs/2610.19712>

**(4) Lost in Implicit Routing: How LLM Agents Fail to Load Relevant Skills at Scale** – Add irrelevant skills to an agent and it loads fewer or none of the relevant ones, even though they are still available. The authors call this skill routing collapse.

Read More : <https://arxiv.org/abs/2610.18522>

**(5) When Code Becomes an LLM Call: An Empirical Study of Call-Site Contracts in Agentic Systems** – An empirical look at what happens to specs and testing when parts of a program's logic, like choosing the next tool or judging whether an action is allowed, become LLM calls.

Read More : <https://arxiv.org/abs/2610.24545>

**(6) The Window Is in the Reasoning: When LLM Agents Decide to Follow Prompt Injections** – Branching rollouts test the common assumption that an agent's choice to follow a prompt injection is settled the moment it reads the injection. The title says the decision window is in the reasoning.

Read More : <https://arxiv.org/abs/2610.24048>

🔖 If this newsletter helps your learning, you may like cert-bank too: free AWS and Palantir certification practice with explanations. <https://hyunhp.github.io/cert-bank/>

That’s all for this week’s edition of LLM Research Weekly!  
I hope you found these insights meaningful and relevant to your work or curiosity in the field. Join me again next week for a new roundup of the latest developments in LLM and generative AI research.

Your thoughts and feedback are always appreciated.

Best regards,  
Hyunho
