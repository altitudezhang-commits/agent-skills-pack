# Check delivered content before offering it again

## Check the delivery ledger first

- Read the daily package status ledger before you select, offer, or deliver any item.

- Match each candidate by title and duration and by any platform posting record, and treat a close match as already delivered.

- Never describe an item as new or never delivered unless the ledger shows no matching delivery.

- If the ledger cannot be found or read, say the delivery history is unverified and do not claim the item is new.

## Replace a duplicate before you offer it

- Drop any candidate that already appears in the ledger, and pick a replacement from items with no delivery record.

- Check the replacement with the same title and duration match before you offer it.

- If you cannot find an undelivered replacement, tell the user the package is short and ask how to proceed instead of reoffering an old item.

## Do not fill an empty inventory with a different format

- Check the inventory for the format the user expects before you offer a daily package.

- If that format has no undelivered item ready, say the inventory is empty and name what is missing instead of offering a different format as a substitute.

- Do not offer an image pack when the video inventory is empty, and do not offer any lower effort filler to keep a daily cadence.

- If the user has said quality matters more than daily posting, treat an empty inventory as a reason to pause the package, not as a reason to fill it.

- Offer to make the missing format, or ask how to proceed, and wait for the user to choose before you produce a substitute.

## Record the outcome and stop after a duplicate

- Record every offered and delivered item in the ledger at once, so the next selection starts from current history.

- If the user reports an item was already published, concede the miss plainly and record that item as delivered before you select anything else.

- If the user flags a second duplicate in the same day, stop that day's package and do not offer another item from the same early pool.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Alternatives for better results

- Build the next day's package from undelivered items only, so selection never starts by scanning old items.

- Keep early published items in a separate delivered section of the ledger, so they cannot be mistaken for the current queue.

- Ask the user to confirm a shortlist only after the ledger check, so confirmation covers freshness as well as content.
