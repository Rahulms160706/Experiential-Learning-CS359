import pygame

SPEED=4
LANE_W=80
FORWARD_SPEED=8      # pixels per frame when moving up/down
LANE_COOLDOWN=12     # frames between lane changes

class Player:
    def __init__(self, x, y):
        self.rect=pygame.Rect(x-20,y-30,40,60)
        self.color=(60,160,220)
        self.move_cooldown=0
        # Snap to the middle of the lane that contains x so the car always
        # sits inside a lane, never straddling a lane line.
        self._snap_to_lane(x//LANE_W)

    def _snap_to_lane(self, lane):
        self.rect.centerx=lane*LANE_W+LANE_W//2

    def snap_to_lane(self):
        """Re-centre the car in whichever lane it is currently in (used after leaving a log)."""
        self._snap_to_lane(self.rect.centerx//LANE_W)

    def move(self, keys, min_x, max_x, min_y, max_y):
        """min_x/max_x bound the play area horizontally, min_y/max_y vertically."""
        # Vertical movement is always allowed (not blocked by the lane cooldown)
        dy=0
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy-=FORWARD_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy+=FORWARD_SPEED
        if dy:
            self.rect.y=max(min_y,min(max_y-self.rect.height,self.rect.y+dy))

        # Lane changes: one lane per key press, then a short cooldown
        if self.move_cooldown>0:
            self.move_cooldown-=1
            return
        step=0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: step-=1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: step+=1
        if step:
            lane=self.rect.centerx//LANE_W
            first_lane=min_x//LANE_W
            last_lane=max_x//LANE_W-1
            new_lane=max(first_lane,min(last_lane,lane+step))
            if new_lane!=lane:
                self._snap_to_lane(new_lane)
                self.move_cooldown=LANE_COOLDOWN

    def draw(self,screen):
        # car body
        pygame.draw.rect(screen,self.color,self.rect,border_radius=8)
        # windows
        pygame.draw.rect(screen,(180,220,240),pygame.Rect(self.rect.x+6,self.rect.y+8,28,18),border_radius=4)
        # wheels
        for wx in [self.rect.x+4,self.rect.right-12]:
            for wy in [self.rect.y+4,self.rect.bottom-14]:
                pygame.draw.rect(screen,(30,30,30),pygame.Rect(wx,wy,8,10),border_radius=3)