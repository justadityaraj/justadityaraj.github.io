---
title: "The 8 Stages of AI Coding: Which One Are You Really On?"
date: "2026-06-06T09:36:55"
modified: "2026-06-08T09:57:19"
slug: "8-stages-of-ai-coding"
original_url: "https://adityarajsingh.com/8-stages-of-ai-coding/"
categories: ["AI Engineering"]
tags: ["Claude"]
excerpt: "There's a ladder for how people actually code with AI, and it has eight rungs, from pasting questions into ChatGPT all the way to agents that run other agents. The model comes from Steve Yegge (\"The Evolution of the Programmer, 2024 to 2026\"), and it's the most useful mental map I've found for this stuff. […]"
---

# The 8 Stages of AI Coding: Which One Are You Really On?

There's a ladder for how people actually code with AI, and it has eight rungs, from pasting questions into ChatGPT all the way to agents that run other agents. The model comes from Steve Yegge ("The Evolution of the Programmer, 2024 to 2026"), and it's the most useful mental map I've found for this stuff. This post walks the eight stages, tells you how to spot which one you're on, and then I'll give you my honest take: where I sit, where I'm headed, and the one stage I'm skipping on purpose.

One thing up front so you don't get confused later. This ladder is about **how many agents you're running and how they're wired together**, the agent-count axis. It is *not* about how much you trust the AI (approve-every-line vs. let-it-rip). That's a separate axis, and I'll cover it in its own post. Plenty of people mash the two together and end up thinking "more autonomy means higher stage." It doesn't. You can be a cautious stage 5 or a reckless stage 2.

Here's the ladder.

## Stage 1: ChatGPT and autocomplete

You ask a chat window a question, copy the answer, paste it into your editor, fix the imports yourself. Or you're on tab-complete, Copilot finishing your lines. The model never touches your repo. *You* are the integration layer, moving code by hand between two windows.

You're here if: your AI lives in a browser tab, or it only completes the line you're already typing.

## Stage 2: IDE sidebar, asks permission

Now the AI is inside your editor: Cursor or Copilot chat in the sidebar. It can read your files and it proposes edits, but it waits. Every change is a diff you approve or reject. Nothing happens without your click.

You're here if: you're approving edits one at a time and it feels safe because of that.

## Stage 3: IDE sidebar, YOLO

Same sidebar, but you've turned the approval gate off. It edits files on its own as part of the conversation. You're still watching, still in one chat thread, but you've stopped clicking "accept" on every line.

You're here if: you trust the sidebar enough to let it write without asking, but it's still one assistant in one panel.

## Stage 4: IDE main window, YOLO with diffs

The agent moves out of the side panel and into the main editor. It changes files across the project on its own, and you review the diffs after the fact instead of before. Still one agent, still inside the IDE, but it's driving now and you're navigating.

You're here if: an agent is making multi-file changes in your editor and you're reviewing the result, not the intent.

## Stage 5: CLI, YOLO, diffs scroll by

You've left the IDE. The agent runs in the terminal (Claude Code, Codex CLI, whatever) and it works fast enough that the diffs scroll past quicker than you can read them. One agent, full autonomy on the task, and you're reading the summary at the end rather than every hunk.

**This is where I live.** Claude Code in a terminal, daily. It's the sweet spot for one person doing real work: fast, scriptable, no IDE overhead, and the model has the whole repo in reach. Most of my day is here.

You're here if: your main coding interface is a CLI agent and you've made peace with not reading every line as it lands.

## Stage 6: Multi-agent CLI, 3 to 5 agents

You run a handful of agents in parallel, one on the backend, one on tests, one reviewing, and you coordinate them. It's still a number a human can hold in their head. You're a lead with a small team, assigning slices and stitching the results.

You're here if: you've got three or four agents going at once and *you* are the one keeping them from stepping on each other.

This is my target. Not because more agents is automatically better. It's because the kind of work I do (features that split cleanly into build / test / review) actually benefits from a few parallel hands, and four is still small enough that I'm the coordinator without it becoming a job in itself.

## Stage 7: 10+ agents, managed by hand

Now you're running ten, twenty, more, and you're still the one wiring them together manually. Routing tasks, resolving conflicts, babysitting context for each one. This is the stage everyone screenshots because it looks impressive. A dashboard of agents, all busy.

You're here if: you're spending more time managing the agents than the agents are saving you.

I'll be blunt: **I'm skipping this one on purpose.** Stage 7 is the glue-work trap. The agents do the coding and you become a full-time air traffic controller, doing the coordination by hand at a scale humans aren't good at. It looks like progress and it feels productive, but most of your effort has quietly moved off the actual problem and onto keeping the swarm from colliding. That's not leverage, that's a second job.

## Stage 8: Agents orchestrate agents

The fix for stage 7's pain isn't more discipline, it's getting out of the loop. At stage 8 you stop managing agents directly and manage the *system* that manages them. A planner spins up workers, a coordinator merges and resolves conflicts, the orchestration that was eating you alive at stage 7 is now code. You set the objective and the topology, the machine handles the traffic.

You're here if: you describe the goal and a system of agents organizes itself to hit it, without you hand-routing each one.

This is the escape hatch. I want to be able to *do* stage 8, to build and run an orchestrated setup when a problem is big enough to need it. But notice what stage 8 actually does: it automates exactly the coordination misery that defines stage 7. So you don't climb through 7 to reach 8. You leapfrog 7 entirely. Six is home, eight is the escape hatch, seven is the thing you jump over.

## So which stage should you be?

Higher isn't better. The right stage is the one that fits the work in front of you, and most good engineers move up and down the ladder during a single week.

- **Learning, or touching unfamiliar code?** Drop to stage 2 or 3. Approve the diffs. You want to actually read what's happening.
- **Doing real solo work in a repo you know?** Stage 5 is the honest answer for most people in 2026. One CLI agent, full speed, you reviewing outcomes.
- **Work that splits into clean parallel tracks?** Stage 6 earns its keep. Just don't add agents for the thrill of it.
- **A genuinely big, parallelizable problem?** That's when you reach for stage 8, and only then. Building orchestration for a task that didn't need it is its own trap.

And here's the part that doesn't change at any rung: **you own the code.** Stage 1 or stage 8, "the agent wrote it" is never an excuse. The whole point of climbing the ladder is to do more, not to care less about what ships. The higher you go, the *more* the discipline matters, because the less of it you're reading line by line.

So: I'm at stage 5, aiming for 6, learning to build 8 for when I need it, and skipping 7 on purpose. Figure out which rung you're actually on, not the one your screenshots suggest, and then ask whether it matches the work. That's the whole game.

That's the map. Also here's <a href="https://adityarajsingh.com/how-i-write-my-claude-md/" class="ek-link">how I write a CLAUDE.md</a> that actually holds up, the IDE-vs-CLI tools compared honestly, and the workflow axis I mentioned at the top. Find your rung first; the rest makes more sense once you have.
