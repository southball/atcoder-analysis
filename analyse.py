import requests
import os
import sqlite3
import json
import math

CONTESTS_JSON = "https://kenkoooo.com/atcoder/resources/contests.json"
MERGED_PROBLEMS_JSON = "https://kenkoooo.com/atcoder/resources/merged-problems.json"
PROBLEM_MODELS_JSON = "https://kenkoooo.com/atcoder/resources/problem-models.json"

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
DB_FILE = os.path.join(ROOT_DIR, "atcoder.db")
INIT_SQL_FILE = os.path.join(ROOT_DIR, "init.sql")

CACHE_DIR = os.path.join(ROOT_DIR, "cache")
CONTESTS_JSON_FILE = os.path.join(CACHE_DIR, "contests.json")
MERGED_PROBLEMS_JSON_FILE = os.path.join(CACHE_DIR, "merged-problems.json")
PROBLEM_MODELS_JSON_FILE = os.path.join(CACHE_DIR, "problem-models.json")

def ensure_dir(directory: str):
    if os.path.exists(directory) and os.path.isdir(directory):
        print("The folder {} is already created.".format(directory))
        return
    elif os.path.exists(directory) and not os.path.isdir(directory):
        raise Exception("{} already exists, but is not a file.".format(directory))
        return
    print("Creating directory {}...".format(directory))
    os.mkdir(directory)

def ensure_file(filename: str, location: str):
    if os.path.exists(filename):
        print("{} already exists.".format(filename))
        return
    print("Downloading {} from {}...".format(filename, location))
    req = requests.get(location)
    open(filename, "wb").write(req.content)

def read_file(filename: str):
    return open(filename, "r").read()

def get_json(filename: str, location: str):
    ensure_file(filename, location)
    file = open(filename, "r")
    return json.load(file)

ensure_dir(CACHE_DIR)

contests = get_json(CONTESTS_JSON_FILE, CONTESTS_JSON)
merged_problems = get_json(MERGED_PROBLEMS_JSON_FILE, MERGED_PROBLEMS_JSON)
problem_models = get_json(PROBLEM_MODELS_JSON_FILE, PROBLEM_MODELS_JSON)

print("Connecting to database at {}".format(DB_FILE))
database = sqlite3.connect(DB_FILE)

print("Initializing database...")
cursor = database.cursor()
cursor.executescript(read_file(INIT_SQL_FILE))

# Insert Data
print("Inserting contests...")
for contest in contests:
    cursor.execute(
        """
        INSERT INTO contests (id, start_epoch_second, duration_second, title, rate_change)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            contest["id"],
            contest["start_epoch_second"],
            contest["duration_second"],
            contest["title"],
            contest["rate_change"]
        ]
    )

print("Inserting merged problems...")
for problem in merged_problems:
    cursor.execute(
        """
        INSERT INTO merged_problems (
            id, contest_id, title,
            shortest_submission_id, shortest_problem_id, shortest_contest_id, shortest_user_id,
            fastest_submission_id, fastest_problem_id, fastest_contest_id, fastest_user_id,
            first_submission_id, first_problem_id, first_contest_id, first_user_id,
            source_code_length, execution_time, point, predict, solver_count
        )
        VALUES (
            ?, ?, ?,
            ?, ?, ?, ?,
            ?, ?, ?, ?,
            ?, ?, ?, ?,
            ?, ?, ?, ?, ?
        )
        """,
        [
            problem["id"],
            problem["contest_id"],
            problem["title"],
            problem["shortest_submission_id"],
            problem["shortest_problem_id"],
            problem["shortest_contest_id"],
            problem["shortest_user_id"],
            problem["fastest_submission_id"],
            problem["fastest_problem_id"],
            problem["fastest_contest_id"],
            problem["fastest_user_id"],
            problem["first_submission_id"],
            problem["first_problem_id"],
            problem["first_contest_id"],
            problem["first_user_id"],
            problem["source_code_length"],
            problem["execution_time"],
            problem["point"],
            problem["predict"],
            problem["solver_count"],
        ]
    )

print("Inserting problem models...")
for id in problem_models:
    model = problem_models[id]
    try:
        cursor.execute(
            """
            INSERT INTO problem_models (id, slope, intercept, variance, difficulty, discrimination, irt_loglikelihood, irt_users, is_experimental)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                id,
                model["slope"],
                model["intercept"],
                model["variance"],
                model["difficulty"],
                model["discrimination"],
                model["irt_loglikelihood"],
                model["irt_users"],
                model["is_experimental"],
            ]
        )
    except KeyError:
        # Incomplete Model
        pass

print("Committing changes to database...")
database.commit()

print("Analyzing...")

class SqliteStddev:
    def __init__(self):
        self.M = 0.0
        self.S = 0.0
        self.k = 1

    def step(self, value):
        if value is None:
            return
        tM = self.M
        self.M += (value - tM) / self.k
        self.S += (value - tM) * (value - self.M)
        self.k += 1

    def finalize(self):
        if self.k < 3:
            return None
        return math.sqrt(self.S / (self.k-2))

database.create_aggregate("STDDEV", 1, SqliteStddev)
for line in cursor.execute(read_file("sql/analyse.sql")):
    print(line)

database.close()
