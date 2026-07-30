from groq import Groq
from dotenv import load_dotenv
import os
import json

from sqlalchemy import text
from src.database.connection import engine


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

DATABASE_URL = os.getenv("DATABASE_URL")

# -----------------------------------
# Load taxonomy
# -----------------------------------

def load_taxonomy():

    with engine.connect() as connection:

        result = connection.execute(

            text("""
            SELECT 
                taxonomy_id,
                name
            FROM skill_taxonomy
            WHERE level = 2
            ORDER BY taxonomy_id
            """)

        )

        return [
            {
                "id": row.taxonomy_id,
                "name": row.name
            }
            for row in result
        ]



# -----------------------------------
# Classify skill with AI
# -----------------------------------

def classify_skill(skill_name, taxonomy):


    taxonomy_text = "\n".join(
        [
            f"{item['id']}: {item['name']}"
            for item in taxonomy
        ]
    )


    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        temperature=0,

        messages=[

            {
                "role":"system",
                "content":f"""
You are a labour market taxonomy classifier.

Classify the skill into exactly ONE taxonomy category.

Available taxonomy:

{taxonomy_text}


Rules:

- Choose the closest professional category.
- Do not create new categories.
- Return only JSON.

Format:

{{
 "taxonomy_id": number,
 "confidence": 0.0
}}

"""
            },

            {
                "role":"user",
                "content":skill_name
            }

        ]

    )


    output = response.choices[0].message.content


    clean = (
        output
        .replace("```json","")
        .replace("```","")
        .strip()
    )


    return json.loads(clean)



# -----------------------------------
# Save suggestion
# -----------------------------------

def save_suggestion(
        skill_id,
        taxonomy_id,
        confidence
):


    with engine.begin() as connection:


        connection.execute(

            text("""
            INSERT INTO skill_taxonomy_suggestions
            (
                skill_id,
                suggested_taxonomy_id,
                confidence_score,
                source,
                status
            )

            VALUES
            (
                :skill_id,
                :taxonomy_id,
                :confidence,
                'AI',
                'pending'
            )

            """),

            {
                "skill_id": skill_id,
                "taxonomy_id": taxonomy_id,
                "confidence": confidence
            }

        )



# -----------------------------------
# Main
# -----------------------------------


taxonomy = load_taxonomy()


print("Loaded taxonomy:")
for item in taxonomy:
    print(item)



with engine.connect() as connection:


    result = connection.execute(

        text("""
        SELECT
            skill_id,
            skill_name
        FROM skills
        ORDER BY skill_id
        """)

    )


    skills = result.fetchall()



print("\nTotal skills:", len(skills))



for skill in skills:


    skill_id = skill.skill_id

    skill_name = skill.skill_name


    print("\n---------------------")

    print(
        "Processing:",
        skill_name
    )


    try:


        result = classify_skill(
            skill_name,
            taxonomy
        )


        print(
            result
        )


        save_suggestion(

            skill_id,

            result["taxonomy_id"],

            result.get(
                "confidence",
                0.5
            )

        )


        print(
            "Saved"
        )



    except Exception as e:


        print(
            "ERROR:",
            skill_name
        )

        print(e)



print("\nFinished")