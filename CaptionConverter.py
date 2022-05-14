import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import tkinter.messagebox as msgbox
from pathlib import Path
from os import startfile as sf
#ValueObject - 필수 값들 저장소
class VO:
    
    Videoname = [] #원본 비디오파일 절대경로
    Captionname = [] #원본 자막파일 절대경로

#사용자 ERROR처리
class  ERR:

    ERRCODE = {
     "noVideofile" : "추가된 동영상파일이 없습니다" ,
     "noCaptionfile":"추가된 자막파일이 없습니다.",
     "notequalcontents":"추가된 동영상과 자막파일의 갯수가 일치하지않습니다.",
     "cancel" : "사용자가 작업을 취소했습니다.",
     "notCaptionfile" : "자막파일이 아닙니다."
     }
   
    def errorcenter(key):
        return msgbox.showwarning("경고",key)
#실행버튼 클릭 후 확인 - True 취소 - False 반환,오류발생시 ERR클래스에 오류메세지 전달   
def notiCenter():
    confirm_user = msgbox.askokcancel("실행","총 %d 개의 자막파일을 변환합니다" %Captionlist_file.size())
    if confirm_user == False:
        ERR.errorcenter(ERR.ERRCODE["cancel"])
        return False
    elif Captionlist_file.size() == 0:
        ERR.errorcenter(ERR.ERRCODE["noCaptionfile"])
        return False
    elif Videolist_file.size() != Captionlist_file.size():
        ERR.errorcenter(ERR.ERRCODE["notequalcontents"])
        return False
   
    elif Videolist_file.size() == 0:
        ERR.errorcenter(ERR.ERRCODE["noVideofile"])
    
    else:
        return True
#비디오파일을 Videoname프로퍼티에 저장
def add_Videofile():
    files = filedialog.askopenfilenames(title="동영상 파일을 선택하세요",\
    filetypes=(("mp4 파일","*.mp4"),("avi 파일","*.avi"),("mkv 파일","*.mkv"),("모든 파일","*.*"))\
    ,initialdir=r"C:\Users\gkgjs\Desktop") #최초에 C:/경로를 보여줌
    for file in files:
        print(file)
        Videolist_file.insert(END,file)
        inform.Videoname.append(file)
def del_Videofile():
    for index in reversed(Videolist_file.curselection()):
        Videolist_file.delete(index)
        inform.Videoname.pop(index)

#자막파일을 Captionname프로퍼티에 저장
def add_Captionfile():
    files = filedialog.askopenfilenames(title="자막파일을 선택하세요",\
        filetypes=(("smi파일","*.smi"),("srt파일","*.srt"),("모든파일","*.*")),\
        initialdir=r"C:\Users\gkgjs\Desktop")

    for file in files:
        print(file)
        Captionlist_file.insert(END,file)
        inform.Captionname.append(file)
        
def del_Captionfile():
    for index in reversed(Captionlist_file.curselection()):
        Captionlist_file.delete(index)
        inform.Captionname.pop(index)


def sep_filepath(lst):
    filename = []

    if len(lst) != 0:
        for i in range(0,len(lst)):
            p = Path(lst[i])
            filename.append(p.stem)
           
    return filename


def clear():
    Videolist_file.delete(first=0,last=Videolist_file.size())
    Captionlist_file.delete(first=0,last=Captionlist_file.size())
    inform.Videoname.clear
    inform.Captionname.clear

#실행버튼 클릭
def start():
    
    if notiCenter() == True:
            Video_fullfilename = sep_filepath(inform.Videoname)
            Caption_fullfilename = sep_filepath(inform.Captionname)
            count = 0
            
            for i in range(0,len(Video_fullfilename)):
                
    
                if Video_fullfilename[i] != Caption_fullfilename[i]:
                    Path(inform.Captionname[i]).replace(str(Path(inform.Videoname[i]).parent/Path(inform.Videoname[i]).stem) + Path(inform.Captionname[i]).suffix)
                    #progressbar
                    p_var.set(len(inform.Captionname[i])/len(inform.Captionname)*100)
                    count += 1
                    if count == len(inform.Captionname):
                        msgbox.showinfo("완료","변환 완료")
                        sf(Path(inform.Videoname[i]).parent)
                        clear()
                else:
                    msgbox.showwarning("알림","파일의 이름이 일치합니다")

# layout
root = Tk()
inform = VO() #VO클래스 타입 인스턴스 생성
root.title("CaptionConverter")
# 동영상파일과 자막파일의 절대경로가 저장되는 리스트
root.geometry("1280x800+320+140")
root.resizable(False,False)           
# 동영상 리스트 프레임
Videolist_frame = Frame(root)

Videolist_frame.pack(fill="both",pady=5,padx=5)
scrollbar = Scrollbar(Videolist_frame)
scrollbar.pack(side="right",fill="y")
Videolist_file = Listbox(Videolist_frame,selectmode="extended",height =15,yscrollcommand=scrollbar.set)
Videolist_file.pack(side="left",fill="both",expand=True)
scrollbar.config(command=Videolist_file.yview)
#파일 프레임(자막,파일추가와 선택삭제)
videofile_frame = Frame(root)
videofile_frame.pack(fill="x",pady=5,padx=5)
btn_add_file = Button(videofile_frame, text= "파일추가",width=12,padx=5,pady=5,command=add_Videofile)
btn_del_Videofile = Button(videofile_frame,text="동영상삭제",width=12,padx=5,pady=5,command=del_Videofile)
btn_add_file.pack(side="left")
btn_del_Videofile.pack(side="right")


#자막 리스트 프레임
Captionlist_frame = Frame(root)
Captionlist_frame.pack(fill="both",pady=5,padx=5)
Captionfile_frame = Frame(root)
Captionfile_frame.pack(fill="x",pady=5,padx=5)
btn_add_Captionfile = Button(Captionfile_frame, text= "자막파일추가",width=12,padx=5,pady=5,command=add_Captionfile)
btn_del_Captionfile = Button(Captionfile_frame,text="자막삭제",width=12,padx=5,pady=5,command=del_Captionfile)
btn_add_Captionfile.pack(side="left")
btn_del_Captionfile.pack(side="right")
scrollbar = Scrollbar(Captionlist_frame)
scrollbar.pack(side="right",fill="y")
Captionlist_file = Listbox(Captionlist_frame,selectmode="extended",height =15,yscrollcommand=scrollbar.set)
Captionlist_file.pack(side="left",fill="both",expand=True)
scrollbar.config(command=Captionlist_file.yview)



#진행상황 Progress bar

frame_progress = LabelFrame(root,text="진행상황")
frame_progress.pack(fill="x",pady=5,padx=5)
p_var = DoubleVar()
progress_bar = ttk.Progressbar(frame_progress,maximum=100,variable=p_var)
progress_bar.pack(fill="x",pady=5,padx=5,ipady=5)

#실행 프레임

frame_run = Frame(root)
frame_run.pack(fill="x",pady=5,padx=5)
btn_close = Button(frame_run,padx=5,pady=5,text="닫기",width=12,command=root.quit)
btn_close.pack(side="right",pady=5,padx=5)
btn_start = Button(frame_run, padx=5,pady=5,text="시작",width=12,command=start)
btn_start.pack(side="right",pady=5,padx=5)




root.mainloop()