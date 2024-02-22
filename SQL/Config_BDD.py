import enum
from sqlalchemy import *
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Optional, List
from datetime import datetime

engine = create_engine("sqlite+pysqlite:///mydb", echo=True)

metadata_obj = MetaData()

class api(enum.Enum):
    oar2_5 = 1
    g5k = 2

class auth_type(enum.Enum):
    none = 1
    password = 2
    cert = 3
    JWT = 4

class campaign_state(enum.Enum):
    create_constraint = True
    cancelled = 1
    in_treatment = 2
    paused = 3
    terminated = 4

class campaign_state2(enum.Enum):
    cancelled = "cancelled"
    in_treatment = "in_treatment"
    paused = "paused"
    terminated = "terminated"
class job_state(enum.Enum):
    to_launch = 1
    launching = 2
    submitted = 3
    running = 4
    remote_waiting = 5
    terminated = 6
    event = 7
    batch_waiting = 8

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
    Column("batch", Enum(api)),   # p'tet mettre api.value
    Column("resource_unit", String(255), default="resource_id"),
    Column("power", Integer),
    Column("properties", String(255)),
    Column("stress_factor", Float, default=0),
    Column("enabled", Boolean, default=true()),
    CheckConstraint("api_auth_type IN ('none', 'password', 'cert', 'JWT')", name="enum_auth"),
)


users_mapping = Table(
    "users_mapping",
    metadata_obj,
    Column("id", Integer),
    Column("grid_login", String(255), primary_key=True),
    Column("cluster_login", String(255)),
    Column("cluster_id", Integer)
)

campagnes = Table(
    "campaigns",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("grid_user", String(255), nullable=False),
    Column("state", Enum(campaign_state), nullable=False),
    Column("type", String(255), nullable=false),
    Column("name", String(255)),
    Column("submission_time", TIMESTAMP),   # manque p'tet la spécification time zone, pour tout les TIMESTAMP d'ailleurs, faire une manip au ctrl h
    Column("completion_time", TIMESTAMP),
    Column("nb_jobs", Integer),
    Column("jdl", Text),
)

campaign_properties = Table(
    "campaign_properties",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("cluster_id", Integer),   # if NULL, then it's a global
    Column("campaign_id", Integer, nullable=False),
    Column("name", String(255), nullable=False),
    Column("value", Text, nullable=False)
)

parameters = Table(
    "parameters",
    metadata_obj,
    Column("id", BigInteger, primary_key=True),    # devrait être un bigserial
    Column("campaign_id", Integer, nullable=False),
    Column("name", String(255)),
    Column("param", Text)
    # manque une contrainte d'unicité sur le couple name et campagne_id
)

bag_of_tasks = Table(
    "bag_of_tasks",
    metadata_obj,
    Column("id", BigInteger, primary_key=True),
    Column("campaign_id", Integer, nullable=False),
    Column("param_id", Integer, nullable=False),
    Column("priority", Integer, nullable=False, default=10),
)

jobs_to_launch = Table(
    "jobs_to_launch",
    metadata_obj,
    Column("id", BigInteger, primary_key=True),
    Column("task_id", BigInteger, nullable=False),
    Column("cluster_id", Integer, nullable=False),
    Column("tag", String(255)),
    Column("queuing_date", TIMESTAMP),
    Column("runner_options", Text),
    Column("order_num", Integer, nullable=False, default=1)
)

jobs = Table(
    "jobs",
    metadata_obj,
    Column("id", BigInteger, primary_key=True),
    Column("campaign_id", Integer, nullable=False),
    Column("param_id", Integer, nullable=False),
    Column("batch_id", Integer),
    Column("cluster_id", Integer),
    Column("collect_id", Integer),
    Column("state", Enum(job_state), nullable=False),
    Column("return_code", Integer),
    Column("submission_time", TIMESTAMP),
    Column("start_time", TIMESTAMP),
    Column("stop_time", TIMESTAMP),
    Column("node_name", String(255)),
    Column("resources_used", Integer),
    Column("remote_id", BigInteger),
    Column("tag", String(255)),
    Column("runner_options", Text),
)

