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
        self.person_pos = 0
        self.move_counter = 0

    def make_move(self, direction):
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
        return (road_number >= Field.NUMBER_OF_ROADS) or (self.roads[road_number] - Field.speed_of(road_number) <= 0)

    @staticmethod
    def speed_of(road_number):
        return Field.FIRST_ROAD_SPEED + road_number - 1

    def __str__(self):
        return ' '.join(str(pos) for pos in self.roads)

    def solve(self, direction):
        while self.person_pos < Field.NUMBER_OF_ROADS:
            if not self.is_hit_on_next(self.person_pos + 1):
                self.make_move(1)
            elif not field.is_hit_on_next(self.person_pos):
                self.make_move(0)
            else:
                if field.is_hit_on_next(self.person_pos - 1):
                    return SOLUTION_DOESNT_EXIST
                field.make_move(-1)




SOLUTION_DOESNT_EXIST = -1


def has_more_than_one_way(field):
    result = 0
    if not field.is_hit_on_next(field.person_pos + 1):
        result += 1
    if not field.is_hit_on_next(field.person_pos):
        result += 1
    if not field.is_hit_on_next(field.person_pos -1):
        result += 1
    return True if result > 1 else False


if __name__ == '__main__':
    with open('/home/ipatrikeev/dev/code_abbey/input.txt') as f:
        case_number = int(f.readline())
        for round in range(case_number):
            car_positions = [int(pos) for pos in f.readline().split()]
            field = Field(car_positions)
            try:
                while field.person_pos < Field.NUMBER_OF_ROADS:
                    if has_more_than_one_way(field):
                        print('more than 1 way!')

                    if not field.is_hit_on_next(field.person_pos + 1):
                        field.make_move(1)
                    elif not field.is_hit_on_next(field.person_pos):
                        field.make_move(0)
                    else:
                        if field.is_hit_on_next(field.person_pos - 1):
                            field.move_counter = SOLUTION_DOESNT_EXIST
                            break
                        field.make_move(-1)
            except ValueError:
                pass
            print(field.move_counter, end=' ')
