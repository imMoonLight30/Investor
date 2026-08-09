from investor.skills.base import Skill


def built_in_skills() -> tuple[Skill, ...]:
    return (
        Skill(
            name="source-quality",
            description="Evaluate the authority, freshness, and independence of evidence.",
            instructions=(
                "For every material claim, identify its source, publication date when known, "
                "and whether another independent source corroborates it. Clearly label inference."
            ),
        ),
        Skill(
            name="investment-research",
            description="Structure company research without presenting it as financial advice.",
            instructions=(
                "Assess the business model, industry, durable advantages, management, financial "
                "quality, valuation assumptions, risks, and disconfirming evidence. Separate facts "
                "from judgments and never promise returns."
            ),
        ),
        Skill(
            name="research-synthesis",
            description="Synthesize evidence into a concise, traceable report.",
            instructions=(
                "Lead with the answer, cite evidence identifiers, preserve material disagreement, "
                "state uncertainty, and list unanswered questions."
            ),
        ),
        Skill(
            name="graham-principles",
            description=(
                "Teach and apply Benjamin Graham's six timeless investing mistakes and his "
                "core investment discipline."
            ),
            instructions=(
                "Ground every answer in Benjamin Graham's investment philosophy and explicitly "
                "check the situation against his six classic mistakes:\n"
                "1. Confusing speculation with investing - require thorough analysis, safety of "
                "principal, and an adequate return before calling something an investment; keep "
                "speculation, if any, to a small separate account.\n"
                "2. Letting Mr. Market control emotions - treat daily price quotes as an offer "
                "from a moody counterparty, not a verdict on business value; the market is a "
                "voting machine short term and a weighing machine long term.\n"
                "3. Following the crowd - flag momentum-driven popularity, historic-high prices, "
                "low dividend yields, heavy leverage, and weak new issues as bubble warning signs; "
                "always ask what the business is really worth versus what is being paid.\n"
                "4. Overpaying for quality - separate business fundamentals from market "
                "expectations; a wonderful business at too high a price can still destroy "
                "capital.\n"
                "5. Ignoring diversification - avoid concentrated bets; favor 10-30 positions "
                "spread across industries, and note when a plan lacks diversification.\n"
                "6. Forgetting the margin of safety - insist on a cushion between estimated "
                "intrinsic value and price paid, since analysis and forecasts are always "
                "imperfect.\n"
                "Distinguish the defensive investor path (simple, diversified, passive) from the "
                "enterprising investor path (active research, undervalued situations, higher time "
                "commitment). Never promise returns, never give personalized financial advice, and "
                "always state this is education, not a recommendation to buy or sell."
            ),
        ),
    )
