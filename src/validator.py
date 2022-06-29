import json


class Validator:
    def __init__(self, json):
        self.json = json
        self.json_error = ""
        self.line_error = 0
        self.row_error = 0
        self.parse_json()

    
    def parse_json(self):
        try:
            json.loads(self.json)
        except json.JSONDecodeError as err:
            self.json_error = err.msg
            self.line_error = err.lineno
            self.row_error = err.colno
            self.valid = False
        else:
            self.valid = True

    def get_error_pos(self):
        return (self.row_error, self.line_error)

    def get_message(self):
        return (self.json_error)

    def valid_json(self):
        if self.valid:
            return True
        else:
            return False

    def pretty_print_json(self):
        json_ugly = json.loads(self.json)
        json_pretty = json.dumps(json_ugly, indent=4)
        return json_pretty