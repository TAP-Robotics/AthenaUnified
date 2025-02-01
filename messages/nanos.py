from pynng import Pair0

class Nanos():
	def __init__(self):
		self.socket = Pair0()
		self.socket.dial("tcp://127.0.0.1:7207")

	async def send_message(self, message: str):
		self.socket.send(message)