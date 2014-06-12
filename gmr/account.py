import requests
import gmr_api
import game

class Account:
	def __init__(self, authKey):
		self.authKey = authKey
		self.playerID = gmr_api.authenticateUser(authKey)
		self.games = []

		if self.playerID == None:
			raise ValueError("Authentication key did not authenticate.")

		self.updateAccount()

	def updateAccount(self):
		response = gmr_api.getGames(self.authKey, self.playerID)

		self.points = response["CurrentTotalPoints"]
		self.name = response["Players"][0]["PersonaName"]

		self.updateGames(response["Games"])

	def updateGames(self, games):
		self.games = []

		for gmrGame in games:
			self.games.append(game.Game(gmrGame))

	def getCurrentTurns(self):
		currentTurns = []

		for gmrGame in self.games:
			if gmrGame.playerHasTurn(self.playerID):
				currentTurns.append(gmrGame)

		return currentTurns