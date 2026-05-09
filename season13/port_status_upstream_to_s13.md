# Upstream Sync Status (from upstream/main)

This file tracks the status of porting/merging changes from the `upstream/main` branch (original HiimFilter repo).

## Status Legend
- [ ] **Pending**: Not yet analyzed or ported.
- [x] **Ported**: Successfully cherry-picked or merged.
- [!] **Ignored**: Intentionally skipped (e.g., CI builds, incompatible logic, or conflicting design).

## Upstream Commits Tracking

- [x] **ac2d2c4** - Limit map mob warnings to MAPTIER<4
- [!] **837593d** - ci: build filters (version 54) (Ignored: Upstream CI specific)
- [x] **61a1d79** - Adjust unique/set star ratings
- [!] **34202e2** - ci: build filters (version 55) (Ignored: Upstream CI specific)
- [x] **ce8d15d** - Merge pull request #762 (fix/maps-warnings-high-tier-scope)
- [x] **de42a01** - S13 res hotfix: t14/t26 Poison 120 -> 75
- [!] **0ca64d4** - ci: build filters (version 56) (Ignored: Upstream CI specific)
- [x] **3d4ebe0** - Merge pull request #763 (update/s13-poison-res-t14-t26)
- [x] **88fbe4b** - Mid-season updates: unid rare tiers, gem filtlvl, boss mat sound, sorc orb
- [!] **7e7462c** - ci: build filters (version 57) (Ignored: Upstream CI specific)
- [x] **a4247a1** - Sorc: extend unid rare staff visibility to FILTLVL<11
- [!] **9fce01f** - ci: build filters (version 58) (Ignored: Upstream CI specific)
- [x] **29094fc** - Merge pull request #765 (update/mid-season-2026-04)
- [x] **882810a** - Crafting: tighten FILTLVL gates, add 4os natural shield rule, exclude pala shields from generic 4os rare
- [!] **33e2993** - ci: build filters (version 59) (Ignored: Upstream CI specific)
- [!] **6f9f697** - Add Vanilla+ Crafting filter; rename variant headers to filter names; drop Closed Beta
- [!] **edea2bf** - ci: build filters (version 60) (Ignored: Upstream CI specific)
- [x] **51ef854** - Merge pull request #766 (update/late-april-2026)
- [x] **10b492e** - Crafting: extend generic crafting unid bases to all crafting filters
- [!] **9bac79c** - ci: build filters (version 61) (Ignored: Upstream CI specific)
- [x] **5f7746d** - Vanilla+: enable formatted charms, mag/rare names, and ID'd mag/rare tooltips
- [!] **cbb9dac** - ci: build filters (version 62) (Ignored: Upstream CI specific)
- [x] **43da270** - Merge pull request #767 (update/late-april-2026)
- [x] **be41d91** - Paladin Crafting: show 4os natural mag/rare paladin shields
- [x] **921e691** - Promote Wraithskin (Diamond Mail) from 0-star to 2-star unique
- [x] **8ee9144** - Add hover tooltip to town gems in Crafting/LLD filter
- [ ] **ed892cd** - Hover tooltips on terminal display rules + small cleanups
- [x] **f3d0c0b** - Currency update: Jah 1.5, Cham 1.5, Zod 3 HR
- [x] **fa3d685** - Uber mat values update
- [x] **8a4f99d** - Show non-eth BotD/Last Wish RW bases at FILTLVL<9
- [ ] **4a70559** - Add filter buckets: per-folder builds, definitions, and READMEs
- [x] **21be22f** - Promote Bloodtree Stump to 4-star unique
- [ ] **798fcd3** - Fix #778: Remove stray comma in charm affix rule
- [ ] **148d5f3** - Auto-generate filter top headers and add filter-bucket tags
- [x] **e07ae62** - Fix #782: Adjust Lazuk Puzzlebox value to 0.5
- [x] **c116506** - Rebalance unique tier ratings
- [ ] **2fb913f** - Rune tier sound tweaks
