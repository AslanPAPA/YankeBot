from aiogram.fsm.state import State, StatesGroup



class Pars(StatesGroup):
    vkSoob = State()
    vkBesed = State()

class Rass(StatesGroup):
    linksForRas = State()
    msgForRas = State()



class Auth(StatesGroup):
    token = State()
    deleteAcc = State()
    SendMsg = State()
