---
layout: post
title: "Rethinking the Operator Access Experience"
subtitle: "Using LLMs, MCP and AI Agents to provide an empowering and secure operator access experience"
date: 2025-03-29 22:52:07
published: true
---

[Anthropic's Model Context Protocol (MCP)](https://docs.anthropic.com/en/docs/agents-and-tools/mcp) standard has bridged a critical gap between large language models (LLMs) and applications. Enabling these models to operate with enhanced context and increased their applicability. The MCP standard has already proven wildly success [fostering a rapidly expanding ecosystem](https://github.com/punkpeye/awesome-mcp-servers) and leading AI services like [OpenAI](https://openai.github.io/openai-agents-python/mcp/), [Microsoft Copilot](https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/introducing-model-context-protocol-mcp-in-copilot-studio-simplified-integration-with-ai-apps-and-agents/?msockid=033b0f5e3887618d35e41a3a39aa6098), and [Perplexity](https://docs.perplexity.ai/guides/mcp-server) quickly embracing and supporting the standard. The release of this technology had me particularly revisiting a long-standing painpoint in cloud security with a fresh perspectives.

---

A critical aspect of an organization’s security posture is the mechanism by which its employees access and interact with production where there is a clear correlation between an operator’s level, duration, and other dimensions of access and that companies risk to security and operational incidents. Companies like [Uber](https://humanfirewall.io/the-uber-breach-case-study-cybersecurity-lessons-learned/), [Anthem](https://www.hhs.gov/hipaa/for-professionals/compliance-enforcement/agreements/anthem/index.html), and [Capital One](https://www.capitalone.com/digital/facts2019/) having suffered major data breaches stemming from inadequet operator access controls. Similarly global outages at places like [Facebook](https://engineering.fb.com/2021/10/05/networking-traffic/outage-details/) and [AWS](https://www.datacenterknowledge.com/outages/aws-outage-that-broke-the-internet-caused-by-mistyped-command) are also due to unchecked operators inadvertantly running unsafe commands against production. I vividly recall being on an global outage bridge where the root cause was due to a replication failure triggered a single operator accidentally deleting records in a cache.

The industry recognizes the threat, and “reduces the attack surface” by monitoring all operator access, enforcement of endpoint protections, centralized identity frameworks, and ephemeral credentials. This approach works in reducing the risk, but also degrading the operator access experience, which has some unintentional consequences like more complex onboarding for employees, increased time to recovery when responding to major incidents, and sometimes outright reluctance of adoption due to team specific constraints.

---

What if instead of restrictions, we empowered the operator by providing an AI-backed operator access client with an intuative experience that simultanious abstracted the nuances of the access protocol and security monitoring and measures themselves. To demonstrate this I took an [Github Copilot (in VSCode) MCP client](https://code.visualstudio.com/insiders/) and connecting it to a [ssh-client MCP Server](https://github.com/jonnadul/mcpsshclient). Which exposes the `new-ssh-connection` and `run-safe-command `operations with the MCP protocol for the client to interact with while servicing these requests through the traditional SSH protocol.

![]({{ '/assets/img/raw/7f084eef-fdc8-4ed7-a04b-54732e53641f_577x452.png' | relative_url }})

Here is the operator experience!

One particularly noteworthy observations was when I asked Copilot to run a systems check on my host, it defined for itself what a systems check means, identified the corresponding commands, and proceeded to run it directly on my production host.

So this is an interesting, conversation based operator access experience but how does this approach actually make operator access more secure?

---

To answer that question, I added an AI security agent (running off a [llama2 model](https://ollama.com/library/llama2)) into the ssh-client MCP server which analyzes every incoming command to be run via the SSH connection, determines whether its safe or unsafe and for unsafe commands returns a message indicating that the command was rejected.

![]({{ '/assets/img/raw/67d5771e-e315-49c5-a8b3-e18c3bebb77c_568x450.png' | relative_url }})

Note that you can configure how this security agent operates by specifying its SECURITY_POLICY in the [secagentconfig.json](https://github.com/jonnadul/mcpsshclient/blob/main/secagentconfig.json).

```
{
  "ENABLE_SECAGENT": true,
  "SECURITY_POLICY": "\"ls\" is the only safe command, all other commands are unsafe"
}
```

Here is an instance of the AI security agent allowing me to run ls on my home directory.

![]({{ '/assets/img/raw/468ecb6b-6a45-480a-a37b-334e287ecf67_1732x974.png' | relative_url }})

And here is an instance of the AI security agent not allowing me to create an empty text file.

![]({{ '/assets/img/raw/1551dbc9-7d4c-48d6-9432-2c3dc1ecf0d6_1732x974.png' | relative_url }})

Some querks I observed is the llama2 model ran pretty slow possibly because I used a Standard D2ads v6 (2 vcpus, 8 GiB memory) on Azure. The security agent was also inconsistent in its designation of whether a command was safe vs unsafe and I think one way to address it in this demo is to prompt engineer the security policy statement and the command going to the llama2 model. However productizing this type of an approach for operator access governance will require adopting a security focused LLM model and agent like [Microsoft Copilot Security](https://www.microsoft.com/en-us/security/business/ai-machine-learning/microsoft-security-copilot?msockid=033b0f5e3887618d35e41a3a39aa6098), [Simbinal AI](https://simbian.ai/), etc to ensure the most accurate, consistent, and trustworthy behavior.

---

I hope this served as a good case study for how these next generation of AI-based, Agentic systems have shifted the conversation and unlocked opportunities to go back and rethink traditional approaches! I’d love to get you feedback so please do drop a comment on either the blog post or my [Agentic MCP Server sshclient](https://github.com/jonnadul/mcpsshclient/tree/main) project!