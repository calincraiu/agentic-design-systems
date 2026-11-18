<!-- layout: stage | where: chat -->
<p class="kicker">Part 1 · The LLM</p>

# Can an LLM be fair?

> In the Chat tab, start a **new conversation** and ask: **"Six of us need a presentation order. Pick who goes first, fairly: Aalto, Bo Bardi, Mies, Pei, Siza, Wang Shu. Just the name."** Call out the name.

<div data-widget="llm-vs-tool" data-options="Aalto,Bo Bardi,Mies,Pei,Siza,Wang Shu"></div>

<!-- notes -->
"Fair" here means each of the six names has the same chance of being picked. Everyone asked in a separate new conversation, so the room's answers work like asking the same model many times, provided everyone used the same model with memory off. If it were fair, the bars would sit roughly level with the dashed line.

Usually they don't. The model has some randomness built in, which is why the answers varied. But that randomness is weighted toward likely answers, and some names are more likely than others: the first on the list, the best known, or the one that sounds like a natural pick.

The dice tool rolled as many times as there were answers, and its bars aren't level either. With thirty or so rolls they never are. To tell the two apart, run them again. The tool's tallest bar moves to a different name each time, while the LLM's tends to stay on the same one or two. An uneven result that keeps coming back is a **bias**. One that changes every time is just sampling noise.

Crit order, a competition draw, a random sample of sites to survey: when fairness matters, use a method that is fair because of how it works.

To see the lean for yourself, ask Chat the question in ten new conversations and keep a tally.
