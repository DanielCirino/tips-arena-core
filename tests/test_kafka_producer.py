from tipsarena_core import gerenciador_filas
import random

# Call the producer.send method with a producer-record
print("Ctrl + C to Stop")

while True:
  gerenciador_filas.produzirMensagem('ta-teste-kafka-python', random.randint(1, 999))
