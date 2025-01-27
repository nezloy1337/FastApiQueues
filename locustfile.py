from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    def on_start(self):
        # Токен авторизации
        self.token = "Bearer iACoW07K75c9Pru09oMgGxTc97vp1WsBqwmJQht8WVM"
        self.headers = {
            "Authorization": self.token,
            "Content-Type": "application/json"
        }
        self.queue_id = 1  # Идентификатор очереди для GET запросов

    @task
    def get_request(self):
        # GET запрос
        self.client.get(
            f"/api_v1/queues/{self.queue_id}",
            headers=self.headers
        )

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 3)

#     locust -f load_testing.py
