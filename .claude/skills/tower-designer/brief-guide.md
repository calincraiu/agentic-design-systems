# Turning a client card into a structured brief

A client card is written the way clients talk: feelings, stories, a few numbers, contradictions, gaps. A structured brief turns that into something tools can check, **without hiding where each part came from**.

## 1. Sort what the card says

| Kind | Example | Where it goes |
|---|---|---|
| Fact with a number | "a plot of 18 by 18 metres" | `site`, or a constraint with `"source": "card"` |
| Quality (words, feelings) | "I'm afraid of heights" | `qualities`: quote the phrase, write your interpretation, list the parameters it touches |
| Wish to maximise or minimise | "every square metre is money" | `priorities` (most important first) |
| Something missing that matters | how high is the headland? | `open_questions`, with why it matters |
| Something you had to decide | "the keeper lives on the lowest two floors" | `assumptions` |

## 2. Translate qualities into parameters and metrics

There is never one right answer, and that is the point. Write down your reading so it can be questioned. Typical moves:

| The client says… | Might mean… | Parameters | Metrics to watch |
|---|---|---|---|
| "landmark", "visible", "iconic" | height, or a distinctive silhouette | floors, twist, lean | height_m, slenderness |
| "doesn't shout", "calm", "modest" | low twist, no lean, moderate height | twist, lean, floors | slenderness, max_cantilever_m |
| "grounded", "solid", "safe" | wide base, taper below 1 | width, depth, taper | slenderness |
| "light", "air", "views for everyone" | more facade per floor area | width, depth, taper | compactness (higher here is wanted) |
| "efficient", "economical" | compact, regular, little overhang | taper, twist, lean | compactness, envelope_m2, gfa_m2 |
| "the neighbours", "afternoon sun" | limit the shadow | floors, lean, lean_dir | shadow_m2 |
| "dramatic", "overhangs", "defies gravity" | lean, taper above 1 | lean, taper | max_cantilever_m |

## 3. Turn hard limits into constraints

A constraint is `metric`, `op`, `value`, `source`. Use only metrics from `uv run tower params`. Mark each one honestly:
- `"card"`: the client wrote it
- `"client"`: the client said it when you asked
- `"assumed"`: you decided it, and the client could disagree

## 4. Ask before you design

Pick the three open questions whose answers would change the design the most. A question about the headland's height changes everything; a question about door handles changes nothing.

## 5. Spot the contradiction

Most cards contain one, for example "visible from far away" against "afraid of heights". Don't resolve it quietly. Name it in the summary, and let the three variants resolve it in different ways.
