from groq import Groq
from dotenv import load_dotenv
import os
import json
from datetime import datetime


# ==========================
# Environment
# ==========================

load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)



# ==========================
# Files
# ==========================

INPUT_FILE = "data/market_insights.json"

RULE_OUTPUT_FILE = "data/market_report_rule_based.md"

AI_OUTPUT_FILE = "data/market_report_ai.md"



# ==========================
# Load Data
# ==========================

def load_insights():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)



# ==========================
# Rule Based Report
# ==========================

def build_rule_based_report(data):


    summary = data["summary"]

    top_skills = data["top_skills"]

    taxonomy = data["taxonomy_demand"]



    report = []


    report.append(
        "# UK Labour Market Intelligence Report\n"
    )


    report.append(
        f"Generated: {datetime.now().strftime('%Y-%m-%d')}\n"
    )



    report.append(
        "## Market Overview\n"
    )


    report.append(
        f"""
The dataset contains {summary['total_skills']} analysed skills
across {summary['total_taxonomies']} labour market taxonomies.

The highest demand skill is:

{summary['highest_demand_skill']}

The highest demand taxonomy is:

{summary['highest_demand_taxonomy']}
"""
    )



    report.append(
        "\n## Top Skills by Job Demand\n"
    )



    for index, skill in enumerate(
        top_skills[:10],
        start=1
    ):


        report.append(
            f"""
{index}. {skill['skill']}

Category: {skill['category']}
Taxonomy: {skill['taxonomy']}
Job demand: {skill['job_demand']} jobs

"""
        )



    report.append(
        "\n## Highest Demand Taxonomies\n"
    )



    for item in taxonomy[:10]:


        report.append(
            f"""
{item['taxonomy']}

Jobs: {item['jobs']}
Skills: {item['skills']}

"""
        )



    report.append(
        "\n## Key Observations\n"
    )


    report.append(
        f"""
- {summary['highest_demand_taxonomy']} shows the highest job demand in the dataset.
- {summary['highest_demand_skill']} is the most frequently requested skill.
- Demand exists across technical, business, domain and soft skill categories.
"""
    )


    return "\n".join(report)



# ==========================
# AI Report Generator
# ==========================

def generate_ai_report(data):


    prompt = f"""

Structure:

# UK Labour Market Intelligence Report

## Executive Summary

## Skill Demand Analysis

## Taxonomy Analysis

## Emerging Skill Clusters

Group related skills into meaningful labour market themes.

## Hiring Insights

Explain employer requirements based only on observed data.

## Strategic Recommendations

Provide recommendations for:
- Job seekers
- Employers
- Training providers

## Data Limitations

Explain dataset scope and limitations.

Rules:

- Always refer to "analysed job postings" or "this dataset".
- Do not claim UK-wide trends.
- Do not infer market growth unless supported by data.
- Avoid unsupported assumptions.
- Use numbers from the dataset.
- Return only markdown.

Dataset:

{json.dumps(data, indent=2)}

"""


    response = client.chat.completions.create(


        model="llama-3.3-70b-versatile",


        messages=[

            {
                "role": "user",
                "content": prompt
            }

        ],


        temperature=0.3

    )



    return response.choices[0].message.content



# ==========================
# Save File
# ==========================

def save_report(content, filename):


    os.makedirs(
        "data",
        exist_ok=True
    )


    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(content)



# ==========================
# Run
# ==========================


print("==============================")
print("GENERATING MARKET REPORTS")
print("==============================")


data = load_insights()



# Rule based

rule_report = build_rule_based_report(data)


save_report(
    rule_report,
    RULE_OUTPUT_FILE
)


print(
    "Created:",
    RULE_OUTPUT_FILE
)



# AI generated

ai_report = generate_ai_report(data)


save_report(
    ai_report,
    AI_OUTPUT_FILE
)


print(
    "Created:",
    AI_OUTPUT_FILE
)



print()

print(
    "Finished"
)