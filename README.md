<div align="center">

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg"><img alt="yuki: менеджер пакетов для Yukino" src="assets/banner-light.svg" width="880"></picture>

<sub>Системный (<code>pacman</code>-подобный) и проектный (<code>cargo</code>-подобный) менеджер пакетов для языка <b>Yukino</b>.<br>Без выделенных серверов · Ed25519 + BLAKE3 · разделение привилегий <code>root / nobody</code> · поддержка PRoot / Termux · атомарный откат.</sub>

<br><br>

<p>
<a href="#start"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/btn-start-dark.svg"><img alt="Быстрый старт" src="assets/btn-start-light.svg" width="235"></picture></a>
<a href="TUTORIAL.md"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/btn-tutorial-dark.svg"><img alt="Свой индекс: туториал" src="assets/btn-tutorial-light.svg" width="285"></picture></a>
<a href="DESIGN.md"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/btn-security-dark.svg"><img alt="Модель защиты" src="assets/btn-security-light.svg" width="235"></picture></a>
<a href="#commands"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/btn-commands-dark.svg"><img alt="Все команды" src="assets/btn-commands-light.svg" width="205"></picture></a>
</p>

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/status-dark.svg"><img alt="статус сборки и самопроверки" src="assets/status-light.svg"></picture>

<p>
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/stat-cmds-dark.svg"><img alt="45 команд" src="assets/stat-cmds-light.svg" width="208"></picture>
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/stat-errors-dark.svg"><img alt="78 ошибок с разбором" src="assets/stat-errors-light.svg" width="208"></picture>
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/stat-servers-dark.svg"><img alt="0 своих серверов" src="assets/stat-servers-light.svg" width="208"></picture>
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/stat-modes-dark.svg"><img alt="3 режима терминала" src="assets/stat-modes-light.svg" width="208"></picture>
</p>

</div>

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/divider-dark.svg"><img alt="" src="assets/divider-light.svg" width="880"></picture>

<a name="about"></a>
## <img src="assets/sec-arrow.svg" height="36" align="absmiddle" alt=""> Что такое yuki

**yuki** объединяет системный менеджер пакетов (`sudo yuki install`, привычные флаги `-S`, `-Syu`, `-Rs`, `-Q` как в `pacman`) и менеджер зависимостей проекта (`yuki add`, секция `[libs.runtime]` в `yuki.toml`).  
Реестр пакетов — это обычный Git-репозиторий: архивы раздаются со статических релизов и зеркал, а целостность и свежесть гарантируются подписями **Ed25519** и хешами **BLAKE3**.

<p align="center"><img src="assets/preview/yuki-live.gif" width="780" alt="живая панель установки с деревом зависимостей"></p>
<p align="center"><sub>Живая многострочная панель (<code>LiveArea</code>): фазы транзакции сверху, дерево зависимостей и параллельные воркеры снизу</sub></p>

<table align="center">
<tr>
<td><picture><source media="(prefers-color-scheme: dark)" srcset="assets/card-signed-dark.svg"><img alt="Подписанный индекс" src="assets/card-signed-light.svg" width="290"></picture></td>
<td><picture><source media="(prefers-color-scheme: dark)" srcset="assets/card-priv-dark.svg"><img alt="Без root до конца" src="assets/card-priv-light.svg" width="290"></picture></td>
<td><picture><source media="(prefers-color-scheme: dark)" srcset="assets/card-fast-dark.svg"><img alt="Параллельные загрузки" src="assets/card-fast-light.svg" width="290"></picture></td>
</tr>
<tr>
<td><picture><source media="(prefers-color-scheme: dark)" srcset="assets/card-tx-dark.svg"><img alt="Транзакции и откат" src="assets/card-tx-light.svg" width="290"></picture></td>
<td><picture><source media="(prefers-color-scheme: dark)" srcset="assets/card-build-dark.svg"><img alt="Нет бинарника? Соберём" src="assets/card-build-light.svg" width="290"></picture></td>
<td><picture><source media="(prefers-color-scheme: dark)" srcset="assets/card-graph-dark.svg"><img alt="Связи пакетов" src="assets/card-graph-light.svg" width="290"></picture></td>
</tr>
</table>

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/divider-dark.svg"><img alt="" src="assets/divider-light.svg" width="880"></picture>

<a name="start"></a>
## <img src="assets/sec-arrow.svg" height="36" align="absmiddle" alt=""> Быстрый старт

