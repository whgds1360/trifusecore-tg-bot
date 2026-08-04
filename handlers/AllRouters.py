from handlers.MainMenu import main_menu_router
from handlers.Start import start_router
from handlers.ForwardMenu import forward_menu_router
from handlers.AiMenu import ai_menu_router
from handlers.TempMailMenu import temp_mail_menu_router

all_routers = [main_menu_router,
               start_router,
               forward_menu_router,
               ai_menu_router,
               temp_mail_menu_router]
