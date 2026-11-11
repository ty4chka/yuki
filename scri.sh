#!/data/data/com.termux/files/usr/bin/sh
# Шаг 1 (запускать в Termux): собрать и отправить тестовый индекс yuki с пакетом hello.
# Запуск:  sh 1-termux-index.sh
# Что нужно заранее: yuki (команда работает), ключ `test` (yuki keys gen test), git,
# репозиторий ty4chka/yuki-index (публичный), релиз hello-1.0.0 с архивом, вход в GitHub (gh auth login).
set -e

OWNER="${OWNER:-ty4chka}"
REPO="${REPO:-yuki-index}"
KEY="${KEY:-test}"
TAG="${TAG:-hello-1.0.0}"
case "$(uname -m)" in
  aarch64|arm64) T=linux-aarch64 ;;
  x86_64) T=linux-x86_64 ;;
  *) echo "неизвестная архитектура: $(uname -m)"; exit 1 ;;
esac
ASSET="hello-1.0.0-$T.tar.zst"
URL="https://github.com/$OWNER/$REPO/releases/download/$TAG/$ASSET"
WORK="$HOME/yuki-index-work"

say() { printf '\n== %s ==\n' "$*"; }
die() { printf '\nОШИБКА: %s\n' "$*"; exit 1; }

say "проверки"
command -v yuki >/dev/null || die "команда yuki не найдена"
command -v git >/dev/null || die "нет git: pkg install git"
PUB="$(yuki keys export "$KEY")" || die "нет ключа $KEY: yuki keys gen $KEY"
[ "${#PUB}" = "64" ] || die "странный публичный ключ: $PUB"
echo "ключ $KEY: $PUB"
CODE="$(curl -sL -o /dev/null -w '%{http_code}' "$URL")"
[ "$CODE" = "200" ] || die "архив не найден ($CODE): $URL (создайте релиз $TAG и приложите $ASSET)"
echo "архив доступен: $URL"

say "рабочий каталог индекса: $WORK"
rm -rf "$WORK"
mkdir -p "$WORK/index" "$WORK/keys"
cd "$WORK"
git init -q -b main
touch index/.gitkeep
echo '* -text' > .gitattributes
echo "$KEY $PUB publisher" > keys/trusted_keys
git config user.email >/dev/null 2>&1 || git config user.email "yuki-test@localhost"
git config user.name >/dev/null 2>&1 || git config user.name "yuki-test"

say "описание релиза"
cat > "$HOME/hello.release.json" <<JSON
{
  "name": "hello", "kind": "app", "version": "1.0.0",
  "summary": "prints hello", "license": "MIT",
  "bin": [ { "target": "$T", "url": "$URL" } ]
}
JSON
cat "$HOME/hello.release.json"

say "yuki index add"
yuki index add "$HOME/hello.release.json" "$KEY"
say "yuki index catalog"
yuki index catalog "$KEY"
say "доверяем ключу $KEY (yuki читает <config>/trusted_keys, а не keys/ из репозитория индекса)"
YUKI_YES=1 yuki keys trust "$KEY" "$PUB" || echo "(ключ уже в доверенных, идём дальше)"

say "yuki index check download"
yuki index check download

say "git push"
git add .
git commit -q -m "hello 1.0.0"
git remote add origin "https://github.com/$OWNER/$REPO.git"
if command -v gh >/dev/null 2>&1; then gh auth setup-git >/dev/null 2>&1 || true; fi
git push -f -u origin main

say "готово"
INDEX_URL="https://raw.githubusercontent.com/$OWNER/$REPO/main"
echo "индекс: $INDEX_URL"
echo "чтобы работали yuki search/install: export YUKI_INDEX=$INDEX_URL   (или запишите URL в <config>/index_url)"
echo "raw.githubusercontent.com кеширует до нескольких минут: подождите перед следующим шагом."

# Подготовка клиента: положить бинарь и второй скрипт в Ubuntu (proot-distro), если он уже установлен
ROOTFS="${PREFIX:-/data/data/com.termux/files/usr}/var/lib/proot-distro/installed-rootfs/ubuntu"
if [ -d "$ROOTFS" ] && [ -f "$HOME/bin/yuki-real" ]; then
  mkdir -p "$ROOTFS/usr/local/bin" "$ROOTFS/root"
  cp "$HOME/bin/yuki-real" "$ROOTFS/usr/local/bin/yuki"
  chmod +x "$ROOTFS/usr/local/bin/yuki"
  [ -f "$HOME/2-ubuntu-client.sh" ] && cp "$HOME/2-ubuntu-client.sh" "$ROOTFS/root/2-ubuntu-client.sh"
  echo "бинарь yuki скопирован в Ubuntu. Дальше: proot-distro login ubuntu -- sh /root/2-ubuntu-client.sh"
else
  echo "Ubuntu не установлен: pkg install proot-distro && proot-distro install ubuntu, потом запустите этот скрипт ещё раз."
fi

