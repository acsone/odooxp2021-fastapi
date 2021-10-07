from locust import HttpUser, task, between

class HelloWorldUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def hello_world(self):
        self.client.get("/partners/1")

