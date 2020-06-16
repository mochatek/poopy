import arcade
import random

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
TITLE = "Poopy"
SCALE = 0.5
POOP_SCALE = 0.25
PLAYER_SPEED = 8
POS_X = [96.0, 224.0, 416.0, 544.0]

class Poop(arcade.Sprite):
    def __init__(self, img, score):
        super().__init__(img)
        self.scale = POOP_SCALE
        self.center_x = random.choice(POS_X)
        self.center_y = 380.0
        self.change_y = random.randint(-4, -2)
        self.score = score

    def update(self):
        if self.bottom < 130:
            self.remove_from_sprite_lists()
        else:
            self.center_y += self.change_y

class Player(arcade.Sprite):
    def __init__(self, obj):
        super().__init__("res\Toilet.png", SCALE)
        self.sprite_lists = obj.sprite_lists
        self._texture = obj._texture
        self.textures = obj.textures
        self._points = obj._points
        self.texture_transform = obj.texture_transform
        self.center_x = 320
        self.center_y = 160
        self.change_x = 0

    def update(self):
        self.center_x += self.change_x
        if self.left <= 16:
            self.left = 16
        elif self.right >= 624:
            self.right = 624


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
        self.background = None
        self.score = None
        self.player = None
        self.player_list = None
        self.baby_list = None
        self.wall_list = None
        self.poop_list = None
        self.frame_count = None
        self.pos_x = None
        self.poop_types = ["res\smile_poop.png", "res\Angry_poop.png"]
        self.poop_sound = None
        self.collect_sound = None

    def setup(self):
        self.background = arcade.load_texture('res\BG.png')
        self.score = 0
        self.frame_count = 0
        self.baby_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.poop_list = arcade.SpriteList()
        map = arcade.tilemap.read_tmx("map.tmx")
        self.player = Player(arcade.tilemap.process_layer(map,'Toilet', SCALE)[0])
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        self.baby_list = arcade.tilemap.process_layer(map,'Baby', SCALE)
        self.wall_list = arcade.tilemap.process_layer(map,'Platform', SCALE)
        self.poop_sound = arcade.load_sound("res\hurt1.wav")

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.wall_list.draw()
        self.player_list.draw()
        self.poop_list.draw()
        self.baby_list.draw()

        score = "SCORE : {}".format(self.score)
        arcade.draw_text(score, 270, 600, arcade.color.DARK_CYAN, 20, bold=True)

    def on_update(self,delta_time):
        self.player_list.update()
        self.poop_list.update()
        self.frame_count += 1
        if self.frame_count > 60:
            ind = random.randint(0, 1)
            if ind == 0:
                score = 5
            else:
                score = -3
            poop = Poop(self.poop_types[ind], score)
            self.poop_list.append(poop)
            arcade.play_sound(self.poop_sound)
            self.frame_count = 0
        catch_list = arcade.check_for_collision_with_list(self.player, self.poop_list)
        for poop in catch_list:
            self.score += poop.score
            poop.remove_from_sprite_lists()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.RIGHT:
            self.player.change_x = PLAYER_SPEED
        elif symbol == arcade.key.LEFT:
            self.player.change_x = -PLAYER_SPEED

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.RIGHT or symbol == arcade.key.LEFT:
            self.player.change_x = 0

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()