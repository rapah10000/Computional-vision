# Computional-vision Equipe Gabaritei
# Rafael Oliveira Carvalho - 8164
# Rafael Henrique dos Santos Simão - 8160
# Nathália Marques Lima - 8163

Estamos importando bibliotecas como OpenCV para manipulação de imagens, NumPy para operações numéricas eficientes e SciPy para funções estatísticas e otimização. Cada uma desempenha um papel crucial na análise da imagem.
Pré-processamento da Imagem: Começamos carregando a imagem da folha de respostas, convertendo-a para escala de cinza e aplicando um limiar binário para destacar as bolhas de respostas.
Detecção de Contornos: Em seguida, utilizamos a função findContours para identificar os contornos na imagem, uma etapa fundamental para distinguir entre as diferentes regiões da folha.
Identificação de Bolhas: Iteramos sobre os contornos para identificar bolhas circulares e retangulares. As condições específicas nos permitem diferenciar entre essas formas e destacá-las na imagem.
Detecção de Linhas na Folha de Respostas: A transformada de Hough é aplicada para detectar linhas na folha, fornecendo informações valiosas sobre a estrutura da folha de respostas.
Associação entre Bolhas e Linhas: Associamos as bolhas às linhas detectadas, verificando a proximidade entre os centros das bolhas e as linhas. Essa associação é crucial para identificar corretamente as opções de múltipla escolha.
Organização das Opções: As opções são organizadas com base na distância vertical, agrupando-as em um dicionário para facilitar a análise posterior.
Exibição das Opções Detectadas: Vamos dar uma olhada nas opções organizadas no console. Isso nos proporciona uma visão clara das respostas candidatas.
Comparação com o Gabarito: Carregamos a imagem do gabarito e realizamos um processo semelhante para identificar as bolhas corretas, preparando o terreno para a correção automática.
Correção Automática: Finalmente, comparamos as coordenadas das bolhas detectadas com as do gabarito para determinar as respostas corretas de forma automática.
Exibição das Respostas Corretas: Vamos agora exibir as respostas corretas no console. Essa é a fase em que nosso código revela quais respostas foram marcadas corretamente.
Conclusão: Em resumo, exploramos um código poderoso que utiliza técnicas de visão computacional para automatizar a correção de folhas de respostas de múltipla escolha. Espero que vocês tenham achado esse processo fascinante e informativo!
