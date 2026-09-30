import pygame
import random

LANE_W=80
COLORS=[(220,60,60),(220,140,40),(140,60,180),(60,180,80),(180,180,40),(60,80,200)]

class Car:
    def __init__(self, lane_x, y, direction, speed):
        self.rect=pygame.Rect(lane_x+10,y,60,80)
        self.y=float(y)   # exact position; Rect only stores whole pixels
        self.direction=direction  # 1=down, -1=up
        self.speed=speed
        self.color=random.choice(COLORS)

    def update(self):
        self.y+=self.direction*self.speed
        self.rect.y=round(self.y)

    def off_screen(self,height):
        return self.rect.top>height+100 or self.rect.bottom<-100

    def draw(self,screen):
        pygame.draw.rect(screen,self.color,self.rect,border_radius=8)
        pygame.draw.rect(screen,(180,220,240),pygame.Rect(self.rect.x+8,self.rect.y+10,44,22),border_radius=4)
        for wx in [self.rect.x+6,self.rect.right-16]:
            for wy in [self.rect.y+4,self.rect.bottom-16]:
                pygame.draw.rect(screen,(30,30,30),pygame.Rect(wx,wy,10,12),border_radius=3)
        # headlights on the front of the car (front = bottom when driving down)
        ly=self.rect.bottom-6 if self.direction==1 else self.rect.top+2
        for lx in [self.rect.x+16,self.rect.right-26]:
            pygame.draw.rect(screen,(255,240,150),pygame.Rect(lx,ly,10,4),border_radius=2)

    def draw_beam(self,surface,length):
        """Draw a translucent light cone `length` pixels ahead of the car."""
        r=self.rect
        if self.direction==1:
            y0,y1=r.bottom,r.bottom+length
        else:
            y0,y1=r.top,r.top-length
        pts=[(r.x+16,y0),(r.right-16,y0),(r.right+10,y1),(r.x-10,y1)]
        pygame.draw.polygon(surface,(255,240,150,90),pts)

def make_car(lane_idx,height,speed):
    x=lane_idx*LANE_W
    direction=1 if lane_idx%2==0 else -1
    y=-90 if direction==1 else height+10
    return Car(x,y,direction,speed)

class Log:
    def __init__(self, x, y, width, height, speed):
        self.rect=pygame.Rect(x,y,width,height)
        self.speed=speed   # whole pixels per frame; >0 = moves right

    def update(self, screen_w):
        self.rect.x+=self.speed
        ring=screen_w+self.rect.width   # loop length: log re-enters just off-screen
        if self.speed>0 and self.rect.left>=screen_w: self.rect.x-=ring
        elif self.speed<0 and self.rect.right<=0: self.rect.x+=ring

    def draw(self,screen):
        pygame.draw.rect(screen,(120,80,40),self.rect,border_radius=10)
        pygame.draw.rect(screen,(85,55,25),self.rect,3,border_radius=10)
        for x in range(self.rect.x+25,self.rect.right-10,30):
            pygame.draw.line(screen,(85,55,25),(x,self.rect.y+8),(x,self.rect.bottom-8),2)

def make_logs(y,height,count,speed,screen_w,log_w):
    """`count` evenly spaced logs on one looping row."""
    gap=(screen_w+log_w)//count
    return [Log(i*gap-log_w,y,log_w,height,speed) for i in range(count)]