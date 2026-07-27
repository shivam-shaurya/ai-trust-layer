# TrustShield AI — Presentation

`TrustShield_AI_Presentation.pptx` is a 16-slide deck (problem statement, solution,
architecture, methodology, real evaluation results, honestly-disclosed limitations, and
future work), generated programmatically by `build_deck.py` so every number and claim in
it matches what's actually in the codebase and the paper.

## Regenerating / editing

The deck is code, not a hand-edited file — to change content, edit `build_deck.py` and
re-run it rather than editing the `.pptx` directly (otherwise your edits will be lost the
next time someone regenerates it):

```bash
pip install python-pptx   # not a runtime dependency of the app; only needed here
python presentation/build_deck.py
```

This overwrites `TrustShield_AI_Presentation.pptx` in place.

## Notes

- Every number on the Results slide (slide 11) and the Key Finding slide (slide 12) was
  pulled from the paper (`paper/trustshield_ieee.tex`), which was itself verified by
  running the live pipeline — nothing here is illustrative or invented.
- The architecture diagram (slide 5) intentionally uses a single dashed arrow between the
  Domain Services and Data/External layers rather than per-service arrows, to avoid the
  crossing-line clutter found in an earlier version of the equivalent diagram in the
  paper — the exact per-service mapping is called out in the speaker's own explanation
  in the paper instead.
- I could not visually render this deck in the environment it was built in (no
  PowerPoint or LibreOffice available), so double-check text doesn't overflow any boxes
  before presenting, especially on slides 2, 6, and 9. If anything looks off, the fix is
  almost always a spacing/width tweak in `build_deck.py`, not a from-scratch rebuild.
