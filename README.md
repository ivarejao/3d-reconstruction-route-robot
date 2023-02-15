# T3 - Reconstrução 3D do trajeto de um robô
**Autores:** 
- Igor Varejão
- Otávio Cozer

### Descrição
Esse trabalho consiste na reconstrução 3D do trajeto de um robô acoplado a um aruco a partir da triangulação de 4 câmeras
posicionadas em um mesmo ambiente. Os dados de calibração já foram previamente fornecidos e se encontram em `data/calib`,
já os 4 vídeos se encontram em `data/videos`. Os códigos fonte se encontram em `src/`

### Execução
Para executar o script é preciso ter as seguintes versões das biblioetcas:
```python
- opencv-contrib-python==4.7.0.68
- opencv-python==4.7.0.68
```
Ambas especificadas em `requirements.txt`

Para executar o programa basta especificar o caminho dos vídeos na hora de executar o programa pelo argumento
`--data-path`
**OBS:** É importante especificar o caminho dos dados com relação a onde está sendo chamado o programa.
```bash
python3 main.py --data-path ../data/videos
```
O exemplo acima chama o programa da pasta `src`