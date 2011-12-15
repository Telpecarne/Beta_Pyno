import struct as stc
from numpy import *



def quantumbin(xtc,bin,frames):
    JJ=0
    file=open(bin,'wb')
    filextc=open(xtc,'r')
    filegro=open(bin[:-3]+'gro','w')
    filegro.write('quantum'+'\n')
    for ff in range(frames):
        
        Box_size=zeros(shape=(3,3))
        
        filextc.seek(JJ,0)

        


        #for ii in range(1):
        line = filextc.readline()
        ss=line.split()
            
        N_A=int(ss[2])
        T_S=float(ss[5])
        time=int(ss[1])
        if ff==0:
            file.write(stc.pack('i',N_A))
            #print N_A
       
         
         
        if ff==0:
            filegro.write(str(N_A))
            filegro.write('\n')


        bb=0
        
        for ii in range(3):
            line = filextc.readline()
            ss=line.split()
            Box_size[ii]=float(ss[0]),float(ss[1]),float(ss[2])
            if ff==0:
                file.write(stc.pack('3f',float(ss[0])/10,float(ss[1])/10,float(ss[2])/10))
                #print float(ss[0]),float(ss[1]),float(ss[2])
        file.write(stc.pack('i',N_A))
        #print N_A
        
        file.write(stc.pack('i',time))
        #print time
        file.write(stc.pack('1f',T_S))
        #print T_S
        
        for jj in range(3):
                file.write(stc.pack('3f',Box_size[jj][0]/10,Box_size[jj][1]/10,Box_size[jj][2]/10))
                #print Box_size[jj][0],Box_size[jj][1],Box_size[jj][2]
        num_count=0
        
        
         
         
        
        for jj in range(1,N_A*3+1):
            var = filextc.readline()
            ss=var.split()
            #print ss,jj,'#'
            if jj%3==1:
                if ff==0:
                    a='ATOM  '
                    a+="%5d" % ((jj+2)/3)
                    a+=' '
                    a+=' '+"%-3s" % ss[0]
                    a+=' '
                    a+="%3s" % 'SOL'
                    a+=' '
                    a+="%1s" % ''
                    a+="%4d" % ((jj+2)/3)
                    a+=' '                                     # 27
                    a+='   ' 
                    charge=ss[3]

            if jj%3==2:
                file.write(stc.pack('3f',float(ss[0])/10,float(ss[1])/10,float(ss[2])/10))
                #print  float(ss[0]),float(ss[1]),float(ss[2]),jj/3+1
                if ff==0:
                    a+="%8.3f" % float(ss[0])
                    a+="%8.3f" % float(ss[1])
                    a+="%8.3f" % float(ss[2])
                    a+="%6.2f" % 0    # 55-60
                    a+="%6.2f" % 0  # 61-66
                    a+='          '                            # 67-76
                    a+="%2s" % ''  # 77-78
                    a+="%2s" % '-1'#charge     # 79-80
                    a+='\n'
                    filegro.write(a)

            if jj==(N_A*3):
                file.write(stc.pack('1f',1))
                #print 1
                JJ=filextc.tell()
                break


        if ff==0:
            b='   '+str(Box_size[0][0])[:9]+'  '+str(Box_size[1][1])[:9]+'  '+str(Box_size[2][2])[:9]
            filegro.write(b)
        #print 'FUUUUU',JJ,N_A

quantumbin('new_HISTORY_part1','NEU.bin',62500)
