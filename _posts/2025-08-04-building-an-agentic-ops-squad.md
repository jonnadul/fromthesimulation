---
layout: post
title: "Building an Agentic Ops Squad"
subtitle: "Streamline your service operational debt with AI Agents"
date: 2025-08-04 15:03:15
published: true
---

Whether you are building brand new services, implementing features, or simply maintaining existing services at cloud scale; operational debt will naturally accrue and managing this debt is always a challenge due to prioritization, resourcing, etc. Leaving this debt unmanaged will eventually degrade services and debilitate team efficiencies. What is required is a dedicated team with well-articulated lines of ownership, outcome expectations, and dedicated focus, aka an **Ops Squad**.

The squad** **should comprised of; Site Reliability Engineers who are responsible for triaging and analyzing service incidents and assessing impact to customers and SLA; Software Engineers who are responsible for researching and providing the design and implementation details for a mitigation and resolution along with clear estimates; and an Ops Squad Leader who is responsible for coordinating across the squad to identify the highest customer impacting and SLA degrading incidents that require the lowest cost of resolution and drive the priority of those tasks. This ensures that the Ops Squad maintains the focus and rigor required to meaningfully take ownership and drive down the operational debt.

However, given the dynamic nature of operating large-scale services, it usually proves too unrealistic to keep a dedicated set of resources for an extended period of time on the same objective. It’s also difficult to keep developers in a purely operations focused role for an extended period of time which will eventually cause burnout. Given these challenges, I wanted to try implementing this Ops Squad using AI agents!

---

Basically, I want to implement three agents; the Site Reliability Engineer who has access to service logs, metrics, and customer tickets who is responsible for triaging across all of these data sources to analyze and surface up the highest impacting service incidents and encapsulate the incident severity; the Software Engineer who ingests a given incident, does the research and analysis across internal and external documentation, and provides a technical design and strategy for mitigating and resolving the issue along with a cost estimate; and the Ops Squad Leader responsible for interacting across the Site Reliability Engineer and Software Engineer to generate a list of tasks for the highest impacting incidents with the lowest cost of implementing a solution for the Ops Squad to prioritize.

![]({{ '/assets/img/raw/ba0b7544-b2df-4db0-8379-9167d8dde140_1280x720.jpeg' | relative_url }})

Since I don’t personally own any large-scale services/engineering systems or want to connect to anything at work for a personal project. I decided to scope it down a bit and implement a demonstration of this in [Azure AI Foundry](https://ai.azure.com/). Where I’ll have the Site Reliability Engineer ingest in a [text file of sample Zookeeper logs](https://github.com/logpai/loghub/tree/master/Zookeeper), a generic Software Engineer, and have the Ops Squad Leader create tasks in a [Microsoft Planner](https://planner.cloud.microsoft/).

![]({{ '/assets/img/raw/614f2892-a63e-4a89-8620-42721eb24088_1528x492.png' | relative_url }})

And here are the exact instructions I provided to each agent.

```
Site Reliability Engineer:
Instruction: You are a site reliability engineer, who is responsible for deeply analyzing service logs, telemetry, and other metrics to identify incidents and outages that are high impacting to customers and overall service availability agreements. Articulate each incident in great technical detail using active language and data points, and classify each incident as either high, medium, or low impacting.

Software Engineer:
Instruction: You are a software engineer who is responsible for ingesting production incidents and researching and outlining the technical design, strategy, and approach for addressing the incident. Please provide all technical guidance in great detail, break down into subtasks, and provide a best estimate in weeks for the amount of work necessary to implement.

Operations Squad Leader:
Instruction: You are the operations squad leader responsible for coordinating between the site reliability engineer and software engineer agent to identify the highest impacting incidents with solutions that have the lowest implementation costs and generating a list of tasks.
```

For the Ops Squad Leader I also created connects to the other two agents and an action to create the planner tasks.

![]({{ '/assets/img/raw/c20addce-a23a-4ab1-abe9-766ed9967ce8_1215x661.png' | relative_url }})

Here are the function names and descriptions used for the agent connections.

```
Operations Squad Leader -> Site Reliability Engineer:
Unique Name: Analyze_Service_Logs
Description: Reach out to this agent to get an assessment of all incidents that are customer impacting and affect the service level agreement. Ensure that each incident has well articulated with exact data points, and is provided with a severity of either high, medium, or low.

Operations Squad Leader -> Software Engineer:
Unique Name: Design_And_Estimate_Work
Description: Reach out to this agent to get the exact technical design, strategy, and estimate of work necessary to mitigate and address a given incident. Ensure that a detailed list of exactly what work needs to be done is provided, along with an exact total estimate of the work necessary in weeks.
```

And here is the action which basically links to an Azure Logic App that waits for a POST request containing the task title, and description then updated my planner as appropriate.

![]({{ '/assets/img/raw/e9a2eb1d-b454-4910-87ce-0e95f9bb7e66_1236x795.png' | relative_url }})

*Note: To get this action to work I needed to first publish a new Logic App from the AI Foundry Portal then go into Azure Portal to make the changes I wanted. It wasn’t able to directly link to an existing Logic App I created.*

---

To test this out, I went into the Operations Squad Leader agent’s chat playground and typed in the following prompt.

![]({{ '/assets/img/raw/4ae50107-8d07-4154-8a96-e7608d16bae5_1116x445.png' | relative_url }})

Unfortunately, I hit the rate limit haha however when I checked my planner, I did see four tasks created with titles and descriptions that included a summary of the incident, solution, and breakdown of work along with estimates!

![]({{ '/assets/img/raw/db277e58-aa3d-4c0d-99e0-81401c425d95_1330x1004.png' | relative_url }})

Some interesting ways to expand on this demo:
- Create a trigger to prompt the Operations Squad Leader to run this exercise, which is basically another Logic App. Meaning the trigger can come from anywhere be it ticket creation, email, HTTP request, etc.
- Connect a coding agent, like [Cline](https://cline.bot/), to ingest and perform the changes outlined in the tasks published by the Ops Squad leader.
- Further fine-tuning of the various agents of the Ops Squad.
- Introduce an Ops Squad feedback agent, that is able to follow through on the success of a completed task and use that as feedback to either the prioritization or tuning of the various agents.

I’m truly impressed by how much of the Ops Squad can be offloaded to an agentic team, and am very aware that this is only a few hops away from being full agentic DevOps org. However, this is operations we are talking about and the last thing we want is a system that further contributes to the operational debt haha! So, having a human-in-the-loop is still very critical, for now.

---

Hope you found this post interesting and please do leave a comment if you have feedback!