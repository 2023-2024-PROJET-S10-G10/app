import enum
from sqlalchemy import *
import sys
import os

# Appends the parent directory of the current directory to the Python module search path.
sys.path.append(sys.path[0].replace("/SQL", ""))

from utils.sql import *

metadata_obj = MetaData()

if len(sys.argv) != 2:
    print("Usage:   python Config_BDD.py <path_DB> (default: SQL in /app)")
    print("Example: python Config_BDD.py SQL")
    path = "SQL/"
else:
    path = sys.argv[1]
    if path == "SQL" or path == "SQL/":
        path = "SQL/"
    else:
        path_local = "../" + path
        if os.path.isdir(path_local):
            print(f"The path `{path_local}` is not valid.")
            sys.exit(1)
        path = sys.argv[1]
        if not path.endswith("/"):
            path += "/"

print(path)
engine = create_engine(getPath(path), echo=True)


def initializeCluster():
    metadata_obj.create_all(engine)

    # TODO: Replace dummy values
    clusterLuke = insert(cluster_table).values(
        name="luke",
        api_url="/foo",
        api_username="dova",
        api_password="zer",
        batch=api(1),
        api_auth_type=auth_type(1),
    )
    clusterDahu = insert(cluster_table).values(
        name="dahu",
        api_url="/bar",
        api_username="air",
        api_password="zerzer",
        batch=api(2),
        api_auth_type=auth_type(1),
    )

    with engine.connect() as conn:
        conn.execute(clusterLuke)
        conn.commit()
        conn.execute(clusterDahu)
        conn.commit()


class api(enum.Enum):
    oar2_5 = 1
    g5k = 2


class auth_type(enum.Enum):
    none = 1
    password = 2
    cert = 3
    JWT = 4


class campaign_state(enum.Enum):
    cancelled = 1
    in_treatment = 2
    paused = 3
    terminated = 4


class job_state(enum.Enum):
    to_launch = 1
    launching = 2
    submitted = 3
    running = 4
    remote_waiting = 5
    terminated = 6
    event = 7
    batch_waiting = 8
    cancelled = 9


class event_class(enum.Enum):
    cluster = 1
    job = 2
    campaign = 3
    notify = 4
    log = 5


class event_state(enum.Enum):
    open = 1
    closed = 2


class checkbox(enum.Enum):
    yes = 1
    no = 2


class tap_state(enum.Enum):
    open = 1
    closed = 2


class notifications(enum.Enum):
    mail = 1
    xmpp = 2
    log = 3
    irc = 4


cluster_table = Table(
    "clusters",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(255)),
    Column("api_url", String(255)),
    Column("api_auth_type", Enum(auth_type), default=auth_type(2)),
    Column("api_username", String(255)),
    Column("api_password", String(255)),
    Column("api_auth_header", String(255)),
    Column("api_chunk_size", Integer, default=0),
    Column("ssh_host", String(255)),
    Column("batch", Enum(api)),
    Column("resource_unit", String(255), default="resource_id"),
    Column("power", Integer),
    Column("properties", String(255)),
    Column("stress_factor", Float, default=0),
    Column("enabled", Boolean, default=true()),
    CheckConstraint(
        f"api_auth_type IN ({str(auth_type._member_names_)[1:-1]})",
        name="enum_auth",
    ),
    CheckConstraint(
        f"batch IN ({str(api._member_names_)[1:-1]})", name="enum_batch"
    ),
)

authentification = Table(
    "authentification",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("grid_login", String(255), nullable=False),
    Column("cluster_id", Integer, nullable=False),
    Column("JWT", String(255), nullable=False),
    UniqueConstraint("grid_login", "cluster_id", name="UniqueJWTPerUser"),
)

users_mapping = Table(
    "users_mapping",
    metadata_obj,
    Column("id", Integer),
    Column("grid_login", String(255), primary_key=True),
    Column("cluster_login", String(255)),
    Column("cluster_id", Integer),
)

campagnes = Table(
    "campaigns",
    metadata_obj,
    Column("id", Integer, primary_key=True, index=True),
    Column("grid_user", String(255), nullable=False),
    Column("state", Enum(campaign_state), nullable=False, index=True),
    Column("type", String(255), nullable=False),
    Column("name", String(255)),
    Column("submission_time", TIMESTAMP),
    Column("completion_time", TIMESTAMP),
    Column("nb_jobs", Integer),
    Column("jdl", Text),
    CheckConstraint(
        f"state IN ({str(campaign_state._member_names_)[1:-1]})",
        name="enum_state",
    ),
)

campaign_properties = Table(
    "campaign_properties",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("cluster_id", Integer),  # if NULL, then it's a global
    Column(
        "campaign_id", Integer, nullable=False
    ),  # Double index, je sais pas encore comment faire
    Column("name", String(255), nullable=False),
    Column("value", Text, nullable=False),
)

parameters = Table(
    "parameters",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True, index=True),
    Column("campaign_id", Integer, nullable=False, index=True),
    Column("name", String(255)),
    Column("param", Text),
    UniqueConstraint("campaign_id", "name", name="UniqueParamPerName"),
)

