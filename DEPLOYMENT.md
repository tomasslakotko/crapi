# 🚀 Инструкция по развертыванию Crew Schedule Parser

## 1. Развертывание на Render (Рекомендуемый способ)

**Render** — это современный хостинг, который идеально подходит для этого проекта. Благодаря файлу `render.yaml` в репозитории, развертывание происходит практически автоматически.

### Шаг 1: Загрузите код на GitHub
- Если вы еще этого не сделали, создайте репозиторий на [GitHub](https://github.com/new) и загрузите в него весь код проекта.

### Шаг 2: Создайте Blueprint на Render
1.  Перейдите в [панель управления Render](https://dashboard.render.com/).
2.  Нажмите **New +** и выберите **Blueprint**.
3.  Подключите ваш GitHub-репозиторий.
4.  Render автоматически обнаружит файл `render.yaml` и настроит сервис.
5.  Нажмите **Apply**.

Вот и все! Render соберет Docker-образ из вашего `Dockerfile`, запустит сервис и предоставит вам публичную ссылку вида `https://crew-schedule-parser.onrender.com`.

---

## 2. Развертывание с помощью Docker (универсальный способ)

Этот способ подойдет для любого хостинга, который поддерживает Docker (DigitalOcean, AWS, Vultr и т.д.).

1. **Соберите и запустите контейнер:**
   ```bash
   docker-compose up -d
   ```
2. **Настройте веб-сервер (Nginx, Apache) как обратный прокси** для перенаправления трафика с вашего домена на порт `3000` контейнера.

---

## 3. Локальный запуск для разработки

1. **Клонируйте репозиторий.**
2. **Установите зависимости:**
   ```bash
   npm install
   pip install -r requirements.txt
   ```
3. **Запустите сервер:**
   ```bash
   npm start
   ```
4. **Откройте в браузере:** `http://localhost:3000`

## Тестирование

1. **Создайте тестовый PDF (локально):**
   ```bash
   python3 create_simple_pdf.py
   ```
2. **Загрузите файл `simple_roster.pdf` через веб-интерфейс.**
3. **Проверьте результаты в таблице и скачайте CSV.**

## Продакшн развертывание

### С использованием Docker

1. **Настройте переменные окружения:**
   ```bash
   export NODE_ENV=production
   export PORT=3000
   ```

2. **Запустите с Docker Compose:**
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

3. **Настройте Nginx (опционально):**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:3000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

### Без Docker

1. **Установите PM2:**
   ```bash
   npm install -g pm2
   ```

2. **Запустите приложение:**
   ```bash
   pm2 start server.js --name "crew-schedule-parser"
   pm2 startup
   pm2 save
   ```

3. **Настройте автозапуск:**
   ```bash
   pm2 startup
   ```

## Мониторинг

### Docker
```bash
# Просмотр логов
docker-compose logs -f

# Статус контейнеров
docker-compose ps
```

### PM2
```bash
# Просмотр логов
pm2 logs crew-schedule-parser

# Статус приложений
pm2 status
```

## Обновление

### Docker
```bash
docker-compose pull
docker-compose up -d
```

### PM2
```bash
pm2 reload crew-schedule-parser
```

## Устранение неполадок

### Проблемы с портом
```bash
# Проверьте, что порт 3000 свободен
lsof -i :3000

# Измените порт в docker-compose.yml или через переменную окружения
export PORT=3001
```

### Проблемы с Python
```bash
# Проверьте версию Python
python3 --version

# Переустановите зависимости
pip install -r requirements.txt --force-reinstall
```

### Проблемы с Node.js
```bash
# Проверьте версию Node.js
node --version

# Очистите кэш npm
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
``` 