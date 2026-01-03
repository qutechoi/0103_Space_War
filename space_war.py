#!/usr/bin/env python3
"""
Space War - Galaga Style Shooting Game
클래식 갤러그 스타일의 우주선 슈팅 게임
"""

import pygame
import random
import math
import sys
import array

# 게임 초기화
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# 상수 정의
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# 게임 설정
PLAYER_SPEED = 5
BULLET_SPEED = 7
ENEMY_BULLET_SPEED = 4
ENEMY_SPEED = 2

# 파워업 타입 - 새로운 시스템
POWERUP_TYPES = {
    'SINGLE': {'color': (100, 200, 255), 'name': '일반탄', 'emoji': '💙', 'duration': 0},
    'DOUBLE': {'color': (0, 255, 255), 'name': '더블샷', 'emoji': '💚', 'duration': 10},
    'TRIPLE': {'color': (255, 165, 0), 'name': '트리플샷', 'emoji': '🧡', 'duration': 10},
    'MISSILE': {'color': (255, 100, 100), 'name': '유도탄', 'emoji': '🔴', 'duration': 10},
    'MISSILE_DOUBLE': {'color': (255, 50, 150), 'name': '2발 유도탄', 'emoji': '💗', 'duration': 10},
    'MISSILE_TRIPLE': {'color': (200, 0, 200), 'name': '3발 유도탄', 'emoji': '💜', 'duration': 10},
    'FLAMETHROWER': {'color': (255, 100, 0), 'name': '화염방사기', 'emoji': '🔥', 'duration': 10},
    'SMART_MISSILE': {'color': (255, 215, 0), 'name': '스마트미사일', 'emoji': '⭐', 'duration': 999},
}

# 총알 타입
BULLET_NORMAL = 0
BULLET_DOUBLE = 1
BULLET_TRIPLE = 2
BULLET_MISSILE = 3
BULLET_MISSILE_DOUBLE = 4
BULLET_MISSILE_TRIPLE = 5
BULLET_FLAMETHROWER = 6
BULLET_SMART_MISSILE = 7

# 색상 추가
ORANGE = (255, 165, 0)
PURPLE = (255, 0, 255)
LIGHT_GREEN = (0, 255, 128)
PINK = (255, 100, 100)
LIGHT_YELLOW = (255, 255, 100)
LIGHT_CYAN = (128, 255, 255)


