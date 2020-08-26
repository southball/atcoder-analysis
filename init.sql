DROP TABLE IF EXISTS contests;
DROP TABLE IF EXISTS merged_problems;
DROP TABLE IF EXISTS problem_models; 

CREATE TABLE contests (
  id TEXT NOT NULL PRIMARY KEY,
  start_epoch_second INT,
  duration_second INT,
  title TEXT,
  rate_change TEXT
);

CREATE TABLE merged_problems (
  id TEXT NOT NULL PRIMARY KEY,
  contest_id TEXT,
  title TEXT,
  shortest_submission_id INT,
  shortest_problem_id TEXT,
  shortest_contest_id TEXT,
  shortest_user_id TEXT,
  fastest_submission_id INT,
  fastest_problem_id TEXT,
  fastest_contest_id TEXT,
  fastest_user_id TEXT,
  first_submission_id INT,
  first_problem_id TEXT,
  first_contest_id TEXT,
  first_user_id TEXT,
  source_code_length INT,
  execution_time INT,
  point INT,
  predict REAL,
  solver_count INT
);

CREATE TABLE problem_models (
  id TEXT NOT NULL PRIMARY KEY,
  slope REAL,
  intercept REAL,
  variance REAL,
  difficulty REAL,
  discrimination REAL,
  irt_loglikelihood REAL,
  irt_users REAL,
  is_experimental BOOLEAN
);
