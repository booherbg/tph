from gtfs.entity import *
from gtfs import Schedule
import sys
import os
import sqlalchemy.orm.exc

'''
[(721, <Stop 1180880>),
 (691, <Stop 2430050>),
 (680, <Stop 2851845>),
 (650, <Stop 1161160>),
 (632, <Stop 2240010>)]

'''
if len(sys.argv) == 3:
    gtfs_db = sys.argv[-1]
else:
    gtfs_db = './sorta.db'
schedule = Schedule(gtfs_db, echo=False)

def find_highest_volume_stop():
    NUM_STOPS = 5
    nstops = list()
    for i in xrange(len(schedule.stops)):
        stop = schedule.stops[i]
        nstops.append((len(stop.stop_times), stop))
        nstops.sort()
        nstops.reverse()
        if len(nstops) > NUM_STOPS:
            nstops = nstops[0:NUM_STOPS]
        if i % 20 == 0:
            print "(%.2f%%) %d / %d (highest so far: %d; id=%d)" % ((float(i) / len(schedule.stops))*100, i, len(schedule.stops), nstops[0][0], nstops[0][1].stop_id)
    return nstops
    
if __name__ == '__main__':
    if len(sys.argv) not in (2,3):
        print "sorry, you've gotta give me a stop id"
        sys.exit(1)
        
    stop_id = int(sys.argv[1])
    
    try:
        stop = Stop.query.filter_by(stop_id=stop_id).one()
    except sqlalchemy.orm.exc.NoResultFound:
        print "stop id %d not found" % (stop_id)
        sys.exit(1)
        
    trips = set()
    routes = set()
    for time in stop.stop_times:
        trips.add(time.trip)
        routes.add(time.trip.route)
    print "Stop name: %s" % stop.stop_name
    print "There are %d trips for this stop (not shown)" % len(trips)
    #for trip in trips:
    #    print trip.trip_id, trip.trip_headsign
        
    print ""
    print "Routes that this stop is on:"
    for route in routes:
        print "Route %s: %s (%d)" % (str(route.route_short_name), str(route.route_long_name), int(route.route_id))

