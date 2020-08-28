SELECT
  a.contest_type AS contest_type,
  UPPER(SUBSTR(p.id, -1)) AS position,
  AVG(m.difficulty) AS difficulty_avg,
  STDDEV(m.difficulty) AS difficulty_std
FROM problem_models m
JOIN contests c ON c.id = p.contest_id
JOIN merged_problems p ON m.id = p.id
JOIN contest_analysis a ON a.contest_id = c.id
WHERE m.difficulty IS NOT NULL
  AND position in ("A", "B", "C", "D", "E", "F")
GROUP BY contest_type, position
