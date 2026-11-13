# Verify a free offer before counting it

## Check the official terms first

- Read the official pricing or free tier page before you repeat a free claim.

- Record the exact free quota, the expiry date, and whether a card or identity check is required.

- Treat a forwarded post, an aggregator listing, or a signup page headline as an unverified claim until the official page confirms it.

- Distinguish a long term free tier from a free trial and from a credit that needs a payment method first.

- Stop and correct the claim at once when the official page asks for a card, a minimum payment, or identity verification before any free use.

## Prove it with a live call

- Run one real call through the offer before you add it to any pool, roster, or report.

- Count registration alone as not usable, because an account and a key can exist while the service still refuses to serve.

- Treat a payment method required error, a quota exhausted response, or a dead login as a failed acceptance test.

- Mark the offer suspended with the exact blocking step when the live call fails, and do not count it as available while it waits for the user.

- Record the live call result, the model or endpoint used, and the time of the test beside the offer.

## Distinguish egress blockage from a dead service

- When an authenticated call hangs, times out, or returns no response while an unauthenticated call to the same service returns quickly, treat the result as egress blockage and not as a dead key or a dead service.

- Run the control pair on the same endpoint, first without credentials and then with credentials, and record both results with their timings before you draw a conclusion.

- Do not mark a key as dead, a quota as exhausted, or an offer as suspended on an authenticated hang alone, because a blocked egress path charges no quota and proves nothing about the service.

- Mark the offer as egress blocked with the exact failing step, and retry it from a different egress such as the Simular Box or the user Windows machine before you count it as unavailable.

- Remember that this pattern has hit authenticated calls for Fish Audio, Weir, and the JetBrains auth backends, while unauthenticated calls to the same services returned at once.

## Patrol the roster for dead channels

- Check every roster entry against a live call on a regular cycle, and report only when something changed.

- Remove or mark suspended any entry whose quota is exhausted, whose login expired, or whose model vanished from the catalog.

- Never let a scheduled task run as if a channel were live after its last live call failed.

- Check official release pages and changelogs as well as aggregators, forums, and social posts, because official free tiers often appear only in vendor docs.

- Add official release wording to the search terms, such as free tier and now available, alongside wool hunting wording.

## Reconcile a miss the same day

- Review any free offer the user forwards that the pipeline missed, and record why the search missed it.

- Add the missing source or keyword to the patrol on the same day, so the same miss cannot repeat silently.

- Keep a miss visible until its source is added, and do not treat a user forward as proof that the pipeline would have found it.

- Report a counted offer only with its live call proof and its official terms, so the user can see what was verified and what remains untested.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Alternatives for better results

- Use a positive control when a service returns nothing, by testing a known working offer first before you declare a channel dead.

- Ask the user only for the blocking step a live call exposed, such as a card or a verification code, and keep the rest of the work with the agent.

- Keep a separate suspended list, so a blocked offer stays visible for retry without being counted as live.
