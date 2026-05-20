# ml_engine/__init__.py
validator = None

def get_validator():
    global validator
    if validator is None:
        from django.conf import settings
        from ml_engine.inference import SyrianCurrencyValidator
        validator = SyrianCurrencyValidator(
            model_weights_path=str(settings.ML_MODEL_PATH),
            references_dir=str(settings.ML_REFERENCES_DIR)
        )
    return validator