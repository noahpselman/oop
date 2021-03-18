class Quarter():
    """
    quarters make sense to be an object since on occasion
    we'll need to know it's temporal relationship to other
    quarters and the present day.
    note: 9/10 times quarters are represented by strings
    in this application
    """

    def __init__(self, **kwargs) -> None:

        self.name = kwargs['name']
        self.start_date = kwargs['start_date']
        self.end_date = kwargs['end_date']

    def __repr__(self):
        return f"""{self.name}:  start: {self.start_date}, end: {self.end_date}"""
