import pytest
from playwright.sync_api import sync_playwright

from apps.boards.services import create_project_with_board


@pytest.mark.django_db(transaction=True)
@pytest.mark.e2e
def test_login_create_project_and_task(live_server, django_user_model):
    user = django_user_model.objects.create_user(
        username="e2e",
        email="e2e@example.com",
        password="password123",
    )
    project = create_project_with_board(creator=user, name="E2E Team", description="browser flow")
    assert project.board.columns.count() >= 1

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"{live_server.url}/accounts/login/")
        page.get_by_label("Username or email").fill("e2e")
        page.get_by_label("Password").fill("password123")
        page.get_by_role("button", name="Login").click()
        page.get_by_role("link", name="E2E Team").click()
        page.get_by_role("link", name="New task").click()
        page.get_by_label("Title").fill("Browser task")
        page.get_by_label("Description").fill("Created from Playwright")
        page.get_by_role("button", name="Save").click()
        page.get_by_text("Browser task").wait_for()
        browser.close()
