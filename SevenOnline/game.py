class Game(object):
    """Handles all data over the lifetime of a single game."""

    CARDS_PER_ROUND = 7


    def __init__(self, host, password, name, max_players,
                 ):
        """Initializes the game with the parameters from CreateHandler."""
        self.host = host
		current_age = 0
		current_turn = 0
        self.deck = BuildDeck(current_age)
        self.password = password
        self.name = name
        self.max_players = max_players



        self.players = {}
        self.order = []
        self.perma_banned = set()

        self.InitGame()
        self.Ping()

    def InitGame(self):
        """Initializes the game into a BEGIN state."""
        self.state = States.BEGIN
        self.round = Round.make_zeroeth()
        self.turn = 0
        self.deck.reset()

    def Ping(self):
        """Updates the game to appear currently active."""
        self.last_active = time.time()

    def clue_maker(self):
        """Returns the User who made, or is making, the current clue."""
        return self.order[self.turn]

    def get_card(self, cid):
        """Returns the Card from the deck with the given card id."""
        return self.deck.get_card(cid)

    def AddPlayer(self, user, colour):
        """Adds a user with a given colour to the game, or throws APIError."""
        if self.state != States.BEGIN:
            raise APIError(Codes.BEGIN_BAD_STATE)
        if len(self.players) >= self.max_players:
            raise APIError(Codes.JOIN_FULL_ROOM)
        if not BunnyPalette.is_colour(colour):
            raise APIError(Codes.NOT_A_COLOUR, colour)
        if colour in self.colours.values():
            raise APIError(Codes.COLOUR_TAKEN)
        if user in self.perma_banned:
            raise APIError(Codes.JOIN_BANNED)
        if not user in self.players:  # idempotent
            self.players[user] = Player(user)
            self.order.append(user)
        self.colours[user] = colour  # alow colour changing

    def KickPlayer(self, user, is_permanent=False):
        """Kicks a user from the game, or throws APIError."""
        if not user in self.players:
            raise APIError(Codes.KICK_UNKNOWN_USER)
        if len(self.players) <= Limits.MIN_PLAYERS and \
           self.state != States.BEGIN:
            raise APIError(Codes.NOT_ENOUGH_PLAYERS)
        if self.state in (States.PLAY, States.VOTE):
            raise APIError(Codes.KICK_BAD_STATE)
        self.players.pop(user)
        turn = self.order.index(user)
        self.order.remove(user)
        # Readjust turn in case game is currently running
        if self.turn > turn:
            self.turn -= 1
        self.turn %= len(self.players)
        if is_permanent:
            self.perma_banned.add(user)

    def start_game(self):
        """Transitions from BEGIN to CLUE, or throws APIError."""
        if self.state != States.BEGIN:
            raise APIError(Codes.BEGIN_BAD_STATE)
        if len(self.players) < Limits.MIN_PLAYERS:
            raise APIError(Codes.NOT_ENOUGH_PLAYERS)
        random.shuffle(self.order)
        for user in self.players:
            for _ in range(self.CARDS_PER_ROUND):
                card = self.deck.deal()
                if card is None:
                    self.init_game()  # rewind the dealing
                    raise APIError(Codes.DECK_TOO_SMALL)
                self.players[user].deal(card)
        self.state = States.CLUE
        self.ping()

    def create_clue(self, user, clue, card):
        """Transitions from CLUE to PLAY, or throws APIError."""
        if self.state != States.CLUE:
            raise APIError(Codes.CLUE_BAD_STATE)
        if user != self.clue_maker():
            raise APIError(Codes.CLUE_NOT_TURN)
        if len(clue) < Limits.MIN_CLUE_LENGTH:
            raise APIError(Codes.CLUE_TOO_SHORT)
        if len(clue) > self.max_clue_length:
            raise APIError(Codes.CLUE_TOO_LONG)
        if not self.players[user].has_card(card):
            raise APIError(Codes.NOT_HAVE_CARD)
        self.round = Round(self.players, clue, self.clue_maker())
        self.round.play_card(user, card)
        self.players[user].deal(self.deck.deal())
        self.state = States.PLAY
        self.ping()

    def play_card(self, user, card):
        """Makes the given user play a card, or throws APIError."""
        if self.state != States.PLAY:
            raise APIError(Codes.PLAY_BAD_STATE)
        if user == self.clue_maker():
            raise APIError(Codes.PLAY_NOT_TURN)
        if not user in self.players:
            raise APIError(Codes.PLAY_UNKNOWN_USER)
        if self.round.has_played(user):
            raise APIError(Codes.PLAY_ALREADY)
        if not self.players[user].has_card(card):
            raise APIError(Codes.NOT_HAVE_CARD)
        self.round.play_card(user, card)
        self.players[user].deal(self.deck.deal())
        if self.round.has_everyone_played():
            # Transition from PLAY to VOTE.
            self.round.cast_vote(self.clue_maker(),
                                 self.round.user_to_card[self.clue_maker()])
            self.state = States.VOTE
        self.ping()

    def cast_vote(self, user, card):
        """Make the given user vote for a card, or throws APIError."""
        if self.state != States.VOTE:
            raise APIError(Codes.VOTE_BAD_STATE)
        if user == self.clue_maker():
            raise APIError(Codes.VOTE_NOT_TURN)
        if not user in self.players:
            raise APIError(Codes.VOTE_UNKNOWN_USER)
        if not self.round.has_card(card):
            raise APIError(Codes.VOTE_INVALID)
        if self.round.has_voted(user):
            raise APIError(Codes.VOTE_ALREADY)
        self.round.cast_vote(user, card)
        if self.round.has_everyone_voted():
            # Transition from VOTE to CLUE or END.
            self._do_scoring()
            self.turn = (self.turn + 1) % len(self.players)
            self.state = States.CLUE
            if self.deck.is_empty():
                self.state = States.END
            for p in self.players.itervalues():
                if p.score >= self.max_score:
                    self.state = States.END
        self.ping()

    def _do_scoring(self):
        """Increments the scores of all players for this Round."""
        for user in self.players:
            v = self.round.card_to_voted_users[self.round.user_to_card[user]]
            if user == self.clue_maker():
                if len(v) == 0 or len(v) == len(self.players) - 1:
                    for u in self.players:
                        if u != user:
                            self.round.score(u, self.SCORE_FOR_LOSS)
                else:
                    self.round.score(user, self.SCORE_FOR_CORRECT)
                    for u in v:
                        self.round.score(u, self.SCORE_FOR_CORRECT)
            else:
                self.round.score(user, self.SCORE_FOR_TRICK*len(v))
