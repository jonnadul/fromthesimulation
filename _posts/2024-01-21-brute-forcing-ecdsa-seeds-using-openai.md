---
layout: post
title: "Solving a Cryptographic Mystery"
subtitle: "An attempt to brute force the original ECDSA seeds"
date: 2024-01-21 08:17:36
categories: [imported]
tags: [substack]
published: true
substack_id: 140211946.brute-forcing-ecdsa-seeds-using-openai
---

A few months back I came across this [blog post](https://saweis.net/posts/nist-curve-seed-origins.html) by [Steve Weis](https://infosec.exchange/@sweis) which goes as follows.

Since the inception of [ECDSA](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm) there have been controversies and debate especially around the seed values used at its foundation. These seed values were chosen by Jerry Solinas, a NSA employee collaborating with the authors of the ECDSA RFC at the time, and it was unearthed that he didn’t choose this at random and instead used a phrase. The phrase was allegedly just a [SHA-1](https://en.wikipedia.org/wiki/SHA-1) hash of the phrase “Jerry deserves a raise…”. Jerry has since forgotten the exact phrase and had even attempted to uncover it himself without success. Unfortunately Jerry died in early 2023.

So the question remains, what was the original phrase? Even prominent cryptographers and security folks have asked and even [set cash bounties](https://words.filippo.io/dispatches/seeds-bounty/)! I felt I had to give it a shot.

---

## The Approach

According to the blog post, Jerry simply SHA-1 hashed an English sentence along with a discrete number of digits to generate the ECDSA seed values. Something like:

```
seed = SHA-1("Jerry and Bob need raises123")
```

Since the format is pretty simple, and most of the value is dictionary words, I figure it’ll be a small enough search space for me to run a [brute-force](https://en.wikipedia.org/wiki/Brute-force_attack) and try all possible ways to say the phrase and add incrementing permutations of char values and SHA-1 hash it to see it’ll match any of the ECDSA seed values.

1.

Using OpenAI seems like the easiest way find out all the ways to say “Jerry and Bob need raises”.

2.

For the additional values, I’ll recursively generate all permutations of chars from the full [ASCII values](https://www.asciitable.com) and attach it both to the front, back, and front/back of the phrase.

3.

Even if the search space is truly this narrow it’ll take forever to run through this brute-force in series. So I’ll spawn threads for each of the phrases that’ll run through all permutations, to make the effort multithreaded.

Here is my [brute force golang application](https://gist.github.com/jonnadul/ad4eab0bac13cf44cb42e401045e1dac).

---

## The Results

I ran the above application for 48 hours on a 1 OCPU E2 VM in my free tier account on Oracle Cloud. And unfortunately I was unable to uncover any of the ECDSA seeds. But I made a few interesting observations.

After the first 200 or so the phrases being returned by OpenAI were getting longer and wordier making their likeliness to be the original phrase less plausible. Placing restrictions on the phrases returned, like asking OpenAI to reducing word count, only caused it to give-up earlier. The strategy for the additional values needs to be further thought out like increasing the max length to beyond 3 and trying attempts where I sprinkle it through the phrase than just pre-pending/post-pending. Also obviously I’ll need a beefier hardware, the 1 OCPU was being nearly fully utilized at almost 98% for the entire 48 hours!

At this point my initial approach has hit a brick wall. But I have some ideas on how to iterate on this approach further, so stay tuned!

[Subscribe now](https://fromthesimulation.substack.com/subscribe?)