class SoundManager:
    """사운드 관리 클래스"""

    def __init__(self):
        self.sounds = {}
        self.create_sounds()

    def create_tone(self, frequency, duration, volume=0.1):
        """특정 주파수의 톤 생성"""
        sample_rate = 22050
        n_samples = int(round(duration * sample_rate))

        # 사인파 생성
        buf = array.array('h')
        max_sample = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
        for i in range(n_samples):
            sample = int(max_sample * volume * math.sin(2 * math.pi * frequency * i / sample_rate))
            buf.append(sample)
            buf.append(sample)  # 스테레오

        sound = pygame.mixer.Sound(buffer=buf)
        return sound

    def create_shoot_sound(self):
        """총알 발사 사운드 생성"""
        sample_rate = 22050
        duration = 0.1
        n_samples = int(round(duration * sample_rate))

        buf = array.array('h')
        max_sample = 2 ** 14

        for i in range(n_samples):
            # 주파수가 감소하는 효과
            freq = 800 - (i / n_samples) * 400
            volume = 0.3 * (1 - i / n_samples)
            sample = int(max_sample * volume * math.sin(2 * math.pi * freq * i / sample_rate))
            buf.append(sample)
            buf.append(sample)

        return pygame.mixer.Sound(buffer=buf)

    def create_explosion_sound(self):
        """폭발 사운드 생성"""
        sample_rate = 22050
        duration = 0.3
        n_samples = int(round(duration * sample_rate))

        buf = array.array('h')
        max_sample = 2 ** 14

        for i in range(n_samples):
            # 노이즈 기반 폭발음
            volume = 0.4 * (1 - i / n_samples)
            sample = int(max_sample * volume * (random.random() * 2 - 1))
            buf.append(sample)
            buf.append(sample)

        return pygame.mixer.Sound(buffer=buf)

    def create_hit_sound(self):
        """적 명중 사운드 생성"""
        sample_rate = 22050
        duration = 0.15
        n_samples = int(round(duration * sample_rate))

        buf = array.array('h')
        max_sample = 2 ** 14

        for i in range(n_samples):
            freq = 1200 - (i / n_samples) * 800
            volume = 0.25 * (1 - i / n_samples)
            sample = int(max_sample * volume * math.sin(2 * math.pi * freq * i / sample_rate))
            buf.append(sample)
            buf.append(sample)

        return pygame.mixer.Sound(buffer=buf)

    def create_game_over_sound(self):
        """게임 오버 사운드 생성"""
        sample_rate = 22050
        duration = 0.5
        n_samples = int(round(duration * sample_rate))

        buf = array.array('h')
        max_sample = 2 ** 14

        for i in range(n_samples):
            # 하강하는 톤
            freq = 400 - (i / n_samples) * 300
            volume = 0.3
            sample = int(max_sample * volume * math.sin(2 * math.pi * freq * i / sample_rate))
            buf.append(sample)
            buf.append(sample)

        return pygame.mixer.Sound(buffer=buf)

    def create_level_up_sound(self):
        """레벨업 사운드 생성"""
        sample_rate = 22050
        duration = 0.3
        n_samples = int(round(duration * sample_rate))

        buf = array.array('h')
        max_sample = 2 ** 14

        for i in range(n_samples):
            # 상승하는 톤
            freq = 400 + (i / n_samples) * 400
            volume = 0.25 * (1 - i / n_samples * 0.5)
            sample = int(max_sample * volume * math.sin(2 * math.pi * freq * i / sample_rate))
            buf.append(sample)
            buf.append(sample)

        return pygame.mixer.Sound(buffer=buf)

    def create_powerup_sound(self):
        """파워업 획득 사운드 생성"""
        sample_rate = 22050
        duration = 0.2
        n_samples = int(round(duration * sample_rate))

        buf = array.array('h')
        max_sample = 2 ** 14

        for i in range(n_samples):
            # 상승하는 아르페지오
            progress = i / n_samples
            freq = 600 + math.sin(progress * math.pi * 8) * 200
            volume = 0.2 * (1 - progress * 0.5)
            sample = int(max_sample * volume * math.sin(2 * math.pi * freq * i / sample_rate))
            buf.append(sample)
            buf.append(sample)

        return pygame.mixer.Sound(buffer=buf)

    def create_sounds(self):
        """모든 사운드 생성"""
        try:
            self.sounds['shoot'] = self.create_shoot_sound()
            self.sounds['explosion'] = self.create_explosion_sound()
            self.sounds['hit'] = self.create_hit_sound()
            self.sounds['game_over'] = self.create_game_over_sound()
            self.sounds['level_up'] = self.create_level_up_sound()
            self.sounds['powerup'] = self.create_powerup_sound()
        except Exception as e:
            print(f"사운드 생성 오류: {e}")
            # 사운드 생성 실패 시 빈 딕셔너리 유지
            self.sounds = {}

    def play(self, sound_name):
        """사운드 재생"""
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except:
                pass


