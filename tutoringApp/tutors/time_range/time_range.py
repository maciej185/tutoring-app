from datetime import datetime, timedelta


class TimeRange:
    """Implement methods for working with time ranges."""

    def __init__(self, start: datetime, end: datetime) -> None:
        """Intialization of a TimeRange class instance

        Args:
            start: datetime object indicating the start
                    of the range.
            end: datetime object indicating the end
                    of the range.
        """
        self.start = start
        self.end = end

    @classmethod
    def from_start_and_duration(
        cls: "TimeRange", start: datetime, duration: timedelta
    ) -> "TimeRange":
        """Create class instance with start time and duration of time range.

        Unlike the original class's constructor, the method
        does not require to pass in the end time. Instead,
        only start time and the duration of time range is
        provided and the end time is calculated based on
        that information.

        Args:
            start: datetime object indicating the start
                        of the range.
            duration: timedelta object representing the
                        duration of the time range.
        """
        return cls(start=start, end=start + duration)

    def __contains__(self, time_range: "TimeRange") -> bool:
        """Check if the TimeRange overlaps with another instance of TimeRange class.

        The method checks if the object that the method is called
        on contains another, provided instance of the TimeRange class
        by first checking if the entire time range is contained.
        If that is not true, additional checks are made to
        see if only either start or end of the provided time
        range are contained.

        Args:
            time_range: instance of the TimeRange class.

        Returns:
            Booleand information of whether the provided
            TimeRange instance overlaps with the object
            that the method is called on.
        """
        if self.start <= time_range.start and self.end >= time_range.end:
            return True
        if (
            self.start >= time_range.start
            and self.end >= time_range.end
            and self.start < time_range.end
        ):
            return True
        if (
            self.start <= time_range.start
            and self.end <= time_range.end
            and self.end > time_range.start
        ):
            return True
        return False
