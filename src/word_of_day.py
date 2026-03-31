"""
word_of_day.py — Daily vocabulary builder.
Rotates a curated list of power words — no API needed.
"""

from datetime import date


WORDS = [
    ("Serendipity",    "noun",  "The occurrence of fortunate events by accident.",
     "His discovery of the cure was pure serendipity."),
    ("Ephemeral",      "adj",   "Lasting for a very short time.",
     "Fame is ephemeral; character is forever."),
    ("Perspicacious",  "adj",   "Having a ready insight; shrewd.",
     "A perspicacious investor sees opportunity where others see risk."),
    ("Sanguine",       "adj",   "Optimistic, especially in difficult situations.",
     "She remained sanguine despite the project delays."),
    ("Tenacious",      "adj",   "Holding firmly to purpose; persistent.",
     "His tenacious work ethic made him irreplaceable."),
    ("Laconic",        "adj",   "Using few words; brief and concise.",
     "His laconic reply — 'No.' — ended the debate immediately."),
    ("Sagacious",      "adj",   "Having good judgement; wise.",
     "The sagacious mentor gave advice that changed his career."),
    ("Equanimity",     "noun",  "Mental calmness under pressure.",
     "She handled the crisis with remarkable equanimity."),
    ("Propitious",     "adj",   "Giving or indicating a good chance of success.",
     "This is a propitious moment to launch the product."),
    ("Acumen",         "noun",  "The ability to make good decisions quickly.",
     "His business acumen turned a startup into a unicorn."),
    ("Cogent",         "adj",   "Clear, logical and convincing.",
     "She presented a cogent argument that convinced the panel."),
    ("Diligent",       "adj",   "Having or showing care in one's work.",
     "Diligent practice separates good from great."),
    ("Audacious",      "adj",   "Showing willingness to take bold risks.",
     "An audacious vision backed by relentless execution wins."),
    ("Pragmatic",      "adj",   "Dealing with things sensibly and realistically.",
     "A pragmatic approach beats endless theorising."),
    ("Resilient",      "adj",   "Able to recover quickly from difficulties.",
     "Resilient systems — and people — adapt and survive."),
    ("Eloquent",       "adj",   "Fluent or persuasive in speaking or writing.",
     "His eloquent pitch secured the funding in 10 minutes."),
    ("Fastidious",     "adj",   "Very attentive to detail; hard to please.",
     "A fastidious code reviewer catches bugs others miss."),
    ("Inquisitive",    "adj",   "Curious; eager to learn.",
     "Stay inquisitive — curiosity is the engine of innovation."),
    ("Meticulous",     "adj",   "Showing great attention to detail.",
     "Meticulous documentation saves hours of future debugging."),
    ("Prolific",       "adj",   "Present in large numbers; highly productive.",
     "Prolific builders ship 10x more than those who wait for perfect."),
    ("Resolute",       "adj",   "Admirably purposeful, determined.",
     "Be resolute in your goals but flexible in your methods."),
    ("Succinct",       "adj",   "Briefly and clearly expressed.",
     "A succinct email gets replies faster than a long one."),
    ("Versatile",      "adj",   "Able to adapt to many functions.",
     "A versatile developer is always in demand."),
    ("Zenith",         "noun",  "The highest point reached; peak.",
     "He was at the zenith of his career at just 28."),
    ("Ardent",         "adj",   "Enthusiastic or passionate.",
     "An ardent love for code drives true craftsmanship."),
    ("Catalyst",       "noun",  "A person or thing that causes change.",
     "That internship was the catalyst for his entire career."),
    ("Deft",           "adj",   "Neatly skillful and quick.",
     "Her deft handling of the client's concerns saved the deal."),
    ("Formidable",     "adj",   "inspiring respect through being impressively strong.",
     "Consistent effort makes you a formidable competitor."),
    ("Grit",           "noun",  "Courage and resolve; strength of character.",
     "Talent is common. Grit is rare."),
    ("Heuristic",      "noun",  "A practical approach that is not guaranteed to be perfect.",
     "A good heuristic beats paralysis by analysis every time."),
]


def get_word_of_day() -> str:
    """Returns today's word of the day — deterministic, rotates daily."""
    idx = date.today().timetuple().tm_yday % len(WORDS)
    word, pos, definition, example = WORDS[idx]
    return (
        f"📚 *Word of the Day*\n"
        f"  *{word}* _({pos})_\n"
        f"  _{definition}_\n"
        f"  📝 \"{example}\""
    )
