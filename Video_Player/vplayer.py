
import sys
import time
import datetime

import cv2
from PyQt5 import QtCore, QtGui

from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, QPoint,QDir

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from sources import sources

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets

class CommonHelper(object):
    @staticmethod
    def read(qss):
        try:
            with open(qss, mode='r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(e)
            return ''


class Player(QLabel):
    double_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(Player, self).__init__(parent)

        self.mouse_pressed = False
        self.mouse_position = None

        self.setPixmap(QPixmap(':welcome.png'))
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setMinimumSize(640, 360)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == QtCore.Qt.LeftButton:
            self.mouse_pressed = True
            self.mouse_position = event.globalPos() - self.parent().pos()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if QtCore.Qt.LeftButton and self.mouse_pressed:
            self.parent().move(event.globalPos() - self.mouse_position)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.mouse_pressed = False

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self.double_clicked.emit()


class Slider(QSlider):
    signal_valueChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(Slider, self).__init__()

    def wheelEvent(self, e: QtGui.QWheelEvent) -> None:
        pass

    def dragMoveEvent(self, a0: QtGui.QDragMoveEvent) -> None:
        pass

    def dragLeaveEvent(self, a0: QtGui.QDragLeaveEvent) -> None:
        print(self.value())

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        current_x = event.pos().x()
        per = current_x * 1.0 / self.width()
        value = per * (self.maximum() - self.minimum()) + self.minimum()
        self.signal_valueChanged.emit(value)


class UI(QWidget):
    def __init__(self, parent=None):
        super(UI, self).__init__(parent, flags=QtCore.Qt.WindowStaysOnTopHint)

        self.setWindowTitle('Video Player')
        self.setWindowIcon(QIcon(':logo.png'))

        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self.player = Player(self)
        self.player.double_clicked.connect(self.action_double_clicked)

        self.play = QPushButton('', self)
        self.play.setIcon(QIcon(self.style().standardIcon(QStyle.SP_MediaPlay)))
        self.play.clicked.connect(self.action_play)

        self.reset = QPushButton('', self)
        self.reset.setIcon(QIcon(':reset.svg'))
        self.reset.clicked.connect(self.action_reset)

        

        

        self.open = QPushButton('', self)
        self.open.setIcon(QIcon(':open.svg'))
        self.open.setObjectName('open')
        self.open.clicked.connect(self.action_open)

        self.spin = QSpinBox(self)

        self.slider = Slider(self)
        self.slider.setOrientation(QtCore.Qt.Horizontal)

       
        openAction = QAction(QIcon('open.png'), '&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.action_open)

        
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        live_record_Action = QAction(QIcon('open.png'), '&Live Record', self)        

        live_record_Action.setStatusTip('Record Videos')
        live_record_Action.triggered.connect(self.startrec)


        fancy_record_Action = QAction(QIcon('open.png'), '&Fancy Record', self)        
        
        fancy_record_Action.setStatusTip('Fancy Recording')
        fancy_record_Action.triggered.connect(self.start_fancy_rec)

        mergeAction = QAction(QIcon('open.png'), '&Merge', self)        
    
        mergeAction.setStatusTip('Merge Videos')
        mergeAction.triggered.connect(self.onClick)


        trimAction = QAction(QIcon('exit.png'), '&Trim', self)        
        
        trimAction.setStatusTip('Trim Video')
        trimAction.triggered.connect(self.trimopenFile)

        saveframeAction = QAction(QIcon('open.png'), '&Save Video frames', self)        
    
        saveframeAction.setStatusTip('Video to frames')
        saveframeAction.triggered.connect(self.onClick1)



        self.menubar = QMenuBar(self)
        actionFile = self.menubar.addMenu("&File")
        recordVideo=self.menubar.addMenu("&Record")
        editVideo=self.menubar.addMenu("&Edit")
        
        


        
        actionFile.addAction(openAction)
        actionFile.addAction(exitAction)
       

        recordVideo.addAction(live_record_Action)
        recordVideo.addAction(fancy_record_Action)

        editVideo.addAction(mergeAction)
        editVideo.addAction(trimAction)
        editVideo.addAction(saveframeAction)


        controller_layout = QHBoxLayout()
        
        controller_layout.addWidget(self.play)
        controller_layout.addWidget(self.reset)
        controller_layout.addWidget(self.slider, stretch=1)
        controller_layout.addWidget(self.spin)
        controller_layout.addWidget(self.open)

        controller_layout.setContentsMargins(0, 0, 0, 0)
        controller_layout.setSpacing(0)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.player)
        main_layout.addLayout(controller_layout)
        self.setLayout(main_layout)

    def action_double_clicked(self):
     
        video_url, _ = QFileDialog.getOpenFileName(self, 'Video Player', '', '*.mp4;*.mkv;*.rmvb')
        if video_url:
            self.video_url = video_url
            self.action_reset()

    def action_open(self):
        pass

    def action_play(self):
        pass

    def action_reset(self):
        pass
    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)

    def exitCall(self):
        sys.exit(app.exec_())

    def startrec(self):
        cap = cv2.VideoCapture(0)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
        size = (width, height)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('recordvideo1.avi', fourcc, 20.0, size)

        while(True):
            _, frame = cap.read()
            cv2.imshow('Recording...', frame)
            out.write(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        out.release()
        cv2.destroyAllWindows()
    
    def start_fancy_rec(self):                                                                              #save Video while skipping alternate frames
        cap = cv2.VideoCapture(0)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
        size = (width, height)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('recordvideo2.avi', fourcc, 20.0, size)
        c=2
        framecheck=0


        while(True):
            _, frame = cap.read()
            cv2.imshow('Recording...', frame)
            if framecheck%c==0:
                out.write(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            framecheck+=1
        


        cap.release()
        out.release()
        cv2.destroyAllWindows()

    def trimopenFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())

        if fileName != '':
            self.takeinputs(fileName)
    
    def takeinputs(self,fileName): 
        input_start_time, done1 = QtWidgets.QInputDialog.getInt( 
             self, 'Input Dialog', 'Enter time in seconds from which trimming should start:')  
  
        input_end_time, done2 = QtWidgets.QInputDialog.getInt( 
           self, 'Input Dialog', 'Enter the time in seconds at which trimming should end ')   
  
  
        if done1 and done2 : 
             
            self.extract_clip(fileName,int(input_start_time),int(input_end_time))
    
        
    def extract_clip(self,fileName,begin,end):
        time_begin=begin
        time_end=end
        video_path=fileName
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        duration = int(frame_count / fps)
        if time_begin < 0 or time_end > duration:
            ValueError('Invalid time inputs')
            return -1

        start_frame = time_begin * fps
        end_frame = time_end * fps
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output_{}_{}.avi'.format(time_begin, time_end), fourcc, fps, (int(cap.get(3)), int(cap.get(4))))

        current_frame = start_frame
        while(cap.isOpened()):
            current_frame += 1
            ret, frame = cap.read()
            out.write(frame)
            if current_frame >= end_frame:
                break

        cap.release()
        cv2.destroyAllWindows()
        print("Successful")
        QMessageBox.about(self, "Trimming done", "The Input video has been succesfully trimmed ")

    def onClick(self):                                                                  #Open New Window for Merge Action
        self.SW = SecondWindow()
        self.SW.show()
    def onClick1(self):                                                                 #Open New window to Save Video to frames
        self.TW = ThirdWindow()
        self.TW.show()

    
class SecondWindow(QWidget):
    li=list()

    def __init__(self):
        super().__init__()
        li=list()

        self.initUI()

    def initUI(self):
        self.video1path = QPushButton('Choose Video 1')
        self.video1path.setMaximumWidth(150)
        self.video2path = QPushButton('Choose Video 2')
        self.setdir = QPushButton('Change save dir')
        self.video1path.clicked.connect(self.openvideo1)
        self.video2path.clicked.connect(self.openvideo2)
        self.setdir.clicked.connect(self.setpath)
        




        self.video1pathEdit = QLabel('Video 1 not selected ')
        self.video2pathEdit = QLabel('Video 2 not selected ')
        self.setdirEdit = QLabel('Change Save dir')


        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.video1path, 1, 0)
        grid.addWidget(self.video1pathEdit, 1, 1)

        grid.addWidget(self.video2path, 2, 0)
        grid.addWidget(self.video2pathEdit, 2, 1)

        grid.addWidget(self.setdir, 3, 0)
        grid.addWidget(self.setdirEdit, 3, 1)

        self.setLayout(grid)

        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('Merge')
        self.show()
    def openvideo1(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())

        if fileName != '':
           
            self.li.append(fileName)
            self.video1pathEdit.setText(fileName)
            
    def openvideo2(self):
        fileName1, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())

        if fileName1 != '':
           
            self.li.append(fileName1)
            self.video2pathEdit.setText(fileName1)
    
    

    def setpath(self):
        fileName2= str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        if fileName2 != '':
           
            self.setdirEdit.setText(fileName2)
            fileName=self.li[0]
            fileName1=self.li[1]
            self.merge_clip(fileName,fileName1,fileName2)

    
    def merge_clip(self,file_name,file_name1,file_name2):
        check=0
        video_path=self.li[0]
        video_path1=self.li[1]
        out_path=file_name2
        print("Video 1 path",video_path)
        print("Video 2 path",video_path1)
        output_filename=out_path+"/mergeoutput.avi"
        print(output_filename)
        cap = cv2.VideoCapture(video_path)
        cap1 = cv2.VideoCapture(video_path1)
        fps = cap.get(cv2.CAP_PROP_FPS)
        fps2 = cap.get(cv2.CAP_PROP_FPS)
  
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
    
        dim=(int(cap.get(3)), int(cap.get(4)))
        out = cv2.VideoWriter(output_filename, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))
    

        while(cap.isOpened() or cap1.isOpened()):
     
            ret, frame = cap.read()
            if ret==True:
                out.write(frame)
            else:
                ret1,frame1=cap1.read()
                if ret1==True:
  
                    frame1 = cv2.resize(frame1, dim)
                    if ret1==True:
                        out.write(frame1)
                        check=1
                    else:
                        break
                else:
                    break



      
        out.release()
        cap.release()

        cv2.destroyAllWindows()
        print("Successfully Merged")
        if check==1:
            QMessageBox.about(self, "Merging Done", "The Input videos have been succesfully Merged ")
    
