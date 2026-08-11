from features.main_menu.main_menu_router import main_menu_router
from features.start.start_router import start_router
from features.forwarding.forward_router import forward_menu_router
from features.ai_chat.ai_router import ai_menu_router
from features.temp_mail.temp_mail_router import temp_mail_menu_router

all_routers = [main_menu_router,
               start_router,
               forward_menu_router,
               ai_menu_router,
               temp_mail_menu_router]
