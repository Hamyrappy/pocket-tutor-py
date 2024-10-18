# pocket-tutor-py
Tutor-copilot for python 
Разработан на HSE AI Assistant hack командой "И другие"

### Ссылки
Репозиторий: https://github.com/Hamyrappy/pocket-tutor-py

### Запуск

Запустите main.py

### Структура
.
├── app <------------------------ модели и утилиты из бейзлайна
├── cache
├── data
│   ├── complete<------------------------ подготовленные данные, сабмиты
│       ├── submission.csv <------------------------ сюда main.py сохраняет сабмиты
│   ├── processed <----------------------- промежуточный этап подготовки данных
│   └── raw <----------------------------- исходные данные
│       ├── submit_example.csv
│       ├── test
│       │   ├── solutions.xlsx
│       │   ├── tasks.xlsx
│       │   └── tests.xlsx
│       └── train
│           ├── solutions.xlsx
│           ├── tasks.xlsx
│           └── tests.xlsx
├── logs
├── main.py <---------------------------- Основной файл проекта, генерит финальный сабмит.
├── notebooks
│   └── yandexgpt.ipynb
├── poetry.lock
├── pyproject.toml
├── README.md
└── tests
    ├── test_correctness.py <------------------------ проверить на корректность сабмит
    └── test_embedding_generation.py <--------------- попробовать генерацию эмбеддингов и подсчёт метрики
    └── test_tester.py <--------------- корректность работы тест-системы

