---
title: "How I Write My CLAUDE.md: The Rules That Actually Matter"
date: "2026-06-07T09:39:59"
modified: "2026-06-08T09:56:44"
slug: "how-i-write-my-claude-md"
original_url: "https://adityarajsingh.com/how-i-write-my-claude-md/"
categories: ["AI Engineering"]
tags: ["Claude"]
excerpt: "CLAUDE.md is the markdown file Claude Code reads before it touches your repo, the standing instructions that ride along in every session (Cursor and Codex call it agents.md, Antigravity calls it gemini.md, same idea). Most people treat it like a wiki and dump everything they know into it. That's the mistake. This post is the […]"
---

# How I Write My CLAUDE.md: The Rules That Actually Matter

CLAUDE.md is the markdown file Claude Code reads before it touches your repo, the standing instructions that ride along in every session (Cursor and Codex call it agents.md, Antigravity calls it gemini.md, same idea). Most people treat it like a wiki and dump everything they know into it. That's the mistake. This post is the handful of rules I actually follow when I write one, and the reasoning behind each, because I learned most of them by getting them wrong first.

Quick confession to set the tone: when I sat down and actually audited my own CLAUDE.md a while back, it was long, and it was stuffed with "NEVER do this" and "Don't ever do that." Turns out that's close to the worst way to write one. Here's what I do now.

## Treat it as context-window real estate, not a wiki

The single idea everything else hangs off: an LLM does its best work on an empty context, and coherence degrades as you fill it. Not when you hit the limit, *before* you hit it. Every line in your CLAUDE.md is a line the model carries through every single turn of every session, competing for attention with the actual code.

So the file isn't free. A 600-line CLAUDE.md doesn't make the agent smarter, it makes it slightly worse at everything, all the time. The question for every line is "is this worth the rent?" Most lines aren't. When I trimmed mine, the output got *more* reliable, not less. That surprised me, and it's the whole reason I rewrote how I think about this file.

## Write rules as "do this," not "never do that"

This is the big one, and it's the mistake I was making. LLMs are noticeably worse at holding onto negative instructions than positive ones. Tell a model "never use inline styles" and some fraction of the time it hears "inline styles." Tell it "put all styling in the stylesheet" and you've pointed it at the behavior you actually want.

So I flip every rule I can from a prohibition into a direction:

``` wp-block-code
Bad:  Never write comments explaining obvious code.
Good: Comment only the non-obvious "why," not the "what."

Bad:  Don't add try/except everywhere.
Good: Let errors surface. Catch only where you have a real recovery path.

Bad:  Never use the old API client.
Good: Use the client in lib/api. It's the only supported one.
```

Same information, but the second column tells the model where to go instead of what to dodge. I keep a few `IMPORTANT:` flags in caps for the genuinely load-bearing ones, that part does work. But the framing is positive by default now.

## Only load-bearing rules earn a spot

Here's the test I run on every line: *would the agent get this wrong without it?* If the model already does the right thing by default, the rule is dead weight, it's just paying rent to repeat what would've happened anyway.

The rules that earn their place are corrections for things that actually went wrong. The agent kept reaching for the deprecated helper, so I added a line pointing at the right one. It kept over-engineering simple functions, so I added "simpler is better, don't reach for a pattern the problem doesn't have." Those are real failures I'm preventing. "Write clean code" is not a rule, it's a wish, and the model can't act on it. Delete the wishes, keep the corrections.

## Give it a goal and a checklist, not vibes

The most useful thing at the top of a CLAUDE.md isn't a coding standard, it's a crisp statement of what the project is and what "done and correct" looks like. A short success checklist the agent can tick off does more than ten style rules, because it tells the model what game it's playing.

``` wp-block-code
## Goal
A small invoicing API. Customers, invoices, payments. JSON over HTTP.

## Definition of done for any change
- Tests pass (pytest).
- New endpoints have at least one test.
- No new dependency without a one-line reason in the PR.
- Migrations are reversible.
```

That block steers more behavior than a wall of preferences ever will.

## Nest the files, general up top, specific deep

CLAUDE.md nests by directory, and this is underused. The root file loads in every session. A CLAUDE.md inside a subfolder loads *only* when the agent works on files in that folder, and the inner file overrides the outer one where they conflict.

So I keep the root file short and genuinely global, the stuff true everywhere. Then the specific, fiddly rules live next to the code they govern:

``` wp-block-code
CLAUDE.md                      # global: goal, done-criteria, house style
  frontend/CLAUDE.md           # loads only when touching frontend/
  services/billing/CLAUDE.md   # the gnarly Stripe rules, where they belong
```

The billing rules don't tax every session, they only show up when the agent is actually in the billing code. General rules stay cheap, specific rules stay close. That's the model worth exploiting on purpose.

## Link out instead of inlining everything

If there's a long doc the agent only sometimes needs, the architecture overview, the deploy runbook, don't paste it into CLAUDE.md. Point at it: "For deployment, read docs/deploy.md." The agent loads it when the task calls for it and ignores it otherwise. You get the information available without paying for it every turn. Inlining a doc you need 5% of the time is the wiki mistake in a different outfit.

## So, do you sweat this file or let it hang?

There are two camps right now. One says sweat the CLAUDE.md, invest in it, prune and rewrite it, stay on top of the context. The other says let it hang out, give the agent skills and loops and let it self-correct toward the goal.

My honest position: sweat it for anything load-bearing, let it hang on throwaway work. A prototype I'll delete next week doesn't need a tuned file, I'll let the agent run. But for code that ships and that I own, a tight, deliberate CLAUDE.md is leverage I'm not giving up. The less the file carries, the more reliably it carries it.

That ties back to something I wrote in <a href="https://adityarajsingh.com/8-stages-of-ai-coding/" class="ek-link">the 8 stages of AI coding</a>: coherence is the scarce resource at every level, tokens, agents, scope. Your CLAUDE.md is just the token-level version of the same fight.

That's the file. Short, positive, load-bearing only, nested, with a clear goal up top. If you go audit yours right now, I'd bet you find the same thing I did: half of it is wishes and "nevers" that are quietly making the agent dumber. Cut those first.
