import os
import numpy as np
from model_utils import predict

def test_predict_output_type():
    """Verifica que el modelo retorna una clase y una confianza."""
    pred_class, confidence = predict("download.jpg")
    assert isinstance(pred_class, int), "La clase predicha debe ser un entero."
    assert isinstance(confidence, float), "La confianza debe ser un float."

def test_predict_confidence_range():
    _, confidence = predict("download.jpg")
    assert 0.0 <= confidence <= 100.0, "La confianza debe estar entre 0 y 100."

def test_predict_class_range():
    """Verifica que la clase predicha esté dentro del rango de etiquetas de ImageNet."""
    pred_class, _ = predict("download.jpg")
    assert 0 <= pred_class < 1000, "La clase predicha debe estar entre 0 y 999 (ImageNet)."

def test_confidence_threshold():
    _, confidence = predict("download.jpg")
    assert confidence > 0.2, "La confianza es muy baja, puede indicar problemas en el modelo"

if __name__ == "__main__":
    test_predict_output_type()
    test_predict_confidence_range()
    test_predict_class_range()
    print("✅ Todas las pruebas fueron exitosas")

