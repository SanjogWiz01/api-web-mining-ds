"""
Tests for task CRUD endpoints.
"""


class TestCreateTask:
    """Tests for POST /tasks/."""

    def test_create_task_success(self, authenticated_client):
        """Should create a task and return it."""
        response = authenticated_client.post("/tasks/", json={
            "title": "Test Task",
            "description": "A test task description",
            "priority": "high",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["description"] == "A test task description"
        assert data["priority"] == "high"
        assert data["status"] == "todo"
        assert data["is_completed"] is False

    def test_create_task_minimal(self, authenticated_client):
        """Should create a task with only the required title field."""
        response = authenticated_client.post("/tasks/", json={
            "title": "Minimal Task",
        })
        assert response.status_code == 201
        assert response.json()["title"] == "Minimal Task"
        assert response.json()["priority"] == "medium"

    def test_create_task_unauthorized(self, client):
        """Should return 401 without authentication."""
        response = client.post("/tasks/", json={"title": "Fail"})
        assert response.status_code == 401

    def test_create_task_empty_title(self, authenticated_client):
        """Should reject a task with an empty title."""
        response = authenticated_client.post("/tasks/", json={"title": ""})
        assert response.status_code == 422


class TestListTasks:
    """Tests for GET /tasks/."""

    def test_list_tasks_empty(self, authenticated_client):
        """Should return an empty list when no tasks exist."""
        response = authenticated_client.get("/tasks/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_tasks_with_data(self, authenticated_client):
        """Should return all tasks belonging to the user."""
        authenticated_client.post("/tasks/", json={"title": "Task 1"})
        authenticated_client.post("/tasks/", json={"title": "Task 2"})
        authenticated_client.post("/tasks/", json={"title": "Task 3"})

        response = authenticated_client.get("/tasks/")
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_list_tasks_pagination(self, authenticated_client):
        """Should respect skip and limit parameters."""
        for i in range(5):
            authenticated_client.post("/tasks/", json={"title": f"Task {i}"})

        response = authenticated_client.get("/tasks/?skip=2&limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2


class TestGetTask:
    """Tests for GET /tasks/{task_id}."""

    def test_get_task_success(self, authenticated_client):
        """Should return a specific task by ID."""
        create_resp = authenticated_client.post("/tasks/", json={"title": "Find Me"})
        task_id = create_resp.json()["id"]

        response = authenticated_client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "Find Me"

    def test_get_task_not_found(self, authenticated_client):
        """Should return 404 for a non-existent task."""
        response = authenticated_client.get("/tasks/99999")
        assert response.status_code == 404


class TestUpdateTask:
    """Tests for PUT /tasks/{task_id}."""

    def test_update_task_title(self, authenticated_client):
        """Should update the task title."""
        create_resp = authenticated_client.post("/tasks/", json={"title": "Old Title"})
        task_id = create_resp.json()["id"]

        response = authenticated_client.put(f"/tasks/{task_id}", json={
            "title": "New Title",
        })
        assert response.status_code == 200
        assert response.json()["title"] == "New Title"

    def test_update_task_complete(self, authenticated_client):
        """Should mark task as done when is_completed is set to True."""
        create_resp = authenticated_client.post("/tasks/", json={"title": "Complete Me"})
        task_id = create_resp.json()["id"]

        response = authenticated_client.put(f"/tasks/{task_id}", json={
            "is_completed": True,
        })
        assert response.status_code == 200
        assert response.json()["is_completed"] is True
        assert response.json()["status"] == "done"


class TestDeleteTask:
    """Tests for DELETE /tasks/{task_id}."""

    def test_delete_task_success(self, authenticated_client):
        """Should delete a task and confirm deletion."""
        create_resp = authenticated_client.post("/tasks/", json={"title": "Delete Me"})
        task_id = create_resp.json()["id"]

        response = authenticated_client.delete(f"/tasks/{task_id}")
        assert response.status_code == 200
        assert "deleted" in response.json()["detail"].lower()

        # Verify it's gone
        get_resp = authenticated_client.get(f"/tasks/{task_id}")
        assert get_resp.status_code == 404

    def test_delete_task_not_found(self, authenticated_client):
        """Should return 404 when deleting a non-existent task."""
        response = authenticated_client.delete("/tasks/99999")
        assert response.status_code == 404