<table>
<tr>
  <td width="92" valign="top"><img src="assets/num-1.svg" width="68" alt="1"></td>
  <td valign="top">
    <b>Соберите бинарник и запустите эталонную самопроверку</b><br>
    После сборки команда <code>yuki selftest</code> проверит криптографию BLAKE3/Ed25519, упаковщик tar, политику путей и пул потоков на эталонных векторах.
  </td>
</tr>
</table>

```bash
cd yuki && yukino build release
sudo install -m 755 yuki-work/local/build/release/*/yuki/yuki /usr/local/bin/yuki
yuki selftest && yuki doctor
```

<table>
<tr>
  <td width="92" valign="top"><img src="assets/num-2.svg" width="68" alt="2"></td>
  <td valign="top">
    <b>Подключите индекс и добавьте доверенный ключ издателя</b><br>
    Клиент выведет отпечаток ключа (fingerprint) и запросит подтверждение перед записью в хранилище доверия.
  </td>
</tr>
</table>

```bash
sudo mkdir -p /etc/yuki
echo https://example.org/yuki-index/main | sudo tee /etc/yuki/index_url
sudo yuki keys trust main <публичный-ключ-ed25519>
```

<table>
<tr>
  <td width="92" valign="top"><img src="assets/num-3.svg" width="68" alt="3"></td>
  <td valign="top">
    <b>Устанавливайте системные пакеты и библиотеки проектов</b><br>
    Поддерживаются как нативные подкоманды <code>yuki</code>, так и короткие флаги в стиле <code>pacman</code>.
  </td>
</tr>
</table>

```bash
yuki -Ss grep                  # поиск по индексу и описанию
yuki -Si ripgrep               # карточка пакета, хеши, издатели и зависимости
sudo yuki -S ripgrep pcre2     # установка одним планом и одной транзакцией
sudo yuki -Syu                 # полное обновление системы одной транзакцией
sudo yuki -Rs ripgrep          # удаление пакета вместе с ненужными зависимостями
yuki add json-yukino           # добавление библиотеки в yuki.toml текущего проекта
sudo yuki rollback             # атомарный откат последней системной транзакции
```

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/divider-dark.svg"><img alt="" src="assets/divider-light.svg" width="880"></picture>

<a name="how"></a>
## <img src="assets/sec-priv.svg" height="36" align="absmiddle" alt=""> Пятифазная архитектура установки и разделение привилегий

Процесс `root` включается только для проверки подписей и атомарной записи в файловую систему. Вся работа с сетью, разбор внешних данных и сборка из исходников изолированы в непривилегированном процессе `nobody` (с автоматическим распознаванием окружения **PRoot / Termux** по `/proc/self/status`).

<table>
<tr>
  <td width="92" valign="top"><img src="assets/num-1.svg" width="68" alt="1"></td>
  <td valign="top"><b>Загрузка метаданных индекса в изолированном процессе</b><br><code>fork()</code> → сброс групп и UID (<code>setgroups</code>, <code>setgid</code>, <code>setuid(65534)</code>, <code>prctl(NO_NEW_PRIVS)</code>) → скачивание <code>.json</code> и <code>.sig</code> во временный каталог <code>stage/dl/entries/</code>.</td>
  <td valign="top" align="right"><img src="assets/who-nobody.svg" height="28" alt="nobody"></td>
</tr>
<tr>
  <td width="92" valign="top"><img src="assets/num-2.svg" width="68" alt="2"></td>
  <td valign="top"><b>Повторная криптографическая проверка в Root и согласие</b><br>Проверка подписей <code>Ed25519</code> (с доменом <code>yuki-v1</code>), ролей <code>publisher</code>, монотонного счётчика <code>seq/seen</code> и срока <code>expires</code>. Запрос подтверждения <code>[Y/n]</code> выводится до старта живой панели <code>LiveArea</code>.</td>
  <td valign="top" align="right"><img src="assets/who-root.svg" height="28" alt="root"></td>
</tr>
<tr>
  <td width="92" valign="top"><img src="assets/num-3.svg" width="68" alt="3"></td>
  <td valign="top"><b>Параллельное скачивание и песочница сборки</b><br>Пул потоков (до 16 воркеров) скачивает архивы и считает <code>BLAKE3</code> на лету; при отсутствии бинарника исходники собираются в <code>bubblewrap</code> (<code>--unshare-all</code>, без сети) и сверяются с подписанным хешем.</td>
  <td valign="top" align="right"><img src="assets/who-nobody.svg" height="28" alt="nobody"></td>
