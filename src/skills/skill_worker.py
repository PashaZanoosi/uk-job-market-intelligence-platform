from src.skills.skill_pipeline import run_skill_pipeline

BATCH_SIZE = 10


def start_worker():

    print("=" * 60)
    print("SKILL WORKER RUN")
    print("=" * 60)

    result = run_skill_pipeline(
        batch_size=BATCH_SIZE
    )

    print(result)

    print("=" * 60)
    print("SKILL WORKER FINISHED")
    print("=" * 60)

    return result


if __name__ == "__main__":
    start_worker()