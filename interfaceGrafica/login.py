from cProfile import label
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QToolTip, QLabel, QLineEdit
from PyQt5 import QtGui

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.top = 100
        self.left = 100
        self.width = 800
        self.height = 600
        self.titulo = "Janela Teste"

        logo = QLabel(self)
        logo.move(205,75)
        logo.setPixmap(QtGui.QPixmap('images/insight.png'))
        logo.resize(390, 110)

        label1 = self.createLabel(278, 200, 'email:')
        line1 = self.createInputLine(275, 235, 250, 35)
        label1.setBuddy(line1)
        label2 = self.createLabel(278, 300, 'senha:')
        line2 = self.createInputLine(275, 335, 250, 35)
        label2.setBuddy(line2)
        
        btn1 = self.createButton(100, 400, 250, 50, 'Criar Cadastro')
        self.buttonStyle(btn1, '#8fffb2', colorHover='#41945b')
        btn1.clicked.connect(self.btnCadastroClick)
        btn2 = self.createButton(450, 400, 250, 50, 'login')
        self.buttonStyle(btn2, '#b0ddff', colorHover='#5a7f9c')
        btn2.clicked.connect(self.btnLoginClick)
        self.loadWindow()

    def loadWindow(self):
        """Carrega a janela que está sendo criada.
        """

        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.titulo)
        self.show()

    # -------- CONFIGURAÇÃO DOS BOTÕES ---------------------

    def createButton(self, x, y, width, height, title):
        """Cria um botão na posição e com as características informadas nas variáveis.

        Args:
            x (int): Posição horizontal do canto superior esquerdo do botão.
            y (int): Posição vertical do canto superior esquerdo do botão.
            width (int): Largura do botão.
            height (int): Altura do botão.
            title (str): Título escrito no botão.

        Returns:
            QPushButton: Botão criado.
        """

        btn = QPushButton(title, self)
        btn.move(x,y)
        btn.resize(width, height)
        return btn
    
    def buttonStyle(self, btn, color, fWeight='bold', bRadius=15, colorHover='#8f8542'):
        """Muda a aparência do botão.

        Args:
            btn (QPushButton): Botão onde deve ocorrer a mudança.
            color (str): Hexadecimal da cor de fundo.
            fWeight (str, optional): Peso da fonte a ser escrita. Defaults to 'bold'.
            bRadius (int, optional): Tamanho em pixels do raio da borda do botão. Defaults to 15.
            colorHover (str, optional): Hexadecimal da cor de fundo quando o mouse fica em cima dele. Defaults to '#8f8542'.
        """

        colorSetup = f'QPushButton {{background-color:{color}; border-radius:{bRadius}; font-weight:{fWeight};}}QPushButton:hover {{background-color:{colorHover};}}'
        btn.setStyleSheet(colorSetup)

    # -- ------------- funções especificas ------------
    
    def btnCadastroClick(self):
        """Função que o botão de cadastro exerce quando é clicado.
        """

        print('Botão de cadastro clicado')
    
    def btnLoginClick(self):
        """Função que o botão de login exerce quando é clicado.
        """

        print('Botão de login clicado')
    
    # -------- FIM CONFIGURAÇÃO DOS BOTÕES ---------------------

    # -------- CONFIGURAÇÃO DOS INPUTS -------------------------

    def createInputLine(self, x, y, width, height):
        """Cria um input de resposta curta.
        Args:
            x (int): Posição horizontal do canto superior esquerdo do input.
            y (int): Posição vertical do canto superior esquerdo do input.
            width (int): Largura do input.
            height (int): Altura do input.

        Returns:
            _type_: _description_
        """

        inputLine = QLineEdit(self)
        inputLine.move(x,y)
        inputLine.resize(width, height)
        return inputLine
    
    # -------- FIM CONFIGURAÇÃO DOS INPUTS ---------------------

    # -------- CONFIGURAÇÃO DOS LABELS -------------------------

    def createLabel(self, x, y, text, width=100, height=30):
        """Cria um rótulo para um elemento

        Args:
            x (int): Posição horizontal do canto superior esquerdo do rótulo.
            y (int): Posição vertical do canto superior esquerdo do rótulo.
            text (str): Texto contido no rótulo
            width (int, optional): Largura do rótulo. Defaults to 100.
            height (int, optional): Altura do rótulo. Defaults to 30.

        Returns:
            QLabel: Rótulo criado.
        """

        label = QLabel(self)
        label.setText(text)
        label.move(x, y)
        label.resize(width, height)
        return label

    # -------- FIM CONFIGURAÇÃO DOS LABELS ---------------------


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = Window()
    sys.exit(app.exec_())