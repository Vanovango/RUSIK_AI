def main():
    from ultralytics import YOLO

    # Load a model
    model = YOLO("yolo11n-seg.yaml")  # build a new model from YAML

    # Train the model
    results = model.train(data="./config/train_config.yaml", epochs=75, batch=1, device=0)


if __name__ == '__main__':
    main()
