from .scraper import PESURedditScraper
from pprint import pprint
import dotenv
import os

PESU_KEYWORDS = [
    "PESSAT",
    "KCET",
    "COMEDK",
    "Cutoff",
    "Management Quota",
    "Fee Structure",
    "Scholarship",
    "Branches",
    "CSE",
    "AIML",
    "ECE",
    "EEE",
    "ME",
    "BT",
    "BBA",
    "B.Tech",
    "Curriculum",
    "Syllabus",
    "Faculty",
    "CGPA",
    "Ring Road Campus",
    "Electronic City Campus",
    "Hostel",
    "Hostel Rules",
    "Library",
    "Labs",
    "Canteen",
    "Food Court",
    "Wi-Fi",
    "Sports Facilities",
    "Gym",
    "Auditorium",
    "Parking",
    "Location",
    "Infrastructure",
    "Aatmatrisha",
    "Maaya",
    "Clubs",
    "Events",
    "Fests",
    "Attendance",
    "Dress Code",
    "Campus Life",
    "Ragging",
    "Freshers",
    "Hangout Spots",
    "Student crowd",
    "Competitions",
    "Batch",
    "Social Life",
    "ISA",
    "ESA",
    "Grading",
    "Relative Grading",
    "Backlog",
    "Revaluation",
    "Makeup Exam",
    "Assignments",
    "Projects",
    "Flipped Classroom",
    "CIE",
    "Question Papers",
    "Study materials",
    "Academic Pressure",
    "Cheating",
    "Placements",
    "Internship",
    "Highest Package",
    "Average Package",
    "Placement Cell",
    "Companies",
    "Tier 1 Companies",
    "Mass Recruitment",
    "CGPA for placements",
    "Resume",
    "Alumni Network",
    "Higher Studies",
    "GRE/GMAT",
    "Core Company",
    "Startup",
    "PESU",
    "PESIT",
    "Management",
    "Dr. M.R. Doreswamy",
    "Prof. D. Jawahar",
    "HOD",
    "Course Registration",
    "Timetable",
    "Student ID",
    "Mental Health",
    "Grievances",
    "Transcripts",
    "Transport",
    "PESU App",
    "Autonomy",
    "Rankings",
    "VS",
    "Review",
    "Worth it?",
    "Advice"
]

dotenv.load_dotenv()

def print_divider():
    pprint(f"\n\n {'*' * 80} \n\n")

prs = PESURedditScraper(os.getenv("client_id"), os.getenv("client_secret"), os.getenv("user_agent"))

res = prs.scrape(2, PESU_KEYWORDS)
pprint(res)

""" print_divider()

pprint(prs.scrape(3, "new"))
print_divider()

pprint(prs.scrape(3, "top"))
print_divider()

pprint(prs.scrape(3, "rising"))
print_divider()

pprint(prs.scrape(3, "controversial") """