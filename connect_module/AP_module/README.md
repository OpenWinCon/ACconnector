# ACconnector - Connect Module

Connect module은 미리 설정된 tunnel을 통해 실제로 Remote AP와 ONOS 사이에 패킷을 주고 받을 수 있도록 하는 모듈입니다.

### Topology
네트워크 구성은 제일 상위에 있는 README 파일에 설명한 것과 동일하다고 가정합니다.

### Module 실행
프로그램은 connector.py 안에 모두 포함되어 있으므로 실행은 sudo 권한을 주고 파이썬 프로그램을 실행하면 됩니다.  
`sudo python connector.py`

이는 해당 프로그램이 linux 경로 상에서 root 권한이 필요한 곳에 접근할 뿐만 아니라 iptable을 조작하는 등의 명령을 수행하기 때문에 필요합니다.

### Module Interface
프로그램의 실행하면 5개의 메인 메뉴 항목이 보이게 됩니다. 

1. Check forward settings

  해당 항목에서는 유저가 설정해 두었던 forward setting을 출력합니다.
  각각의 forward setting은 들어오는 interface, 나가야하는 tunnel interface, forward mode로 구성되어 있습니다.
  forward mode는 3가지의 숫자로 표시되는데 아래와 같습니다.

  1 | Full forward  
  2 | Selective forward  
  3 | Openflow only forward  
  
2. Update forward setting

  해당 항목에서는 유저가 필요한 새로운 설정을 update할 수 있도록 하며 위의 forward setting에 필요한 정보를 입력하게 됩니다.
  
3. Delete forward setting

  해당 항목에서는 유저가 기존에 입력해 놓은 설정 중 필요없는 항목을 삭제하는 것으로 들어오는 interface의 정보만 입력하면 삭제가 가능합니다.
  
4. Start forwarding
  
  해당 항목에서는 유저가 기존에 입력해놓은 대로 실제로 포워딩을 시작할 수 있도록 합니다. Forwarding을 수행하는 중에는 외부 입력을 받을 수 없으므로 중지시키려면 Ctrl^c 를 통해서 Interrupt를 발생시켜야 합니다.
  
5. Program quit
  
  해당 항목은 프로그램을 종료시킵니다.