</tr>
<tr>
  <td width="92" valign="top"><img src="assets/num-4.svg" width="68" alt="4"></td>
  <td valign="top"><b>Карантин артефактов и предраспаковочный аудит архива</b><br>Root копирует обычные файлы в <code>stage/art/</code>, заново проверяет <code>BLAKE3</code>, проводит <code>audit_tar</code> (лимиты размера, запрет спецфайлов и обхода путей), распаковывает и восстанавливает права из заголовков tar.</td>
  <td valign="top" align="right"><img src="assets/who-root.svg" height="28" alt="root"></td>
</tr>
<tr>
  <td width="92" valign="top"><img src="assets/num-5.svg" width="68" alt="5"></td>
  <td valign="top"><b>Журналируемая транзакция и фиксация в базе</b><br>Захват блокировки, резервные копии заменяемых файлов в <code>tx/&lt;id&gt;/bak</code>, синхронизация журнала <code>sync()</code>, атомарный <code>rename</code> и запись в <code>/var/lib/yuki/db/</code>. При сбое питания — автооткат при следующем запуске.</td>
  <td valign="top" align="right"><img src="assets/who-root.svg" height="28" alt="root"></td>
</tr>
</table>

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/divider-dark.svg"><img alt="" src="assets/divider-light.svg" width="880"></picture>

<a name="commands"></a>
## <img src="assets/sec-grid.svg" height="36" align="absmiddle" alt=""> Карта команд и совместимость с pacman

Любая команда снабжена встроенной справкой (`yuki help <команда>`), диагностика кодов доступна через `yuki explain Y0301`, а при опечатке в имени команды работает нечёткий поиск по расстоянию Левенштейна.

<table>
<tr>
  <th align="left" width="33%">Системные пакеты (<code>sudo</code>)</th>
  <th align="left" width="33%">Поиск, граф и аудит</th>
  <th align="left" width="34%">Проекты, ключи и реестр</th>
</tr>
<tr valign="top">
<td>

* `install` / `reinstall` — установка с планом
* `uninstall [-s]` — удаление (+ зависимости)
* `autoremove` — очистка пакетов-сирот
* `upgrade` — обновление всей системы
* `self-update` — безопасное обновление `yuki`
* `hold` / `unhold` — заморозка версий
* `rollback` / `history` — откат и журнал

</td>
<td>

* `search` / `show` — поиск и карточка в индексе
* `list` / `info` — установленные пакеты
* `files` / `owns` — файлы пакета и владелец пути
* `why` / `tree` / `rdeps` — дерево и причины установки
* `related` / `graph [dot]` — граф связей (Graphviz)
* `orphans` / `outdated` — сироты и обновления
* `check` / `sys-audit` — целостность файлов по хешам

</td>
<td>

* `add` / `remove` / `update` — зависимости в `yuki.toml`
* `fetch` / `audit` — кэш и проверка проекта
* `keys gen|trust|list|refresh` — ключи и ротация
* `pack` — воспроизводимая сборка `.tar.zst`
* `index add|cosign|check|catalog` — управление индексом
* `theme` / `config` — палитра и настройки
* `doctor` / `clean` / `selftest` — диагностика

</td>
</tr>
</table>

<details><summary><b>Таблица трансляции флагов в стиле pacman</b></summary>

| Флаг `pacman` | Эквивалент в `yuki` | Флаг `pacman` | Эквивалент в `yuki` |
| :--- | :--- | :--- | :--- |
| `yuki -S <pkg>` | `yuki install <pkg>` | `yuki -Q` | `yuki list` |
| `yuki -Syu` | `yuki upgrade` | `yuki -Qi <pkg>` | `yuki info <pkg>` |
| `yuki -Ss <q>` | `yuki search <q>` | `yuki -Ql <pkg>` | `yuki files <pkg>` |
| `yuki -Si <pkg>` | `yuki show <pkg>` | `yuki -Qo <path>` | `yuki owns <path>` |
| `yuki -R <pkg>` | `yuki uninstall <pkg>` | `yuki -Qe` / `-Qd` | явные / установленные как зависимости |
| `yuki -Rs <pkg>` | `yuki uninstall -s <pkg>` | `yuki -Qdt` | `yuki orphans` |
| `yuki -Sc` / `-Scc` | `yuki clean` / `clean --all` | `yuki -Qu` / `-Qk` | `yuki outdated` / `yuki check` |

