# TrustShield AI — IEEE Paper

`trustshield_ieee.tex` is a complete IEEE conference-format paper (IEEEtran class)
describing the system, methodology, real evaluation results, and honestly-disclosed
limitations discovered during testing.

## Compiling to PDF

No local LaTeX distribution was available in the environment this was written in, so
this hasn't been compiled to PDF yet. Easiest path (no install required):

1. Go to [overleaf.com](https://www.overleaf.com), create a free account.
2. New Project → Upload Project → upload `trustshield_ieee.tex`.
3. Overleaf ships the IEEEtran class by default — just click **Recompile**.

To compile locally instead, install a LaTeX distribution (MiKTeX on Windows, or TeX Live)
and run:

```bash
pdflatex trustshield_ieee.tex
pdflatex trustshield_ieee.tex   # run twice so citation numbers resolve
```

## Content notes

- Every reference in the bibliography is a real, verifiable paper (RAG, SelfCheckGPT,
  calibration, Sentence-BERT, FAISS, OWASP LLM Top 10, Transformer, SQuAD). Nothing
  fabricated or unverifiable was cited.
- All numbers in the Results table were obtained by actually running the live pipeline
  against the current SQuAD-derived corpus, not invented for illustration.
- Section VIII (Discussion and Limitations) reports a genuine finding from testing: the
  composite Retrieval Quality formula under-discriminates for small, single-chunk-per-
  document corpora, and explains why. This is real, not a rhetorical "limitations"
  section filler.
- Only two of the five planned Trust Score signals are implemented (prompt safety,
  retrieval quality); this is stated plainly in the abstract, methodology, and
  discussion rather than implied to be complete.