class ThirdWindow(QWidget):
    li=list()

    def __init__(self):
        super().__init__()
        li=list()

        self.initUI()

    def initUI(self):
        self.video1path = QPushButton('Choose Video ')
        self.changesavedir = QPushButton('Set Directory')
        self.video1path.clicked.connect(self.openvideo1)
        self.changesavedir.clicked.connect(self.setpath)
        




        self.video1pathEdit = QLabel('Video 1 not selected ')
        self.changesavedirEdit = QLabel('Video 2 not selected ')


        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.video1path, 1, 0)
        grid.addWidget(self.video1pathEdit, 1, 1)

        grid.addWidget(self.changesavedir, 2, 0)
        grid.addWidget(self.changesavedirEdit, 2, 1)


        self.setLayout(grid)

        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('Get Frames')
        self.show()
    def openvideo1(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())

        if fileName != '':
            
            self.li.append(fileName)
            self.video1pathEdit.setText(fileName)
            
    
    
    

    def setpath(self):
        fileName2= str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        if fileName2 != '':
            
            self.changesavedirEdit.setText(fileName2)
            fileName=self.li[0]
            self.extractImages(fileName,fileName2)
    
    def extractImages(self,pathIn, pathOut):
        
        vidcap = cv2.VideoCapture(pathIn)
        success,image = vidcap.read()
        count = 0
        success = True

        while success:
            success,image = vidcap.read()
            
            cv2.imwrite( pathOut + "\\frame%d.jpg" % count, image)     
            
            count += 1
        vidcap.release()
        cv2.destroyAllWindows()
        QMessageBox.about(self, "Saving Done", "The frames from Input video have been saved")

