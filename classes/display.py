"""Display Class"""
import time

class Display:
    """Display progress of process.

    Attributes:
        start_time (float): Seconds since epoch to when progress starts.
        elapsed_time (float): Seconds since progress started.
        last_updated (float): Seconds since epoch to when progress was
            last updated.
    """

    def __init__(self):
        self.start_time = None
        self.elapsed_time = None
        self.last_updated = None

    def start(self, message=None):
        """Initiates start time. Can display start messages.
        Args:
            message (string): Optional start message.

        Returns:
            None

        Raises:
            None
        """

        self.start_time = time.time()
        if message:
            print(message)

    def update_progress_bar(self, step, end):
        """
        Args:
            step (float): Current iteration of process.
            end (float): Final iteration of process.

        Returns:
            None

        Raises:
            None
        """

        percent = float(step) / float(end)

        start_time = self.start_time
        current_time = time.time()

        if self.last_updated and current_time < self.last_updated + 0.017:
            return
        else:
            self.last_updated = current_time

        elapsed_time = current_time - start_time
        self.elapsed_time = elapsed_time
        estimated_time = (elapsed_time / percent) - elapsed_time
        hours = int(estimated_time / 3600.0)
        minutes = int((estimated_time - (hours * 3600)) / 60.0)
        seconds = int(estimated_time - (minutes * 60) - (hours * 3600))
        time_remaining = "{:02d}:{:02d}:{:02d}".format(
            hours,
            minutes,
            seconds
        )

        progress_bar = "{}".format('\u2588' * int(percent * 25.0))
        remainder = (percent * 25.0) - len(progress_bar)

        if remainder >= 0.75:
            progress_bar += '\u258a'
        elif remainder >= 0.5:
            progress_bar += '\u258c'
        elif remainder >= 0.25:
            progress_bar += '\u258e'

        progress_bar += ' ' * (25 - len(progress_bar))
        output = "    {:05.2f}% |{}| Time Remaining: {}".format(
            percent * 100.0,
            progress_bar,
            time_remaining
        )
        print(' ' * 80, end='\r')
        print(output, end='\r')

    def finish(self):
        """Displays elapsed time of process. Clears attributes.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """

        hours = int(self.elapsed_time / 3600.0)
        minutes = int(self.elapsed_time / 60.0)
        seconds = int(self.elapsed_time - (minutes * 60) - (hours * 3600))
        elapsed_time = "{:02d}:{:02d}:{:02d}".format(
            hours,
            minutes,
            seconds
        )

        print("   100.00% |{}|   Elapsed Time: {} ".format(
            '\u2588' * 25,
            elapsed_time
        ))

        self.start_time = None
        self.elapsed_time = None
        self.last_updated = None
