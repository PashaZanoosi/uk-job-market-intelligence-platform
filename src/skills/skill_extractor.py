# =====================================================
# skill_extractor.py
# Groq AI Skill Extraction Module
# =====================================================


import os
import json
import time


from dotenv import load_dotenv
from groq import Groq



# =====================================================
# Environment
# =====================================================

load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)



# =====================================================
# Configuration
# =====================================================

MODEL_NAME = "llama-3.1-8b-instant"

TEMPERATURE = 0

BATCH_SIZE = 10

MAX_DESCRIPTION_LENGTH = 3000

MAX_RETRIES = 3

RETRY_DELAY = 60



# =====================================================
# Final Skill Structure
# =====================================================

SKILL_TYPES = [

    "Technical Skill",

    "Tool / System Skill",

    "Analytical Skill",

    "Operational Skill",

    "Business Skill",

    "Management Skill",

    "ُSoft Skill",

    "Domain Skill",

    "Compliance Skill",

    "Language Skill"

]



SKILL_CATEGORIES = [

    "Data, Analytics & AI",

    "Software & IT",

    "Engineering & Technical",

    "Science & Research",

    "Finance & Accounting",

    "Sales, Marketing & Commercial",

    "Customer & Service",

    "Operations & Supply Chain",

    "Manufacturing & Production",

    "Healthcare & Care",

    "Hospitality & Food Service",

    "Construction & Trades",

    "Education & Training",

    "Administration & Office",

    "Leadership & People",

    "Legal & Compliance",

    "Personal Effectiveness",

    "Languages",

    "Other"

]



# =====================================================
# Helpers
# =====================================================

def chunk_list(
    items,
    size
):

    for i in range(
        0,
        len(items),
        size
    ):

        yield items[i:i + size]



def clean_json_response(
    content
):

    content = content.strip()


    if content.startswith("```"):

        content = (

            content

            .replace(
                "```json",
                ""
            )

            .replace(
                "```",
                ""
            )

            .strip()

        )


    return content



# =====================================================
# Prompt
# =====================================================

