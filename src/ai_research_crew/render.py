from ai_research_crew.models import VerifiedReport


def render_markdown(report: VerifiedReport, topic: str) -> str:
    lines = [
        f"# Research Report: {topic}",
        "",
        "## Executive Summary",
        report.executive_summary,
        "",
        "## Key Findings",
    ]
    for kf in report.key_findings:
        lines.append(f"- {kf.text} ([source]({kf.source_url}))")

    if report.unverified_claims:
        lines += ["", "## ⚠️ Flagged / Unverified Claims",
                  "_These findings could not be confidently traced back to a source and should be treated with caution:_", ""]
        for claim in report.unverified_claims:
            lines.append(f"- {claim}")

    lines += ["", "## Future Outlook", report.future_outlook, "", "## Sources"]
    for src in report.sources:
        lines.append(f"- {src}")

    return "\n".join(lines)
