# =====================================================
# skill_database.py
# Save extracted skills into database
# =====================================================


from sqlalchemy import text

from src.database.connection import engine



# =====================================================
# Get or Create Skill
# =====================================================

def get_or_create_skill(
    skill_name,
    skill_type,
    skill_category
):


    select_sql = text("""
        SELECT
            skill_id

        FROM skills

        WHERE
            LOWER(skill_name) = LOWER(:skill_name)

        LIMIT 1
    """)


    insert_sql = text("""
        INSERT INTO skills
        (
            skill_name,
            skill_type,
            skill_category
        )

        VALUES
        (
            :skill_name,
            :skill_type,
            :skill_category
        )

        RETURNING skill_id
    """)



    with engine.begin() as connection:


        result = connection.execute(

            select_sql,

            {
                "skill_name": skill_name
            }

        ).fetchone()



        if result:


            return result.skill_id



        result = connection.execute(

            insert_sql,

            {

                "skill_name":
                    skill_name,

                "skill_type":
                    skill_type,

                "skill_category":
                    skill_category

            }

        ).fetchone()



        return result.skill_id



# =====================================================
# Link Skill To Job
# =====================================================

def link_skill_to_job(

    job_id,

    skill_id

):


    sql = text("""
        INSERT INTO job_skills
        (
            job_id,
            skill_id
        )

        VALUES
        (
            :job_id,
            :skill_id
        )

        ON CONFLICT DO NOTHING
    """)



    with engine.begin() as connection:


        connection.execute(

            sql,

            {

                "job_id":
                    job_id,

                "skill_id":
                    skill_id

            }

        )



# =====================================================
# Save All Skills For Job
# =====================================================

def save_job_skills(

    job_id,

    skills

):


    saved = 0


    for skill in skills:


        skill_id = get_or_create_skill(

            skill["skill_name"],

            skill["skill_type"],

            skill["skill_category"]

        )



        link_skill_to_job(

            job_id,

            skill_id

        )


        saved += 1



    return saved