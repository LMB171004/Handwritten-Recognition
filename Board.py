from PyQt5.Qt import QWidget, QColor, QPixmap, QIcon, QSize, QCheckBox
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QSplitter,\
    QComboBox, QLabel, QSpinBox, QFileDialog
from PaintBoard import PaintBoard
 
class MainWidget(QWidget):
 
 
    def __init__(self, Parent=None):
        '''
        Constructor
        '''
        super().__init__(Parent)
         
        self.__InitData() #先初始化数据，再初始化界面
        self.__InitView()
     
    def __InitData(self):
        '''
                  初始化成员变量
        '''
        self.__paintBoard = PaintBoard(self)
        self.__colorList = QColor.colorNames() #获取颜色列表(字符串类型)
         
    def __InitView(self):
        '''
                  初始化界面
        '''
        self.setFixedSize(640,480)
        self.setWindowTitle("PaintBoard Example PyQt5")
         
         
        main_layout = QHBoxLayout(self) #新建一个水平布局作为本窗体的主布局
        main_layout.setSpacing(10) #设置主布局内边距以及控件间距为10px
     
         
        main_layout.addWidget(self.__paintBoard) #在主界面左侧放置画板
         
        sub_layout = QVBoxLayout() #新建垂直子布局用于放置按键
        sub_layout.setContentsMargins(10, 10, 10, 10) #设置此子布局和内部控件的间距为10px
         self.__btn_Paint = QPushButton("保存作品")
        self.__btn_Paint.setParent(self)
        self.__btn_Paint.clicked.connect(self.on_btn_Paint_Clicked)
        sub_layout.addWidget(self.__btn_Paint)
                    
        self.__cbtn_Eraser = QCheckBox("  使用橡皮擦")
        self.__cbtn_Eraser.setParent(self)
        self.__cbtn_Eraser.clicked.connect(self.on_cbtn_Eraser_clicked)
        sub_layout.addWidget(self.__cbtn_Eraser)
         
        splitter = QSplitter(self) #占位符
        sub_layout.addWidget(splitter)
         
        self.__label_penThickness = QLabel(self)
        self.__label_penThickness.setText("画笔粗细")
        self.__label_penThickness.setFixedHeight(20)
        sub_layout.addWidget(self.__label_penThickness)
         
        self.__spinBox_penThickness = QSpinBox(self)
        self.__spinBox_penThickness.setMaximum(20)
        self.__spinBox_penThickness.setMinimum(2)
        self.__spinBox_penThickness.setValue(10) #默认粗细为10
        self.__spinBox_penThickness.setSingleStep(2) #最小变化值为1
        self.__spinBox_penThickness.valueChanged.connect(self.on_PenThicknessChange)#关联spinBox值变化信号和函数on_PenThicknessChange
        sub_layout.addWidget(self.__spinBox_penThickness)
         
        self.__label_penColor = QLabel(self)
        self.__label_penColor.setText("画笔颜色")
        self.__label_penColor.setFixedHeight(20)
        sub_layout.addWidget(self.__label_penColor)
         
        self.__comboBox_penColor = QComboBox(self)
        self.__fillColorList(self.__comboBox_penColor) #用各种颜色填充下拉列表
        self.__comboBox_penColor.currentIndexChanged.connect(self.on_PenColorChange) #关联下拉列表的当前索引变更信号与函数on_PenColorChange
        sub_layout.addWidget(self.__comboBox_penColor)
 
        main_layout.addLayout(sub_layout) #将子布局加入主布局
 
 
    def __fillColorList(self, comboBox):
 
        index_black = 0
        index = 0
        for color in self.__colorList: 
            if color == "black":
                index_black = index
            index  = 1
            pix = QPixmap(70,20)
            pix.fill(QColor(color))
            comboBox.addItem(QIcon(pix),None)
            comboBox.setIconSize(QSize(70,20))
            comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
 
        comboBox.setCurrentIndex(index_black)
         
    def on_PenColorChange(self):
        color_index = self.__comboBox_penColor.currentIndex()
        color_str = self.__colorList[color_index]
        self.__paintBoard.ChangePenColor(color_str)
 
    def on_PenThicknessChange(self):
        penThickness = self.__spinBox_penThickness.value()
        self.__paintBoard.ChangePenThickness(penThickness)
     
    def on_btn_Save_Clicked(self):
        savePath = QFileDialog.getSaveFileName(self, 'Save Your Paint', '.\\', '*.png')
        print(savePath)
        if savePath[0] == "":
            print("Save cancel")
            return
        image = self.__paintBoard.GetContentAsQImage()
        image.save(savePath[0])
         
    def on_cbtn_Eraser_clicked(self):
        if self.__cbtn_Eraser.isChecked():
            self.__paintBoard.EraserMode = True #进入橡皮擦模式
        else:
            self.__paintBoard.EraserMode = False #退出橡皮擦模式
         
         
    def Quit(self):
        self.close()
