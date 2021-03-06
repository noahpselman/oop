class Quarter():

    def __init__(self, **kwargs) -> None:
        # TODO
        self.name = kwargs['name']
        self.start_date = kwargs['start_date']
        self.end_date = kwargs['end_date']

    def __repr__(self):
        return f"""{self.name}:  start: {self.start_date}, end: {self.end_date}"""
