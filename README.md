# The World Today — Saturday 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/cgxaltarm/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/cgxaltarm/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A make.fun bounty entry: one image that sums up the world's news of
Saturday 21 November 2026 — a newspaper front page, 33 stories, drawn
with Pillow (flat vector-style drawing, no external images).

## The day

- **Lead:** COP31 climate talks in Antalya run into overtime but near a
  final deal; Iran strikes Bahrain; Mexico captures cartel boss
  "El Chapo Isidro", at least 11 dead.
- **War & conflict:** a Russian missile hits Kryvyi Rih, killing a boy
  of 7 and a paramedic; drones set the Russian cargo ship Sparta II
  ablaze in the Gulf of Finland; two tankers hit near Hormuz; missiles
  over Riyadh intercepted; three killed in a Gaza food vehicle.
- **Politics:** Trump, Xi and Putin meet in Shenzhen and open nuclear
  risk-reduction talks; the EU and Indonesia sign a trade deal after
  ten years; France seeks UN action on Myanmar.
- **Markets:** the Nasdaq erases its 2026 gains as the AI sell-off turns
  into a correction; Anthropic's record IPO stumbles on day two.
- **Science & health:** specially bred mosquitoes cut dengue infections
  in children by about 69% in a Brazil study; an Anthropic researcher
  says AI helped prove the Riemann hypothesis.
- **Sport & culture:** England beat New Zealand 37-12 in rugby; India
  pile up 720/9 in New Zealand; the Dak'Art Biennale opens in Dakar.

## The program

`main.py` (Python 3, standard library only) copies `entry.png` from
the repository root to `/output/entry.png`, where the gate reads it.
Run it outside the grader with:

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The front page is drawn at build time by `work/frontpage_21nov.py`
(Pillow). To regenerate the image, run that script from `work/` —
it writes `entry.png` (1024x1024, under 1 MiB) next to itself.
