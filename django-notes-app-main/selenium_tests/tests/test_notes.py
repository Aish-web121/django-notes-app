from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..pages.notes_page import NotesPage
from ..pages.noteformpage import NoteFormPage

def test_notes_crud(driver):
    notes = NotesPage(driver)

    # Wait until page header appears
    WebDriverWait(driver, 10).until(lambda d: notes.verify_loaded() != "")

    initial_count = notes.get_notes_count()

    # Create a new note
    notes.click_add_button()
    form = NoteFormPage(driver)
    form.fill_title("Test Note from pytest")
    form.fill_body("This is a test body - created by pytest.")
    form.save()

    # Wait until at least one note is present after save
    WebDriverWait(driver, 10).until(lambda d: notes.get_notes_count() > initial_count)

    new_count = notes.get_notes_count()
    assert new_count >= initial_count + 1, f"Expected at least {initial_count + 1} notes, got {new_count}"