events = Table(
    "events",
    metadata_obj,
    Column("id", BigInteger, primary_key=True),
    Column("class", Enum(event_class),nullable=False),
    Column("code", String(32), nullable=False),
    Column("state", Enum(event_state), nullable=False),
    Column("job_id", Integer),
    Column("cluster_id", Integer),
    Column("campaign_id", Integer),
    Column("parent", Integer),
    Column("checked", Enum(checkbox)),
    Column("notified", Boolean, nullable=False, default=False_),
    Column("date_open", TIMESTAMP),
    Column("date_closed", TIMESTAMP),
    Column("date_update", TIMESTAMP),
    Column("message", Text),
)

queue_counts = Table(
    "queue_counts",
    metadata_obj,
    Column("date", TIMESTAMP),
    Column("campaign_id", Integer),
    Column("cluster_id", Integer),
    Column("jobs_count", Integer),
)

admission_rules = Table(
    "admission_rules",
    metadata_obj,
    Column("id", Integer, nullable=False),
    Column("code", Text)
)

user_notifications = Table(
    "user_notifications",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("grid_user", String(255), nullable=False),
    Column("type", Enum(notifications)),
    Column("identity", String(255)),
    Column("severity", String(32)),
    # contrainte unique
)

grid_usage = Table(
    "grid_usage",
    metadata_obj,
    Column("id", BigInteger, nullable=False),
    Column("date", TIMESTAMP, nullable=False),
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
    Column("grid_user", String(255), nullable=False),
    Column("cluster_id", Integer, nullable=False),
    Column("priority", Integer, nullable=False),
)

tasks_affinity = Table(
    "tasks_affinity",
    metadata_obj,
    Column("id", BigInteger, nullable=False),
    Column("param_id", Integer, nullable=False),
    Column("cluster_id", Integer, nullable=False),
    Column("priority", Integer, nullable=False),
)

taps = Table(
    "taps",
    metadata_obj,
    Column("id", BigInteger, nullable=False),
    Column("cluster_id", Integer, nullable=False),
    Column("campaign_id", Integer, nullable=False),
    Column("state", Enum(tap_state), nullable=False, default=tap_state(1)),
    Column("rate", BigInteger, nullable=False),
    Column("close_date", TIMESTAMP),

)

class Base(DeclarativeBase):
  pass

class Cluster(Base):
  __tablename__ = "clusters"

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(255))
  api_url: Mapped[str] = mapped_column(String(255))
  api_auth_type: Mapped[str] = mapped_column(Enum(auth_type), nullable=True)  # heu pas sûr que ce soit un mapped[str] lui
  api_username: Mapped[str] = mapped_column(String(255), nullable=False)
  api_password: Mapped[str] = mapped_column(String(255))

  api_auth_header: Mapped[str] = mapped_column(String(255), nullable=True)
  api_chunk_size: Mapped[int] = mapped_column(Integer)
  ssh_host: Mapped[str] = mapped_column(String(255), nullable=True)
  batch: Mapped[str] = mapped_column(Enum(api))                  # heu ici aussi
  resource_unit: Mapped[str] = mapped_column(String(255), nullable=True)
  power: Mapped[int] = mapped_column(Integer, nullable=True)
  properties: Mapped[str] = mapped_column(String(255), nullable=True)
  stress_factor: Mapped[float] = mapped_column(Float, nullable=True)
  enabled: Mapped[bool] = mapped_column(Boolean)

metadata_obj.create_all(engine)


stmt = insert(campagnes).values(grid_user="clément", state=campaign_state(2), submission_time=datetime.now())

with engine.connect() as conn:
    result = conn.execute(stmt)
    #conn.execute(insert(cluster_table).values(name="Luke", api_url="/prout", api_username="dova", api_password="zer", batch=api(1), api_auth_type="pouet"))
    conn.commit()
