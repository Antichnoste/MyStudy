#!/bin/bash

REPO_DIR="repo_git"

if [ -d "$REPO_DIR" ]; then
    rm -rf "$REPO_DIR"
    echo "Папка $REPO_DIR успешно удалена."
else
    echo "Репозиторий не найден, очистка не требуется."
fi