<!-- layout: diagram | where: app -->
<p class="kicker">Groundwork</p>

# Same model. Chat talks, Code acts.

<div data-widget="figure" data-name="tabs"></div>

> Demo, the same sentence in both tabs: **"Make a file called hello.md that says hello."** Where does the file end up?

<!-- notes -->
In the demo, the same sentence went to the same model in both tabs and gave different results. Chat showed you the file's text, or offered a download. Chat can run small calculations and make files, but it does so in its own workspace on the provider's computers, so nothing on your computer changes. Code asked for permission, and then the file was in your folder.

The difference is what each tab connects the model to. In Code, Claude works inside the folder you opened, alongside your files and tools. Everything it does there goes through the app, and the app asks you first about anything you haven't already allowed. Those "Allow?" dialogs are **permission prompts**. Read them before you click, since each one says exactly which command or file change is about to happen.

The folder you open works a bit like giving a contractor the keys to one room rather than the whole building. It isn't a sealed room, though. With your permission Claude can reach beyond it, for instance to fetch a web page, which is one more reason to read the prompts.

Once you have your own folder, ask the Code tab to make a file, then find it in File Explorer or Finder.