class VideoTimer(QThread):
    signal_update_frame = pyqtSignal()
    signal_finished = pyqtSignal()

    def __init__(self):
        super(VideoTimer, self).__init__()
        self.playing = False
        self.fps = 0
        self.mutex = QMutex()

    def run(self):
        with QMutexLocker(self.mutex):
            self.playing = True
        while self.playing:
            self.signal_update_frame.emit()
            time.sleep(1 / self.fps)
        self.signal_finished.emit()

    def pause(self):
        with QMutexLocker(self.mutex):
            self.playing = False



class MainWindow(UI):
    VIDEO_TYPE_OFFLINE = 0
    VIDEO_TYPE_REAL_TIME = 1
    

    def __init__(self):
        super(MainWindow, self).__init__()
        APP_NAME="Video Player"

        self.setWindowTitle(APP_NAME)

        self.video_url = ''
        self.video_fps = 0
        self.video_total_frames = 0
        self.video_height = 0
        self.video_width = 0
        self.num = None

        self.current_frame = None

        self.timer = VideoTimer()
        self.timer.signal_update_frame.connect(self.video_play)
        self.timer.signal_finished.connect(self.video_paused)
      
        self.video_capture = cv2.VideoCapture()

        self.slider.signal_valueChanged.connect(self.video_jump)

    def video_jump(self, num):
        self.num = num
        self.slider.setValue(num)
        self.spin.setValue(num)
        self.get_frame(num)

    def video_paused(self):
        if self.num >= self.video_total_frames:
            self.action_reset()

    def video_play(self):
        if self.num is None:
            self.num = self.video_capture.get(cv2.CAP_PROP_POS_FRAMES) + 1
        else:
            self.num += 1
        self.slider.setValue(self.num)
        self.spin.setValue(self.num)
        self.get_frame()

    def action_double_clicked(self):
        [self.action_open, self.action_play][self.video_capture.isOpened()]()

    def action_reset(self):
        APP_NAME="Video Player"
        self.video_capture.open(filename=self.video_url)
        self.setWindowTitle(f'{APP_NAME} - {self.video_url}')
        self.video_fps = self.video_capture.get(cv2.CAP_PROP_FPS)
        self.video_total_frames = self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
        self.video_height = self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.video_width = self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.num = None
        self.timer.fps = self.video_fps
        self.slider.setMaximum(self.video_total_frames)
        self.spin.setSuffix(f'/{self.video_total_frames}')
        self.spin.setMaximum(self.video_total_frames)
        self.video_play()



    def action_open(self):
        video_url, _ = QFileDialog.getOpenFileName(self, 'Video Player', '', '*.mp4;*.mkv;*.rmvb')
        if video_url:
            self.video_url = video_url
            self.action_reset()

    def action_play(self):
        if self.video_capture.isOpened():
            self.play.setIcon(QIcon([':pause.svg', ':play.svg'][self.timer.playing]))
            [self.timer.start, self.timer.pause][self.timer.playing]()
        elif self.video_url:
            self.action_reset()

    def get_appropriate_size(self):
        if (self.player.width() / self.player.height()) > (self.video_width / self.video_height):
            return self.player.height() * (self.video_width / self.video_height), self.player.height()
        else:
            return self.player.width(), self.player.width() / (self.video_width / self.video_height)

    def get_frame(self, num=None):
        if self.video_capture.isOpened():
            if num is not None:
                self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, num)
            success, frame = self.video_capture.read()
            if success:
                self.current_frame = QImage(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).flatten(),
                                            self.video_width, self.video_height, QImage.Format_RGB888)
                self.player.setPixmap(QPixmap.fromImage(self.current_frame).scaled(*self.get_appropriate_size()))
            else:
                if self.num >= self.video_total_frames:
                    self.timer.pause()
                    self.play.setIcon(QIcon(':play.svg'))

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key_Space:
            self.action_play()
        event.accept()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        if not self.timer.playing and self.current_frame:
            self.player.setPixmap(QPixmap.fromImage(self.current_frame).scaled(*self.get_appropriate_size()))

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if self.timer.playing:
            self.timer.pause()
            APP_NAME="Video Player"
            close = QMessageBox.warning(self, APP_NAME,
                                        'Video playing, close app?',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if close == QMessageBox.No:
                event.ignore()
    




if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()

    win.show()
    sys.exit(app.exec_())