</details>

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/divider-dark.svg"><img alt="" src="assets/divider-light.svg" width="880"></picture>

<a name="security"></a>
## <img src="assets/sec-sign.svg" height="36" align="absmiddle" alt=""> Контуры криптографической и системной защиты

<table>
<tr>
  <th align="left" width="28%">Вектор угрозы</th>
  <th align="left" width="38%">Механизм защиты в архитектуре yuki</th>
  <th align="left" width="34%">Модули реализации</th>
</tr>
<tr>
  <td><b>Подмена индекса или архива в сети</b></td>
  <td>Двойная подпись <code>Ed25519</code> (с префиксом домена <code>yuki-v1\n</code>) и проверка <code>BLAKE3</code> как в воркере, так и повторно в <code>root</code>.</td>
  <td><code>verify.ykn</code> · <code>index.ykn</code></td>
</tr>
<tr>
  <td><b>Атака отката (Rollback) и заморозки</b></td>
  <td>Монотонный счётчик ревизии <code>seq</code> (хранится в локальной базе <code>seen</code>) и жёсткий срок годности метаданных <code>expires</code>.</td>
  <td><code>index.ykn</code> · <code>sysplan.ykn</code></td>
</tr>
<tr>
  <td><b>Разделение ролей ключей CI и мейнтейнеров</b></td>
  <td>Ключ <code>renewer</code> может только продлевать срок действия индекса; выпуск версий требует порога подписей <code>publisher</code> (<code>cosign</code>).</td>
  <td><code>trust.ykn</code> · <code>rotation.ykn</code></td>
</tr>
<tr>
  <td><b>Вредоносные пути и спецфайлы в tar</b></td>
  <td>Предраспаковочный <code>audit_tar</code>, разрешение только <code>usr/</code>, <code>opt/</code>, <code>etc/</code>, запрет спецфайлов и лимиты на размер/число файлов.</td>
  <td><code>verify.ykn</code> · <code>policy.ykn</code></td>
</tr>
<tr>
  <td><b>Компрометация при сетевом разборе или сборке</b></td>
  <td>Сброс привилегий до <code>nobody</code> + <code>no_new_privs</code>, сборка в изолированном <code>bubblewrap</code> без сети, честная детекция PRoot.</td>
  <td><code>priv.ykn</code> · <code>stage.ykn</code> · <code>sysbuild.ykn</code></td>
</tr>
<tr>
  <td><b>Сбой питания или падение посреди установки</b></td>
  <td>Предварительный бэкап заменяемых файлов и синхронизированный на диск <code>journal</code> с автоматическим откатом при старте.</td>
  <td><code>apply.ykn</code> · <code>sysdb.ykn</code></td>
</tr>
</table>

Подробная спецификация модели угроз и границ доверия приведена в [`DESIGN.md`](DESIGN.md).

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/divider-dark.svg"><img alt="" src="assets/divider-light.svg" width="880"></picture>

<a name="look"></a>
## <img src="assets/sec-palette.svg" height="36" align="absmiddle" alt=""> Адаптивный терминальный интерфейс и темы

<table>
<tr>
<td><img src="assets/preview/yuki-sys-install.png" alt="sudo yuki install"></td>
<td><img src="assets/preview/yuki-sys-errors.png" alt="ошибки с подсказками"></td>
</tr>
<tr>
<td align="center"><sub>Многофазная установка <code>sudo yuki install</code></sub></td>
<td align="center"><sub>Структурированная диагностика с кодом и ссылкой на <code>yuki explain</code></sub></td>
</tr>
</table>

<p align="center"><img src="assets/preview/yuki-modes.png" width="540" alt="truecolor, ansi и ASCII"></p>
<p align="center"><sub>Автоматическая адаптация терминала: <code>TrueColor → 256 → ANSI 16 → Mono</code> и <code>UTF-8 → ASCII</code> (с поддержкой <code>NO_COLOR=1</code>)</sub></p>

Внешний вид настраивается одним файлом `theme.toml` (пользовательским в `~/.config/yuki/theme.toml` или системным в `/etc/yuki/theme.toml`):

<p align="center"><img src="assets/palette.svg" width="580" alt="палитра темы"></p>

```toml
# ~/.config/yuki/theme.toml  или  /etc/yuki/theme.toml
palette = "ansi"            # "rgb" (TrueColor) | "ansi" (цвета терминала) | "mono"

[colors]
accent = "ansi:cyan"
good   = "#a6e3a1"
warn   = "#f9e2af"
bad    = "#f38ba8+bold"

[style]
animation    = true         # по умолчанию включена при живом интерактивном stdout
bar_gradient = true
```

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/divider-dark.svg"><img alt="" src="assets/divider-light.svg" width="880"></picture>

