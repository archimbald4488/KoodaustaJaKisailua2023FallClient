from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apiwrapper.websocket_wrapper import ClientContext
from apiwrapper.models import GameState, Command, ActionType, CompassDirection, ShootActionData, TurnActionData, MoveActionData, ShipData


ai_logger = getLogger("team_ai")
"""You can use this logger to track the behaviour of your bot. 

This is preferred to calling print("msg") as it offers 
better configuration (see README.md in root)

Examples:
    >>> ai_logger.debug("A message that is not important but helps with understanding the code during problem solving.")
    >>> ai_logger.info("A message that you want to see to know the state of the bot during normal operation.")
    >>> ai_logger.warning("A message that demands attention, but is not yet causing problems.")
    >>> ai_logger.error("A message about the bot reaching an erroneous state")
    >>> ai_logger.exception("A message that is same as error, but can be only called in Except blocks. " +
    >>>                     "Includes exception info in the log")
    >>> ai_logger.critical("A message about a critical exception, usually causing a premature shutdown")
"""


def process_tick(context: ClientContext, game_state: GameState) -> Command | None:
    """Main function defining the behaviour of the AI of the team

    Arguments:
        context (ClientContext): persistent context that can store data and state between ticks. Wiped on game creation
        game_state (GameState): the current state of the game

    Returns:
        Command: `apiwrapper.models.Command` instance containing the type and data of the command to be executed on the
        tick. Returning None tells server to move 0 steps forward.

    Note:
        You can get tick time in milliseconds from `context.tick_length_ms` and ship turn rate in 1/8th circles from
        `context.turn_rate`.

        If your function takes longer than the max tick length the function is cancelled and None is returned.
    """
    ai_logger.info("processing tick")

    x = 0 # 1-3, liikkumismäärän mukaan!
    m = 3 # massa
    s = 3 # nopeus
    Nsuunta = CompassDirection.North
    NEsuunta = CompassDirection.NorthEast
    Esuunta = CompassDirection.East
    SEsuunta = CompassDirection.SouthEast
    Ssuunta = CompassDirection.South
    SWsuunta = CompassDirection.SouthWest
    Wsuunta = CompassDirection.West
    NWsuunta = CompassDirection.NorthWest

    move_command = Command(action=ActionType.Move, payload=MoveActionData(distance=x))
    shoot_command = Command(action=ActionType.Shoot, payload=ShootActionData(mass=m, speed=s))
    turn_command = Command(action=ActionType.Turn, payload=TurnActionData(direction=suunta))

    if (ShipData.heat >= 20):
        x = 3
        move_command = Command(action=ActionType.Move, payload=MoveActionData(distance=x))
        return move_command
    
    
    """ 
    1: Tsekataan ympäristö --> näkyykö vihollista tai seinää, missä?

    
    2a (vihollinen): 
        jos (seinä x lähellä):
            move_command = Command(action_type=ActionType.Turn
            
        jos (vihollinen suunnassa x) [eli suoraan koordinaatistossa horisontaalisti, vertikaalisesti tai ristiin]:
            move_command = Command(action_type=ActionType.Shoot
        muuten:
            laske lähin suunta, jossa vihollinen on sijainniltaan aiemman kohdan mukainen
            move_command = Command(action_type=ActionType.Move

    2b (seinä): 
        jos (toinen seinä):
            käännytään vastakkaiseen suuntaan seinän 2 kanssa
            move_command = Command(action_type=ActionType.Turn
        käännytään kulkemaan seinän kanssa yhdensuuntaisesti
        move_command = Command(action_type=ActionType.Turn

    2e (ei mitään):
        move_command = Command(action_type=ActionType.Move
    """
    return move_command
