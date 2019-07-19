# mytimedelta
Object to represent a duration, the difference between two times. Create for easy time calculations during sports competitions.

The time provided by the measuring device (ChronoTrack) is in the format: HH:MM:SS.CS. During the competition lasting longer than 24 hours, the time on device passses 24 hours and counts the next hours as 25, 26, 27... Trying to make calculations easier, the date marker was removed and competitors result are calculated without conversion to a different format.


The module was based on standard datetime module and timedelta objects
