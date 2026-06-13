#set text(font: ("Times New Roman", "Liberation Serif"), lang: "ru", size: 12pt)
#set par(justify: true, first-line-indent: 1.25cm)
#set page(
  paper: "a4",
  margin: (top: 2cm, bottom: 2cm, left: 1.5cm, right: 1.5cm),
)
#set heading(numbering: "1.1")


#align(center)[
  #text(weight: "bold")[Министерство науки и высшего образования Российской Федерации] \
  Федеральное государственное автономное образовательное учреждение высшего образования \
  *«Национальный исследовательский университет ИТМО»* \
  \
  Факультет Программной инженерии и компьютерной техники
  
  #v(5cm)
  
  #text(size: 16pt, weight: "bold")[Лабораторная работа №2] \
  по дисциплине «Основы программной инженерии»
  
  #text(size: 14pt)[Вариант: *1232*] \
  
  #v(4cm)
]

#align(right)[
  #block(width: 31%)[
    #align(left)[
      *Преподаватель:* \
      Лазеев Сергей Максимович \
      \
      *Выполнил:* \
      Караганов Павел Эдуардович \
      Группа: P3210
    ]
  ]
]

#place(bottom + center)[Санкт-Петербург, 2026]
#pagebreak()

#outline(indent: 2em, depth: 3)
#pagebreak()

#heading(numbering: none)[Блок-схема варианта]

#align(center)[
  #figure(
    image("img/exercise.png", width: 100%),
  )
]

= Список команд, использованных для создания и настройки Git-репозитория

1. `bash remove_git.bash` -- удаление ранее созданного каталога репозитория перед повторным запуском.
2. `mkdir repo_git` -- создание каталога локального Git-репозитория.
3. `cd repo_git` -- переход в рабочий каталог репозитория.
4. `git init` -- инициализация пустого Git-репозитория.
5. `unzip -o ../commits/commitN.zip -d .` -- восстановление состояния файлов для ревизии `rN`.
6. `git add .` -- добавление изменений в индекс.
7. `git commit -m "rN" --author="..."` -- создание коммита ревизии `rN` с нужным автором.
8. `git checkout -b blue_branch_1` -- создание и переключение на ветку `blue_branch_1`.
9. `git checkout -b blue_branch_2` -- создание и переключение на ветку `blue_branch_2`.
10. `git checkout main` -- возврат в основную ветку `main`.
11. `git merge --no-ff --no-commit <branch>` -- слияние ветки без авто-коммита (для ручной обработки конфликтов).

= Ревизии Git и последовательности команд

#table(
  columns: (auto, 2fr, 2fr),
  stroke: .5pt,
  inset: 6pt,
  [*Ревизия*], [*Последовательность команд*], [*Комментарий*],

  [r0],
  [`unzip commit0.zip` -> `git add .` -> `git commit -m "r0" --author="Red ..."`],
  [Начальное состояние файлов в основной ветке.],

  [r1],
  [`unzip commit1.zip` -> `git add .` -> `git commit -m "r1" --author="Red ..."`],
  [Последовательное изменение в `main`.],

  [r2],
  [`unzip commit2.zip` -> `git add .` -> `git commit -m "r2" --author="Red ..."`],
  [Последний коммит до первого ветвления.],

  [r3],
  [`git checkout -b blue_branch_1` -> `unzip commit3.zip` -> `git commit ...`],
  [Первый коммит синего автора в ветке `blue_branch_1`.],

  [r4],
  [`git checkout main` -> `unzip commit4.zip` -> `git commit ...`],
  [Продолжение разработки в основной ветке.],

  [r5],
  [`git checkout blue_branch_1` -> `unzip commit5.zip` -> `git commit ...`],
  [Изменение в параллельной ветке `blue_branch_1`.],

  [r6],
  [`git checkout main` -> `unzip commit6.zip` -> `git commit ...`],
  [Следующая ревизия в `main`.],

  [r7],
  [`git checkout blue_branch_1` -> `unzip commit7.zip` -> `git commit ...`],
  [Подготовка к выделению дополнительной ветки.],

  [r8],
  [`git checkout -b blue_branch_2` -> `unzip commit8.zip` -> `git commit ...`],
  [Создана ветка `blue_branch_2` от `blue_branch_1`.],

  [r9],
  [`unzip commit9.zip` -> `git add .` -> `git commit -m "r9" --author="Blue ..."`],
  [Развитие ветки `blue_branch_2`.],

  [r10],
  [`git checkout main` -> `git merge --no-ff --no-commit blue_branch_2` -> разрешение конфликтов -> `unzip commit10.zip` -> `git commit ...`],
  [Фиксация результата первого слияния в `main`.],

  [r11],
  [`unzip commit11.zip` -> `git add .` -> `git commit -m "r11" --author="Red ..."`],
  [Обычный коммит в `main` после merge.],

  [r12],
  [`git checkout blue_branch_1` -> `unzip commit12.zip` -> `git commit ...`],
  [Дополнительное изменение в `blue_branch_1`.],

  [r13],
  [`git checkout main` -> `git merge --no-ff --no-commit blue_branch_1` -> разрешение конфликтов -> `unzip commit13.zip` -> `git commit ...`],
  [Фиксация результата второго слияния в `main`.],

  [r14],
  [`unzip commit14.zip` -> `git add .` -> `git commit -m "r14" --author="Red ..."`],
  [Завершающая ревизия в основной ветке.]
)

= Скрипт для создания

#raw(read("../script_git.bash"), block: true, lang: "bash")

= Выводы

В ходе работы была воспроизведена заданная история изменений для Git-репозитория с последовательными коммитами, ветвлениями и слияниями. При выполнении merge использовался режим без автоматического коммита (`--no-commit`), что позволило контролируемо разрешать конфликты и фиксировать итоговое состояние в отдельных ревизиях. Полученная структура истории соответствует блок-схеме варианта и подтверждает корректность построенной последовательности действий в Git.