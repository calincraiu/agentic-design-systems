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
An **LLM** (large language model) has learned from an enormous amount of text. When it writes, it continues the text so far with something likely to come next. At each step it weighs many possible next words and picks one of the more likely ones, with some randomness, which is why the same question can get slightly different answers. The bars on the slide illustrate this. The numbers are made up and vary between models, but the shape is typical: after "Form follows", one word takes almost all the weight.

You finish those two sentences the same way, from having seen the words together many times. The third question is where likely and true come apart. People often credit the line to Le Corbusier, Mies or the Bauhaus, because it sounds Modernist. Louis Sullivan wrote it, as "form ever follows function", in his 1896 essay *The Tall Office Building Artistically Considered*. The likely answer and the correct one were different, and the likely one felt just as certain.

Most of the time likely and true coincide, which is why LLMs are useful. But a wrong answer is produced the same way as a right one and reads with the same confidence. So the useful question about any answer is where it came from and how you could check it.

You will also hear the word **hallucination** for an answer that is likely but false. The word suggests a malfunction, but nothing in the process went wrong. The model produced a likely answer, and this time the likely answer wasn't true.

In Chat, ask for a detail you know well about a building you know well, then for something more obscure, such as the height of a particular room. Compare the tone of the two answers.
