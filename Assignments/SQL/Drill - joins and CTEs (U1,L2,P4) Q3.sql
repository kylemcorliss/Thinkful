SELECT s.name
	,s.dockcount
	,COUNT(t.trip_id) AS '# of Trips'
FROM stations s
JOIN trips t
ON t.start_station = s.name

GROUP BY s.name
	,s.dockcount
ORDER BY s.dockcount desc