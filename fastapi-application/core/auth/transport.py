from fastapi_users.authentication import CookieTransport

cookie_transport = CookieTransport(

    cookie_secure=False,  # Отключение Secure
    cookie_samesite='none',  # Настройка SameSite ("lax", "strict", "none")
    cookie_max_age=3600,
)
