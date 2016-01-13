SOLUTION_DOESNT_EXIST = -1

class Field:
    NUMBER_OF_ROADS = 11
    FIRST_ROAD_SPEED = 5
    FIRST_ROAD_DISTANCE = 18

    def __init__(self, car_positions, person_pos = 0):
        super().__init__()
        self.roads = []
        for ndx in range(Field.NUMBER_OF_ROADS):
            pos = car_positions[ndx] if len(car_positions) > ndx else 0
            self.roads.append(pos)
        self.person_pos = person_pos
        self.move_counter = 0

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
        return (road_number < 0) or (road_number < Field.NUMBER_OF_ROADS and (self.roads[road_number] - Field.speed_of(road_number) <= 0))

    @staticmethod
    def speed_of(road_number):
        return Field.FIRST_ROAD_SPEED + road_number - 1

    def __str__(self):
        return ' '.join(str(pos) for pos in self.roads)

    def get_allowed_moves(self):
        free_directions = []
        if not self.is_hit_on_next(self.person_pos + 1):
            free_directions.append(1)
        if not self.is_hit_on_next(self.person_pos):
            free_directions.append(0)
        if not self.is_hit_on_next(self.person_pos -1):
            free_directions.append(-1)
        return free_directions

    @staticmethod
    def solve2(x_field):
        solutions = []
        for direction in sorted(x_field.get_allowed_moves(), reverse=True):
            field = Field(x_field.roads, x_field.person_pos)
            field.make_a_move(direction)
            if field.person_pos >= Field.NUMBER_OF_ROADS:
                solutions.append(field.move_counter + x_field.move_counter)
            else:
                solutions.append(Field.solve2(field) + field.move_counter)

        return min(solutions) if len(solutions) > 0 else -1


if __name__ == '__main__':
    with open('W:\\input.txt') as f:
        case_number = int(f.readline())
        for round in range(case_number):
            car_positions = [int(pos) for pos in f.readline().split()]
            field = Field(car_positions)

            print(Field.solve2(field), end=' ')