class PowerUp(pygame.sprite.Sprite):
    """파워업 아이템 클래스"""

    def __init__(self, x, y, font=None):
        super().__init__()
        # 랜덤하게 파워업 타입 선택 (SINGLE 제외)
        available_types = [k for k in POWERUP_TYPES.keys() if k != 'SINGLE']
        self.powerup_type = random.choice(available_types)
        self.powerup_info = POWERUP_TYPES[self.powerup_type]

        # 배경 원 생성
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)

        # 배경 원 그리기
        pygame.draw.circle(self.image, self.powerup_info['color'] + (200,), (20, 20), 18)
        pygame.draw.circle(self.image, WHITE, (20, 20), 18, 2)

        # 심볼/도형으로 파워업 표시
        self.draw_powerup_symbol()

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed_y = 2

    def draw_powerup_symbol(self):
        """파워업 타입별 심볼 그리기"""
        center_x, center_y = 20, 20

        if self.powerup_type == 'DOUBLE':
            # 💚 더블샷: 두 개의 작은 원
            pygame.draw.circle(self.image, WHITE, (center_x - 5, center_y), 4)
            pygame.draw.circle(self.image, WHITE, (center_x + 5, center_y), 4)

        elif self.powerup_type == 'TRIPLE':
            # 🧡 트리플샷: 세 개의 작은 원
            pygame.draw.circle(self.image, WHITE, (center_x - 6, center_y), 3)
            pygame.draw.circle(self.image, WHITE, (center_x, center_y), 3)
            pygame.draw.circle(self.image, WHITE, (center_x + 6, center_y), 3)

        elif self.powerup_type == 'MISSILE':
            # 🔴 유도탄: 화살표
            pygame.draw.polygon(self.image, WHITE, [
                (center_x, center_y - 8),
                (center_x - 6, center_y + 4),
                (center_x, center_y),
                (center_x + 6, center_y + 4)
            ])

        elif self.powerup_type == 'MISSILE_DOUBLE':
            # 💗 2발 유도탄: 두 개의 작은 화살표
            pygame.draw.polygon(self.image, WHITE, [
                (center_x - 5, center_y - 6),
                (center_x - 8, center_y + 2),
                (center_x - 5, center_y),
                (center_x - 2, center_y + 2)
            ])
            pygame.draw.polygon(self.image, WHITE, [
                (center_x + 5, center_y - 6),
                (center_x + 2, center_y + 2),
                (center_x + 5, center_y),
                (center_x + 8, center_y + 2)
            ])

        elif self.powerup_type == 'MISSILE_TRIPLE':
            # 💜 3발 유도탄: 세 개의 작은 화살표
            for i, offset in enumerate([-7, 0, 7]):
                pygame.draw.polygon(self.image, WHITE, [
                    (center_x + offset, center_y - 6),
                    (center_x + offset - 3, center_y + 2),
                    (center_x + offset, center_y),
                    (center_x + offset + 3, center_y + 2)
                ])

        elif self.powerup_type == 'FLAMETHROWER':
            # 🔥 화염방사기: 불꽃 모양
            # 외부 불꽃
            pygame.draw.polygon(self.image, YELLOW, [
                (center_x, center_y - 8),
                (center_x - 6, center_y + 4),
                (center_x - 3, center_y),
                (center_x, center_y + 6),
                (center_x + 3, center_y),
                (center_x + 6, center_y + 4)
            ])
            # 내부 불꽃
            pygame.draw.polygon(self.image, WHITE, [
                (center_x, center_y - 4),
                (center_x - 3, center_y + 2),
                (center_x, center_y + 2),
                (center_x + 3, center_y + 2)
            ])

        elif self.powerup_type == 'SMART_MISSILE':
            # ⭐ 스마트미사일: 별 모양
            points = []
            for i in range(10):
                angle = math.pi * 2 * i / 10 - math.pi / 2
                if i % 2 == 0:
                    radius = 10
                else:
                    radius = 5
                px = center_x + math.cos(angle) * radius
                py = center_y + math.sin(angle) * radius
                points.append((px, py))
            pygame.draw.polygon(self.image, YELLOW, points)
            pygame.draw.polygon(self.image, WHITE, points, 1)

    def update(self):
        """파워업 위치 업데이트"""
        self.rect.y += self.speed_y

        # 화면 밖으로 나가면 제거
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Player(pygame.sprite.Sprite):
    """플레이어 우주선 클래스"""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill(BLACK)

        # 우주선 모양 그리기 (삼각형)
        pygame.draw.polygon(self.image, GREEN, [
            (20, 0),   # 상단 중앙
            (0, 30),   # 좌하단
            (40, 30)   # 우하단
        ])

        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = PLAYER_SPEED
        self.last_shot = 0
        self.shoot_delay = 250  # 밀리초

        # 파워업 상태
        self.current_powerup = None
        self.powerup_timer = 0
        self.bullet_type = BULLET_NORMAL

    def update(self):
        """플레이어 위치 업데이트"""
        keys = pygame.key.get_pressed()

        # 좌우 이동
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

        # 파워업 타이머 감소
        if self.powerup_timer > 0:
            self.powerup_timer -= 1
            if self.powerup_timer == 0:
                self.current_powerup = None
                self.bullet_type = BULLET_NORMAL
                self.shoot_delay = 250  # 발사 속도 초기화

    def activate_powerup(self, powerup_type):
        """파워업 활성화"""
        self.current_powerup = powerup_type
        self.powerup_timer = POWERUP_TYPES[powerup_type]['duration'] * FPS  # 초를 프레임으로 변환

        # 총알 타입 설정
        if powerup_type == 'SINGLE':
            self.bullet_type = BULLET_NORMAL
            self.shoot_delay = 250
        elif powerup_type == 'DOUBLE':
            self.bullet_type = BULLET_DOUBLE
            self.shoot_delay = 250
        elif powerup_type == 'TRIPLE':
            self.bullet_type = BULLET_TRIPLE
            self.shoot_delay = 250
        elif powerup_type == 'MISSILE':
            self.bullet_type = BULLET_MISSILE
            self.shoot_delay = 250
        elif powerup_type == 'MISSILE_DOUBLE':
            self.bullet_type = BULLET_MISSILE_DOUBLE
            self.shoot_delay = 250
        elif powerup_type == 'MISSILE_TRIPLE':
            self.bullet_type = BULLET_MISSILE_TRIPLE
            self.shoot_delay = 250
        elif powerup_type == 'FLAMETHROWER':
            self.bullet_type = BULLET_FLAMETHROWER
            self.shoot_delay = 50  # 매우 빠른 연사
        elif powerup_type == 'SMART_MISSILE':
            self.bullet_type = BULLET_SMART_MISSILE
            self.shoot_delay = 500  # 느린 발사

    def reset_shoot_delay(self):
        """발사 속도 초기화"""
        if self.current_powerup != 'RAPID':
            self.shoot_delay = 250

    def shoot(self, enemies_group=None):
        """총알 발사"""
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullets = []

            if self.bullet_type == BULLET_NORMAL:
                bullets.append(Bullet(self.rect.centerx, self.rect.top, -1, BULLET_NORMAL, enemies_group))

            elif self.bullet_type == BULLET_DOUBLE:
                bullets.append(Bullet(self.rect.centerx - 10, self.rect.top, -1, BULLET_DOUBLE, enemies_group))
                bullets.append(Bullet(self.rect.centerx + 10, self.rect.top, -1, BULLET_DOUBLE, enemies_group))

            elif self.bullet_type == BULLET_TRIPLE:
                bullets.append(Bullet(self.rect.centerx, self.rect.top, -1, BULLET_TRIPLE, enemies_group))
                bullets.append(Bullet(self.rect.centerx - 15, self.rect.top, -1, BULLET_TRIPLE, enemies_group))
                bullets.append(Bullet(self.rect.centerx + 15, self.rect.top, -1, BULLET_TRIPLE, enemies_group))

            elif self.bullet_type == BULLET_MISSILE:
                bullets.append(Bullet(self.rect.centerx, self.rect.top, -1, BULLET_MISSILE, enemies_group))

            elif self.bullet_type == BULLET_MISSILE_DOUBLE:
                bullets.append(Bullet(self.rect.centerx - 12, self.rect.top, -1, BULLET_MISSILE_DOUBLE, enemies_group))
                bullets.append(Bullet(self.rect.centerx + 12, self.rect.top, -1, BULLET_MISSILE_DOUBLE, enemies_group))

            elif self.bullet_type == BULLET_MISSILE_TRIPLE:
                bullets.append(Bullet(self.rect.centerx, self.rect.top, -1, BULLET_MISSILE_TRIPLE, enemies_group))
                bullets.append(Bullet(self.rect.centerx - 15, self.rect.top, -1, BULLET_MISSILE_TRIPLE, enemies_group))
                bullets.append(Bullet(self.rect.centerx + 15, self.rect.top, -1, BULLET_MISSILE_TRIPLE, enemies_group))

            elif self.bullet_type == BULLET_FLAMETHROWER:
                # 화염방사기: 짧고 넓은 불꽃
                bullets.append(Bullet(self.rect.centerx, self.rect.top, -1, BULLET_FLAMETHROWER, enemies_group))

            elif self.bullet_type == BULLET_SMART_MISSILE:
                bullets.append(Bullet(self.rect.centerx, self.rect.top, -1, BULLET_SMART_MISSILE, enemies_group))

            return bullets
        return []