<a name="index"></a>
## <img src="assets/sec-graph.svg" height="36" align="absmiddle" alt=""> Свой индекс пакетов за 5 шагов

<table>
<tr><td width="92" valign="top"><img src="assets/num-1.svg" width="68" alt="1"></td><td valign="top"><b>Создайте репозиторий из шаблона</b><br>Скопируйте каталог <a href="yuki-index-template/"><code>yuki-index-template/</code></a>, включите защиту ветки <code>main</code> и правила <code>CODEOWNERS</code>.</td></tr>
<tr><td width="92" valign="top"><img src="assets/num-2.svg" width="68" alt="2"></td><td valign="top"><b>Сгенерируйте ключи Ed25519</b><br>Выполните <code>yuki keys gen main</code>, добавьте публичный ключ в <code>keys/trusted_keys</code> с ролью <code>publisher</code>, а секретный ключ храните офлайн.</td></tr>
<tr><td width="92" valign="top"><img src="assets/num-3.svg" width="68" alt="3"></td><td valign="top"><b>Упакуйте воспроизводимый архив</b><br>Команда <code>yuki pack</code> соберёт детерминированный архив <code>.tar.zst</code> с обнулением <code>mtime</code> и проверит политику файловых путей.</td></tr>
<tr><td width="92" valign="top"><img src="assets/num-4.svg" width="68" alt="4"></td><td valign="top"><b>Опубликуйте и подпишите запись</b><br>Выполните <code>yuki index add релиз.json main</code> (при пороге <code>publish_threshold &gt; 1</code> второй мейнтейнер добавляет подпись через <code>yuki index cosign</code>).</td></tr>
<tr><td width="92" valign="top"><img src="assets/num-5.svg" width="68" alt="5"></td><td valign="top"><b>Включите автоматическую проверку и продление в CI</b><br>Пайплайн проверяет каждый PR через <code>yuki index check download</code> и раз в месяц продлевает <code>expires</code> отдельным ключом <code>renewer</code>.</td></tr>
</table>

Полное руководство мейнтейнера: [`TUTORIAL.md`](TUTORIAL.md). Готовый шаблон индекса: [`yuki-index-template/`](yuki-index-template/).

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/divider-dark.svg"><img alt="" src="assets/divider-light.svg" width="880"></picture>

<a name="faq"></a>
## <img src="assets/sec-q.svg" height="36" align="absmiddle" alt=""> Частые вопросы (FAQ)

<details><summary><b>Нужны ли мне выделенные серверы для хостинга пакетов?</b></summary>
Нет. Индекс хранится в обычном Git-репозитории, а архивы раздаются со статических HTTPS-релизов и зеркал. Клиент сам проверяет подписи <code>Ed25519</code> и хеши <code>BLAKE3</code>.
</details>

<details><summary><b>Как yuki работает внутри PRoot / Termux на Android?</b></summary>
Модуль <code>priv.ykn</code> определяет эмуляцию <code>PRoot</code> по реальному UID ядра в <code>/proc/self/status</code> (в режиме fail-closed) и корректно пропускает системные вызовы смены UID и <code>kill(-1)</code>, которые иначе завершили бы сеанс Termux.
</details>

<details><summary><b>Что происходит, если для моей архитектуры нет готового бинарника?</b></summary>
<code>yuki</code> покажет сборочный рецепт, список исходников и хешей, предупредит о запуске сборки и после вашего согласия соберёт пакет внутри изолированной песочницы <code>bubblewrap</code> без доступа к сети.
</details>

<details><summary><b>Как безопасно отозвать скомпрометированный ключ?</b></summary>
Опубликуйте подписанный файл <code>keys/rotation.json</code> с порогом подписей действующих издателей и выполните <code>sudo yuki keys refresh</code>. Отозванный ключ заносится в <code>revoked_keys</code> и никогда не может быть доверен повторно.
</details>

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/divider-dark.svg"><img alt="" src="assets/divider-light.svg" width="880"></picture>

<p align="center"><sub><b>yuki</b> · пакетный менеджер для Yukino · <a href="TUTORIAL.md">руководство по индексу</a> · <a href="DESIGN.md">архитектура и модель угроз</a></sub></p>
