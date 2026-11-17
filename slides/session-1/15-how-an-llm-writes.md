<!-- layout: statement | where: app -->
<p class="kicker">Part 1 · The LLM</p>

# An LLM continues text with what's likely.

<div class="cols" markdown="1">
<div markdown="1">

> Finish the sentence: **"A house has walls, a floor, and a …"**
>
> And this one: **"Form follows …"**
>
> Now: **who first wrote that sentence?**

</div>
<div data-widget="figure" data-name="next-word"></div>
</div>

<!-- notes -->
**The idea.** An **LLM** (large language model) is the AI inside Claude. It learned from an enormous amount of text. When it writes, it continues what's there with what is *likely* to come next. At every step it weighs many possible next words, and picks one of the likely ones, with a little randomness. That is why the same question can get slightly different answers. The bars sketch it: for each sentence, a few possible next words, each with a weight. The numbers are made up to show the shape; real ones vary by model. The shape is the point: after "Form follows", one word wins almost every time.

You did the same thing in class, whether or not you were the one asked. Nobody had to *think* to finish "a house has walls, a floor, and a roof" or "form follows function": you've seen those words together so often that the ending arrives by itself. Then comes the question of who first wrote it. Many people guess Le Corbusier, Mies van der Rohe or the Bauhaus, because the line sounds like Modernism. It was the American architect Louis Sullivan, in 1896, in an essay on the tall office building. The likely answer and the true answer were different, and the likely one felt just as certain.

**Why it matters.** Most of the time, likely and true are the same, which is why LLMs are so useful. But the answer comes out the same way, with the same confidence, either way. So the question is never "does it sound sure?" but "where did this come from, and how could I check it?" The rest of Part 1 is about the parts you add so that you *can* check. The next slide shows how it writes a whole answer this way: one small piece at a time.

**A word you'll hear.** When an LLM writes something likely but false, people call it a **hallucination**. The word makes it sound like a fault that could be fixed. It isn't: the false answer was written the same way as the true ones. In this course we say it plainly: likely isn't the same as true.

**Try it yourself.** In Chat, ask for a detail you know well about a building you know well. Then ask for something more obscure about it, such as the exact height of a room. Notice that the tone doesn't change.
