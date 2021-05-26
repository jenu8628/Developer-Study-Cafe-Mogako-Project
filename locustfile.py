from locust import HttpUser,TaskSet,task,between

# 생명 주기
# 1. Locust setup
# 2. TaskSet setup
# 3. TaskSet on_start
# 4. TaskSet tasks…
# 5. TaskSet on_stop
# 6. TaskSet teardown
# 7. Locust teardown

# 실행 명령어 locust
# locust -f locustfile.py

# 접속 url: localhost:8089

# EC2는 VM 환경이므로 테스트는 무의미하다

class WebsiteUser(HttpUser):
    wait_time = between(5, 15)
    
    @task
    # 로그인 로그아웃 반복
    def on_start(self):
        self.client.post("/user/login/", json={"username":"abcd@naver.com", "password":"abcd@naver.com"}),
        self.client.get("/user/logout/")

    # @task
    # # 기본 페이지 조회
    # def index(self):
    #     self.client.get("/")
