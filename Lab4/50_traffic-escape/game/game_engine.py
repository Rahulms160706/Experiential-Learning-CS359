import json
import os
import pygame
import random
from game.player import Player,LANE_W
from game.traffic import make_car,make_logs

LANES=8
WIDTH=LANES*LANE_W
HEIGHT=600
FPS=60
BG=(60,60,60)
HUD_H=30
SIDEWALK_H=50

# Feature 1: lives
START_LIVES=3
INVULN_FRAMES=90          # brief protection from cars after losing a life

# Feature 2: river lane with logs
RIVER_TOP=240
RIVER_H=80
RIVER_BOTTOM=RIVER_TOP+RIVER_H
LOG_W=160
LOG_COUNT=3
LOG_SPEED=2               # pixels per frame, moving right

# Feature 3: high scores
SCORE_FILE=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"highscores.json")
MAX_SCORES=5
WIN_BONUS=100             # extra points for reaching the top

# Feature 4: day/night
CYCLE_FRAMES=30*FPS       # 30 seconds
NIGHT_BEAM=170            # headlight length at night (pixels)

def load_scores():
    """Read the saved top scores; a missing or damaged file just means no scores."""
    try:
        with open(SCORE_FILE) as f:
            data=json.load(f)
        scores=[s for s in data if isinstance(s,int) and not isinstance(s,bool)]
        return sorted(scores,reverse=True)[:MAX_SCORES]
    except (OSError,ValueError,TypeError):
        return []

def save_scores(scores):
    try:
        with open(SCORE_FILE,"w") as f:
            json.dump(scores,f)
    except OSError:
        pass

