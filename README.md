# jump-game

## tkinter로 만든 점프게임입니다.
![점프게임 이미지](jump-game.png "점프게임이미지")
* 방향키(←, ↑, →)를 사용해서 움직일 수 있습니다.
    * ←왼쪽, ↑점프, →오른쪽
* 100점을 모으거나 남은 시간이 없으면 게임이 끝납니다.
    * 스페이스바를 눌러 다시 시작할 수 있습니다.
* tkinter의 canvas를 사용해서 필요한 요소를 화면에 보여줍니다.
```python
canvas = tkinter.Canvas(window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
```
* random을 사용해서 플랫폼의 넓이와 위치를 설정했습니다.
    * 다음 플랫폼의 넓이와 위치는 이전 플랫폼의 위치와 크기를 바탕으로 만들어집니다.
    * 점수를 얻으면 플랫폼들이 다시 설정됩니다.
```python

```
## 참고자료/reference
* [make snake game(YouTube)](https://www.youtube.com/results?search_query=make+snake+game).
* Microsoft Copilot