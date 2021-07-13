import requests
import os
import sys


class Trello:
	def __init__(self):
		# It is better and safer to use environmental variables to store credentials, but for recruitment purpose I hardcoded it.
		self.key = os.environ.get("TRELLO_KEY")
		self.token = os.environ.get("TRELLO_TOKEN")
		self.key_token = f"?key={self.key}&token={self.token}"

		if self.key is None or self.token is None:
			print("Valid Trello key (TRELLO_KEY) and token (TRELLO_TOKEN) must be set in environment variables prior executing tests!")
			sys.exit(1)

	@staticmethod
	def check_server_status():
		try:
			status_code = requests.get(f'https://api.trello.com/').status_code
			return status_code
		except requests.exceptions.ConnectionError:
			return 1

	def create_board(self, board_name):
		board = requests.post(f'https://api.trello.com/1/boards/{self.key_token}&name={board_name}')
		if board.status_code == 200:
			return board.json()["id"]
		else:
			return {"status_code": board.status_code, "text": board.text}

	def get_board_lists(self, board_id):
		all_lists = requests.get(f'https://api.trello.com/1/boards/{board_id}/lists{self.key_token}')
		list_id_with_name = {trello_list["name"]: trello_list["id"] for trello_list in all_lists.json()}
		return list_id_with_name

	def create_card(self, list_id, card_name):
		card = requests.post(f'https://api.trello.com/1/cards/{self.key_token}&name={card_name}&idList={list_id}')
		if card.status_code == 200:
			return card.json()["id"]
		else:
			return {"status_code": card.status_code, "text": card.text}

	def update_card(self, card_id, new_card_name='', move_to_list_id=''):
		parameters = ''
		if move_to_list_id:
			move_to_list_id = f'&idList={move_to_list_id}'
		if new_card_name:
			new_card_name = f'&name={new_card_name}'
		parameters = new_card_name + move_to_list_id
		update_card = requests.put(f'https://api.trello.com/1/cards/{card_id}/{self.key_token}{parameters}')
		return {"status_code": update_card.status_code, "text": update_card.text}

	def add_card_comment(self, card_id, comment_text):
		card_comment = requests.post(f'https://api.trello.com/1/cards/{card_id}/actions/comments{self.key_token}&text={comment_text}')
		return {"status_code": card_comment.status_code, "text": card_comment.text}

	def delete_card(self, card_id):
		deleted_card = requests.delete(f'https://api.trello.com/1/cards/{card_id}{self.key_token}')
		return {"status_code": deleted_card.status_code, "text": deleted_card.text}

	def board_delete(self, board_id):
		removed_board = requests.delete(f'https://api.trello.com/1/boards/{board_id}{self.key_token}')
		return {"status_code": removed_board.status_code, "text": removed_board.text}
