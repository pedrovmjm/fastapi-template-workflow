#!/usr/bin/env bash
# Sanitiza titulo e corpo de commit ou PR removendo autoria de ferramentas de IA.
#
# Uso:
#   scripts/sanitize-ai-attribution.sh mensagem.txt
#   scripts/sanitize-ai-attribution.sh --write mensagem.txt
#   scripts/sanitize-ai-attribution.sh --title "titulo" corpo-pr.md
#   echo "mensagem" | scripts/sanitize-ai-attribution.sh
#
# Saida:
#   stdout  -> texto sanitizado (exceto com --write)
#   stderr  -> violacoes removidas e status final
#   exit 0  -> apto_para_publicar=sim
#   exit 1  -> ainda ha autoria de IA ou entrada invalida

set -euo pipefail

readonly SCRIPT_NAME="sanitize-ai-attribution"

readonly -a AI_TOOL_TOKENS=(
  "cursor"
  "claude code"
  "claude"
  "codex"
  "copilot"
  "github copilot"
  "chatgpt"
  "openai"
  "gemini"
  "anthropic"
  "gpt-4"
  "gpt-3"
  "gpt4"
  "gpt3"
  "aider"
  "cody"
  "tabnine"
  "windsurf"
  "devin"
  "amazon q"
  "amazonq"
  "ferramenta de ia"
  "assistente de ia"
  "ai assistant"
  "ai tool"
)

title=""
body_file=""
write_mode=false

usage() {
  cat >&2 <<EOF
Uso:
  ${SCRIPT_NAME}.sh [arquivo]
  ${SCRIPT_NAME}.sh --write [arquivo]
  ${SCRIPT_NAME}.sh --title "titulo" [arquivo_corpo]
  cat mensagem.txt | ${SCRIPT_NAME}.sh
EOF
}

normalize_line() {
  tr '[:upper:]' '[:lower:]' <<<"$1" | tr -s ' '
}

contains_ai_tool_token() {
  local normalized="$1"
  local token

  for token in "${AI_TOOL_TOKENS[@]}"; do
    if [[ "$normalized" == *"$token"* ]]; then
      return 0
    fi
  done

  return 1
}

should_remove_line() {
  local line="$1"
  local trimmed
  local normalized

  trimmed="${line#"${line%%[![:space:]]*}"}"
  normalized="$(normalize_line "$trimmed")"

  if [[ "$normalized" == generated-by:* ]] \
    || [[ "$normalized" == generated\ by:* ]] \
    || [[ "$normalized" == made-with:* ]]; then
    return 0
  fi

  if [[ "$normalized" == made\ with\ * ]] && contains_ai_tool_token "$normalized"; then
    return 0
  fi

  if [[ "$normalized" == co-authored-by:* ]] \
    || [[ "$normalized" == co\ authored-by:* ]]; then
    if contains_ai_tool_token "$normalized" \
      || [[ "$normalized" == *"@cursor.com"* ]] \
      || [[ "$normalized" == *"cursoragent@"* ]]; then
      return 0
    fi
  fi

  if [[ "$normalized" == created-with:* ]] \
    || [[ "$normalized" == created-by:* ]] \
    || [[ "$normalized" == created\ by:* ]]; then
    if contains_ai_tool_token "$normalized"; then
      return 0
    fi
  fi

  return 1
}

has_ai_attribution() {
  local text="$1"
  local line

  while IFS= read -r line || [[ -n "$line" ]]; do
    if should_remove_line "$line"; then
      return 0
    fi
  done <<<"$text"

  return 1
}

sanitize_text() {
  local input="$1"
  local -a kept=()
  local -a removed=()
  local line

  while IFS= read -r line || [[ -n "$line" ]]; do
    if should_remove_line "$line"; then
      removed+=("$line")
    else
      kept+=("$line")
    fi
  done <<<"$input"

  while ((${#kept[@]} > 0)) && [[ -z "${kept[-1]// }" ]]; do
    unset 'kept[-1]'
  done

  SANITIZED_OUTPUT=""
  if ((${#kept[@]} > 0)); then
    local index
    for index in "${!kept[@]}"; do
      if [[ $index -gt 0 ]]; then
        SANITIZED_OUTPUT+=$'\n'
      fi
      SANITIZED_OUTPUT+="${kept[$index]}"
    done
  fi

  REMOVED_LINES=("${removed[@]}")
}

parse_args() {
  if [[ $# -eq 0 ]]; then
    body_file="-"
    return 0
  fi

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --write)
        write_mode=true
        ;;
      --title)
        shift
        title="${1:-}"
        if [[ -z "$title" ]]; then
          echo "${SCRIPT_NAME}: --title exige um valor." >&2
          exit 1
        fi
        ;;
      -h | --help)
        usage
        exit 0
        ;;
      *)
        body_file="$1"
        ;;
    esac
    shift
  done
}

read_body() {
  if [[ "$body_file" == "-" ]]; then
    cat
  elif [[ -f "$body_file" ]]; then
    cat "$body_file"
  else
    echo "${SCRIPT_NAME}: arquivo nao encontrado: ${body_file}" >&2
    exit 1
  fi
}

emit_result() {
  local sanitized_body="$1"
  local sanitized_title="$2"

  if [[ -n "$sanitized_title" ]] && has_ai_attribution "$sanitized_title"; then
    echo "${SCRIPT_NAME}: titulo contem autoria de IA e nao foi sanitizado automaticamente." >&2
    echo "APTO_PARA_PUBLICAR=nao" >&2
    exit 1
  fi

  if has_ai_attribution "$sanitized_body"; then
    echo "${SCRIPT_NAME}: texto ainda contem autoria de IA apos sanitizacao." >&2
    echo "APTO_PARA_PUBLICAR=nao" >&2
    exit 1
  fi

  if ((${#REMOVED_LINES[@]} > 0)); then
    echo "${SCRIPT_NAME}: violacoes removidas:" >&2
    local line
    for line in "${REMOVED_LINES[@]}"; do
      echo "  - ${line}" >&2
    done
  fi

  local output=""
  if [[ -n "$sanitized_title" ]]; then
    output="$sanitized_title"
    if [[ -n "$sanitized_body" ]]; then
      output+=$'\n\n'"$sanitized_body"
    fi
  else
    output="$sanitized_body"
  fi

  if [[ "$write_mode" == true ]]; then
    if [[ -z "$body_file" || "$body_file" == "-" ]]; then
      echo "${SCRIPT_NAME}: --write exige um arquivo." >&2
      exit 1
    fi
    if [[ -n "$output" ]]; then
      printf '%s\n' "$output" >"$body_file"
    else
      : >"$body_file"
    fi
  else
    if [[ -n "$output" ]]; then
      printf '%s\n' "$output"
    fi
  fi

  echo "APTO_PARA_PUBLICAR=sim" >&2
}

main() {
  parse_args "$@"

  local body
  body="$(read_body)"

  sanitize_text "$body"

  emit_result "$SANITIZED_OUTPUT" "$title"
}

main "$@"
