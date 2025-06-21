# Crew Schedule Parser - Парсер графиков экипажа

Веб-платформа для автоматического парсинга графиков экипажа из PDF файлов Lufthansa Netline Crewlink.

## 🌐 Live Demo / Живая демонстрация

**🚀 [Try it now / Попробовать сейчас](https://crew-schedule-parser.onrender.com)**

## 🚀 One-Click Deploy / Развертывание в один клик

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

*Нажмите кнопку выше для автоматического развертывания на Render*

## 🚀 Возможности

- Загрузка PDF файлов через веб-интерфейс
- Автоматический парсинг графиков экипажа
- Экспорт результатов в CSV формат
- **🔐 Защищенный REST API с ключом доступа**
- Современный и удобный интерфейс
- Поддержка drag & drop загрузки файлов
- Адаптивный дизайн для мобильных устройств

## 📋 Требования

- Node.js (версия 14 или выше)
- Python 3.7 или выше
- pip (менеджер пакетов Python)

## 🛠️ Установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone <your-repo-url>
   cd crew-schedule-parser
   ```

2. **Установите Node.js зависимости:**
   ```bash
   npm install
   ```

3. **Установите Python зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Запуск

1. **Запустите сервер:**
   ```bash
   npm start
   ```

2. **Откройте браузер и перейдите по адресу:**
   ```
   http://localhost:3000
   ```

## 📖 Использование

1. Откройте веб-интерфейс в браузере
2. Перетащите PDF файл с графиком экипажа в область загрузки или нажмите "Выбрать файл"
3. Дождитесь завершения обработки
4. Просмотрите результаты в таблице
5. Скачайте CSV файл с результатами

## 📁 Структура проекта

```
crew-schedule-parser/
├── server.js                 # Express сервер
├── package.json             # Node.js зависимости
├── requirements.txt         # Python зависимости
├── public/
│   └── index.html          # Веб-интерфейс
├── netline-crewlink-parser/ # Python парсер
│   ├── parser.py           # Парсер PDF файлов
│   └── TXTtoCSV.py         # Конвертер в CSV
├── uploads/                # Временная папка для загруженных файлов
├── outputs/                # Папка для результатов
├── create_simple_pdf.py    # Генератор тестовых PDF
└── README.md              # Документация
```

## 🔧 Технологии

- **Backend:** Node.js, Express
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **PDF Parsing:** Python, pdfplumber, pandas
- **File Upload:** Multer
- **PDF Generation:** ReportLab (для тестирования)

## 🤖 API для интеграции

Платформа предоставляет защищенный REST API для программного парсинга расписаний.

**📖 Для AI агентов (Cursor AI):** См. [CURSOR_AI_INTEGRATION.md](./CURSOR_AI_INTEGRATION.md) для подробной документации по интеграции.

### 🔐 Аутентификация

API защищен ключом доступа. Для использования API необходимо:

1. **Установить переменную окружения `API_KEY`** при развертывании
2. **Передавать ключ в заголовке `x-api-key`** при каждом запросе

#### Настройка API ключа на Render:
1. Перейдите в Dashboard → Ваш сервис → Environment
2. Добавьте переменную: `API_KEY` = `ваш-секретный-ключ`
3. Нажмите "Save Changes"

**Эндпоинт:** `POST /api/parse`

**Заголовки:**
- `x-api-key: ваш-секретный-ключ`
- `Content-Type: multipart/form-data`

**Тело запроса:** `multipart/form-data`
- **Поле:** `pdfFile`
- **Значение:** Файл PDF с расписанием.

**Пример запроса с помощью cURL:**
```bash
curl -X POST \
  -H "x-api-key: ваш-секретный-ключ" \
  -F "pdfFile=@/путь/к/вашему/roster.pdf" \
  https://crew-schedule-parser.onrender.com/api/parse
```

**Пример запроса с помощью JavaScript:**
```javascript
const formData = new FormData();
formData.append('pdfFile', fileInput.files[0]);

fetch('https://crew-schedule-parser.onrender.com/api/parse', {
  method: 'POST',
  headers: {
    'x-api-key': 'ваш-секретный-ключ'
  },
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

**Пример успешного ответа (200 OK):**
```json
{
    "success": true,
    "data": [
        {
            "Date": "Fri20",
            "Weekday": "Fri",
            "Day Number": "20",
            "Duty Type": "FLIGHT",
            "Duty Location": "",
            "Check-In Airport": "",
            "Check-In Time": "",
            "Check-Out Time": "",
            "Hotel": "",
            "Flight Number": "OS 231",
            "Departure Airport": "VIE",
            "Departure Time": "1300",
            "Arrival Time": " 1410",
            "Arrival Airport": "BER",
            "Aircraft": "A220",
            "Requested": "False",
            "Flight Time": "05:45",
            "Duty Time": "09:35",
            "Rest Time": "",
            "Meals": ""
        }
    ]
}
```

**Пример ответа с ошибкой аутентификации (401 Unauthorized):**
```json
{
    "success": false,
    "error": "Unauthorized: Invalid API Key"
}
```

**Пример ответа с ошибкой обработки (500 Internal Server Error):**
```json
{
    "success": false,
    "error": "Сообщение об ошибке"
}
```

## 📝 Формат данных

Парсер извлекает следующие данные из PDF:
- Дата и день недели
- Тип дежурства (C/I - Check In, C/O - Check Out)
- Информация о рейсах (номер, аэропорты, время)
- Информация об отелях
- Время работы и отдыха (FT - Flight Time, DT - Duty Time, RT - Rest Time)
- Информация о питании

## 🧪 Тестирование

Для тестирования платформы создан генератор тестовых PDF файлов:

```bash
python3 create_simple_pdf.py
```

Это создаст файл `simple_roster.pdf` с примером расписания экипажа.

## 🌐 Развертывание

### Быстрое развертывание на Render
1. **Нажмите кнопку "Deploy to Render"** выше
2. **Подключите свой GitHub аккаунт** к Render
3. **Форкните этот репозиторий** в свой GitHub
4. **Выберите ваш форк** в списке репозиториев
5. **Добавьте переменную окружения:**
   - Ключ: `API_KEY`
   - Значение: `ваш-секретный-ключ-для-api`
6. **Нажмите "Deploy"**

### Локальное развертывание
1. Установите зависимости (см. раздел "Установка")
2. (Опционально) Установите переменную окружения: `export API_KEY=your-secret-key`
3. Запустите сервер: `npm start`
4. Откройте http://localhost:3000

### Развертывание на сервере
1. Загрузите код на сервер
2. Установите Node.js и Python
3. Установите зависимости
4. **Установите переменную окружения `API_KEY`**
5. Настройте процесс-менеджер (PM2, systemd)
6. Настройте веб-сервер (Nginx, Apache) для проксирования запросов

## 🔒 Безопасность

- **🔐 API защищен ключом доступа**
- Валидация типов файлов (только PDF)
- Ограничение размера загружаемых файлов
- Автоматическая очистка временных файлов
- CORS настройки для веб-интерфейса

## 🐛 Устранение неполадок

### Проблемы с Python
- Убедитесь, что установлен Python 3.7+
- Проверьте установку зависимостей: `pip list`
- Используйте `python3` вместо `python`

### Проблемы с Node.js
- Проверьте версию Node.js: `node --version`
- Переустановите зависимости: `rm -rf node_modules && npm install`

### Проблемы с парсингом
- Убедитесь, что PDF файл имеет правильный формат
- Проверьте, что файл не поврежден
- Используйте тестовый файл для проверки работы парсера

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

MIT License

## 🙏 Благодарности

Основано на парсере [netline-crewlink-parser](https://github.com/Peskyleo1/netline-crewlink-parser) от Peskyleo1.

## 📞 Поддержка

Если у вас возникли вопросы или проблемы, создайте Issue в репозитории. 