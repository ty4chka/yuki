#!/usr/bin/env bash
# Опубликованные релизы неизменяемы: старые версии в записи не должны меняться.
# Запускается в CI на pull request:  scripts/immutable.sh origin/main
set -euo pipefail
base="${1:-origin/main}"
bad=0
for f in $(git diff --name-only "$base"...HEAD -- 'index/*.json'); do
  git cat-file -e "$base:$f" 2>/dev/null || continue            # новый пакет
  old=$(git show "$base:$f" | jq -c '.versions')
  new=$(jq -c '.versions' "$f")
  # каждая старая версия должна остаться такой же (кроме перехода yanked: false -> true)
  n=$(jq -n --argjson o "$old" --argjson n "$new" '
    [ $o[] | . as $v
      | ($n | map(select(.version == $v.version)) | .[0]) as $m
      | select($m == null or ($m | del(.yanked)) != ($v | del(.yanked))) ] | length')
  if [ "$n" != "0" ]; then echo "::error file=$f::a published release was modified or removed"; bad=1; fi
done
exit $bad
