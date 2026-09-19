#!/usr/bin/env bash
# deploy.sh — interview-* skill 部署与发布脚本
#
# 事实源：本仓库各 skill 目录。副本：~/.workbuddy/skills/<skill-name>/
# 流程：校验 frontmatter → 比对差异 → 部署副本 → (可选) 提交并推送
#
# 用法：
#   ./deploy.sh                      校验 + 部署
#   ./deploy.sh --check              只校验差异，不改动任何文件
#   ./deploy.sh --commit "提交信息"   校验 + 部署 + 提交 + 推送
#   ./deploy.sh --no-delete          部署时不删除副本里的多余文件
#
# 说明：本机在 ~/Documents 下的 git 仓库里，sandbox 会拒绝 unlink .git/*.lock，
#      导致 git status 之类操作残留索引锁，后续 git 写操作全部失败。
#      本脚本在每次 git 写操作前自动清理陈旧锁（先确认无进程占用）。
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST_ROOT="${HOME}/.workbuddy/skills"
MODE="deploy"
RSYNC_DELETE=1
COMMIT_MSG=""
BRANCH="main"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check)     MODE="check"; shift ;;
    --commit)    MODE="commit"; COMMIT_MSG="${2:-}"; shift 2 ;;
    --no-delete) RSYNC_DELETE=0; shift ;;
    -h|--help)   sed -n '2,16p' "$0"; exit 0 ;;
    *)           echo "未知参数: $1（用 --help 查看用法）" >&2; exit 2 ;;
  esac
done

if [[ "$MODE" == "commit" && -z "$COMMIT_MSG" ]]; then
  echo "--commit 需要提交信息，例：./deploy.sh --commit \"fix: 调整骨架规则\"" >&2
  exit 2
fi

# ---------- git 辅助 ----------

clear_locks() {
  local locks
  locks="$(find "${REPO}/.git" -name '*.lock' 2>/dev/null || true)"
  [[ -z "$locks" ]] && return 0
  while IFS= read -r lk; do
    [[ -z "$lk" ]] && continue
    if lsof "$lk" >/dev/null 2>&1; then
      echo "   !! 锁被活跃进程占用，跳过：${lk#"${REPO}/"}" >&2
    else
      rm -f "$lk" && echo "   清理陈旧锁：${lk#"${REPO}/"}"
    fi
  done <<< "$locks"
}

git_ro() { GIT_OPTIONAL_LOCKS=0 git -C "$REPO" "$@"; }

# ---------- 校验 + 部署 ----------

deployed=0
differences=0
problems=0
fail=0

echo "仓库：${REPO}"
echo "副本：${DEST_ROOT}"
echo
printf '%-20s %-12s %s\n' "SKILL" "状态" "说明"
printf '%-20s %-12s %s\n' "-----" "----" "----"

for d in "$REPO"/*/; do
  name="$(basename "$d")"
  [[ -f "${d}SKILL.md" ]] || continue
  dest="${DEST_ROOT}/${name}"

  # 1) frontmatter 校验：首行 ---，且前 6 行内含 name:
  if [[ "$(head -1 "${d}SKILL.md")" != "---" ]] || ! sed -n '1,6p' "${d}SKILL.md" | grep -q '^name:'; then
    printf '%-20s %-12s %s\n' "$name" "缺frontmatter" "SKILL.md 首行须为 --- 且含 name:（否则装上也注册不了）"
    problems=$((problems + 1))
    fail=1
    continue
  fi

  # 2) 差异比对
  if [[ ! -d "$dest" ]]; then
    status="未安装"
    note="副本不存在，将首次安装"
    differences=$((differences + 1))
  elif diff -rq "$d" "$dest" >/dev/null 2>&1; then
    status="一致"
    note="无需操作"
  else
    status="有差异"
    # 注意：diff -rq 发现差异时返回 1，配合 set -o pipefail 会中断脚本 —— 必须 `|| true` 兜住
    note="$( { diff -rq "$d" "$dest" 2>/dev/null || true; } | wc -l | tr -d ' ' ) 处文件不一致，将同步"
    differences=$((differences + 1))
  fi

  if [[ "$MODE" == "check" ]]; then
    printf '%-20s %-12s %s\n' "$name" "$status" "$note"
    continue
  fi

  if [[ "$status" == "一致" ]]; then
    printf '%-20s %-12s %s\n' "$name" "已最新" "副本与仓库一致，跳过"
    continue
  fi

  # 3) 部署
  mkdir -p "$dest"
  RsyncOpts=(-a)
  [[ "$RSYNC_DELETE" == "1" ]] && RsyncOpts+=(--delete)
  if rsync "${RsyncOpts[@]}" "${d}" "${dest}/" ; then
    printf '%-20s %-12s %s\n' "$name" "已部署" "${note}"
    deployed=$((deployed + 1))
  else
    printf '%-20s %-12s %s\n' "$name" "部署失败" "rsync 返回非 0"
    problems=$((problems + 1))
    fail=1
  fi
done

echo
if [[ "$MODE" == "check" ]]; then
  echo "校验完成：${differences} 个 skill 需要部署，${problems} 个问题。"
  [[ "$fail" == "0" ]] || exit 1
  exit 0
fi
echo "部署完成：${deployed} 个，问题 ${problems} 个。"

# ---------- 提交 + 推送 ----------

if [[ "$MODE" == "commit" ]]; then
  echo
  echo "== git =="
  clear_locks

  if [[ -z "$(git_ro status --porcelain)" ]]; then
    echo "无待提交改动，跳过 commit"
  else
    git -C "$REPO" add -A
    clear_locks
    git -C "$REPO" commit -q -m "$COMMIT_MSG"
    echo "已提交：$(git_ro log --oneline -1)"
  fi

  clear_locks
  if ! git -C "$REPO" push origin "$BRANCH" 2>&1 | tail -3; then
    echo "推送失败，清锁后重试一次…"
    clear_locks
    git -C "$REPO" fetch --prune origin >/dev/null 2>&1 || true
    clear_locks
    git -C "$REPO" push origin "$BRANCH" 2>&1 | tail -3
  fi

  clear_locks
  git -C "$REPO" fetch --prune origin >/dev/null 2>&1 || true
  clear_locks
  echo
  echo "本地/远端状态："
  git_ro status -sb
  git_ro log --oneline -1
fi

exit "$fail"
