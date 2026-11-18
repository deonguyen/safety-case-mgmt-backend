SELECT 
    c.id AS component_id,
    COALESCE(c.name, 'Uncategorized') AS component_name,
    COUNT(DISTINCT cit.specification_id) AS unique_specification_implement,
    COUNT(DISTINCT ps.specification_id) AS unique_specification
FROM public.project_specification ps
JOIN public.specification s 
    ON ps.specification_id = s.id
LEFT JOIN public.component c 
    ON ps.component_id = c.id
LEFT JOIN public.code_implementation_trace cit 
    ON cit.project_specification_id = ps.id 
   AND cit.project_id = ps.project_id
WHERE ps.project_id = %s
  AND ps.specification_id IS NOT NULL
  AND s.source ILIKE 'Github'
GROUP BY c.id, c.name
ORDER BY component_name;