bag_of_tasks = Table(
    "bag_of_tasks",
    metadata_obj,
    Column("id", Integer, primary_key=True, index=True),
    Column("campaign_id", Integer, nullable=False, index=True),
    Column("param_id", Integer, nullable=False),
    Column("priority", Integer, nullable=False, default=10),
    UniqueConstraint("campaign_id", "param_id", name="UniquePriorityPerParam"),
)

jobs_to_launch = Table(
    "jobs_to_launch",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("task_id", Integer, nullable=False),
    Column("cluster_id", Integer, nullable=False, index=True),
    Column("tag", String(255)),
    Column("queuing_date", TIMESTAMP),
    Column("runner_options", Text),
    Column("order_num", Integer, nullable=False, default=1),
)

jobs = Table(
    "jobs",
    metadata_obj,
    Column("id", Integer, primary_key=True, index=True),
    Column("campaign_id", Integer, nullable=False, index=True),
    Column("param_id", Integer, nullable=False, index=True),
    Column("batch_id", Integer, index=True),
    Column("cluster_id", Integer, index=True),
    Column("collect_id", Integer),
    Column("state", Enum(job_state), nullable=False, index=True),
    Column("return_code", Integer),
    Column("submission_time", TIMESTAMP),
    Column("start_time", TIMESTAMP),
    Column("stop_time", TIMESTAMP),
    Column("node_name", String(255)),
    Column("resources_used", Integer),
    Column("remote_id", Integer),
    Column("tag", String(255), index=True),
    Column("runner_options", Text),
    CheckConstraint(
        f"state IN ({str(job_state._member_names_)[1:-1]})", name="enum_state"
    ),
)

events = Table(
    "events",
    metadata_obj,
    Column("id", Integer, primary_key=True, index=True),
    Column("class_e", Enum(event_class), nullable=False, index=True),
    Column("code", String(32), nullable=False, index=True),
    Column("state", Enum(event_state), nullable=False, index=True),
    Column("job_id", Integer, index=True),
    Column("cluster_id", Integer, index=True),
    Column("campaign_id", Integer, index=True),
    Column("parent", Integer),
    Column("checked", Enum(checkbox)),
    Column("notified", Boolean, nullable=False, default=False, index=True),
    Column("date_open", TIMESTAMP),
    Column("date_closed", TIMESTAMP),
    Column("date_update", TIMESTAMP),
    Column("message", Text),
    CheckConstraint(
        f"state IN ({str(event_state._member_names_)[1:-1]})",
        name="enum_state",
    ),
    CheckConstraint(
        f"class_e IN ({str(event_class._member_names_)[1:-1]})",
        name="enum_class",
    ),
    CheckConstraint(
        f"checked IN ({str(checkbox._member_names_)[1:-1]})",
        name="enum_checkbox",
    ),
)

queue_counts = Table(
    "queue_counts",
    metadata_obj,
    Column("date", TIMESTAMP),
    Column("campaign_id", Integer),
    Column("cluster_id", Integer),
    Column("jobs_count", Integer),  # double index
)

admission_rules = Table(
    "admission_rules",
    metadata_obj,
    Column("id", Integer, nullable=False),
    Column("code", Text),
)

user_notifications = Table(
    "user_notifications",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("grid_user", String(255), nullable=False, index=True),
    Column("type", Enum(notifications)),
    Column("identity", String(255)),
    Column("severity", String(32)),
    UniqueConstraint(
        "grid_user", "identity", "type", name="UniqueUserNotification"
    ),
    CheckConstraint(
        f"type IN ({str(notifications._member_names_)[1:-1]})",
        name="enum_notification",
    ),
)

grid_usage = Table(
    "grid_usage",
    metadata_obj,
    Column("id", Integer, nullable=False),
    Column("date", TIMESTAMP, nullable=False, index=True),
    Column("cluster_id", Integer),
    Column("max_resources", Integer),
    Column("used_resources", Integer),
    Column("unavailable_resources", Integer),
    Column("used_by_cigri", Integer),
)

users_priority = Table(
    "users_priority",
    metadata_obj,
    Column("id", Integer, nullable=False),
    Column("grid_user", String(255), nullable=False, index=True),
    Column("cluster_id", Integer, nullable=False, index=True),
    Column("priority", Integer, nullable=False),
)

tasks_affinity = Table(
    "tasks_affinity",
    metadata_obj,
    Column("id", Integer, nullable=False, index=True),
    Column("param_id", Integer, nullable=False, index=True),
    Column("cluster_id", Integer, nullable=False, index=True),
    Column("priority", Integer, nullable=False),
)

taps = Table(
    "taps",
    metadata_obj,
    Column("id", Integer, nullable=False, index=True),
    Column("cluster_id", Integer, nullable=False),
    Column("campaign_id", Integer, nullable=False),  # double index
    Column("state", Enum(tap_state), nullable=False, default=tap_state(1)),
    Column("rate", Integer, nullable=False),
    Column("close_date", TIMESTAMP),
    CheckConstraint(
        f"state IN ({str(tap_state._member_names_)[1:-1]})", name="enum_state"
    ),
)

initializeCluster()
