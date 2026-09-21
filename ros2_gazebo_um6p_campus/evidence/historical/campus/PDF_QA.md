# Final tutorial PDF quality record

14 September 2026. PASS. Final PDF: tutorial/tutorial.pdf; SHA-256 `2db9c642e490c8ac71858c666e857c22b06b74b08ffa34fb1aaa6d1e2e0fd5a7`.

Compiled with Tectonic 0.17.0 from the delivered tutorial.tex, chapters.tex and listings.tex; listings import 39 actual maintained files. Final compile log: tutorial-compile.log. The 34-page PDF was rendered with Poppler at 95 dpi. Every final page (1-34) was visually inspected in nine contact sheets after the last compilation. Checked page numbering, contents, prose, tables, code wrapping, margins, references and actual Gazebo figure. No clipped code, overlapping text, broken glyphs or unreadable figures observed. No Overfull or undefined-reference warning appears in the final compiler log. Underfull table-cell spacing warnings remain and were visually checked; they do not clip text.

Earlier draft inspection found a sparse contents continuation, table break and overflowing prose; these were corrected before the final compile and full review. Page images/contact sheets are disposable QA files in tutorial/qa-final and excluded from the distribution.

The figure is the actual final Gazebo screenshot, copied byte-for-byte from evidence/gui/2026-09-14T14:14:41.229415443.png. It is not an illustration or concept rendering. Exact first-party LaTeX and its figure asset are included. TeX packages remain installation-time mutable dependencies, as documented.
