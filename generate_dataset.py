import csv
import random
import textwrap

TOTAL = 150
DISTRIBUTION = {
    "normal": 80,
    "spam": 40,
    "high_priority": 30,
}

# Word pools for subject generation
SUBJECT_STARTS = [
    "Meeting",
    "Update",
    "Reminder",
    "Invitation",
    "Report",
    "Request",
    "Follow-up",
    "Proposal",
    "Notes",
    "Action",
    "Status",
    "Summary",
    "Question",
    "Schedule",
    "Confirmation",
]

SUBJECT_VERBS = [
    "about",
    "for",
    "regarding",
    "on",
    "due",
    "about the",
]

SUBJECT_OBJECTS = [
    "project timeline",
    "next steps",
    "your feedback",
    "the budget",
    "team assignments",
    "the deadline",
    "deliverables",
    "the quarterly plan",
    "the report",
    "invoice",
]

# Sentence fragments to build email bodies
NORMAL_SENTENCES = [
    "I wanted to share a brief update on the current status.",
    "Please find the attached notes from our last call.",
    "Let me know if you have any questions about the plan.",
    "I will follow up with the team later this week.",
    "We completed the first phase and are moving forward.",
    "The document includes suggested changes and next steps.",
    "Thanks for your input on this matter.",
    "I scheduled a short meeting to review progress.",
    "This is a quick heads-up on the timeline change.",
]

SPAM_SENTENCES = [
    "Congratulations! You have been selected to claim your prize.",
    "Limited time offer — act now to receive an exclusive discount.",
    "Click the link below to verify your account and unlock rewards.",
    "Earn money from home with this simple trick.",
    "This is not a scam — instant approval with no credit check.",
    "You are pre-approved for a special loan offer today.",
    "Lowest prices guaranteed — buy now before stock runs out.",
    "Claim your free gift card by entering your details.",
]

PHISHING_SENTENCES = [
    "Your account will be locked unless you confirm your credentials.",
    "Please provide your login details to avoid service interruption.",
    "Verify your payment information immediately to prevent suspension.",
    "We noticed unusual activity — reset your password now.",
]

HIGH_PRIORITY_SENTENCES = [
    "This requires your immediate attention and a response today.",
    "Deadline is tomorrow and the deliverable must be signed off.",
    "Escalate this to management if you cannot resolve it by end of day.",
    "Payment is overdue — please process the invoice immediately.",
    "This task impacts the launch date and cannot be delayed.",
    "We need the final figures to complete the audit by Friday.",
    "Please prioritize this action and confirm once done.",
]

# Helper functions

def make_subject(label):
    # Subjects should be short sentences (3-7 words)
    if label == "spam":
        starts = [
            "Act now",
            "Limited offer",
            "You won",
            "Special Promotion",
            "Claim your prize",
            "Exclusive deal",
        ]
        subj = random.choice(starts)
        # Randomly add a short tail
        tail = random.choice(["today", "— limited time", "for you", "now", "while supplies last"]) 
        return f"{subj} {tail}".strip()

    if label == "high_priority":
        subj = random.choice([
            "Urgent: action required",
            "Immediate attention needed",
            "Deadline approaching",
            "Payment overdue",
            "Escalation: response needed",
            "Critical update required",
        ])
        return subj

    # normal
    start = random.choice(SUBJECT_STARTS)
    verb = random.choice(SUBJECT_VERBS)
    obj = random.choice(SUBJECT_OBJECTS)
    # keep it short
    subject = f"{start} {verb} {obj}"
    # Trim to 3-7 words: if too long, shorten
    words = subject.split()
    if len(words) > 7:
        subject = " ".join(words[:6])
    return subject


def make_sentence_pool(label):
    if label == "spam":
        # mix spam and phishing fragments to keep it spammy/promotional
        return SPAM_SENTENCES + PHISHING_SENTENCES
    if label == "high_priority":
        return HIGH_PRIORITY_SENTENCES
    return NORMAL_SENTENCES


def make_body(label):
    pool = make_sentence_pool(label)
    # Bodies must be 2–5 sentences
    count = random.randint(2, 5)
    sentences = []
    for _ in range(count):
        s = random.choice(pool)
        # Small chance to append a normal connective to make it more natural for normal emails
        if label == "normal" and random.random() < 0.3:
            s = s.rstrip('.') + '. '
        sentences.append(s)
    # Join and ensure whitespace tidy
    body = " ".join(sentences)
    # Wrap long body but preserve sentences
    return textwrap.fill(body, width=100)


def generate_rows():
    rows = []
    for label, count in DISTRIBUTION.items():
        for _ in range(count):
            subj = make_subject(label)
            body = make_body(label)
            rows.append({"subject": subj, "body": body, "label": label})
    random.shuffle(rows)
    # If counts don't sum to TOTAL, adjust (defensive)
    if len(rows) != TOTAL:
        # Trim or pad with normal
        while len(rows) < TOTAL:
            rows.append({"subject": make_subject("normal"), "body": make_body("normal"), "label": "normal"})
        if len(rows) > TOTAL:
            rows = rows[:TOTAL]
    return rows


def write_csv(rows, path="emails.csv"):
    with open(path, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["subject", "body", "label"]) 
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


if __name__ == '__main__':
    rows = generate_rows()
    out_path = "emails.csv"
    write_csv(rows, out_path)

    # Print counts
    counts = {"normal": 0, "spam": 0, "high_priority": 0}
    for r in rows:
        counts[r["label"]] = counts.get(r["label"], 0) + 1

    print(f"Wrote {len(rows)} emails to {out_path}")
    print(f"Counts:")
    for k in ["normal", "spam", "high_priority"]:
        print(f"  {k}: {counts.get(k,0)}")
