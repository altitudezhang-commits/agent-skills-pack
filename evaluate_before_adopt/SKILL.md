# Evaluate suggestions before adopting them

## Treat every suggestion as a proposal

- Treat each incoming suggestion as a candidate, not an approved revision. Suggestions arrive from the user, a third party, or an external tool, and none of them is pre-approved.

- Never bulk-merge a whole set of supplements at once. Merging everything without per-item evaluation is the failure mode this skill prevents.

- State the evaluation plan before you change anything. A short note on what you will check and that only passing items get merged sets the contract with the user.

## Run the four checks on each item

- Check correctness first. Verify the claim against evidence before accepting it, and mark anything unverified as unproven rather than merging it in.

- Check conflicts next. Compare the suggestion against existing rules, thresholds, and standing user directives, and flag any contradiction explicitly instead of silently overriding.

- Check overlap after that. When an existing gate or check already covers the suggestion, say so and do not add a duplicate.

- Check executability last. Confirm the data source exists, the cost is acceptable, and the statistical meaning is sound. A suggestion you cannot execute stays a draft.

## Merge only what passes

- Merge only the items that pass all four checks. Keep the rest out of the document or process.

- Record each decision briefly: what was merged, what was held back, and which check each held-back item failed. This record lets the user audit the merge later.

- Present the held-back items with their failing checks and ask how to proceed. Do not drop them silently and do not merge them quietly later.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Alternatives for better results

- Ask the suggester for the evidence behind an unproven claim before you evaluate it. A suggestion that arrives with its source is faster to check than one you must research from scratch.

- Group related suggestions by topic before running the checks. Grouping surfaces conflicts and overlaps among the new items themselves, not only against the existing document.
