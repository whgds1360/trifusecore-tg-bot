from handlers.MainMenu import *
from handlers.Start import *
from handlers.ForwardMenu import *
from handlers.AiMenu import ai_menu_router

all_routers = [main_menu_router, start_router, forward_menu_router, ai_menu_router]
