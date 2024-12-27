const API_URL = "localhost:8080/convert";

document.getElementById("currency-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    // Получаем введённые данные
    const amount = parseFloat(document.getElementById("amount").value);
    const fromCurrency = document.getElementById("from-currency").value;
    const toCurrency = document.getElementById("to-currency").value;
    const resultElement = document.getElementById("result");

    // Проверка на корректный ввод
    if (isNaN(amount) || amount <= 0) {
        resultElement.textContent = "Введите корректную сумму.";
        return;
    }

    try {
        // Запрос к API для получения курсов валют
        const response = await fetch(`${API_URL}?base=${fromCurrency}&symbols=${toCurrency}`);
        const data = await response.json();

        if (data.success) {
            const rate = data.rates[toCurrency];
            const convertedAmount = (amount * rate).toFixed(2);
            resultElement.textContent = `Результат: ${convertedAmount} ${toCurrency}`;
        } else {
            resultElement.textContent = "Ошибка: не удалось получить курсы валют.";
        }
    } catch (error) {
        console.error("Ошибка при получении данных с API:", error);
        resultElement.textContent = "Произошла ошибка. Попробуйте ещё раз.";
    }
});