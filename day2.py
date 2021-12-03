from utils import get_input_list_from_day


class Submarine:
    def move_forward(self, amount):
        raise NotImplementedError

    def move_up(self, amount):
        raise NotImplementedError

    def move_down(self, amount):
        raise NotImplementedError

    def move(self, direction, amount):
        if direction == 'forward':
            self.move_forward(amount)
        elif direction == 'up':
            self.move_up(amount)
        elif direction == 'down':
            self.move_down(amount)
        else:
            raise Exception("This direction is not possible.")

    @staticmethod
    def read_command(command):
        direction, amount = command.split(' ')
        return direction, int(amount)

    def execute_command(self, command):
        self.move(*self.read_command(command))

    def take_route(self, command_list):
        for command in command_list:
            self.execute_command(command)


class Submarine1(Submarine):
    def __init__(self):
        self.horizontal_pos = 0
        self.depth = 0

    def move_forward(self, amount):
        self.horizontal_pos += amount

    def move_up(self, amount):
        self.depth -= amount

    def move_down(self, amount):
        self.depth += amount


class Submarine2(Submarine):
    def __init__(self):
        self.horizontal_pos = 0
        self.depth = 0
        self.aim = 0

    def move_forward(self, amount):
        self.horizontal_pos += amount
        self.depth += self.aim * amount

    def move_up(self, amount):
        self.aim -= amount

    def move_down(self, amount):
        self.aim += amount


if __name__ == "__main__":
    input_list = get_input_list_from_day(2, str)
    sub1 = Submarine1()
    sub2 = Submarine2()
    sub1.take_route(input_list)
    sub2.take_route(input_list)
    print(f"Part 1: {sub1.horizontal_pos * sub1.depth}")
    print(f"Part 2: {sub2.horizontal_pos * sub2.depth}")
