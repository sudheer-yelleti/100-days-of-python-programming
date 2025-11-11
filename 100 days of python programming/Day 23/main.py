import time
from turtle import Screen

from car_manager import CarManager
from player import Player
from scoreboard import Scoreboard

COLLISION_DISTANCE = 20
screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)
screen.listen()

player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()
screen.onkey(fun=player.move, key="Up")

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()

    car_manager.create_car()
    car_manager.move_cars()

    # Detect player collision with the car.
    for car in car_manager.all_cars:
        if player.distance(car) <= COLLISION_DISTANCE:
            game_is_on = False
            scoreboard.game_over()

    # Detect if the player successfully made it to the other side without hitting any cars
    if player.is_player_at_finish_line():
        player.reset_player_position()
        car_manager.level_up()
        scoreboard.update_level()

screen.exitonclick()
