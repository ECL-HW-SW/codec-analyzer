from SVT import svt_codec
from LIBAOM import libaom_codec

teste = libaom_codec()
print(teste.get_qp())
teste.set_qp(27)
print(teste.get_qp())
teste.encode()
teste.decode()
