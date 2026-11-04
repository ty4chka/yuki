import os
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")

def pic(name, alt, width=None, link=None):
    w = f' width="{width}"' if width else ""
    img = (f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">'
           f'<img alt="{alt}" src="assets/{name}-light.svg"{w}></picture>')
    return f'<a href="{link}">{img}</a>' if link else img

def icon(name, h=34):
    return f'<img src="assets/sec-{name}.svg" height="{h}" align="absmiddle" alt="">'

def step(n, title, body, who=None):
    chip = f'<img src="assets/who-{who}.svg" height="28" alt="{who}">' if who else ""
    return (f'<tr><td width="96" valign="top"><img src="assets/num-{n}.svg" width="72" alt="{n}"></td>'
            f'<td valign="top"><b>{title}</b><br>{body}</td><td valign="top" align="right">{chip}</td></tr>')

md = []
md.append(f'''<div align="center">

{pic("banner", "yuki: менеджер пакетов для Yukino", 880)}

<sub>The package manager for Yukino. No servers, with signatures and rollback.</sub>

<p>
{pic("btn-start", "Быстрый старт", 230, "#start")}
{pic("btn-tutorial", "Свой индекс: туториал", 280, "TUTORIAL.md")}
</p>
<p>
{pic("btn-security", "Модель защиты", 230, "DESIGN.md")}
{pic("btn-commands", "Все команды", 200, "#commands")}
</p>

{pic("status", "статус: ещё не собирался")}

<p>
{pic("stat-cmds", "команд", 205)}
{pic("stat-errors", "ошибок с разбором", 205)}
{pic("stat-servers", "своих серверов", 205)}
{pic("stat-modes", "режима терминала", 205)}
</p>

</div>

{pic("divider", "", 880)}
''')

md.append(f'''<a name="about"></a>
## {icon("arrow")} Что это

**yuki** ставит приложения в систему (`sudo yuki install`, как pacman) и библиотеки в проекты (`yuki add`, запись в `yuki.toml`).
Реестр это обычный git-репозиторий: файлы раздаёт GitHub, а доверие строится на подписях и хешах, поэтому **свои серверы не нужны**.

<p align="center"><img src="assets/preview/yuki-live.gif" width="760" alt="установка с растущим деревом зависимостей"></p>
<p align="center"><sub>Живая панель: фазы сверху, дерево зависимостей растёт снизу, загрузки идут параллельно</sub></p>

<table align="center">
<tr>
<td>{pic("card-signed", "Подписанный индекс", 290)}</td>
<td>{pic("card-priv", "Без root до конца", 290)}</td>
<td>{pic("card-fast", "Параллельные загрузки", 290)}</td>
</tr>
<tr>
<td>{pic("card-tx", "Транзакции и откат", 290)}</td>
<td>{pic("card-build", "Нет бинарника? Соберём", 290)}</td>
<td>{pic("card-graph", "Связи пакетов", 290)}</td>
</tr>
</table>
''')

md.append(f'''<a name="start"></a>
## {icon("arrow")} Быстрый старт

<table>
<tr><td width="96" valign="top"><img src="assets/num-1.svg" width="72" alt="1"></td><td valign="top"><b>Соберите и проверьте сборку</b><br>первая сборка покажет ошибки компиляции, исправьте их, затем <code>selftest</code> сверит хеши, подписи и потоки с эталонами</td></tr>
</table>

```bash
cd yuki && yukino build --release
sudo install -m 755 target/release/yuki /usr/local/bin/yuki
yuki selftest && yuki doctor
```

<table>
<tr><td width="96" valign="top"><img src="assets/num-2.svg" width="72" alt="2"></td><td valign="top"><b>Укажите индекс и доверенный ключ</b><br>отпечаток ключа покажут и попросят подтвердить</td></tr>
</table>

```bash
sudo mkdir -p /etc/yuki
echo https://raw.githubusercontent.com/YOU/yuki-index/main | sudo tee /etc/yuki/index_url
sudo yuki keys trust main <публичный-ключ>
```

<table>
<tr><td width="96" valign="top"><img src="assets/num-3.svg" width="72" alt="3"></td><td valign="top"><b>Пользуйтесь</b><br>флаги как у pacman работают</td></tr>
</table>

```bash
yuki -Ss grep                  # поиск
yuki -Si ripgrep               # описание
sudo yuki -S ripgrep pcre2     # установка, одним планом и одной транзакцией
sudo yuki -Syu                 # обновить всё, тоже одной транзакцией
sudo yuki -Rs ripgrep          # удалить вместе с ненужными зависимостями
yuki related ripgrep           # что с чем связано
sudo yuki rollback             # отменить последнюю транзакцию
```
''')

