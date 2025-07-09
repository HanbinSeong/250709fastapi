# 실습목차
- [2025-07-08](#250708-git-action-실습)
- [2025-07-09](#250709-jenkins-실습)

---

# 250708 - Git Action 실습
# Git Action
Git Action으로 AWS서버에 CI/CD구조를 가지는 플로우를 이해하기 위해 실습하는 리포지토리

## 작동방식
`.github/workflows` 디렉토리에 .yml 파일로 스크립트로 자동화 실행

## 환경변수
ECR_REPOSITORY          = Amazon ECR/프라이빗 레지스트리/리포지토리 이름 (e.g. my-react-app)
EC2_HOST                = EC2 인스턴스 퍼블릭 DNS
EC2_USER                = 인스턴스 유저 이름(e.g. ubuntu)
EC2_KEY                 = 인스턴스 시작할 때, 키 페어(로그인) (e.g. aws-sever-key.pem 내부내용)
AWS_ACCESS_KEY_ID       = IAM/사용자/본인/액세스키
AWS_SECRET_ACCESS_KEY   = IAM/사용자/본인/비밀 액세스 키
AWS_REGION              = AWS 서버 지역(e.g. ap-northeast-3)

# EC2 서버 초기셋팅(Docker)
- SSH 접속
  ```
  sudo apt update
    sudo apt install -y docker.io
    sudo systemctl enable docker
    sudo systemctl start docker
    sudo usermod -aG docker $USER
    exit
    이후 재접속
  ```
- SSH 로컬환경에서 접속할 때, 키페어 경로는 `C:\Users\user`로 설정 (cmd 초기 디렉토리가 여기라서 접속할 때 편함)

## 서버 SSH 연결안될 경우
```
    # PowerShell에서 파일을 읽기 전용으로 설정
    attrib +R your-key.pem
    
    # GitBash 
    chmod 400 your-key.pem

```

## S3 - (main.yml)
정적 웹 사이트 호스팅
## EC2 - (docker.yml)
하나의 컴퓨터 객체(서버 운영)
Docker 활용 가능 > Amazon ECR/프라이빗 레지스트리 (이미지 저장)
보안그룹 인바운드 규칙 필요
- SSH
  - 유형: SSH
  - 소스: Anywhere IPv4
- HTTP
  - 유형: 사용자 지정 TCP
  - 포트범위: 사용포트번호
  - 소스: Anywhere IPv4

# 서버규모
- 개인: EC2 하나로 프론트 백엔드 DB 전부 해결가능 + ECR(Docker 이미지)
- 운영규모: 규모에 따라 다르지만, 보통 S3(웹작동방식이나, 트래픽 많아지면 별도 서버 구성), ECS, RDS 각각 서버운영

---

# 250709 - 젠킨스 실습
react환경 및 fastapi를 하나의 EC2(우분트 t2.medium) 환경에서 세팅할거임.

## EC2 초기 프로그램 설치
```SSH
# Jenkins
sudo apt update
sudo apt install openjdk-17-jdk -y
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt update && sudo apt install jenkins -y
sudo systemctl start jenkins
sudo systemctl enable jenkins

# Docker
sudo apt install docker.io -y
sudo systemctl enable docker
sudo apt install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER
```

### 젠킨스 KEY값 확인
```
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

### 웹상에서 젠킨스 설치
1. `{퍼블릭DNS}:8080` 접속
2. 시크릿 키 입력
3. 권장설치옵션
4. `admin` 계정 설정