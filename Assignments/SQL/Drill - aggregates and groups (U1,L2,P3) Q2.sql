SELECT start_station
	,COUNT(trip_id) AS '# of trips'
FROM trips

GROUP BY start_station
ORDER BY COUNT(trip_id) desc