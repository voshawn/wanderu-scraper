
-- Merge QA to PROD

INSERT INTO tripsprod (tripid, carrier, origintime, origincity, 
	originlocation, destinationtime, destinationcity, destinationlocation, 
	price, duration, features, dateoftrip, datescraped)

SELECT tripid, carrier, origintime, origincity, originlocation, 
destinationtime, destinationcity, destinationlocation, price, duration, 
features, dateoftrip, datescraped 

FROM tripsqa; 