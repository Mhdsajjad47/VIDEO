"""Topic agent for AI video factory."""

from __future__ import annotations


def get_topics() -> list[str]:
    """Return a curated list of education and career topics."""
    return [
        "BBA Aviation career scope",
        "Future of AI jobs",
        "Careers after BCA",
        "Logistics industry growth",
        "How to choose the right college",
        "MBA career options",
        "Engineering vs BCA",
        "Hotel management careers",
        "Data science scope in India",
        "Digital marketing careers",
        "BBA finance career path",
        "Pharmacy career opportunities",
        "Law career guidance",
        "Architecture career scope",
        "Media and journalism careers",
        "BBA HR career scope",
        "Nursing career in India",
        "Fashion design courses",
        "Interior design career",
        "Animation and VFX scope",
        "Cyber security careers",
        "Event management scope",
        "Travel and tourism courses",
        "Sports management careers",
        "Aviation ground staff scope",
        "Paramedical courses scope",
        "Agriculture courses career",
        "Social work career",
        "Library science career",
        "B.Ed teaching career",
        "Best diploma courses after 12th",
        "Study abroad admissions roadmap",
        "Top scholarships for Indian students",
        "Career planning after graduation",
        "How internships boost employability",
    ]


if __name__ == "__main__":
    topics = get_topics()
    print(f"Total topics: {len(topics)}")
    for i, topic in enumerate(topics, start=1):
        print(f"{i:02d}. {topic}")
