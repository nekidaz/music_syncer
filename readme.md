# 🎵 Music Syncer

> Сервис для синхронизации любимых треков между **Spotify** и **YouTube Music**.

---

## 📌 Возможности

- 🔄 Синхронизация треков из **Liked Songs** Spotify в плейлист YouTube Music
- ➕ Добавление новых треков
- ➖ Удаление треков, если они исчезли из "любимых" в Spotify
- 🔒 Безопасная авторизация через `.env` и OAuth
- ⚙️ Production-ready воркер с логированием и планировщиком

---

## 🚀 Быстрый старт

### 1. Установи зависимости

```bash
pip install -r requirements.txt
```

### 2. Создай `.env` файл

```env
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback

YTMUSIC_CLIENT_ID=your_ytmusic_client_id
YTMUSIC_CLIENT_SECRET=your_ytmusic_client_secret
```

---

### 3. Авторизация YouTube Music

Создай файл `oauth.json` через браузер и [официальную инструкцию ytmusicapi](https://ytmusicapi.readthedocs.io/en/latest/setup.html#authenticated-requests)

---

## 🧠 Как работает

Воркеры запускаются один раз в сутки и:

1. Загружают все любимые треки из Spotify
2. Получают/создают плейлист в YouTube Music
3. Сравнивают содержимое
4. Добавляют новые треки
5. Удаляют те, которые были удалены из Spotify

---


## 📁 Структура проекта

```
music_syncer/
├── clients/
│   ├── spotify.py
│   └── youtube_music.py
├── services/
│   └── music_sync_service.py
├── worker/
│   └── daily_worker.py
├── config/
│   └── config.py
├── models/
│   └── track.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 📅 План на будущее

- [ ] Синхронизация YouTube → Spotify
- [ ] Кэширование и лог аналитики

---

## 🛡 Безопасность

- OAuth-секреты **никогда не хранятся в коде**
- `.env` файл — только локально
- GitHub Push Protection активен

---

## 👨‍💻 Автор

Made with ❤️ by [@nekidaz](https://github.com/nekidaz)
