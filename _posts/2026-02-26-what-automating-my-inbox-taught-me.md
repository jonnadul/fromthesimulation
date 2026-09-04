---
layout: post
title: "What Automating My Inbox Taught Me About Agentic Behavior"
date: 2026-02-26 16:02:27
published: true
---

I use outlook for my personal email, and I like it because of its rules engine which is really powerful and helps keep my inbox organized. But the need to create and test new rules double check the existing ones are running I just hate the management overhead. So, I automated my outlook inbox folder management!

Using [n8n](https://n8n.io/) I created a workflow that triggers a call into an agent, backed by a [gpt-5.1-chat](https://ai.azure.com/catalog/models/gpt-5.1-chat) instance hosted on [Azure AI Foundry](https://ai.azure.com/), for every incoming email then proceeds to classify the email to either an existing or new folder then proceeds to move it. The agent is connected with tools for getting folder names and creating folders to achieve this.

Here is a diagram of this workflow.

![]({{ '/assets/img/raw/710cc6f2-2206-46fc-80c9-9779fed98db5_899x548.png' | relative_url }})

This workflow ran into some interesting issues. The agent was able to properly classify the incoming emails but consistently failed with moving it to the classified folder because specifically the Outlook create folder, and move message, tools worked against the message and folder ID rather than name. Even with the other tools providing folder names and IDs the agent still struggled in managing the mapping.

I tried to fix this by forcing a structured output which explicitly returned a folder ID rather than name, but even that didn’t fully address the issue. And interestingly I got a couple instances where the agent hallucinated some folder ID values!

---

At its core, the issue I’m actually trying to solve is automate the moving of my incoming email to some folder which I need to run deterministically. The part where I need AI and agents to play a part is to intelligently determine what the folder should be, where I’m ok if it performs an incorrect classification every now and then.

With this in mind, I took a slightly different approach where I focused the agent on only reading the list of current folder names then taking an incoming email and just generating a folder name it should be classified to. Then moved out all of the logic around mapping the folder name to ID, determining whether that exists, and if not creating the new folder as just follow on automation.

Here is the updated workflow.

![]({{ '/assets/img/raw/b43917a4-1b9a-4f1c-bb25-861123d17694_1938x576.png' | relative_url }})

And this worked a lot better! The agent still does some weird classifications like I have both a **Substack** folder and a separate one called **systemdesignone** where I just get [The System Design Newsletter](https://newsletter.systemdesign.one/) but, in this workflow, I’m guaranteed that an incoming email into my inbox always get moved to some folder. That makes me a happy camper!

---

AI and agentic systems are extremely powerful in rationalizing and addressing (via MCP/tooling) large complex and ambiguous problem statements where there are multiple potential solutions. However, when it comes to issues that are scoped and specific with only one clear solution these systems start to faulter. With some of the best examples being math problems!

What I learned is that **sometimes** the more effective use of AI and Agentic systems is to employ them within a larger deterministic service.

---

Let me know if you agree or disagree! All feedback welcome is welcome!