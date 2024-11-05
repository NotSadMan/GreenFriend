from aiogram import Router


def setup_routers() -> Router:
    import bot.handlers.admin.message as admin_message
    import bot.handlers.admin.callback as admin_callback
    import bot.handlers.user.message as user_message
    import bot.handlers.user.register_plant as register_plant
    import bot.handlers.user.my_plants as my_plants

    admin_message.register_handlers()
    admin_callback.register_handlers()
    user_message.register_handlers()
    register_plant.register_handlers()
    my_plants.register_handlers()


    router = Router()
    router.include_router(admin_message.router)
    router.include_router(admin_callback.router)
    router.include_router(user_message.router)
    router.include_router(register_plant.router)
    router.include_router(my_plants.router)

    return router
