import pandas as pd


DOMAINS = [
    "Communication",
    "Social Interaction",
    "Sensory",
    "Routine",
    "Behavior",
    "Daily Activity",
]


def calculate_domain_counts(df):
    """
    Count observations for each domain.
    """

    counts = {
        domain: 0
        for domain in DOMAINS
    }

    if df.empty:
        return counts

    for _, row in df.iterrows():

        domains = row.get("domains", "")

        if pd.isna(domains):
            continue

        for domain in str(domains).split("|"):

            domain = domain.strip()

            if domain in counts:
                counts[domain] += 1

    return counts


def calculate_baseline(df):
    """
    Calculate historical domain counts.
    """

    if df.empty:
        return {
            domain: 0
            for domain in DOMAINS
        }

    return calculate_domain_counts(df)


def calculate_recent(df, days=7):
    """
    Calculate domain counts in the most recent period.
    """

    if df.empty:
        return {
            domain: 0
            for domain in DOMAINS
        }

    data = df.copy()

    data["date"] = pd.to_datetime(
        data["date"],
        errors="coerce"
    )

    latest_date = data["date"].max()

    if pd.isna(latest_date):
        return calculate_domain_counts(data)

    start_date = latest_date - pd.Timedelta(days=days)

    recent = data[
        data["date"] >= start_date
    ]

    return calculate_domain_counts(recent)


def calculate_context_patterns(df):
    """
    Identify observation counts by context and domain.
    """

    patterns = []

    if df.empty:
        return patterns

    for _, row in df.iterrows():

        context = row.get(
            "context",
            "Not specified"
        )

        domains = row.get(
            "domains",
            ""
        )

        if pd.isna(domains):
            continue

        for domain in str(domains).split("|"):

            domain = domain.strip()

            if domain:
                patterns.append({
                    "context": context,
                    "domain": domain
                })

    if not patterns:
        return []

    pattern_df = pd.DataFrame(patterns)

    grouped = (
        pattern_df
        .groupby(["context", "domain"])
        .size()
        .reset_index(name="count")
    )

    return grouped.to_dict(
        orient="records"
    )


def build_analytics_data(df):
    """
    Prepare analytics information for AI trend summarization.
    """

    baseline = calculate_baseline(df)

    recent = calculate_recent(df)

    context_patterns = calculate_context_patterns(df)

    return {
        "baseline": baseline,
        "recent": recent,
        "context_patterns": context_patterns,
    }