md.append(f'''<a name="how"></a>
## {icon("priv")} Как проходит установка

Root появляется только там, где нужно менять систему, и ничему не верит на слово.

<table>
{step(1, "Ребёнок приносит записи индекса", "<code>fork</code>, отказ от root, <code>no_new_privs</code>", "nobody")}
{step(2, "Root заново проверяет и строит план", "подпись, срок, откат, роли ключей, подтверждение содержимого, вопрос «продолжить?»", "root")}
{step(3, "Параллельное скачивание и сборка", "пул потоков, хеш считается в воркере; сборка в bubblewrap без сети, результат сверяется с подписанным хешем", "nobody")}
{step(4, "Root копирует к себе и проверяет файлы", "BLAKE3, аудит архива, политика путей, безопасные симлинки, процессы nobody убиты", "root")}
{step(5, "Транзакция с журналом", "журнал и резервные копии на диск до первого изменения, автооткат после сбоя", "root")}
</table>
''')

md.append(f'''<a name="commands"></a>
## {icon("grid")} Команды

`yuki help <команда>` даёт примеры, `yuki explain Y0301` объясняет любую ошибку, при опечатке подсказывает правильную команду.

<table>
<tr><th align="left">Система (<code>sudo</code>)</th><th align="left">Посмотреть</th><th align="left">Проекты и сервис</th></tr>
<tr valign="top"><td>

`install` `reinstall`<br>
`uninstall [-s]` `autoremove`<br>
`upgrade` `self-update`<br>
`hold` `unhold`<br>
`rollback` `history`

</td><td>

`search` `show`<br>
`list` `info` `files` `owns`<br>
`why` `tree` `rdeps` `related`<br>
`graph [dot]` `orphans`<br>
`outdated` `check` `sys-audit`

</td><td>

`add` `remove` `update`<br>
`fetch` `audit`<br>
`keys` `theme` `pack`<br>
`index add|cosign|check|catalog`<br>
`doctor` `config` `clean` `selftest`

</td></tr>
</table>

<details><summary><b>Флаги как в pacman</b></summary>

| pacman | yuki | pacman | yuki |
|---|---|---|---|
| `-S pkg` | установить | `-Q` | список |
| `-Syu` | обновить всё | `-Qi pkg` | info |
| `-Ss слово` | поиск | `-Ql pkg` | files |
| `-Si pkg` | описание | `-Qo путь` | owns |
| `-R pkg` | удалить | `-Qe` / `-Qd` | явные / зависимости |
| `-Rs pkg` | с ненужными зависимостями | `-Qdt` | сироты |
| `-Sc` / `-Scc` | очистить кэш | `-Qu` / `-Qk` | устаревшие / проверка файлов |

</details>
''')

md.append(f'''<a name="security"></a>
## {icon("sign")} Защита

| Угроза | Чем закрыта |
|---|---|
| Подмена архива или индекса | BLAKE3 + Ed25519, повторная проверка в root |
| Откат и «замороженный» индекс | `seq`, `expires`, локальное состояние `seen` |
| Утёкший ключ автопродления | роль `renewer` не может подписать содержимое релизов |
| Утёкший ключ издателя | порог издателей (`publish_threshold`), `cosign`, ротация и отзыв |
| Вредный архив | аудит до распаковки, политика путей, проверка симлинков, лимиты |
| Компрометация сети или сборки | разделение привилегий, bubblewrap, подписанный хеш результата |
| Сбой питания посреди установки | журнал на диск, автооткат при следующем запуске |

Подробно и **что не защищено** описано в [`DESIGN.md`](DESIGN.md).
''')

