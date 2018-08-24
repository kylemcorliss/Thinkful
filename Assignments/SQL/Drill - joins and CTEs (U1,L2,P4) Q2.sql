SELECT t.name
	,s.docks_available
	,COUNT(s.timestamp) AS '# of'
FROM status s
JOIN stations t
ON s.station_id = t.station_id

WHERE s.docks_available = 0

GROUP BY t.name
	,s.docks_available	
ORDER BY COUNT(s.timestamp) desc