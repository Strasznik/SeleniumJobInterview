from conftest import Trello
import pytest
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

TRELLO = Trello()


class TestCasesTrelloSelenium:
    board_id = ""
    username = "kamilgrzywinski@gmail.com"
    password = "Plentific"
    expected_card_names = ["Test_Updated_Card_Name", "Third_Card"]
    new_comment = "Additional_Test_Card_Comment"

    def setup_class(self):
        if TRELLO.check_server_status() != 200:
            pytest.xfail("Trello API is unreachable. Internet connection or server is down. Tests execution terminated.")

    def setup_method(self):
        TestCasesTrelloSelenium.board_id = TRELLO.create_board("Plentific_Test_Board")
        list_id = TRELLO.get_board_lists(TestCasesTrelloSelenium.board_id)["Doing"]
        cards = ["First_Card", "Second_Card", "Third_Card"]
        all_cards = dict()
        for card in cards:
            card_id = TRELLO.create_card(list_id, card)
            created_card = requests.get(f'https://api.trello.com/1/cards/{card_id}{TRELLO.key_token}')
            all_cards[created_card.json()["name"]] = {"status_code": created_card.status_code, "id": created_card.json()["id"]}

        first_card_id = all_cards[cards[0]]["id"]
        TRELLO.update_card(first_card_id, "Test_Updated_Card_Name")

        second_card_id = all_cards[cards[1]]["id"]
        TRELLO.delete_card(second_card_id)

        third_card_id = all_cards[cards[2]]["id"]
        TRELLO.add_card_comment(third_card_id, "Test_Card_Comment")

    def teardown_method(self):
        TRELLO.board_delete(TestCasesTrelloSelenium.board_id)

    def trello_login_and_board_selection(self, selenium):
        selenium.get(f'https://id.atlassian.com/login?application=trello&email={self.username}')
        cont = selenium.find_element_by_id("login-submit")
        cont.click()
        passwd = selenium.find_element_by_id("password")
        passwd.send_keys(self.password)
        cont.click()
        WebDriverWait(selenium, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'css-155ohwf')))
        selenium.get(f"https://trello.com/appSwitcherLogin?login_hint={self.username}")
        board = selenium.find_elements_by_class_name("board-tile-details-name")[0]
        board.click()

    def find_cards_on_board(self, selenium):
        cards = selenium.find_elements_by_class_name("js-member-droppable")
        card_names = [elem.text.split("\n")[0] for elem in cards]
        comments = [elem.text.split("\n")[1] for elem in cards if len(elem.text.split("\n")) > 1]
        return cards, card_names, comments

    def close_card_window(self, selenium):
        close_window = selenium.find_elements_by_class_name("js-close-window")[0]
        close_window.click()

    def test_selenium_board_verification(self, selenium):
        selenium.implicitly_wait(10)
        selenium.maximize_window()
        self.trello_login_and_board_selection(selenium)

        _, card_names, card_comments = self.find_cards_on_board(selenium)

        assert len(card_names) == 2 and card_names == self.expected_card_names, "Number of cards or their names are incorrect."
        assert len(card_comments) == 1 and card_comments[0] == "1", "Number of commented cards or number of expected comments are incorrect."

    def test_selenium_added_comment_verification(self, selenium):
        selenium.implicitly_wait(10)
        selenium.maximize_window()
        self.trello_login_and_board_selection(selenium)

        cards, card_names, card_comments = self.find_cards_on_board(selenium)

        cards[1].click()  # Second_Card

        comment_focus = selenium.find_elements_by_class_name("comment-frame")[0]
        comment_focus.click()

        write_comment = selenium.find_elements_by_class_name("js-new-comment-input")[0]
        write_comment.send_keys(self.new_comment)

        save_comment = selenium.find_elements_by_class_name("js-add-comment")[0]
        save_comment.click()

        self.close_card_window(selenium)
        selenium.refresh()

        cards, card_names, card_comments = self.find_cards_on_board(selenium)

        assert len(card_comments) == 1 and card_comments[0] == "2", "Number of commented cards or number of expected comments are incorrect."

    def test_selenium_move_card_to_done_verification(self, selenium):
        selenium.implicitly_wait(10)
        selenium.maximize_window()
        self.trello_login_and_board_selection(selenium)

        cards, card_names, card_comments = self.find_cards_on_board(selenium)

        cards[1].click()
        move_card = selenium.find_elements_by_class_name("js-move-card")[0]
        move_card.click()

        select_trello_list = selenium.find_elements_by_class_name("js-select-list")[0]
        select_trello_list.click()
        # I'm aware that available lists could change and using Keys.DOWN might not be valid in future but I assume that we are testing hermetic environment.
        select_trello_list.send_keys(Keys.DOWN)
        select_trello_list.send_keys(Keys.ENTER)
        submit = select_list = selenium.find_elements_by_class_name("js-submit")[0]
        submit.click()

        self.close_card_window(selenium)
        selenium.refresh()

        cards, card_names, card_comments = self.find_cards_on_board(selenium)
        not_moved_card_location = cards[0].location["x"]
        moved_card_location = cards[1].location["x"]
        # I'm aware that there are much better way to verify that. This one is naive/inaccurate solution. I simply wannet to show other approach :)
        assert not_moved_card_location == 296 and moved_card_location == 576, "Card was not properly set/moved to DONE state"
