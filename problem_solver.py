SOLUTION_DOESNT_EXIST = -1


class Solver:
    def __init__(self, direction, person_pos=0):
        super().__init__()
        self.direction = direction
        self.person_pos = person_pos

    def move(self, x_field):
        if x_field.is_hit_on_next(self.person_pos + self.direction):
            raise ValueError("Person is hit")
        self.person_pos += self.direction

    def __eq__(self, other):
        if isinstance(other, Solver):
            return (self.direction == other.direction) and (self.person_pos == other.person_pos)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self):
        return "Solver({0}, {1})".format(self.direction, self.person_pos)


class Field:
    NUMBER_OF_ROADS = 11
    FIRST_ROAD_SPEED = 5
    FIRST_ROAD_DISTANCE = 18

    def __init__(self, car_positions):
        super().__init__()
        self.roads = []
        for ndx in range(Field.NUMBER_OF_ROADS):
            pos = car_positions[ndx] if len(car_positions) > ndx else 0
            self.roads.append(pos)
        self.solvers = self.generate_new_solvers(0)

    def make_a_move(self):
        for solver in self.solvers:
            solver.move(self)
        # move cars
        speed = Field.FIRST_ROAD_SPEED
        distance = Field.FIRST_ROAD_DISTANCE
        for ndx in range(Field.NUMBER_OF_ROADS):
            self.roads[ndx] -= speed
            if self.roads[ndx] < 0:
                self.roads[ndx] += distance
            speed += 1
            distance += 1

    def is_hit_on_next(self, road_number):
        return (road_number < 0) or (road_number < Field.NUMBER_OF_ROADS and (self.roads[road_number] >= 0 and self.roads[road_number] - Field.speed_of(road_number) <= 0))

    @staticmethod
    def speed_of(road_number):
        return Field.FIRST_ROAD_SPEED + road_number

    def get_allowed_moves(self, person_pos):
        free_directions = []
        if not self.is_hit_on_next(person_pos + 1):
            free_directions.append(1)
        if not self.is_hit_on_next(person_pos):
            free_directions.append(0)
        if not self.is_hit_on_next(person_pos - 1):
            free_directions.append(-1)
        return free_directions

    def generate_new_solvers(self, person_pos):
        new_solvers = set()
        for possible_move in self.get_allowed_moves(person_pos):
            new_solvers.add(Solver(possible_move, person_pos))
        return new_solvers

    @staticmethod
    def solve(x_field):
        iteration = 1
        new_solvers = set()
        while True:
            x_field.make_a_move()
            for solver in x_field.solvers:
                if solver.person_pos >= Field.NUMBER_OF_ROADS:
                    return iteration
                new_solvers.update(x_field.generate_new_solvers(solver.person_pos))

            if len(new_solvers) == 0:
                return SOLUTION_DOESNT_EXIST

            x_field.solvers = list(new_solvers)
            new_solvers = set()
            iteration += 1


if __name__ == '__main__':
    with open('/home/ipatrikeev/dev/input.txt') as f:
        case_number = int(f.readline())
        for round in range(case_number):
            car_positions = [int(pos) for pos in f.readline().split()]
            field = Field(car_positions)
            print(Field.solve(field), end=' ')
