AC connector - (Remote AP - Controller connector)

AC connector는 원격에 있는 AP가 Controller의 control을 받을 수 있도록 하기 위한 기능을 제공하는 모듈 혹은 프로그램입니다.
AP와 Controller를 기존에 존재하는 터널 프로토콜 들을 사용해서 연결하고 필요에 따라서 해당하는
컨트롤 트래픽이나 데이터 트래픽을 터널을 통해서 전달될 수 있도록 합니다.

프로그램은 현 버전에서 2개의 모듈로 구성되어 있으며 각각 터널을 통제하는 모듈과 실제 트래픽 전달에 관여하는 모듈입니다.

각각은 필요에 맞춰 HostAP와 OpenWRT에 맞춰서 모듈을 다시 나눌 예정으로 되어있습니다.
