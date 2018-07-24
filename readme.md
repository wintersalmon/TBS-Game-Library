# TBS-Game-Library

- 2018년 01월 - 현재
- Turn Based Strategy Game Library
- 턴제 보드게임을 빠르게 프로토타이핑 할 수 있는 라이브러리를 개발하는 프로젝트

### 기술 스택

- Python (3.6.3)
- Kivy (1.10.1.dev0)
- Twisted (18.4.0)

### 설명

- Data, Event, Manager, Interface 순으로 Layer 를 분리하여서 설계의 복잡도를 줄이고, 개발 과정을 단순화 하였다
- 초기 게임 ```settings``` 값과 게임 내에서 실행된 모든 ```Event``` 값을 이용해서 게임의 특정 ```status``` 에 도달 할 수 있는 특징을 가지고 있다
	- 이 특징을 이용해서 Save & Load, Replay, Asynchronous Multiplay, AI 등을 간단하게 구현한다
- 작은 규모의 턴제 보드게임 (tic-tac-toe, othello, chess) 등을 하나씩 구현하면서 라이브러리 추가, 설계 변경, 테스트 코드 작성 등의 작업을 통해 프로젝트를 발전시킨다.
- Data 객체들은 SerializableMixin 을 상속받아서 저장, 전송이 가능한 상태가 된다
- Event 객체들은 update(forward), rollback(backward) 두가지 메서드를 구현하여서 게임의 상태를 양방향으로 변경 할 수 있다
- Manager 객체들은 게임 로직 레이어와 사용자 인터페이스의 연결을 돕는 중간자 역활 한다

### 예제 실행 방법

- `/tbs` must be Sources Root
- `/example` must be Sources Root

``` bash
cd examples

main.py play <package> [--cli]    # create new game
main.py replay <package> [--cli]  # load saved game in replay mode
# --cli: load game in CLI(command line interface) mode
```

### ToDo

- 원래 CLI, GUI 두가지 인터페이스를 지원하려 했으나 설계의 복잡도가 증가 하고 공통 라이브러리를 만드는데 어려움이 만아 GUI 만을 지원하도록 변경한다
- GUI 는 공용 라이브러리에 포함하지 않고 프로젝트별 독립 구현으로 변경한다
- Kivy 내에서 지원하는 Twisted 를 통해서 멀티플레이 기능을 구현한다
- 게임의 상태를 Serialize 할 수 있다는 특징을 이용해서 AI Player 를 구현한다