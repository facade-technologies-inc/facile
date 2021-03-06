"""
..
    /------------------------------------------------------------------------------\
    |                 -- FACADE TECHNOLOGIES INC.  CONFIDENTIAL --                 |
    |------------------------------------------------------------------------------|
    |                                                                              |
    |    Copyright [2019] Facade Technologies Inc.                                 |
    |    All Rights Reserved.                                                      |
    |                                                                              |
    | NOTICE:  All information contained herein is, and remains the property of    |
    | Facade Technologies Inc. and its suppliers if any.  The intellectual and     |
    | and technical concepts contained herein are proprietary to Facade            |
    | Technologies Inc. and its suppliers and may be covered by U.S. and Foreign   |
    | Patents, patents in process, and are protected by trade secret or copyright  |
    | law.  Dissemination of this information or reproduction of this material is  |
    | strictly forbidden unless prior written permission is obtained from Facade   |
    | Technologies Inc.                                                            |
    |                                                                              |
    \------------------------------------------------------------------------------/

This file contains the super tokens class that initializes tokens as a list and a function that
iterates through the tokens in the token list.
"""

from threading import Lock

if 'CONTEXT' not in locals():
    try:  # Facile
        from libs.env import CONTEXT
        from libs.env import InvalidContextException
    except ImportError:  # Sphinx
        from .libs.env import CONTEXT
        from .libs.env import InvalidContextException

if CONTEXT in ("Facile", "Sphinx"):
    from tguiil.tokens import Token
elif CONTEXT in ("API"):
    # from .tokens import Token
    pass
else:
    raise InvalidContextException(f"Invalid context: {CONTEXT}")


class SuperToken:
    """
    A super token is used to identify a component in multiple states. They can be ignored if the user
    does not care about specific components.
    """
    id_counter = 1

    def __init__(self, token, parent: 'SuperToken'):
        """
        Constructs a unique identifier and a way to hide certain components

        :param token: The first token to be added to the SuperToken that's being created.
        :type token: Token
        :param parent: The parent of the SuperToken being created.
        :type parent: SuperToken or NoneType
        :return: None
        :rtype: NoneType
        """
        self._tokenListLock = Lock()
        self.tokens = [token]
        self.id = SuperToken.id_counter
        SuperToken.id_counter += 1
        self.ignoreFlag = False

        width = token.rectangle.width()
        height = token.rectangle.height()

        if parent is None:
            px = 0
            py = 0
        elif token.parentRect:
            px = token.parentRect.left
            py = token.parentRect.top
        else:  # Sometimes parentRect is still none for some reason so we have to deal with it
            px = parent.tokens[0].rectangle.left
            py = parent.tokens[0].rectangle.top
        self.posRelativeToParent = (
            token.rectangle.left - px, token.rectangle.top - py, width, height)

    def addToken(self, tokenA):
        """
        The addToken function adds a token to the supertoken.

        :param tokenA: Returns the super token of the token to which the component belongs to
        :type tokenA: Token
        :return: None
        :rtype: SuperToken
        """
        self._tokenListLock.acquire()
        try:
            self.tokens.append(tokenA)
        finally:
            self._tokenListLock.release()

    def getTokens(self) -> list:
        """
        Gets a copy of the token list. It's important that this is a copy because 2 threads may access token
        data at a time.

        This function shares a common mutex with the addToken function.

        :return: list of tokens
        :rtype: list[Token]
        """
        copy = []
        self._tokenListLock.acquire()
        try:
            copy = self.tokens[:]
        finally:
            self._tokenListLock.release()
            return copy

    def shouldContain(self, token2):
        """
        determines if this SuperToken should contain the token provided

        :param token2: The token that we would like to add to the super token
        :type token2: Token
        :return: The decision about whether it should be contained or not and the certainty
        :rtype: Token.Match, float
        """
        DEBUG_TOKEN_COMPARISON = False

        bestCloseScore = 0
        for token in self.tokens:
            result = token.isEqualTo(token2)
            decision, score = result

            if DEBUG_TOKEN_COMPARISON:
                print()
                print("/------------------------------------------------")
                print("COMPARE:")
                print("\t", token)
                print("\t", token2)
                print(decision, score)
                print("\\------------------------------------------------")
                print()

            if decision == Token.Match.EXACT:
                return Token.Match.EXACT, score
            elif decision == Token.Match.CLOSE:
                if score > bestCloseScore:
                    bestCloseScore = score

        if bestCloseScore == 0:
            return Token.Match.NO, 0

        return Token.Match.CLOSE, bestCloseScore

    def __str__(self):
        return "SuperToken:\n\t" + "\n\t".join([str(token) for token in self.tokens])

    def __repr__(self):
        return self.__str__()

    def asDict(self) -> dict:
        """
        Get a dictionary representation of the visibility behavior.

        .. note::
            This is not just a getter of the __dict__ attribute.

        :return: The dictionary representation of the object.
        :rtype: dict
        """
        d = {}
        d["id"] = self.id
        d["tokens"] = [t.asDict() for t in self.tokens]
        d["ignoreFlag"] = self.ignoreFlag
        d['relativePos'] = list(self.posRelativeToParent)
        return d

    @staticmethod
    def fromDict(d: dict) -> 'SuperToken':
        """
        Creates a super token from a dictionary.

        :param d: The dictionary that represents the Component.
        :type d: dict
        :return: The SuperToken object that was constructed from the dictionary
        :rtype: SuperToken
        """

        if d is None:
            return None

        st = SuperToken.__new__(SuperToken)
        st._tokenListLock = Lock()
        st.tokens = [Token.fromDict(t) for t in d['tokens']]
        st.ignoreFlag = d['ignoreFlag']
        st.id = d['id']
        st.posRelativeToParent = tuple(d['relativePos'])
        return st
