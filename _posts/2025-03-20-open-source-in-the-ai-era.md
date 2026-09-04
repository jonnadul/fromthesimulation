---
layout: post
title: "Cautions in the Open-Source AI-era"
subtitle: "Some thoughts and retrospections"
date: 2025-03-20 05:13:19
published: true
---

When I read about industry leaders like [Yann LeCun advocating the benefits of open-sourcing AI models](https://www.businessinsider.com/meta-ai-yann-lecun-deepseek-open-source-openai-2025-1) I feel conflicted. Open-source has been the driving force for innovation by fostering open collaboration and community engagement. However its operating model has been severally strained by our evolving world of threat actors and I fear for the consequences in the AI-era.

We had the infamous [Apache Log4J remote execution CVE](https://www.cisa.gov/news-events/news/apache-log4j-vulnerability-guidance) a couple of years ago which impacted the entire internet, and almost everyone in the industry [spent their holidays doing patching and running security scans](https://www.reddit.com/r/sysadmin/comments/reqc6f/log4j_0day_being_exploited_mega_thread_overview/?rdt=42128). Then more recently a nation-state actor was found to have [hidden a SSH backdoor in the foundational and popular XZ utils](https://www.techrepublic.com/article/xz-backdoor-linux/) on Linux. There was also an incident with the popular GitHub Actions [tj-actions/changed-file that allowed attackers to exfiltrate secrets](https://www.cve.org/CVERecord?id=CVE-2025-30066). That all combined with the [fatigue experience by open-source maintainers](https://www.theregister.com/2025/02/16/open_source_maintainers_state_of_open/) further exacerbates the owes and eroded trust of the ecosystem.

---

The proverbial cat is out of the bag however and we are ushered into the open-source AI-era. So maintainers and consumers of open-source AI models need to be responsible custodians of the trust and integrity of the ecosystem so we can safely collaborate and innovate together.

The open-source AI model maintainers should learn from the industry and:

- Audit their models for security and code quality regularly; employ secure access control measures.
- Run vulnerability scanning (see [Sleepy Pickle](https://www.darkreading.com/threat-intelligence/sleepy-pickle-exploit-subtly-poisons-ml-models)). They should also further protect the behavior integrity of their models from data poisoning attacks by.
- Ensuring encryption in transit (TLS) on their data ingestion pipelines.
- Embedding watermarks in the dataset to detect manipulation.
- Employ adversarial training to ensure models are less susceptible to prompt injections attacks.

Most importantly, open-source AI models maintainers need to adopt a culture of trust and transparency both in the security practices they employ to ensure the integrity of the models the release and in timely disclosure of vulnerabilities.

The consumers of open-source AI models should also learn from the industry on supply-chain protection best practices and:

- Audit and track their consumption of OSS/AI and dependencies.
- Employ vulnerability scanning.
- Access control best practices.
- Ensure deployment integrity of these models into their production environment.

Consumers should also ingest multiple AI models to further spread the risk of being impacted by a single vulnerability. And lastly ensure they have a robust CI/CD and patching strategy to ensure they can quickly act to patch vulnerabilities.

Finally the end customers of these open-source AI models and services need to exercise extreme caution and ensure they are not sharing personal or work-related information, maintaining awareness of the context behind certain models (especially ones originating from China), and being vigilant in staying up-to-date on patches.

The open-source ecosystem is a bit of a burning building at the moment, and introducing AI-models into the mix feels like adding more fuel. However I’m cautiously optimistic.