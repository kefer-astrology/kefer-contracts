# Kefer Astrology Individual Contributor Agreement — DRAFT

> **Status: draft for legal review. Not in effect. Do not sign.**
> Prepared to identify the permissions the Kefer Astrology nonprofit needs.
> Jurisdiction-specific points are marked **[COUNSEL]**.

## Why an agreement is needed

| Goal | Without agreement | With agreement |
|---|---|---|
| Use public MIT contributions in public repos | Works (inbound = outbound MIT) | Same |
| Use public contributions inside **private/proprietary** modules | MIT already permits this, with notice preservation | Same, plus clear provenance warranties |
| Relicense a repository later (e.g. AGPL → MIT, or dual licensing) | Needs consent of **every** copyright holder | The nonprofit may relicense |
| Enforce rights, register, license commercially | Only individual authors can | The nonprofit holds an exclusive, sublicensable license |
| Contributions to **private** repositories (schools, interpretations, research, graphics) | Ownership unclear | Covered by the exclusive license or a work-for-hire/employment contract |

## Proposed model

1. **Public MIT repositories** (`tauri-application`, `kefer-contracts`, and
   `function-wrapper` once relicensed): DCO sign-off (`Signed-off-by:`) on
   every commit + inbound = outbound MIT. Low friction; sufficient because MIT
   already allows proprietary reuse.
2. **Private repositories and core maintainers**: this agreement (exclusive
   license), or an employment / service contract with an IP clause.

## Draft terms

1. **Definitions.** "Nonprofit" means the Kefer Astrology legal entity
   **[COUNSEL: exact name, registration]**. "Contribution" means any work
   submitted by You to a Kefer repository, issue tracker or design file.
2. **License grant.** You grant the Nonprofit a perpetual, worldwide,
   royalty-free, irrevocable, **exclusive** (for private repositories) or
   **non-exclusive** (for public repositories) license to use, reproduce,
   modify, distribute, sublicense and relicense Your Contributions under any
   terms, including proprietary terms.
   **[COUNSEL: under the Czech Copyright Act (121/2000 Coll.) an author's
   economic rights are not transferable inter vivos — an exclusive license
   with the right to sublicense and assign the license is the usual
   equivalent of an assignment. Confirm form, scope and remuneration clauses
   (§ 2358 et seq. Civil Code).]**
3. **Patent license.** A perpetual, worldwide, royalty-free patent license
   for claims necessarily infringed by Your Contribution.
4. **Moral rights.** You consent to modification and to publication without
   attribution where the Nonprofit deems it necessary.
   **[COUNSEL: moral rights are inalienable in many jurisdictions; draft as
   consent, not waiver.]**
5. **Your representations.** The Contribution is Your original work, or You
   identify third-party material and its license; Your employer has waived or
   does not hold rights in it; You disclose material generated with AI tools.
6. **Third-party and restricted material.** You will not submit material
   whose license is incompatible with the target repository (e.g. GPL/AGPL
   code into MIT repositories; Swiss Ephemeris code or data; texts such as the
   Sabian symbols without clearance).
7. **No obligation.** The Nonprofit is not required to use a Contribution.
8. **Governing law.** **[COUNSEL]**

## Existing contributions that need written permission

See `PHASE1_READINESS.md` (workspace root) for the audit. In short: the
principal author's grant to the Nonprofit; a courtesy relicensing consent from
the 2023 prototype author for `function-wrapper`; confirmation that no
employer holds rights; and a policy for AI-assisted commits.
