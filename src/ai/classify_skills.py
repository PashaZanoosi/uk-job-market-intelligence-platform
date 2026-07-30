from groq import Groq
from dotenv import load_dotenv
import os
import json
import time
from sqlalchemy import text
from src.database.connection import engine

# ==========================
# Environment
# ==========================

load_dotenv()

client = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)

# ==========================
# Settings
# ==========================

BATCH_SIZE = 25

MODEL = (
    "llama-3.3-70b-versatile"
)

# ==========================
# Load Taxonomy
# ==========================

def load_taxonomy():

    with engine.connect() as connection:

        result = connection.execute(

            text(
                """
                SELECT
                    taxonomy_id,
                    name

                FROM skill_taxonomy

                WHERE level = 2

                ORDER BY taxonomy_id
                """
            )

        )

        return [

            {

                "id":
                    row.taxonomy_id,

                "name":
                    row.name

            }

            for row in result

        ]

# ==========================
# Classify Skill Batch
# ==========================

def classify_skill_batch(
    skills,
    taxonomy
):

    taxonomy_text = "\n".join(

        [
            f"{item['id']}: "
            f"{item['name']}"

            for item in taxonomy
        ]

    )

    skill_text = "\n".join(

        [
            (
                f"{skill['skill_id']}: "
                f"{skill['skill_name']}"
            )

            for skill in skills
        ]
    )

    response = (

        client.chat.completions.create(

            model=MODEL,
            temperature=0,
            messages=[
                {
                    "role":
                        "system",

                    "content":
                        f"""

You classify labour market skills.

Assign each skill to the most
appropriate taxonomy category.

Available taxonomy:

{taxonomy_text}

Rules:

1. Classify every skill.

2. Use only taxonomy IDs
provided above.

3. Return only valid JSON.

4. Do not add explanations.

Required format:

[
    {{
        "skill_id": 1,
        "taxonomy_id": 12
    }}
]

"""

                },

                {

                    "role":
                        "user",

                    "content":
                        f"""

Skills:

{skill_text}

"""

                }

            ]

        )

    )


    output = (

        response
        .choices[0]
        .message
        .content

    )


    output = (

        output

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

    return json.loads(
        output
    )

# ==========================
# Update Database
# ==========================

def update_skill_taxonomies(
    classifications
):

    with engine.begin() as connection:

        for item in classifications:

            connection.execute(

                text(
                    """
                    UPDATE skills

                    SET taxonomy_id =
                        :taxonomy_id

                    WHERE skill_id =
                        :skill_id
                    """
                ),

                {

                    "taxonomy_id":
                        item[
                            "taxonomy_id"
                        ],

                    "skill_id":
                        item[
                            "skill_id"
                        ]

                }

            )

# ==========================
# Main
# ==========================

print(
    "=============================="
)

print(
    "START AI SKILL CLASSIFICATION"
)

print(
    "==============================",
    flush=True
)

print(
    "Loading taxonomy...",
    flush=True
)


taxonomy = load_taxonomy()

print(
    f"Taxonomy categories: "
    f"{len(taxonomy)}",
    flush=True
)

print(
    "Loading unclassified skills...",
    flush=True
)

with engine.connect() as connection:

    result = connection.execute(

        text(
            """
            SELECT
                skill_id,
                skill_name

            FROM skills

            WHERE taxonomy_id
                IS NULL

            ORDER BY skill_id
            """
        )

    )

    skills = [

        {

            "skill_id":
                row.skill_id,

            "skill_name":
                row.skill_name

        }

        for row in result

    ]

print(
    f"Skills waiting for "
    f"classification: "
    f"{len(skills)}",
    flush=True
)

if not skills:

    print(
        "No skills require "
        "classification."
    )

    print(
        "Finished"
    )

    raise SystemExit

# ==========================
# Process Batches
# ==========================

total_batches = (

    len(skills)

    +

    BATCH_SIZE

    -

    1

) // BATCH_SIZE

for start in range(

    0,

    len(skills),

    BATCH_SIZE

):

    batch_number = (

        start // BATCH_SIZE

    ) + 1

    batch = (

        skills[
            start:
            start + BATCH_SIZE
        ]
    )

    print()

    print(
        "=============================="
    )

    print(
        f"Batch "
        f"{batch_number}/"
        f"{total_batches}"
    )

    print(
        f"Skills in batch: "
        f"{len(batch)}"
    )

    print(
        "==============================",
        flush=True
    )

    try:
        print(
            "Sending batch to Groq...",
            flush=True
        )

        classifications = (
            classify_skill_batch(
                batch,
                taxonomy
            )
        )

        print(
            "Groq response received.",
            flush=True
        )

        update_skill_taxonomies(
            classifications
        )

        print(
            f"Saved skills: "
            f"{len(classifications)}",
            flush=True
    )

    except Exception as error:

        print(
            f"Batch "
            f"{batch_number} "
            f"failed"
        )

        print(
            error
        )

        raise

    time.sleep(
        1
    )

print()
print( "==============================" )
print( "SKILL CLASSIFICATION COMPLETE" )
print( "==============================" )
