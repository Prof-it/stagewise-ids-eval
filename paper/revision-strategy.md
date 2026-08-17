
# Strategic Revision Plan for "Beyond End-to-End Metrics" (ETECOM Condensation Version)


## 1. Overarching Goal & Reviewer Context

Reviewers acknowledge careful execution and strong experimental protocol, but raise concerns about novelty (metrics not truly new), generality, and scope. This revision’s goal: **reframe the work as a “stage-oriented evaluation protocol” for residual-forward cascaded IDS, explicitly narrowing claims and dramatically condensing the manuscript to ETECOM’s 4–6 page limit, without altering format/spacing.**


## 2. Reviewer Points – Key Actions & Language

A. **Conceptual framing:**
   - Globally rephrase the contribution as a “stage-oriented evaluation protocol” rather than invention of new metrics.
   - Emphasize conceptual/evaluative clarity, not novelty, in the abstract and introduction.
   - Recast CDR, ΔRecall, ΔFPR as *derived evaluation quantities*, not “novel metrics.”

B. **Scope Correction:**
   - Insert a short taxonomy distinguishing “residual/recovery cascades” (this work) vs. “confirmation/refinement cascades.”
   - Explicitly narrow the protocol’s direct applicability to residual-forward cascades; state explicitly that it does not apply to all cascade types.

C. **Empirical Limitation:**
   - Consistently clarify: results are demonstrated on one dataset (CICIDS2017), one hybrid Snort–IF pipeline.
   - Promise generalization (datasets, detectors, cascades) as future work, not a present claim.

D. **Technical/Terminology Refinement:**
   - Clearly distinguish the “1% FPR calibration target” from the observed FPR on the residual set, e.g., in methodology/results.
   - Add a statement on differing denominators for ΔRecall and ΔFPR, using explicit language to aid interpretability.

E. **Positioning:**
   - Reframe throughout: this is a transparent, evidence-driven *protocol*, offering a reproducible template for future study.
   - Address reviewer critiques head-on in main text language.


## 3. Condensation—Concrete Stepwise Actions

**A. Do not change template/class/layout. No margin, font, or spacing adjustments.**

**B. Section Reorganization:**
  1. Introduction – 0.7p (focus: transparency, stage-oriented evaluation protocol)
  2. Related Work – 0.6p (super-compressed, see below)
  3. Methodology – 1.3p
      - 3.1 Stage-oriented evaluation (short, use concise equations)
      - 3.2 Experimental setup (merge dataset, preprocessing, detectors; compress prose)
      - 3.3 Evaluation quantities (CDR, ΔRecall, ΔFPR: 3 eqns, single explanatory paragraph)
  4. Results – 1.5p
      - Key table: main threshold results only
      - Figure: ΔRecall–ΔFPR curve
      - Merge class-level results into single concise table
      - Flow-matching/calibration → text only; remove table; refer to supplement for extra details.
  5. Discussion – 0.8p (compressed: main finding, class effect, methodological implication, limitations; <5 paragraphs)
  6. Conclusion – 0.3p (single paragraph: protocol, main gain, implication, future work)
  7. References – 0.8p

**C. Elimination and fusion steps:**
  - Related Work:
    * Reduce to single (max: two) subsections. Combine hybrid IDS, cascade ML, threshold work, research gap.
    * Use direct, harmonized prose as modeled in detailed plan above.
  - Methodology:
    * Rewrite residual concept as a single paragraph and two equations. Directly connect to Snort + IF.
    * Merge "framework instantiation" and "experiment protocol" into "experimental setup."
    * Stage 1 and Stage 2 = minor sentences inline.
    * Flow-matching implementation: single compressed paragraph (see suggested rewrite).
    * Feature selection: single compressed paragraph; delete feature appendix.
  - Metrics section:
    * Remove extended prose per metric; three equations plus one summary paragraph. No “example calculations” appendix.
  - Tables and Results:
    * Keep main operating-point table, ΔRecall–ΔFPR curve, and a merged class-level table (Attack / Snort Recall / Residual / CDR).
    * Delete more generic results/class tables, merge where possible.
    * Sensitivity analysis: result as text, no dedicated table; relocate detail to supplement.
  - Appendices:
    * Remove numerical and feature appendices entirely.
  - Discussion:
    * Rewrite to eliminate result summary repetition. Focus on what findings mean, not what happened. Include explicit limitations.
  - Conclusion:
    * Shorten to single summarizing paragraph.
  - Preserve credibility:
    * Maintain experimental detail on Snort config, IF training, threshold calibration, random seeds.
    * Minimize explanation, maximize reported evidence.


## 4. Expected Outline (for ETECOM, 4–6 pages)

1. **Abstract** (protocol, limited scope, real benefit, direct reviewer response)
2. **Introduction** (transparency, reproducibility, clear scope, why stage-oriented evaluation matters)
3. **Related Work** (very tight; aggregate-metrics-in-IDS vs. stage-wise-in-cascades)
4. **Methodology** (ultra-compressed theory, setup, metrics; equations as centerpiece)
5. **Results** (main operating point, ΔRecall–ΔFPR, concise class table; all extra in supplement)
6. **Discussion & Limitations** (impact, class dependence, methodology implications, limits—all concise)
7. **Conclusion** (single paragraph)
8. **References**


## 5. Step-By-Step Revision Instructions for Agents

1. **Reframe globally:** Rewrite all references to “novel metrics” as “evaluation quantities.” Say “protocol” not “framework.”
2. **Cut and fuse sections:** Merge and compress as detailed above. Move/minimize technical implementation prose unless it’s directly related to reproduction or credibility.
3. **Tables/figures:** Remove all but essential. If data is needed for reproducibility but not central to the argument, relocate to supplement or GitHub.
4. **Prose:** Each paragraph should justify its presence—combine/summarize wherever possible. Prioritize brevity, especially where equations speak for themselves.
5. **Direct reviewer engagement:** Visibly address reviewer critiques inside the main text (e.g., “As noted by Reviewer 2, …” or “To clarify observed FPR and calibration targets, …”).
6. **Limitations:** Move, highlight, or condense as needed; make sure limitations are unmissable.
7. **Experimental details:** Don’t cut details around tools/versions/calibration/randomization that make results credible—only compress explanation.
8. **Final check:** Before reducing layout, verify actual post-condensation page count and only adjust formatting if absolutely required, never as a first step.

---
**This updated strategy transforms your detailed plan into agent-ready instructions—stepwise, actionable, and tied to explicit ETECOM-appropriate manuscript structure.**