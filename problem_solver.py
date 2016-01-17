SOLUTION_DOESNT_EXIST = -1


class Field:
    the_solution = 999999
    entries = 0
    ways = 0
    NUMBER_OF_ROADS = 11
    FIRST_ROAD_SPEED = 5
    FIRST_ROAD_DISTANCE = 18

    def __init__(self, car_positions, person_pos=0, move_counter=0):
        super().__init__()
        self.roads = []
        for ndx in range(Field.NUMBER_OF_ROADS):
            pos = car_positions[ndx] if len(car_positions) > ndx else 0
            self.roads.append(pos)
        self.person_pos = person_pos
        self.move_counter = move_counter

    def make_a_move(self, direction):
        self.person_pos += direction
        self.move_counter += 1
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
        return (road_number < 0) or (
            road_number < Field.NUMBER_OF_ROADS and (self.roads[road_number] - Field.speed_of(road_number) <= 0))

    @staticmethod
    def speed_of(road_number):
        return Field.FIRST_ROAD_SPEED + road_number - 1

    def __str__(self):
        return 'person_pos=' + str(self.person_pos) + ', move_counter=' + str(self.move_counter) + ' ' + ' '.join(
                str(pos) for pos in self.roads)

    def get_allowed_moves(self):
        free_directions = []
        if not self.is_hit_on_next(self.person_pos + 1):
            free_directions.append(1)
        if not self.is_hit_on_next(self.person_pos):
            free_directions.append(0)
        if not self.is_hit_on_next(self.person_pos - 1):
            free_directions.append(-1)
        return free_directions

    @staticmethod
    def solve(x_field):
        for direction in x_field.get_allowed_moves():
            field = Field(x_field.roads, x_field.person_pos)
            field.make_a_move(direction)
            if field.person_pos >= Field.NUMBER_OF_ROADS:
                return field.move_counter + x_field.move_counter
            else:
                return Field.solve(field) + field.move_counter
        return SOLUTION_DOESNT_EXIST

    @staticmethod
    def solve2(x_field):
        solutions = []
        for direction in x_field.get_allowed_moves():
            solution = Field.solve(x_field)
            if solution > 0:
                solutions.append(solution)
        return min(solutions) if len(solutions) > 0 else -1

    @staticmethod
    def solve3(x_field):
        if x_field.move_counter > 100:
            return -1
        allowed_directions = x_field.get_allowed_moves()
        new_field = x_field
        for direction in allowed_directions:
            if len(x_field.solutions) != 0 and x_field.move_counter > min(x_field.solutions):
                return -1
            if len(allowed_directions) > 1:
                new_field = Field(x_field.roads, x_field.person_pos, x_field.move_counter, x_field.solutions)
            new_field.make_a_move(direction)
            if new_field.person_pos >= Field.NUMBER_OF_ROADS:
                new_field.solutions.append(new_field.move_counter)
            else:
                solution = Field.solve3(new_field)
                if solution >= 0:
                    new_field.solutions.append(solution)
        return min(new_field.solutions) if len(new_field.solutions) > 0 else -1

    @staticmethod
    def solve4(x_field):
        Field.entries += 1
        if Field.the_solution != -1 and x_field.move_counter + 1 >= Field.the_solution: return
        allowed_moves = x_field.get_allowed_moves()
        Field.ways += len(allowed_moves)
        for move in allowed_moves:
            new_field = Field(x_field.roads, x_field.person_pos, x_field.move_counter)
            new_field.make_a_move(move)
            if new_field.person_pos >= Field.NUMBER_OF_ROADS:
                if new_field.person_pos < Field.the_solution:
                    Field.the_solution = new_field.move_counter
                    print(new_field)
            else:
                Field.solve4(new_field)
                # if solution >= 0:
                #     print(new_field)
                #     solutions.append(solution)
                # return min(solutions) if len(solutions) > 0 else -1


if __name__ == '__main__':
    with open('/home/ipatrikeev/dev/input.txt') as f:
        case_number = int(f.readline())
        for round in range(case_number):
            car_positions = [int(pos) for pos in f.readline().split()]
            field = Field(car_positions)
            Field.solve4(field)
            print(Field.the_solution, end=' ')
