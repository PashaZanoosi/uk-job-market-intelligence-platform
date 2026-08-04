from src.skills.skill_pipeline import run_skill_pipeline


BATCH_SIZE = 10


def start_worker():

    result = run_skill_pipeline(
        batch_size=BATCH_SIZE
    )

    print("=" * 50)
    print("SKILL WORKER REPORT")
    print("=" * 50)

    print(f"Processed : {result['processed']}")
    print(f"Completed : {result['completed']}")
    print(f"Unavailable : {result['unavailable']}")
    print(f"Failed : {result['failed']}")
    print(f"Pending Remaining : {result['pending']}")

    print("=" * 50)

    return result


if __name__ == "__main__":
    start_worker()