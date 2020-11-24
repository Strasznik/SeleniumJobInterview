from conftest import Trello
import pytest
import requests

TRELLO = Trello()


class TestCasesTrello:
    board_id = ""
    expected_board_name = "Plentific_Test_Board"
    expected_cards = ["First_Card", "Second_Card", "Third_Card"]
    # Default Trello lists are: Done, Doing, To Do
    edited_list = "Doing"

    def setup_class(self):
        if TRELLO.check_server_status() != 200:
            pytest.xfail("Trello API is unreachable. Internet connection or server is down. Tests execution terminated.")

    def setup_method(self):
        TestCasesTrello.board_id = TRELLO.create_board(TestCasesTrello.expected_board_name)

    def teardown_method(self):
        TRELLO.board_delete(TestCasesTrello.board_id)

    def create_trello_cards(self):
        all_cards = dict()
        list_id = TRELLO.get_board_lists(TestCasesTrello.board_id)[TestCasesTrello.edited_list]
        for card in TestCasesTrello.expected_cards:
            card_id = TRELLO.create_card(list_id, card)
            created_card = requests.get(f'https://api.trello.com/1/cards/{card_id}{TRELLO.key_token}')
            all_cards[created_card.json()["name"]] = {"status_code": created_card.status_code, "id": created_card.json()["id"]}
        return all_cards

    def test_positive_check_created_board(self):
        board = requests.get(f'https://api.trello.com/1/boards/{TestCasesTrello.board_id}{TRELLO.key_token}')
        assert board.status_code == 200 and board.json()["name"] == TestCasesTrello.expected_board_name, "Trello board was not created properly"

    def test_positive_create_cards(self):
        all_cards = self.create_trello_cards()
        cards_status_codes = [all_cards[key]["status_code"] for key in all_cards.keys()]
        # Condition list(all_cards.keys()) == TestCasesTrello.cards is checking if three cards were created as expected
        assert list(all_cards.keys()) == TestCasesTrello.expected_cards and all(value == 200 for value in cards_status_codes), \
            "Trello lists were not created properly"

    def test_positive_card_update(self):
        all_cards = self.create_trello_cards()
        card_id = all_cards[self.expected_cards[0]]["id"]
        card_new_name = "Test_Updated_Card_Name"
        TRELLO.update_card(card_id, card_new_name)
        updated_card = requests.get(f'https://api.trello.com/1/cards/{card_id}{TRELLO.key_token}')
        assert updated_card.status_code == 200 and updated_card.json()["name"] == card_new_name, "Trello card was not updated properly"

    def test_positive_add_card_comment(self):
        all_cards = self.create_trello_cards()
        card_id = all_cards[self.expected_cards[0]]["id"]
        card_comment = "Test_Card_Comment"
        TRELLO.add_card_comment(card_id, card_comment)
        card = requests.get(f'https://api.trello.com/1/cards/{card_id}/actions/{TRELLO.key_token}').json()
        assert len(card) == 1 and card[0]["data"]["text"] == "Test_Card_Comment", "Trello card comment was not added properly"

    def test_positive_delete_card(self):
        all_cards = self.create_trello_cards()
        card_id = all_cards[self.expected_cards[0]]["id"]
        card_status_before_rmv = requests.get(f'https://api.trello.com/1/cards/{card_id}{TRELLO.key_token}').status_code
        TRELLO.delete_card(card_id)
        card_after_rmv = requests.get(f'https://api.trello.com/1/cards/{card_id}{TRELLO.key_token}')
        card_status_after_rmv = card_after_rmv.status_code
        card_response_text_after_rmv = card_after_rmv.text
        assert card_status_before_rmv == 200 and card_status_after_rmv == 404 and \
               card_response_text_after_rmv == "The requested resource was not found.", "Trello card was not deleted properly"

    def test_positive_move_card_to_done_list(self):
        done_list = "Done"
        done_list_id = TRELLO.get_board_lists(TestCasesTrello.board_id)[done_list]
        doing_list_id = TRELLO.get_board_lists(TestCasesTrello.board_id)[TestCasesTrello.edited_list]
        all_cards = self.create_trello_cards()
        card_id = all_cards[self.expected_cards[0]]["id"]
        current_card = requests.get(f'https://api.trello.com/1/cards/{card_id}{TRELLO.key_token}')
        TRELLO.update_card(card_id, move_to_list_id=done_list_id)
        updated_card = requests.get(f'https://api.trello.com/1/cards/{card_id}{TRELLO.key_token}')
        assert current_card.json()["idList"] == doing_list_id and updated_card.status_code == 200 and updated_card.json()["idList"] == done_list_id, \
            "Trello card was not updated properly"

    def test_negative_check_invalid_key(self):
        board = requests.get(f'https://api.trello.com/1/boards/{TestCasesTrello.board_id}?key=invalid_key&token={TRELLO.token}')
        assert board.status_code == 401 and board.text == "invalid key", "Server response status code or error message was incorrect"

    def test_negative_check_invalid_token(self):
        board = requests.get(f'https://api.trello.com/1/boards/{TestCasesTrello.board_id}?key={TRELLO.key}&token=invalid_token')
        assert board.status_code == 401 and board.text == "invalid token", "Server response status code or error message was incorrect"

    def test_negative_create_invalid_board(self):
        board = TRELLO.create_board("")
        assert board["status_code"] == 400 and board["text"] == "invalid value for name", "Server response status code or error message was incorrect"

    def test_negative_exceed_ten_boards(self):
        # My Trello account limit for boards is 10. 9 are created here and 1 is created in setup_method.
        # I'm aware that I should check if there are any boards created before executing this test to properly check "10 boards limitation", but for purpose
        # of recruitment process I assumed that this solution is enough.
        boards = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        boards_ids = [TRELLO.create_board(board) for board in boards]
        eleven_board = TRELLO.create_board("ten")
        for board_id in boards_ids:
            TRELLO.board_delete(board_id)
        assert eleven_board["status_code"] == 400 and eleven_board["text"] == "{\"message\":\"Board must be in a team — specify an idOrganization\"}", \
            "Server response status code or error message was incorrect"

    def test_negative_create_invalid_card(self):
        all_cards = self.create_trello_cards()
        card_id = all_cards[self.expected_cards[0]]["id"]
        card = TRELLO.create_card(card_id, "")
        assert card["status_code"] == 404 and card["text"] == "could not find the board that the card belongs to", \
            "Server response status code or error message was incorrect"

    def test_negative_update_not_existing_card(self):
        card_new_name = "Test_Updated_Card_Name"
        card_id = ""
        updated_card = TRELLO.update_card("not_existing_card", card_new_name)
        assert updated_card["status_code"] == 400 and updated_card["text"] == "invalid id", "Trello card was not updated properly"

    def test_negative_create_card_comment_with_too_long_name(self):
        list_id = TRELLO.get_board_lists(TestCasesTrello.board_id)[TestCasesTrello.edited_list]
        # If I would have proper requirements I would create border cases for card name limitations. I took 17 000 value from manual testing (I simply notice
        # that around this value Trello is giving 431 server error).
        card = TRELLO.create_card(list_id, "".join(str(x) for x in range(17000)))
        assert card["status_code"] == 431 and card["text"] == "", "Server response status code or error message was incorrect"

    def test_negative_delete_not_existing_card(self):
        updated_card = TRELLO.delete_card("not_existing_card")
        assert updated_card["status_code"] == 400 and updated_card["text"] == "invalid id", "Trello card was not updated properly"
