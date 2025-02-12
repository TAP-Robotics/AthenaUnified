import logging
from dataclasses import dataclass
from pynng import Pair0

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, handlers=[
    logging.FileHandler("zeusy.log"),
    logging.StreamHandler()
])

@dataclass
class Message:
	message: str
	content: str
	def to_dict(self):
		"""Convert the Message object to a dictionary."""
		return {
		    "message": self.message,
		    "content": self.content
		}

class Nanos():
	def __init__(self):
		logger.info("Initializing Pair to Pair connection")
		self.socket = Pair0()
		self.socket.dial("tcp://127.0.0.1:7207")
		logger.info("Pair to Pair initialized")

	async def send_message(self, message: bytes) -> None:
		try:
			self.socket.send(message)
		except Exception as e:
			logger.error(f"An error occured when sending message to pair: {e}")
			raise
	
	async def receive_message(self) -> bytes:
		try:
			message = self.socket.recv()
			return message
		except Exception as e:
			logger.error(f"An error occurred while receiving message: {e}")
			raise
