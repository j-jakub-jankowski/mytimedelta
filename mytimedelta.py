class mytimedelta:
    """Represent the difference between two datetime objects.

    Supported operators:
    - add, subtract mytimedelta

    Representation: (hours, minutes, seconds, centiseconds).
    """
    __slots__ = '_hours', '_minutes', '_seconds', '_centiseconds','_hashcode'

    def __new__(cls, hours=0, minutes=0, seconds=0, centiseconds=0):
        h = m = s = cs = 0

        # Get rid of all fractions, and normalize s and us..
        assert isinstance(h, int)
        h = hours

        assert isinstance(minutes, int)
        hours, minutes = divmod(minutes, 60)
        h += hours
        m = int(minutes)    # can't overflow
        assert isinstance(m, int)
        assert abs(m) <= 60
        # minutes isn't referenced again before redefinition

        if isinstance(seconds, float):
            secondsfrac, seconds = _math.modf(seconds)
            assert seconds == int(seconds)
            seconds = int(seconds)
            assert abs(secondsfrac) <= 1.0
        else:
            secondsfrac = 0

        assert isinstance(seconds, int)        
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        h += hours
        m += minutes
        s = seconds

        assert isinstance(h, int)
        assert isinstance(m, int)
        assert isinstance(seconds, int)
        assert abs(m) <= 2 * 60
        assert abs(s) <  60

        csint = round(secondsfrac * 100)
        assert abs(csint) < 100
        assert isinstance(csint, int)
        
        assert isinstance(centiseconds, int)
        seconds, centiseconds = divmod(centiseconds + csint, 100)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        h += hours
        m += minutes
        s += seconds
        cs = centiseconds

        assert isinstance(h, int)
        assert isinstance(m, int)
        assert isinstance(s, int)
        assert isinstance(cs, int)        
        assert abs(m) <= 3 * 60
        assert abs(s) <  2 * 60
        assert abs(cs) <  100        

        # Just a little bit of carrying possible for microseconds and seconds.
        seconds, cs = divmod(cs, 100)
        s += seconds
        minutes, s = divmod(s, 60)
        m += minutes
        hours, m = divmod(m, 60)
        h += hours

        assert isinstance(h, int)
        assert isinstance(m, int) and 0 <= m < 60
        assert isinstance(s, int) and 0 <= s < 60
        assert isinstance(cs, int) and 0 <= cs < 100
        
        if abs(h) > 999:
            raise OverflowError("mytimedelta # of hours is too large: %d" % h)

        self = object.__new__(cls)
        self._hours = h
        self._minutes = m
        self._seconds = s
        self._centiseconds = cs
        self._hashcode = -1
        return self

    def __repr__(self):
        args = []
        if self._hours:
            args.append("hours=%d" % self._hours)
        if self._minutes:
            args.append("minutes=%d" % self._minutes)
        if self._seconds:
            args.append("seconds=%d" % self._seconds)
        if self._centiseconds:
            args.append("centiseconds=%d" % self._centiseconds)            
        if not args:
            args.append('0')
        return "%s.%s(%s)" % (self.__class__.__module__,
                              self.__class__.__qualname__,
                              ', '.join(args))

    def __str__(self):
        hh = self._hours
        mm = self._minutes
        ss = self._seconds
        # cs = self._centiseconds
        s = "%02d:%02d:%02d" % (hh, mm, ss)
        # s = "%02d:%02d:%02d.%02d" % (hh, mm, ss, cs)
        return s

    def total_seconds(self):
        """Total seconds in the duration."""
        return (self.hours * 36000 + self.minutes * 60 + self.seconds + self.centiseconds/100)

    # Read-only field accessors
    @property
    def hours(self):
        """hours"""
        return self._hours

    @property
    def minutes(self):
        """minutes"""
        return self._minutes

    @property
    def seconds(self):
        """seconds"""
        return self._seconds
    
    @property
    def centiseconds(self):
        """centiseconds"""
        return self._centiseconds
    

    def __add__(self, other):
        if isinstance(other, mytimedelta):
            # for CPython compatibility, we cannot use
            # our __class__ here, but need a real mytimedelta
            return mytimedelta(self._hours + other._hours,
                             self._minutes + other._minutes,
                             self._seconds + other._seconds,
                             self._centiseconds + other._centiseconds)
        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, mytimedelta):
            # for CPython compatibility, we cannot use
            # our __class__ here, but need a real mytimedelta
            return mytimedelta(self._hours - other._hours,
                             self._minutes - other._minutes,
                             self._seconds - other._seconds,
                             self._centiseconds - other._centiseconds)
        return NotImplemented

    def get_time(self):
        """Get time from string in format HH:MM:SS.CS"""
        time = self.split(':')
        h = int(time[0])
        m = int(time[1])
        s = float(time[2])
        
        return mytimedelta(hours = h, minutes = m, seconds = s)

    def __bool__(self):
        return (self._hourss != 0 or
                self.minutes != 0 or
                self._seconds != 0 or
                self._centiseconds != 0)

""""
    def _to_microseconds(self):
        return ((self._days * (24*3600) + self._seconds) * 1000000 +
                self._microseconds)


    # Comparisons of mytimedelta objects with other.

    def __eq__(self, other):
        if isinstance(other, mytimedelta):
            return self._cmp(other) == 0
        else:
            return False

    def __le__(self, other):
        if isinstance(other, mytimedelta):
            return self._cmp(other) <= 0
        else:
            _cmperror(self, other)

    def __lt__(self, other):
        if isinstance(other, mytimedelta):
            return self._cmp(other) < 0
        else:
            _cmperror(self, other)

    def __ge__(self, other):
        if isinstance(other, mytimedelta):
            return self._cmp(other) >= 0
        else:
            _cmperror(self, other)

    def __gt__(self, other):
        if isinstance(other, mytimedelta):
            return self._cmp(other) > 0
        else:
            _cmperror(self, other)

    def _cmp(self, other):
        assert isinstance(other, mytimedelta)
        return _cmp(self._getstate(), other._getstate())

    def __hash__(self):
        if self._hashcode == -1:
            self._hashcode = hash(self._getstate())
        return self._hashcode
"""
