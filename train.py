def main():
    from ultralytics import YOLO

    # Load a model
    model = YOLO("yolo11n-seg.yaml")  # build a new model from YAML

    # Train the model
    results = model.train(data="./config/train_config.yaml", epochs=75, batch=1, device=0)


if __name__ == '__main__':
    main()


# Каждый раз, когда ты захочешь сохранить что-то в репозитории, используй эти команды
# git add . / добавляет все неучтенные файлы в локальный гит
# git commit -m "#текст коммита" / создает файл коммита (то, что будет отправлено на сервер гитхаб)
# текст коммита будет выведен рядом с изменненными файлами
# git push -u origin main/или другая ветка, к которой ты подключен.
# Флаг -U означает, что ты будешь подключен к потоку репозитория: то есть ты можешь загружать изменения с репозитория
# и загружать со своего компьютера (локального гита)
