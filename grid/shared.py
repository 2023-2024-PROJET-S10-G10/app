def print_events(events: list):
    if not events:
        print("No events!")
    else:
        for event in events:
            job = ""
            if event["job_id"]:
                job = f" of job {event['job_id']}"

            cluster = ""
            if event["cluster_name"]:
                cluster = f" on {event['cluster_name']}"

            because = ""
            if event["parent"]:
                because = f" because of {event['parent']}"

        print(
            "------------------------------------------------------------------------------"
        )
        print(
            f"{event['id']}: ({event['state']}) {event['code']}{job} at {event['date_open']}{cluster}{because}"
        )
        if event["message"]:
            print(event["message"])
    print(
        "------------------------------------------------------------------------------"
    )


def print_job(jobs):
    if not jobs:
        print("No such jobs!")
    else:
        for key, value in jobs:
            if key != "links":
                print(f"{key}: {value}")
