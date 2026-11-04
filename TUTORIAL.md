# yuki: туториал, от нуля до своего индекса и первого пакета

Всё делается без серверов: индекс это обычный git-репозиторий на GitHub (или Codeberg/GitLab).
Клиент берёт из него по HTTPS нужные файлы и сам проверяет подписи.

> Код yuki ещё не компилировался на реальной машине. Первый шаг ниже даст список ошибок сборки, их надо поправить, затем запустите `yuki selftest`.

## 0. Что понадобится

* Linux, [yukino](https://github.com/yukitsuri/yukino) (компилятор `yukic` и менеджер `yukino`)
* `git`, аккаунт GitHub
* для сборки из исходников на клиентах: `bubblewrap` и `timeout` (coreutils)
* на CI: `jq`, `curl` (есть на раннерах GitHub)

## 1. Собрать и поставить yuki

```bash
cd yuki
yukino build --release
sudo install -m 755 target/release/yuki /usr/local/bin/yuki     # путь к бинарнику зависит от вашей сборки
yuki version
yuki selftest         # эталонные проверки собранного бинарника
yuki doctor           # проверит окружение и подскажет, что поправить
```

## 2. Создать репозиторий индекса

1. На GitHub: **New repository** → `yuki-index`, публичный, без README.
2. Скопируйте шаблон и отправьте:

```bash
cp -r yuki-index-template yuki-index && cd yuki-index
git init -b main
git add . && git commit -m "init index"
git remote add origin git@github.com:YOU/yuki-index.git
git push -u origin main
```

3. Замените `YOU` и `@YOUR-ORG/...` в `CODEOWNERS` и `.github/workflows/*.yml` на свои.
4. Защитите ветку `main` (Settings → Branches → Add rule):
   * Require a pull request before merging, Require review from Code Owners
   * Require status checks: `verify index`
   * Require signed commits, Do not allow bypassing
5. Адрес индекса для клиентов:

```
https://raw.githubusercontent.com/YOU/yuki-index/main
```

> В репозитории обязателен `.gitattributes` с `* -text`: иначе перевод строк изменит байты файлов и подписи перестанут сходиться.

## 3. Ключи

Подписывающий ключ создаётся на машине мейнтейнера, лучше офлайн:

```bash
yuki keys gen main            # секретный seed лежит в ~/.config/yuki/keys/main.seed (права 0600)
yuki keys export main         # публичный ключ, 64 hex: его можно публиковать
```

* **Секретный ключ не коммитьте и бэкапьте офлайн** (зашифрованный диск, менеджер паролей).
* Публичный ключ положите в `keys/trusted_keys` репозитория индекса (по образцу `trusted_keys.example`). CI проверяет записи именно им.
* Рекомендуется 3 ключа (владелец, запасной, CI-продление) и порог 2 из 3 для ротации (раздел 9).

## 4. Настроить клиента

```bash
export YUKI_INDEX=https://raw.githubusercontent.com/YOU/yuki-index/main      # для системных установок положите в /etc/yuki/index_url
sudo mkdir -p /etc/yuki && echo "$YUKI_INDEX" | sudo tee /etc/yuki/index_url
sudo yuki keys trust main <публичный-ключ>        # покажет отпечаток, сверьте его с владельцем и подтвердите
yuki doctor
```

## 5. Первый пакет-приложение

### 5.1 Собрать архив пакета

Пакет это дерево файлов, как оно ляжет в систему (только `usr/`, `opt/`, `etc/`):

```bash
mkdir -p pkgroot/usr/bin pkgroot/usr/share/doc/hello
install -m 755 hello pkgroot/usr/bin/hello
echo "hello docs" > pkgroot/usr/share/doc/hello/README
yuki pack hello ./pkgroot hello-1.0.0-linux-x86_64.tar.zst
```

`yuki pack` проверит политику (никаких симлинков, защищённых путей и т.п.), сделает архив, прогонит аудит и напечатает хеш и готовый кусок для записи.

### 5.2 Выложить архив

GitHub → ваш репозиторий пакета → **Releases → Draft a new release** → тег `v1.0.0` → прикрепите `hello-1.0.0-linux-x86_64.tar.zst`.
Ссылка вида `https://github.com/YOU/hello/releases/download/v1.0.0/hello-1.0.0-linux-x86_64.tar.zst` пойдёт в запись.

### 5.3 Описать релиз

`hello.release.json` (хеш можно не писать: `yuki index add` скачает архив, проверит его и вычислит сам):

```json
{
  "name": "hello", "kind": "app", "version": "1.0.0",
  "summary": "prints a friendly greeting", "license": "MIT",
  "bin": [ { "target": "linux-x86_64",
             "url": "https://github.com/YOU/hello/releases/download/v1.0.0/hello-1.0.0-linux-x86_64.tar.zst" } ]
}
```

Название платформы клиенту показывает `yuki config` (поле platform). Для нескольких платформ добавляйте элементы в `bin`.

### 5.4 Добавить в индекс и отправить PR

```bash
cd yuki-index
git checkout -b add-hello
yuki index add ../hello.release.json main       # скачает, проверит, подпишет ключом main
yuki index catalog main                         # обновит catalog.json для `yuki search`
git add index catalog.json catalog.json.sig
git commit -S -m "hello 1.0.0"
git push -u origin add-hello                    # и откройте pull request
```

CI проверит подписи, поля, зависимости, неизменяемость старых релизов и скачает все артефакты. После слияния пакет доступен всем.

### 5.5 Поставить

```bash
yuki search hello
yuki show hello
sudo yuki install hello
hello
```

## 6. Пакет, который собирается из исходников

Если для платформы нет готовой сборки, yuki предложит собрать. В записи указываются архив исходников, команда сборки и **явный список файлов**,
которые попадут в систему (из чего, куда, с каким режимом):

```json
{
  "name": "ripgrep", "kind": "app", "version": "14.1.0",
  "src": {
    "url": "https://github.com/BurntSushi/ripgrep/archive/refs/tags/14.1.0.tar.gz",
    "net": false,
    "build": ["yukino", "build", "--release"],
    "files": [ { "from": "target/release/rg", "to": "usr/bin/rg", "mode": "755" } ]
  }
}
```

Сборка идёт без сети и в песочнице, поэтому все зависимости должны быть внутри архива исходников.

## 7. Библиотеки для проектов

```json
{ "name": "json-yukino", "kind": "lib", "version": "1.2.0",
  "url": "https://github.com/YOU/json-yukino/archive/<commit>.tar.gz", "deps": ["ansi-kit@2.0.1"] }
```

```bash
yuki index add json-yukino.release.json main
# у пользователя, в проекте:
yuki add json-yukino          # запишет в yuki.toml link + checksum всего дерева зависимостей
yukino build
```

## 8. CI и автопродление

* `verify-pr.yml` запускает `yuki index check download` для каждого PR. Доверенные ключи берутся из **целевой** ветки, а не из PR,
  иначе автор PR мог бы подсунуть свой ключ.
* В `verify-pr.yml` и `renew.yml` впишите ссылку на релиз бинарника yuki и его blake3 (`yuki verify` проверит его перед запуском).
* Записи живут 90 дней. `renew.yml` раз в месяц открывает PR с продлением. Для него создайте отдельный ключ `renew`, добавьте его публичную часть
  в `trusted_keys` и положите seed в секрет `YUKI_RENEW_SEED` окружения `signing` (с ручным одобрением).
  Помните: любой доверенный ключ технически может подписать любую запись, поэтому PR от бота тоже проходит ревью (в диффе должны меняться только `seq` и `expires`).

## 9. Ротация и отзыв ключей

`keys/rotation.json` (пример в шаблоне):

```json
{ "seq": 2, "expires": 1830297600,
  "add": [ { "name": "main2", "key": "<новый публичный ключ>" } ],
  "revoke": [ "<скомпрометированный публичный ключ>" ] }
```

Подписи собираются у владельцев ключей (каждый на своей машине):

```bash
yuki keys sign main    keys/rotation.json  >> keys/rotation.sigs
yuki keys sign backup  keys/rotation.json  >> keys/rotation.sigs
```

Закоммитьте `rotation.json` и `rotation.sigs`, слейте PR. Клиенты применяют это командой `sudo yuki keys refresh` и только если подписей
от **разных уже доверенных** ключей не меньше порога (`echo 2 | sudo tee /etc/yuki/threshold`). Новый ключ сам себя ввести не может,
отозванный не вернётся.

### Несколько издателей и роли ключей

* Для публичного реестра включите подтверждение содержимого двумя издателями: на клиентах `echo 2 | sudo tee /etc/yuki/publish_threshold`.
* Первый издатель делает `yuki index add …`, второй проверяет дифф и добавляет подпись: `yuki index cosign hello backup`, затем коммит.
* Ключ автопродления в CI заводите с ролью `renewer`: `sudo yuki keys trust renew <pubkey> renewer`. Он может продлить срок записи, но не изменить релизы.
* Для CI (проверка PR) положите в `keys/trusted_keys` строки с ролью третьим словом: `renew <pubkey> renewer`.

## 10. Обновления у пользователей

```bash
sudo yuki upgrade              # все пакеты, одно подтверждение
sudo yuki upgrade hello        # один
sudo yuki self-update          # сам yuki (если нет, откатится автоматически)
yuki outdated                  # что можно обновить
sudo yuki hold hello           # не трогать при upgrade
sudo yuki rollback             # отменить последнюю транзакцию
```

Если нужно срочно снять плохой релиз: `yuki yank hello 1.0.0 main`, PR, слияние. `yuki audit` и `sudo yuki sys-audit` у пользователей покажут его.

## 11. Pacman-шпаргалка

| pacman | yuki |
|---|---|
| `-S pkg` | `sudo yuki -S pkg` |
| `-Syu` | `sudo yuki -Syu` |
| `-Ss word` | `yuki -Ss word` |
| `-Si pkg` | `yuki -Si pkg` |
| `-R pkg`, `-Rs pkg` | `sudo yuki -R pkg`, `sudo yuki -Rs pkg` |
| `-Q`, `-Qi`, `-Ql`, `-Qo` | `yuki -Q`, `-Qi`, `-Ql`, `-Qo` |
| `-Qe`, `-Qd`, `-Qdt` | `yuki -Qe`, `-Qd`, `-Qdt` |
| `-Qu`, `-Qk` | `yuki -Qu`, `yuki -Qk` |

Связи пакетов: `yuki why pkg`, `yuki tree pkg`, `yuki rdeps pkg`, `yuki related pkg`, `yuki graph dot | dot -Tpng -o graph.png`.

## 11a. Скорость и надёжность

* Загрузки параллельные: `YUKI_JOBS=8 sudo yuki install a b c` (по умолчанию до 4 потоков).
* Несколько зеркал индекса: `YUKI_INDEX=https://raw.githubusercontent.com/YOU/yuki-index/main,https://codeberg.org/YOU/yuki-index/raw/branch/main`.
* Платформу можно задать вручную: `YUKI_TARGET=linux-aarch64`.
* Сразу после первой сборки выполните `yuki selftest`: он проверит хеши, подписи, потоки и политику путей.

## 12. Если что-то пошло не так

`yuki doctor` проверит окружение. Любой код ошибки объясняет `yuki explain Y0301`.

| Ошибка | Что делать |
|---|---|
| `Y0202 no trusted keys` | `sudo yuki keys trust <имя> <ключ>` |
| `Y0204 expired` | мейнтейнер: `yuki renew <пакет> <ключ>` или `renew-all` |
| `Y0303 signature` | проверьте `yuki keys list`, `sudo yuki keys refresh`; файл в индексе испорчен или подделан |
| `Y0301 mismatch` | не использовать файл; сравнить хеш с индексом; повторить |
| `Y0742 no sandbox` | поставить `bubblewrap` |
| `Y0722 conflict` | файл принадлежит другому пакету: удалить его или `--overwrite`, если вы уверены |
| `Y0750 need root` | запустить с `sudo` |
| подпись не сходится после push | проверьте `.gitattributes` (`* -text`) |

## 13. Чек-лист безопасности владельца индекса

- [ ] секретные ключи офлайн, есть запасной ключ и порог 2 из 3
- [ ] защита ветки `main`, подписанные коммиты, CODEOWNERS
- [ ] CI проверяет каждый PR и скачивает артефакты
- [ ] есть расписание продления записей
- [ ] бинарник yuki в CI закреплён по blake3
- [ ] вы знаете, как отозвать ключ (`rotation.json`) и снять релиз (`yank`)
