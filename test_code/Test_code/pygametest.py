import pygame
import numpy as np
import sys
import wave
import pyaudio
def play_game(file_path):
    # 오디오 파일 로드
    wf = wave.open(file_path, 'rb')
    p = pyaudio.PyAudio()

    # Pygame 초기화
    pygame.init()

    # 화면 설정
    width, height = 864, 480  # 임시 크기 (전체 화면으로 설정된 이후에는 무시됨)
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    pygame.display.set_caption('Audio Visualization')

    # 마우스 숨기기
    pygame.mouse.set_visible(False)

    # 파이게임 시계 설정
    clock = pygame.time.Clock()  # 시계 생성

    # 사운드 스트림 설정
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # 시각화 설정
    buffer_size = 1024
    samples = np.zeros(buffer_size)
    x = np.arange(0, buffer_size)
    line = pygame.Surface((width, height))

    # 무지개 색상 배열 정의
    rainbow_colors = [
        (148, 0, 211),  # 보라
        (75, 0, 130),   # 남색
        (0, 0, 255),    # 파랑
        (0, 255, 0),    # 초록
        (255, 255, 0),  # 노랑
        (255, 165, 0),  # 주황
        (255, 0, 0)     # 빨강
    ]

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 오디오 읽기
        data = wf.readframes(buffer_size)
        if not data:
            break

        samples = np.frombuffer(data, dtype=np.int16)

        # 시각화 업데이트
        line.fill((0, 0, 0))  # 검은 배경
        for i in range(min(buffer_size, width)):  # 최소값 사용
            y = height // 2 - samples[i] / 30

            # 무지개 색상 선택
            rainbow_index = int(i / buffer_size * len(rainbow_colors))
            color = rainbow_colors[rainbow_index]

            pygame.draw.aaline(line, color, (i, height // 2), (i, y), 1)  # 무지개 선 (안티 에일리어싱 적용)

        # 화면에 표시
        screen.blit(line, (0, 0))
        pygame.display.flip()

        # 사운드 출력
        stream.write(data)

        clock.tick(60)  # 초당 60프레임으로 제한

    # 종료 시 정리
    pygame.mouse.set_visible(True)  # 마우스 원래대로 표시
    pygame.quit()
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()
    sys.exit()

