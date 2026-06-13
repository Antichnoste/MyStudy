#!/bin/bash

RED="Red <red@example.com>"
BLUE="Blue <blue@example.com>"

REPO_DIR="repo_git"
COMMITS_DIR="../commits"

bash remove_git.bash
mkdir "$REPO_DIR"
cd "$REPO_DIR" || exit

git init

make_commit() {
    local rev=$1
    local author=$2

    unzip -o "${COMMITS_DIR}/commit${rev}.zip" -d .

    git add .

    git commit -m "r${rev}" --author="$author"
    
    echo "Коммит r${rev} создан."
}

make_commit 0 "$RED"
make_commit 1 "$RED"
make_commit 2 "$RED"

git checkout -b blue_branch_1

make_commit 3 "$BLUE"

git checkout main
make_commit 4 "$RED"

git checkout blue_branch_1
make_commit 5 "$BLUE"

git checkout main
make_commit 6 "$RED"

git checkout blue_branch_1
make_commit 7 "$BLUE"

git checkout -b blue_branch_2

make_commit 8 "$BLUE"
make_commit 9 "$BLUE"

git checkout main
#git merge --no-ff blue_branch_2 --no-commit -Xours(theirs)

git merge --no-ff --no-commit blue_branch_2
if [ $? -ne 0 ]; then
    echo "Конфликт! Разрешите его и нажмите Enter, чтобы продолжить..."
    read -p "Нажмите Enter для продолжения..."
fi

make_commit 10 "$RED"
make_commit 11 "$RED"

git checkout blue_branch_1
make_commit 12 "$BLUE"

git checkout main

#git merge --no-ff blue_branch_1 --no-commit -Xours(theirs)
git merge --no-ff --no-commit blue_branch_1
if [ $? -ne 0 ]; then
    echo "Конфликт! Разрешите его и нажмите Enter, чтобы продолжить..."
    read -p "Нажмите Enter для продолжения..."
fi

make_commit 13 "$RED"

make_commit 14 "$RED"

#git merge --ff-only --squash --abort -s <strategy>