def in_river(rect):
    return RIVER_TOP<=rect.centery<RIVER_BOTTOM

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Traffic Escape")
        self.clock=pygame.time.Clock()
        self.font=pygame.font.SysFont("monospace",24,bold=True)
        self.big_font=pygame.font.SysFont("monospace",44,bold=True)
        self.night_overlay=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        self.night_overlay.fill((5,10,40,150))
        self.light_layer=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        self.high_scores=load_scores()
        self.reset()

    def reset(self):
        self.player=Player(WIDTH//2,HEIGHT-80)
        self.cars=[]
        self.logs=make_logs(RIVER_TOP+10,RIVER_H-20,LOG_COUNT,LOG_SPEED,WIDTH,LOG_W)
        self.timer=0
        self.spawn_interval=50
        self.speed=3
        self.score=0
        self.lives=START_LIVES
        self.invuln=0
        self.is_night=False
        self.cycle_timer=0
        self.rank=None
        self.game_over=False
        self.won=False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: return False
            if event.type==pygame.KEYDOWN and event.key==pygame.K_r: self.reset()
        return True

    def lose_life(self):
        self.lives-=1
        if self.lives<=0:
            self.game_over=True
            self.finish()
        else:
            # back to the start line, briefly immune to cars
            self.player=Player(WIDTH//2,HEIGHT-80)
            self.invuln=INVULN_FRAMES

    def finish(self):
        """Run ended: record the score in the persistent top 5."""
        points=self.score//10
        if points>0:
            self.high_scores.append(points)
            self.high_scores.sort(reverse=True)
            del self.high_scores[MAX_SCORES:]
            if points in self.high_scores:
                self.rank=self.high_scores.index(points)
            save_scores(self.high_scores)

    def update(self):
        if self.game_over or self.won: return
        keys=pygame.key.get_pressed()
        # keep the player inside the window: horizontally 0..WIDTH, vertically
        # from the top edge down to the start line (top of the bottom sidewalk)
        self.player.move(keys,0,WIDTH,0,HEIGHT-SIDEWALK_H)

        # day/night: flip every 30 seconds
        self.cycle_timer+=1
        if self.cycle_timer>=CYCLE_FRAMES:
            self.cycle_timer=0
            self.is_night=not self.is_night

        self.timer+=1
        if self.timer>=self.spawn_interval:
            lane=random.randint(0,LANES-1)
            car=make_car(lane,HEIGHT,self.speed)
            # don't spawn on top of a car that is still near the spawn point
            if not any(car.rect.inflate(0,60).colliderect(c.rect) for c in self.cars):
                self.cars.append(car)
                self.timer=0
                self.spawn_interval=max(22,self.spawn_interval-0.2)

        hit=False

        # river: while in the water lane the player must be standing on a log
        on_river=in_river(self.player.rect)
        log_under=None
        if on_river:
            for lg in self.logs:
                if lg.rect.left<=self.player.rect.centerx<=lg.rect.right:
                    log_under=lg
                    break
        for lg in self.logs: lg.update(WIDTH)
        if on_river:
            if log_under:
                r=self.player.rect      # the log carries the player along
                r.x=max(0,min(WIDTH-r.width,r.x+log_under.speed))
            else:
                hit=True                # fell in the water
        else:
            self.player.snap_to_lane()  # back on the road: line up with a lane again

        if self.invuln>0: self.invuln-=1
        for c in self.cars:
            c.update()
            # cars pass under the river, so they can't hit anyone while inside it
            if (not on_river and self.invuln==0 and not in_river(c.rect)
                    and c.rect.colliderect(self.player.rect)):
                hit=True
        self.cars=[c for c in self.cars if not c.off_screen(HEIGHT)]
        self.score+=1
        if self.score%300==0: self.speed=min(10,self.speed+0.5)

        if hit: self.lose_life()
        # a crash on the same frame as reaching the top counts as a crash
        if not self.game_over and self.player.rect.top<=10:
            self.won=True
            self.score+=WIN_BONUS*10   # score is stored x10 (HUD shows score//10)
            self.finish()

    def draw_river(self):
        pygame.draw.rect(self.screen,(40,110,190),pygame.Rect(0,RIVER_TOP,WIDTH,RIVER_H))
        for y in (RIVER_TOP+4,RIVER_BOTTOM-6):
            pygame.draw.line(self.screen,(90,160,230),(0,y),(WIDTH,y),2)
        for lg in self.logs: lg.draw(self.screen)

    def draw(self):
        self.screen.fill(BG)
        # road markings
        for i in range(LANES+1):
            pygame.draw.line(self.screen,(100,100,100),(i*LANE_W,0),(i*LANE_W,HEIGHT),2)
        for y in range(0,HEIGHT,60):
            for i in range(LANES):
                pygame.draw.rect(self.screen,(200,200,100),pygame.Rect(i*LANE_W+LANE_W//2-3,y,6,30))
        # sidewalks
        pygame.draw.rect(self.screen,(150,130,110),pygame.Rect(0,HEIGHT-SIDEWALK_H,WIDTH,SIDEWALK_H))
        pygame.draw.rect(self.screen,(150,130,110),pygame.Rect(0,0,WIDTH,HUD_H))
        for c in self.cars: c.draw(self.screen)
        self.draw_river()   # drawn over the cars: they drive under the water lane
        if self.is_night:
            self.screen.blit(self.night_overlay,(0,0))
            self.light_layer.fill((0,0,0,0))
            for c in self.cars:
                if not in_river(c.rect): c.draw_beam(self.light_layer,NIGHT_BEAM)
            self.screen.blit(self.light_layer,(0,0))
        # blink while protected after losing a life
        if self.invuln==0 or (self.invuln//6)%2==0:
            self.player.draw(self.screen)
        hud=pygame.Rect(0,0,WIDTH,HUD_H)
        pygame.draw.rect(self.screen,(20,20,20),hud)
        best=max(self.high_scores[0] if self.high_scores else 0,self.score//10)
        s=self.font.render(f"Score: {self.score//10}  Best: {best}  R=Restart",True,(220,220,220))
        self.screen.blit(s,(6,4))
        for i in range(self.lives):
            pygame.draw.circle(self.screen,(220,60,60),(WIDTH-20-i*26,HUD_H//2),9)
        if self.game_over:
            self._msg("GAME OVER",(220,60,60))
        elif self.won:
            self._msg("YOU MADE IT!",(80,220,80))
        pygame.display.flip()

    def _msg(self,text,color):
        ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        ov.fill((0,0,0,170))
        self.screen.blit(ov,(0,0))
        m=self.big_font.render(text,True,color)
        self.screen.blit(m,(WIDTH//2-m.get_width()//2,100))
        yours=self.font.render(f"Your score: {self.score//10}",True,(220,220,220))
        self.screen.blit(yours,(WIDTH//2-yours.get_width()//2,165))
        head=self.font.render("TOP 5",True,(240,200,60))
        self.screen.blit(head,(WIDTH//2-head.get_width()//2,215))
        if not self.high_scores:
            line=self.font.render("No scores yet",True,(160,160,160))
            self.screen.blit(line,(WIDTH//2-line.get_width()//2,255))
        for i,pts in enumerate(self.high_scores):
            col=(255,230,80) if i==self.rank else (200,200,200)
            line=self.font.render(f"{i+1}. {pts}",True,col)
            self.screen.blit(line,(WIDTH//2-line.get_width()//2,255+i*30))
        sub=self.font.render("Press R to Restart",True,(200,200,200))
        self.screen.blit(sub,(WIDTH//2-sub.get_width()//2,440))

    def run(self):
        running=True
        while running:
            running=self.handle_events()
            if not running: break
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()