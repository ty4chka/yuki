# yuki-index

Подписанный индекс пакетов для [yuki](https://github.com/YOU/yuki). Здесь нет серверов: клиенты берут нужные файлы по HTTPS
из этого репозитория и проверяют подписи сами.

```
index/ab/cd/<имя>.json        запись пакета
index/ab/cd/<имя>.json.sig    подпись Ed25519
catalog.json(.sig)            каталог для `yuki search`
keys/                         ключи для CI и ротация
releases/                     примеры release.json
```

Как пользоваться и как поднять свой индекс: **TUTORIAL.md** в корне проекта yuki.
