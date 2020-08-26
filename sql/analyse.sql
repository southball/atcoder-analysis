SELECT
  CASE c.rate_change
    WHEN " ~ 1199" THEN "ABC_OLD"
    WHEN " ~ 1999" THEN "ABC_NEW"
    WHEN " ~ 2799" THEN "ARC"
    WHEN "1200 ~ " THEN "AGC"
    WHEN "-" THEN "AGC"
    WHEN "All" THEN "AGC"
    ELSE ""
  END contest_type,
  UPPER(SUBSTR(p.id, -1)) position,
  AVG(m.difficulty) AS difficulty_avg,
  STDDEV(m.difficulty) AS difficulty_std
FROM problem_models m
JOIN contests c ON c.id = p.contest_id
JOIN merged_problems p ON m.id = p.id
WHERE m.difficulty IS NOT NULL
  AND position in ("A", "B", "C", "D", "E", "F")
GROUP BY contest_type, position
