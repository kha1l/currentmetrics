from datetime import date


class DataWork:

    def __init__(self, date_end=None):
        self.date_end = date_end

    def set_date(self):
        if self.date_end is None:
            self.date_end = date.today()
            return self.date_end
        else:
            return self.date_end