def build_prompt(jobs):


    job_text = ""


    for job in jobs:


        job_text += f"""

JOB_ID:
{job["job_id"]}


DESCRIPTION:

{job["description"][:MAX_DESCRIPTION_LENGTH]}


----------------------------

"""


    prompt = f"""

You are an expert UK labour market analyst.

Extract professional skills from UK job descriptions.

Your goal is to identify skills that are explicitly mentioned, required, or directly demonstrated through responsibilities.

STRICT EXTRACTION RULES:

Extract a skill only when:

- The skill is explicitly mentioned in the job description.
OR
- The responsibility clearly maps to a recognised professional capability.

Do NOT extract skills based on:

- Job title only
- Seniority level
- Occupation assumptions
- Industry stereotypes
- General workplace expectations

Examples:

"Power BI experience required"
Extract:
Power BI

"SQL knowledge required"
Extract:
SQL

"Works with customers"
Do NOT extract:
Customer Service

"Works as part of a team"
Do NOT extract:
Teamwork


SOFT SKILLS:

Extract soft skills only when explicitly stated.

Examples:

"excellent communication skills"
Extract:
Communication

"strong problem-solving skills"
Extract:
Problem Solving

"must be reliable and punctual"
Extract:
Reliability
Punctuality

Do NOT extract:

"support colleagues"
Teamwork

"deal with customers"
Customer Service

"work in a busy environment"
Time Management


BENEFITS AND NON-SKILLS:

Never extract:

- Salary
- Pension schemes
- Employee benefits
- Holiday entitlement
- Salary sacrifice
- Discounts
- Parking
- Wellbeing support
- Employee Assistance Programme
- Counselling services
- Career progression
- Workplace facilities


SKILL NORMALISATION:

Normalize equivalent skills.

Examples:

"Communication skills" = "Communication"

"Microsoft Packages" = "Microsoft Office"

"Microsoft Excel skills" = "Excel"

Avoid duplicate skills.


SKILL TYPES:

Choose exactly one:

- Technical Skill
- Tool / System Skill
- Analytical Skill
- Operational Skill
- Business Skill
- Management Skill
- Soft Skill
- Domain Skill
- Compliance Skill
- Language Skill


CLASSIFICATION RULES:

Soft Skill:

Use for human behaviour, personal qualities, and interpersonal abilities.

Examples:

Communication
Teamwork
Problem Solving
Reliability
Punctuality
Adaptability
Flexibility
Patience
Creativity
Attention to Detail
Time Management


Tool / System Skill:

Use for software, platforms, applications, and systems.

Examples:

Power BI
Excel
Microsoft Office
AutoCAD
SAP
AWS
React


Technical Skill:

Use for programming languages, technical knowledge, engineering knowledge, and technical methods.

Examples:

SQL
Python
Java
Software Architecture
Engineering
Data Modelling


Database and programming languages:

Always use Technical Skill.

Examples:

SQL
Python
Java
C#


Analytical Skill:

Use only for analytical methods and data-related capabilities.

Examples:

Data Analysis
Forecasting
Statistical Analysis
Financial Modelling

Do NOT classify these as Analytical Skill:

Problem Solving
Decision Making
Judgement

They are Soft Skills.


Management Skill:

Use for managing people or teams.

Examples:

Leadership
Team Management
Performance Management
Recruitment


Business Skill:

Use for commercial and business activities.

Examples:

Sales
Negotiation
Budget Management
Commercial Awareness


Operational Skill:

Use for processes and operational responsibilities.

Examples:

Stock Control
Scheduling
Project Management


Compliance Skill:

Use for regulations, legal requirements, mandatory checks, and compliance certifications.

Examples:

DBS Check
COSHH
GDPR


Domain Skill:

Use for industry-specific knowledge.

Examples:

Neurosurgery
Healthcare
Hospitality
Social Care


Language Skill:

Use for spoken or written languages.

Examples:

English
German
French


SKILL CATEGORIES:

Choose exactly one:

Data, Analytics & AI
Software & IT
Engineering & Technical
Science & Research
Finance & Accounting
Sales, Marketing & Commercial
Customer & Service
Operations & Supply Chain
Manufacturing & Production
Healthcare & Care
Hospitality & Food Service
Construction & Trades
Education & Training
Administration & Office
Leadership & People
Legal & Compliance
Personal Effectiveness
Languages
Other


CATEGORY RULES:

Soft Skills:
→ Personal Effectiveness

Languages:
→ Languages

SQL:
→ Data, Analytics & AI

Power BI:
→ Data, Analytics & AI

Microsoft Office:
→ Software & IT

DBS Check:
→ Legal & Compliance

Food Safety:
→ Hospitality & Food Service


Never create new categories.

Never output:

None
Unknown
N/A


OUTPUT RULES:

Return JSON only.

Every extracted skill must contain:

- skill_name
- skill_type
- skill_category

Output format:

{{
    "jobs":[
        {{
            "job_id":"123",
            "skills":[
                {{
                "skill_name":"SQL",
                "skill_type":"Technical Skill",
                "skill_category":"Data, Analytics & AI"
                }}
            ]
        }}
    ]
}}


Jobs:

{job_text}

"""


    return prompt



# =====================================================
# Groq Extraction
# =====================================================

def extract_skills_batch(
    jobs
):


    prompt = build_prompt(
        jobs
    )



    response = client.chat.completions.create(

        model=MODEL_NAME,

        messages=[

            {
                "role":"system",
                "content":prompt
            }

        ],

        temperature=TEMPERATURE,

        response_format={
            "type":"json_object"
        }

    )


    content = clean_json_response(

        response
        .choices[0]
        .message
        .content

    )


    return json.loads(
        content
    )



# =====================================================
# Retry Wrapper
# =====================================================

def extract_with_retry(
    jobs
):


    for attempt in range(
        1,
        MAX_RETRIES + 1
    ):


        try:

            print(
                f"Groq attempt {attempt}/{MAX_RETRIES}"
            )


            return extract_skills_batch(
                jobs
            )


        except Exception as e:


            print(
                "Groq error:",
                e
            )


            if attempt < MAX_RETRIES:

                time.sleep(
                    RETRY_DELAY
                )


            else:

                raise



# =====================================================
# Main Interface
# =====================================================

def extract_skills(
    jobs
):


    results = {

        "jobs":[]

    }



    batches = list(

        chunk_list(

            jobs,

            BATCH_SIZE

        )

    )


    for index, batch in enumerate(
        batches,
        start=1
    ):


        print(
            f"Processing batch {index}/{len(batches)}"
        )


        batch_result = extract_with_retry(

            batch

        )


        results["jobs"].extend(

            batch_result.get(
                "jobs",
                []
            )

        )


    return results