class Enemy(pygame.sprite.Sprite):
    """적 우주선 클래스"""

    def __init__(self, x, y, enemy_type=0):
        super().__init__()
        self.enemy_type = enemy_type
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLACK)

        # 적 타입에 따라 색상 변경
        colors = [RED, YELLOW, CYAN]
        color = colors[enemy_type % 3]

        # 적 모양 그리기 (역삼각형)
        pygame.draw.polygon(self.image, color, [
            (15, 30),  # 하단 중앙
            (0, 0),    # 좌상단
            (30, 0)    # 우상단
        ])

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = ENEMY_SPEED
        self.direction = 1  # 1: 오른쪽, -1: 왼쪽
        self.original_x = x
        self.original_y = y
        self.move_range = 50
        self.last_shot = 0
        self.shoot_delay = random.randint(2000, 5000)

    def update(self):
        """적 위치 업데이트"""
        # 좌우로 이동
        self.rect.x += self.speed * self.direction

        # 범위를 벗어나면 방향 전환
        if abs(self.rect.x - self.original_x) > self.move_range:
            self.direction *= -1
            self.rect.y += 3  # 아래로 조금 이동 (10 -> 3으로 감소)

    def shoot(self):
        """총알 발사 (확률적)"""
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            if random.random() < 0.3:  # 30% 확률로 발사
                self.last_shot = now
                self.shoot_delay = random.randint(2000, 5000)
                bullet = Bullet(self.rect.centerx, self.rect.bottom, 1, BULLET_NORMAL)
                return bullet
        return None