md.append(f'''<a name="look"></a>
## {icon("palette")} Как выглядит

<table>
<tr>
<td><img src="assets/preview/yuki-sys-install.png" alt="sudo yuki install"></td>
<td><img src="assets/preview/yuki-sys-errors.png" alt="ошибки с подсказками"></td>
</tr>
<tr>
<td align="center"><sub><code>sudo yuki install</code></sub></td>
<td align="center"><sub>ошибка всегда с <code>help</code> и ссылкой на <code>yuki explain</code></sub></td>
</tr>
</table>

<p align="center"><img src="assets/preview/yuki-modes.png" width="520" alt="truecolor, ansi и ASCII"></p>
<p align="center"><sub>Один результат в трёх режимах: truecolor, цвета вашего терминала (<code>palette = "ansi"</code>) и ASCII</sub></p>

Одна тема, настраиваемая файлом `theme.toml`: цвета, символы, анимация. Всё подстраивается само: truecolor → 256 → 16 → без цвета,
UTF-8 → ASCII, живой терминал → простой лог для CI. `NO_COLOR=1` работает.

<p align="center"><img src="assets/palette.svg" width="560" alt="палитра темы"></p>

```toml
# ~/.config/yuki/theme.toml  или  /etc/yuki/theme.toml
palette = "ansi"            # "rgb" | "ansi" (цвета терминала) | "mono"

[colors]
accent = "ansi:cyan"
bad    = "#f38ba8+bold"

[style]
animation = true
bar_gradient = true
```

> Картинки показывают логику кода, а не снимки реального запуска. Названия пакетов, хеши и цифры в них выдуманы.
''')

md.append(f'''<a name="index"></a>
## {icon("graph")} Свой индекс за вечер

<table>
{step(1, "Репозиторий", "скопируйте <code>yuki-index-template/</code>, включите защиту ветки <code>main</code> и CODEOWNERS")}
{step(2, "Ключи", "<code>yuki keys gen main</code>, публичную часть в <code>keys/trusted_keys</code>, секрет офлайн")}
{step(3, "Пакет", "<code>yuki pack</code> собирает архив и проверяет политику, релиз выкладывается на GitHub")}
{step(4, "Запись", "<code>yuki index add релиз.json main</code> скачает, проверит и подпишет; второй издатель делает <code>cosign</code>")}
{step(5, "CI", "<code>yuki index check download</code> на каждый PR и ежемесячное продление ключом <code>renewer</code>")}
</table>

Пошагово: [`TUTORIAL.md`](TUTORIAL.md). Шаблон репозитория: [`yuki-index-template/`](yuki-index-template/).
''')

md.append(f'''<a name="faq"></a>
## {icon("q")} FAQ

<details><summary><b>Нужны ли мне свои серверы?</b></summary>
Нет. Индекс лежит в git-репозитории, клиент берёт файлы по HTTPS (можно указать несколько зеркал) и сам проверяет подписи.
</details>

<details><summary><b>Почему установка только через sudo?</b></summary>
Установка меняет систему. Но сеть и сборка выполняются без прав, а root проверяет всё заново и применяет одну транзакцию с журналом.
</details>

<details><summary><b>Что, если нет готового бинарника?</b></summary>
yuki покажет команду сборки, список файлов, режим песочницы и закреплён ли результат подписанным хешем, и спросит согласие. В скриптах нужен <code>--allow-build</code>.
</details>

<details><summary><b>Как обновляется сам yuki?</b></summary>
<code>sudo yuki self-update</code>. Новый бинарник обязан запуститься, иначе обновление откатывается.
</details>

<details><summary><b>Утёк ключ. Что делать?</b></summary>
Подписать <code>rotation.json</code> с отзывом нужным числом ключей и выполнить <code>sudo yuki keys refresh</code>. Отозванный ключ больше не вернётся.
</details>

<details><summary><b>Это уже работает?</b></summary>
Исходники написаны по документации Yukino, но ни разу не компилировались на реальной машине. Ожидайте ошибок при первой сборке, затем запустите <code>yuki selftest</code>.
</details>

{pic("divider", "", 880)}

<p align="center"><sub>yuki · для <a href="https://github.com/yukitsuri/yukino">Yukino</a> · <a href="TUTORIAL.md">туториал</a> · <a href="DESIGN.md">модель защиты</a></sub></p>
''')

open(OUT, "w", encoding="utf-8").write("\n".join(md))
print("README.md", os.path.getsize(OUT), "bytes")
