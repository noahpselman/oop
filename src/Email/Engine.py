from __future__ import annotations


class Engine():
    def __init__(self):
        None

    def send(self, to: List[str], from_: str, msg: str):
        """
        you didn't really think i would send emails, did you?
        """
        print(f"Sending {msg} to {', '.join(to)} from {from_}")
        return True
