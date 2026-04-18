"""
Run full outreach campaign — sends cold emails to all prospects.
Uses the audit-based outreach for businesses with websites,
and cold template for others.
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.prospect_finder import get_all_prospects
from agent.cold_outreach import send_outreach_campaign, generate_all_outreach_templates


def run_campaign():
    print("=" * 60)
    print("  LAUNCHING FULL OUTREACH CAMPAIGN")
    print("=" * 60)

    # Generate templates first
    print("\n[1/2] Generating email templates...")
    templates = generate_all_outreach_templates()
    print(f"  Generated {len(templates)} templates\n")

    # Load all prospects
    prospects = get_all_prospects()
    total_sent = 0
    total_failed = 0

    # Send to each niche
    print("[2/2] Sending emails...\n")
    for niche_key, niche_prospects in prospects.items():
        if not niche_prospects:
            continue
        print(f"  Niche: {niche_key} ({len(niche_prospects)} prospects)")
        result = send_outreach_campaign(niche_key, niche_prospects)
        total_sent += result["sent"]
        total_failed += result["failed"]
        time.sleep(2)  # Pause between niches

    print("\n" + "=" * 60)
    print(f"  CAMPAIGN COMPLETE")
    print(f"  Sent: {total_sent}")
    print(f"  Failed: {total_failed}")
    print(f"  Total: {total_sent + total_failed}")
    print("=" * 60)


if __name__ == "__main__":
    run_campaign()