class Bullet(pygame.sprite.Sprite):
    """총알 클래스"""

    def __init__(self, x, y, direction, bullet_type=BULLET_NORMAL, enemies_group=None):
        super().__init__()
        self.bullet_type = bullet_type
        self.direction = direction
        self.enemies_group = enemies_group
        self.target = None
        self.kill_count = 0  # 스마트 미사일용
        self.lifetime = 0  # 화염방사기용

        # 총알 타입별 설정
        if bullet_type == BULLET_NORMAL:
            self.image = pygame.Surface((4, 10))
            self.image.fill(CYAN if direction == -1 else RED)
            self.speed = -BULLET_SPEED if direction == -1 else ENEMY_BULLET_SPEED
            self.speed_x = 0
            self.speed_y = self.speed

        elif bullet_type == BULLET_DOUBLE or bullet_type == BULLET_TRIPLE:
            self.image = pygame.Surface((5, 12))
            self.image.fill(ORANGE)
            self.speed = -BULLET_SPEED if direction == -1 else ENEMY_BULLET_SPEED
            self.speed_x = 0
            self.speed_y = self.speed

        elif bullet_type in [BULLET_MISSILE, BULLET_MISSILE_DOUBLE, BULLET_MISSILE_TRIPLE]:
            # 유도탄
            self.image = pygame.Surface((8, 14), pygame.SRCALPHA)
            pygame.draw.polygon(self.image, RED, [(4, 0), (0, 14), (8, 14)])
            pygame.draw.circle(self.image, YELLOW, (4, 10), 2)
            self.speed = 5
            self.speed_x = 0
            self.speed_y = -self.speed if direction == -1 else self.speed

        elif bullet_type == BULLET_FLAMETHROWER:
            # 화염방사기: 작고 짧은 불꽃
            size = random.randint(6, 10)
            self.image = pygame.Surface((size, size), pygame.SRCALPHA)
            color = random.choice([
                (255, 100, 0),   # 주황
                (255, 150, 0),   # 밝은 주황
                (255, 50, 0),    # 빨강-주황
                (255, 200, 0),   # 노랑-주황
            ])
            pygame.draw.circle(self.image, color, (size//2, size//2), size//2)
            self.speed = -BULLET_SPEED * 1.2
            self.speed_x = random.uniform(-1, 1)
            self.speed_y = self.speed
            self.lifetime = random.randint(15, 25)  # 짧은 수명

        elif bullet_type == BULLET_SMART_MISSILE:
            # 스마트 미사일: 5킬까지 추적
            self.image = pygame.Surface((12, 18), pygame.SRCALPHA)
            pygame.draw.polygon(self.image, (255, 215, 0), [(6, 0), (0, 18), (12, 18)])
            pygame.draw.circle(self.image, WHITE, (6, 12), 3)
            pygame.draw.circle(self.image, RED, (6, 12), 2)
            self.speed = 6
            self.speed_x = 0
            self.speed_y = -self.speed

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def find_nearest_enemy(self):
        """가장 가까운 적 찾기"""
        if not self.enemies_group or len(self.enemies_group) == 0:
            return None

        nearest = None
        min_distance = float('inf')

        for enemy in self.enemies_group:
            distance = math.sqrt(
                (enemy.rect.centerx - self.rect.centerx) ** 2 +
                (enemy.rect.centery - self.rect.centery) ** 2
            )
            if distance < min_distance:
                min_distance = distance
                nearest = enemy

        return nearest

    def update(self):
        """총알 위치 업데이트"""
        # 유도탄 AI
        if self.bullet_type in [BULLET_MISSILE, BULLET_MISSILE_DOUBLE, BULLET_MISSILE_TRIPLE, BULLET_SMART_MISSILE]:
            target = self.find_nearest_enemy()

            if target:
                # 타겟 방향 계산
                dx = target.rect.centerx - self.rect.centerx
                dy = target.rect.centery - self.rect.centery
                distance = math.sqrt(dx**2 + dy**2)

                if distance > 0:
                    # 유도 강도
                    homing_strength = 0.3 if self.bullet_type == BULLET_SMART_MISSILE else 0.2

                    # 속도 벡터 조정
                    self.speed_x += (dx / distance) * homing_strength
                    self.speed_y += (dy / distance) * homing_strength

                    # 속도 정규화
                    speed_magnitude = math.sqrt(self.speed_x**2 + self.speed_y**2)
                    if speed_magnitude > self.speed:
                        self.speed_x = (self.speed_x / speed_magnitude) * self.speed
                        self.speed_y = (self.speed_y / speed_magnitude) * self.speed

        # 화염방사기 수명 감소
        if self.bullet_type == BULLET_FLAMETHROWER:
            self.lifetime -= 1
            if self.lifetime <= 0:
                self.kill()
                return

        # 위치 업데이트
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # 화면을 벗어나면 제거
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    """폭발 효과 클래스"""

    def __init__(self, x, y):
        super().__init__()
        self.images = []

        # 폭발 애니메이션 프레임 생성
        for size in range(10, 50, 10):
            image = pygame.Surface((size, size))
            image.fill(BLACK)
            pygame.draw.circle(image, YELLOW, (size//2, size//2), size//2)
            self.images.append(image)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        """폭발 애니메이션 업데이트"""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.index += 1

            if self.index < len(self.images):
                self.image = self.images[self.index]
                self.rect = self.image.get_rect(center=self.rect.center)
            else:
                self.kill()


class Game:
    """게임 메인 클래스"""

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space War - 갤러그 스타일 슈팅 게임")
        self.clock = pygame.time.Clock()

        # 한글 지원 폰트 설정
        try:
            # macOS, Windows, Linux에서 사용 가능한 한글 폰트 시도
            font_candidates = ['AppleSDGothicNeo', 'AppleGothic', 'Malgun Gothic',
                             'NanumGothic', 'Arial Unicode MS', 'DejaVu Sans']
            font_loaded = False

            for font_name in font_candidates:
                try:
                    self.font = pygame.font.SysFont(font_name, 36)
                    self.small_font = pygame.font.SysFont(font_name, 24)
                    font_loaded = True
                    break
                except:
                    continue

            if not font_loaded:
                # 기본 폰트로 대체
                self.font = pygame.font.Font(None, 36)
                self.small_font = pygame.font.Font(None, 24)
        except:
            self.font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)

        # 사운드 매니저 초기화
        self.sound_manager = SoundManager()

        # 스프라이트 그룹
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        # 게임 상태
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.level = 1

        # 플레이어 생성
        self.player = Player()
        self.all_sprites.add(self.player)

        # 적 생성
        self.spawn_enemies()

    def spawn_enemies(self):
        """적 우주선 생성"""
        # 기존 적 제거
        for enemy in self.enemies:
            enemy.kill()

        # 격자 형태로 적 배치
        rows = 3 + self.level // 2
        cols = 8

        for row in range(min(rows, 5)):
            for col in range(cols):
                x = 100 + col * 80
                y = 50 + row * 60
                enemy = Enemy(x, y, row)
                # 레벨이 올라갈수록 적 속도 증가 (매우 조금씩)
                enemy.speed = ENEMY_SPEED + (self.level - 1) * 0.1
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)

    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over:
                    # 총알 발사 (enemies_group 전달)
                    bullets = self.player.shoot(self.enemies)
                    if bullets:
                        for bullet in bullets:
                            self.all_sprites.add(bullet)
                            self.player_bullets.add(bullet)
                        self.sound_manager.play('shoot')

                if event.key == pygame.K_r and self.game_over:
                    # 게임 재시작
                    self.__init__()

                if event.key == pygame.K_ESCAPE:
                    return False

        return True

    def update(self):
        """게임 상태 업데이트"""
        if self.game_over:
            return

        # 스프라이트 업데이트
        self.all_sprites.update()

        # 적 총알 발사
        for enemy in self.enemies:
            bullet = enemy.shoot()
            if bullet:
                self.all_sprites.add(bullet)
                self.enemy_bullets.add(bullet)

        # 플레이어 총알과 적 충돌 검사
        for bullet in self.player_bullets:
            hits = pygame.sprite.spritecollide(bullet, self.enemies, True)

            if hits:
                for hit in hits:
                    self.score += 10
                    explosion = Explosion(hit.rect.centerx, hit.rect.centery)
                    self.all_sprites.add(explosion)
                    self.explosions.add(explosion)
                    self.sound_manager.play('hit')

                    # 파워업 드롭 (30% 확률)
                    if random.random() < 0.3:
                        powerup = PowerUp(hit.rect.centerx, hit.rect.centery)
                        self.all_sprites.add(powerup)
                        self.powerups.add(powerup)

                    # 스마트 미사일 킬 카운트 증가
                    if bullet.bullet_type == BULLET_SMART_MISSILE:
                        bullet.kill_count += 1
                        if bullet.kill_count >= 5:
                            bullet.kill()
                            break

                # 일반 총알은 적 명중 시 제거
                if bullet.bullet_type not in [BULLET_SMART_MISSILE]:
                    bullet.kill()

        # 파워업과 플레이어 충돌 검사
        powerup_hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for powerup in powerup_hits:
            self.player.activate_powerup(powerup.powerup_type)
            self.sound_manager.play('powerup')

        # 적 총알과 플레이어 충돌 검사
        hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
        if hits:
            self.lives -= 1
            explosion = Explosion(self.player.rect.centerx, self.player.rect.centery)
            self.all_sprites.add(explosion)
            self.explosions.add(explosion)
            self.sound_manager.play('explosion')

            if self.lives <= 0:
                self.game_over = True
                self.sound_manager.play('game_over')

        # 적과 플레이어 충돌 검사
        hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
        if hits:
            self.lives -= 1
            explosion = Explosion(self.player.rect.centerx, self.player.rect.centery)
            self.all_sprites.add(explosion)
            self.explosions.add(explosion)
            self.sound_manager.play('explosion')

            if self.lives <= 0:
                self.game_over = True
                self.sound_manager.play('game_over')

        # 모든 적을 처치하면 다음 레벨
        if len(self.enemies) == 0:
            self.level += 1
            self.sound_manager.play('level_up')
            self.spawn_enemies()

    def draw(self):
        """화면 그리기"""
        # 배경
        self.screen.fill(BLACK)

        # 별 그리기 (배경 효과)
        for i in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.circle(self.screen, WHITE, (x, y), 1)

        # 스프라이트 그리기
        self.all_sprites.draw(self.screen)

        # UI 그리기
        score_text = self.small_font.render(f"점수: {self.score}", True, WHITE)
        lives_text = self.small_font.render(f"생명: {self.lives}", True, WHITE)
        level_text = self.small_font.render(f"레벨: {self.level}", True, WHITE)

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 40))
        self.screen.blit(level_text, (SCREEN_WIDTH - 100, 10))

        # 파워업 상태 표시
        if self.player.current_powerup:
            powerup_info = POWERUP_TYPES[self.player.current_powerup]
            remaining_time = self.player.powerup_timer / FPS
            powerup_text = self.small_font.render(
                f"파워업: {powerup_info['name']} ({remaining_time:.1f}초)",
                True,
                powerup_info['color']
            )
            self.screen.blit(powerup_text, (10, 70))

            # 파워업 게이지 바
            bar_width = 200
            bar_height = 10
            bar_x = 10
            bar_y = 100
            progress = self.player.powerup_timer / (powerup_info['duration'] * FPS)

            # 배경 바
            pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
            # 진행 바
            pygame.draw.rect(self.screen, powerup_info['color'],
                           (bar_x + 2, bar_y + 2, int((bar_width - 4) * progress), bar_height - 4))

        # 게임 오버 화면
        if self.game_over:
            game_over_text = self.font.render("게임 오버!", True, RED)
            restart_text = self.small_font.render("R키를 눌러 재시작", True, WHITE)
            final_score = self.small_font.render(f"최종 점수: {self.score}", True, YELLOW)

            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            score_rect = final_score.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))

            self.screen.blit(game_over_text, text_rect)
            self.screen.blit(restart_text, restart_rect)
            self.screen.blit(final_score, score_rect)

        # 조작 안내
        controls_text = self.small_font.render("조작: ←→ 이동 | SPACE 발사 | R 재시작 | ESC 종료", True, WHITE)
        controls_rect = controls_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 20))
        self.screen.blit(controls_text, controls_rect)

        pygame.display.flip()

    def run(self):
        """게임 메인 루프"""
        running = True

        while running:
            self.clock.tick(FPS)
            running = self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()


def main():
    """메인 함수"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
