DROP TABLE IF EXISTS contest_analysis;

CREATE TABLE contest_analysis (
  contest_id TEXT NOT NULL PRIMARY KEY,
  problem_count INT NOT NULL,
  contest_type TEXT NOT NULL
);

INSERT INTO contest_analysis (contest_id, problem_count, contest_type)
SELECT
  c.id contest_id,
  COUNT(*) problem_count,
  CASE c.rate_change
    WHEN " ~ 1199" THEN "ABC_OLD"
    WHEN " ~ 1999" THEN "ABC_NEW"
    WHEN " ~ 2799" THEN "ARC"
    WHEN "1200 ~ " THEN "AGC"
    WHEN "-" THEN "AGC"
    WHEN "All" THEN "AGC"
    ELSE ""
  END contest_type
FROM contests c
JOIN merged_problems p ON c.id = p.contest_id
GROUP BY c.id;

UPDATE contest_analysis
SET contest_type = "ARC_OLD"
WHERE contest_id LIKE "arc%";

UPDATE contest_analysis
SET contest_type = "ARC_NEW"
WHERE contest_type = "ARC";

-- Special Contests
UPDATE contest_analysis
SET contest_type = ""
WHERE contest_id LIKE "joi%"
OR contest_id LIKE "jag%";

DELETE FROM contest_analysis
WHERE contest_type = "";

-- Scale Difficulty < 400
UPDATE problem_models
SET difficulty = 400.0 / EXP(1.0 - difficulty / 400.0)
WHERE difficulty < 400.0;
