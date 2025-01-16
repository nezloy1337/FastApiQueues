import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_exception_handler():
    return ExceptionHandler()


class ExceptionHandler:
    def handle(self, e:Exception):
        pass
    # def __init__(self):
    #     self.errors = {
    #         IntegrityError: lambda exc: JSONResponse(
    #             status_code=400,
    #             content={"error": "IntegrityError", "detail": str(exc.orig)}
    #         ),
    #
    #     }
    #
    # def handle(self, exception: Exception):
    #     match type(exception):
    #         case IntegrityError:
    #             return self.handle_integrity_error(exception)
    #
    #
    # # обработчики частных ошибок
    # def handle_integrity_error(e: IntegrityError):
    #     logger.info(f"Ошибка целостности данных: { e.args }")
    #
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail=settings.errors_description.conflict_description,
    #     )
    #
    #
    # def handle_unexpected_error(e: Exception):
    #     """
    #     Обрабатывает непредвиденные ошибки, такие как отключение базы данных,
    #     и записывает их в MongoDB. Логируется информация об ошибке и время её возникновения.
    #
    #     Параметры:
    #     e (Exception): Исключение, содержащее информацию об ошибке.
    #
    #     Действия:
    #     1. Преобразует информацию об ошибке в строку.
    #     2. Записывает сообщение об ошибке в лог. (для удобства разработки)
    #     3. Создает экземпляр шаблона журнала ошибок с описанием ошибки и текущей временной меткой.
    #     4. Вставляет журнал ошибки в коллекцию MongoDB.
    #     5. Выбрасывает HTTP-исключение с кодом 500 и сообщением об неизвестной ошибке.
    #     """
    #     error_info = str(e)
    #     logger.info(f"Неизвестная ошибка: {error_info}")
    #
    #     error_log = ExceptionLogTemplate(
    #         description=error_info,
    #         timestamp=datetime.now()
    #     )
    #
    #     error_collection.insert_one(error_log.model_dump(exclude_none=True))
    #
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=settings.errors_description.unknown_error_description,
    #     )
    #
    #
    # def handle_record_not_found(e: HTTPException):
    #     logger.info(f"запись в базе данных не найдена: { e.args }")
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=settings.errors_description.no_entry_description,
    #     )
    #
    #
    # def handle_validation_error(e: ValidationError):
    #     logger.info(f"ошибка валидации данных:{ e.args }")
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=settings.errors_description.validation_error_description,
    #     )


