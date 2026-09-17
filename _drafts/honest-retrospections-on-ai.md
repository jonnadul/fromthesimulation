---
layout: post
title: "Honest Retrospections on the Current State of AI"
---

My first true spark of curiosity for programming came in elementary school, when a friend showed me how to program stick figure animations into my TI-83 calculator and how to get them to dance and fight. I was captivated, and this obsession grew from a afterschool party trick into a genuine passion and career in technology.

I was never one of those technology prodigies inventing new programming languages, most of what I built was throwaway stuff. But that didn't matter, what I ended up falling in love with was the *process*; getting inspiration from a great and usually naive idea; researching technologies, frameworks, APIs, programming languages, design patterns, etc; hacking together a working proof-of-concept; and the sheer satisfaction of seeing it work end-to-end even if not completely is indescribeable. Each failure and setback along the way of adhering to this process has been critical is shaping and growing my skillset and expertise.

This is exactly what I'm concerned AI has taken away from us.

Take for example my old college [capstone project](https://github.com/jonnadul/fetching-robot/tree/master) which was to write driver code to articulate a robot navigating a room full of obsticles to capture and retreive an item of interest (which had to be these bright colored magicians balls because image recognition was so crude back then). After we got past all of the hardware challenges and got a basic PCB board and sensors souldered, our first instinct was to start writing a bunch of kernel modules and drivers to interface with the various sensors, motors, and servos but quickly ran into integration issues when we tried to stitch all of this together in user-mode etc. This became further complicated when we needed to move the object detection components off-board onto an android phone, we were using OpenCV which needed a more powerful cpu, and serve it back to the board and forced us to go back to the drawing board. Moving onto embedded Python, which I haven't heard of before, ended up being the simplest and most straight forward way to unblock this because it struck that perfect balance between nuance bit-level articulation and simplicity in hosting up a server to intercept the OpenCV data. If we had the level of AI technology now back then, I'm sure we could have done the software part of the project *much* faster and would have probably come up with a more optimal solution but I would not have learned nearly as much nor walked away with the appreciation I had for the problem statement we were trying to solve.

The most obvious argument against this is that I'm not really thinking about outcomes here, and that effectively leveraging AI would unblock us from taking on and handling higher order problems. Which I don't disagree with, but it shouldn't negate that we are robbing ourselves the discovery process itself. Which I fear detaches us further and further from the ground truth of how this technology works, setting us up for failure in honestly being able to maintain and do our work or our projects safely. I for sure fear this specific angle and element of the larger alignment issue being discussed!

What got me even writing about this was a recent viral blog post [don't be a meatbag proxy](https://gruhn.me/blog/2026-08-03/) that really resonated with me and I'd argue that we should extend this principal well beyond just person to person interactions and well into how we interact with our software development process, even how we inspect and assess the agent-to-agent interactions. 

## FEEDBACK FROM QWEN ##

I've read through your draft. Here are my recommendations:

## Structural & Flow Issues

1. **The "AI SCRAP" section is a duplicate** — it appears to be an earlier version or raw notes that should be removed entirely. It repeats the TI-83 opening and restates points already made more polished in the main body.

2. **Missing concrete examples of your own work** — You mention the capstone robot project well, but the post would benefit from 1-2 shorter personal anecdotes (like the TI-83 one) woven throughout to break up the essay-like sections and keep it grounded in lived experience.

## Content & Argument Strength

3. **The "attention challenges" line feels unearned** — In section 3, you mention "For people with attention challenges like mine" without any setup. This is a personal detail that lands oddly without context. Either remove it or foreshadow it earlier.

4. **The conclusion is strong but could be sharper** — The final line ("The process isn't just the path to the answer. It *is* the answer.") is excellent. But the paragraph before it reads like advice-giving ("I think we all need to have this conversation"). Consider ending on the stronger, more personal note rather than pivoting to prescriptive.

5. **The Gruhn blog post reference at the top disappears** — You open with a compelling hook about extending "don't be a meatbag proxy" into agent-to-agent interactions, but never return to it. Either develop that thread (it's your most original idea) or cut the reference.

## Specific Line-Level Suggestions

6. **First paragraph**: "grew from a afterschool party trick" → "grew from *an* afterschool party trick"

7. **Section 2 opening**: "Here's something I didn't fully appreciate until recently: the struggle *was* the learning." — This is good, but consider connecting it back to the robot capstone story rather than introducing a new abstract point.

8. **"What We Gain and What We Lose"** — The paragraph about "collective depth of our craft" is your strongest societal observation. Consider making this more specific: what concrete skills or knowledge are we losing? (e.g., reading stack traces, understanding memory, debugging without AI)

9. **The "I use AI tools constantly" section** — This is honest and relatable. Consider adding a specific example of *where* you draw the line in your own workflow to make it actionable for readers.

## Tone & Voice

10. **The post oscillates between personal essay and tech commentary** — Both are good, but pick one dominant register. The personal voice is stronger. Let the societal observations emerge from personal experience rather than standing as separate arguments.

11. **Consider a title tweak** — "Honest Retrospections" is slightly formal for the intimate tone of the piece. Something more direct might better match the content.

## What Works Really Well

- The TI-83 opening is vivid and relatable
- The robot capstone story is your strongest example — it shows, doesn't tell
- The honesty about using AI while worrying about it feels genuine, not performative
- The final line is a perfect closer

Want me to apply any of these suggestions directly to the draft?



## AI SCRAP ##
My first true moment of curiosity with technology came in elementary school, when a friend showed me how to program stick figure fighting animations into my TI-83 calculator. What started as a party trick quickly grew into a genuine passion for programming, 

I wasn't one of those technology prodigies inventing new programming languages. Most of what I built was throwaway stuff. But that didn't matter. What mattered was the *process*: getting an idea, feeling inspired, choosing a language, scoping a proof of concept, hacking something together with a URL, and wrestling through every failure along the way. That process is what made me love programming. It's what shaped my career. And it's exactly what I'm starting to worry AI is taking away from all of us.

## The Process Was the Point

Here's something I didn't fully appreciate until recently: the struggle *was* the learning. Every time I hit a wall — a bug that wouldn't resolve, a concept that refused to click, an architecture decision that turned out to be terrible — I was forced to slow down and actually understand what was going on under the hood.

The TI-83's limited memory taught me discipline. Every line of code had to earn its place. I couldn't just import a library for everything; I had to figure things out, sometimes in ways that were ugly but always *mine*. Those constraints weren't obstacles to creativity — they *were* the creativity.

When you build something from scratch, even something simple, you absorb knowledge by osmosis. You learn about data structures because you needed one. You learn about error handling because your program crashed. You learn about user experience because someone actually tried to use what you made. This wasn't efficient learning, sure. But it was *deep* learning.

## The AI Paradox

Now I can go from idea to working prototype in minutes — sometimes seconds. And honestly, that's incredible. For people with attention challenges like mine, the ability to rapidly iterate and test ideas has been genuinely liberating. The friction that once kept good ideas trapped in my head is gone.

But here's the uncomfortable truth: **I'm less likely to understand how things work when AI builds them for me.**

When an LLM writes the code, I get the output without the journey. I skip the debugging sessions where real understanding crystallizes. I bypass the moments of frustration that force you to dig deeper. The shortcut becomes a detour around my own education.

It's not that AI can't teach you — it absolutely can, and increasingly does. But there's a difference between being *taught* something and *discovering* something. Discovery sticks differently. It rewires your intuition in ways that passive learning doesn't.

## What We Gain and What We Lose

Let me be clear: I'm not anti-AI. The productivity gains are real and enormous. Tasks that once consumed hours now take minutes. Creative blocks dissolve faster. The barrier to entry for building things has never been lower, and that's a good thing.

But lowering barriers has a side effect: it lowers the amount of knowledge you accumulate along the way. When everyone can ship an app without understanding networking, databases, or deployment, what happens to the collective depth of our craft? We're trading breadth for depth, and I'm not sure we've fully reckoned with that trade-off.

There's also something more subtle at stake — the confidence that comes from having struggled through things yourself. When you've built real things the hard way, you develop a kind of technical intuition that's hard to articulate but impossible to fake. You can look at a broken system and *feel* where the problem might be. That intuition doesn't come from reading documentation or following tutorials. It comes from having been lost and finding your way back, repeatedly.

## What I'm Trying to Protect

So where does that leave me? I use AI tools constantly — they're too useful to ignore. But I've started being more intentional about where I draw the line.

I let AI handle the boilerplate, the patterns I already know, the tedious stuff that doesn't teach me anything new. But when I'm learning something unfamiliar, I push back. I try to build it myself first, even if it takes longer, even if my solution is worse. Because in those moments, the goal isn't to ship — it's to grow.

I think we all need to have this conversation with ourselves. AI isn't going away. The question isn't whether we use it; it's *how* we use it. Do we let it become a crutch that replaces our thinking, or do we wield it as a tool that amplifies what we already understand?

The answer might be different for every task. But I think the people who thrive in this new landscape will be the ones who consciously preserve their own learning process — using AI to move faster on things they know, and deliberately resisting its pull when there's something worth struggling for.

Because some things are worth the struggle. The process isn't just the path to the answer. It *is* the answer.
