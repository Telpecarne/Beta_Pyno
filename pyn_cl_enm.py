from numpy import *
import pyn_fort_enm as f_enm
import pyn_fort_general as f
import pylab

class gnm():
    
    def __init__(self,system=None,cutoff=10.0):

        self.contact_map=None

        if system!=None:
            if type(system) in [list,ndarray]:
                self.contact_map=array(system)
            else:
                self.contact_map=self.mk_contact_map(system,cutoff)
            self.eigenvals,self.eigenvects,self.freqs,self.bfacts,self.inverse,self.correl=self.rebuild()
            self.bfacts_pdb,self.factor,self.sqr_dev=self.fitt_bfacts()
            
    def rebuild(self):

        return f_enm.gnm(self.contact_map,len(self.contact_map[0]))
        

    def mk_contact_map(self,system,cutoff):

        self.system=system
        comap=f_enm.contact_map(cutoff,system.coors[0].xyz,system.num_atoms)
        return comap

    def fitt_bfacts(self):
        
        bfacts_pdb=[]
        for ii in range(len(self.contact_map)):
            bfacts_pdb.append(self.system.atom[ii].bfactor)

        aa=0.0
        bb=0.0

        for ii in range(len(self.contact_map)):
            aa+=bfacts_pdb[ii]*self.bfacts[ii]
            bb+=self.bfacts[ii]*self.bfacts[ii]

        aa=aa/bb

        bb=0.0
        for ii in range(len(self.contact_map)):
            bb+=(bfacts_pdb[ii]-aa*self.bfacts[ii])**2
            
        return bfacts_pdb,aa,bb

    def plot_best_cutoff(self):

        ctoff=[]
        r_2=[]
        l=1.0*len(self.system.atom)
        for ii in arange(6.5,12.6,0.1):
            ctoff.append(ii)
            aa=gnm_classic(self.system,cutoff=ii)
            r_2.append((aa.sqr_dev)/l)
            del(aa)

        pylab.plot(ctoff,r_2,'yo')
        pylab.ylabel('<R^2>|atom')
        pylab.xlabel('Cut Off (A)')
        self.best_cutoff=[]
        self.best_cutoff.append(ctoff)
        self.best_cutoff.append(r_2)
        return pylab.show()

    def plot_bfacts(self):

        pylab.plot(self.bfacts_pdb,color="blue")
        pylab.plot(self.factor*self.bfacts,color="red")
        return pylab.show()

    def plot_dispersion_bfacts(self):

        pylab.plot(self.bfacts,self.bfacts_pdb,'yo')
        pylab.plot(self.bfacts,self.factor*self.bfacts,'r--')
        return pylab.show()

    def plot_contact_map(self):

        pylab.gray()
        pylab.matshow(self.contact_map,cmap='binary')
        return pylab.show()

    def plot_inverse(self):

        pylab.gray()
        pylab.matshow(self.inverse,cmap='binary')
        return pylab.show()
    
    def plot_correl_norm_2(self):
        
        #pylab.imshow(self.correl,origin='lower',interpolation=None) 
        vmin=ma.minimum(self.correl)
        vmax=ma.maximum(self.correl)
        vmax=max([abs(vmin),vmax])
        #ref_white=(-vmin)/(vmax-vmin)
        cdict = {                                                                            
            'red'  :  ((0.0,0.0,0.0), (0.5,1.0,1.0), (1.0,1.0,1.0)),
            'green':  ((0.0,0.0,0.0), (0.5,1.0,1.0), (1.0,0.0,0.0)),
            'blue' :  ((0.0,1.0,1.0), (0.5,1.0,1.0), (1.0,0.0,0.0))
            }
        my_cmap = pylab.matplotlib.colors.LinearSegmentedColormap('my_colormap', cdict, 1024)
        pylab.matshow(self.correl,cmap=my_cmap,vmin=-vmax,vmax=vmax)
        pylab.colorbar()
        return pylab.show()

    def plot_correl_norm(self):
        
        cdict = {                                                                            
            'red'  :  ((0.0,0.0,0.0), (0.5,1.0,1.0), (1.0,1.0,1.0)),
            'green':  ((0.0,0.0,0.0), (0.5,1.0,1.0), (1.0,0.0,0.0)),
            'blue' :  ((0.0,1.0,1.0), (0.5,1.0,1.0), (1.0,0.0,0.0))
            }
        my_cmap = pylab.matplotlib.colors.LinearSegmentedColormap('my_colormap', cdict, 1024)
        #pylab.matshow(self.correl,cmap='RdBu',vmin=-1.0,vmax=1.0)
        #pylab.pcolor(self.correl,cmap=my_cmap,vmin=-1.0,vmax=1.0)
        #nx,ny=self.correl.shape
        #pylab.matshow(self.correl,cmap=my_cmap,vmin=-1.0,vmax=1.0,extent=[0,nx,0,ny])
        pylab.matshow(self.correl,cmap=my_cmap,vmin=-1.0,vmax=1.0)
        #if hasattr(self,'system'):
        #    pylab.xticks(arange(0,len(self.system.atom[:]),5),[x.resid_pdb_index for x in self.system.atom[:]],rotation=90)
        #    pylab.yticks(arange(0,len(self.system.atom[:]),5),[x.resid_pdb_index for x in self.system.atom[:]])
        pylab.colorbar()
        return pylab.show()

    def plot_correl(self):
        
        vmin=ma.minimum(self.inverse)
        vmax=ma.maximum(self.inverse)     
        vmax=max([abs(vmin),vmax])
        cdict = {                                                                            
            'red'  :  ((0.0,0.0,0.0), (0.5,1.0,1.0), (1.0,1.0,1.0)),
            'green':  ((0.0,0.0,0.0), (0.5,1.0,1.0), (1.0,0.0,0.0)),
            'blue' :  ((0.0,1.0,1.0), (0.5,1.0,1.0), (1.0,0.0,0.0))
            }
        my_cmap = pylab.matplotlib.colors.LinearSegmentedColormap('my_colormap', cdict, 1024)
        pylab.matshow(self.inverse,cmap=my_cmap,vmin=-vmax,vmax=vmax)
        pylab.colorbar()
        return pylab.show()


    def write(self):

        f_map = open('contact_map.oup','w')
        
        for ii in range(len(self.contact_map)):
            for jj in range(ii+1,len(self.contact_map)):
                if self.contact_map[ii][jj] == True :
                    f_map.write("%s %s \n" %(self.system.atom[ii].pdb_index,self.system.atom[jj].pdb_index))
        f_map.close

        f_vects = open('gnm_vects.oup','w')

        f_vects.write("%s Modes, %s Nodes \n" %(len(self.contact_map),len(self.contact_map)))
        f_vects.write(" \n")
        for ii in range(len(self.contact_map)):
            for jj in range(len(self.contact_map)):
                f_vects.write("%s %f \n" %(self.system.atom[jj].pdb_index,self.eigenvects[ii][jj]))
            f_vects.write(" \n")





class anm():
    
    def __init__(self,system=None,cutoff=10.0):

        self.contact_map=None

        if system!=None:
            self.parent=system
            if type(system) in [list,ndarray]:
                self.contact_map=array(system)
            else:
                self.contact_map=self.mk_contact_map(system,cutoff)
            self.eigenvals,self.eigenvects2,self.freqs,self.bfacts,self.inverse,self.correl=self.build(system)
            self.eigenvects=zeros(shape=(len(self.contact_map)*3,len(self.contact_map),3))
            for aa in range(3*len(self.contact_map)):
                for ii in range(len(self.contact_map)):
                    iii=(ii)*3
                    for jj in range(3):
                        jjj=iii+jj
                        self.eigenvects[aa,ii,jj]=self.eigenvects2[aa,jjj]

            self.bfacts_pdb,self.factor,self.sqr_dev=self.fitt_bfacts()
            
    def build(self,system):

        return f_enm.anm(self.contact_map,system.coors[0].xyz,len(self.contact_map[0]))

    def rebuild(self):

        self.eigenvals,self.eigenvects2,self.freqs,self.bfacts,self.inverse,self.correl=self.build(self.parent)
        self.eigenvects=zeros(shape=(len(self.contact_map)*3,len(self.contact_map),3))
        for aa in range(3*len(self.contact_map)):
            for ii in range(len(self.contact_map)):
                iii=(ii)*3
                for jj in range(3):
                    jjj=iii+jj
                    self.eigenvects[aa,ii,jj]=self.eigenvects2[aa,jjj]

        self.bfacts_pdb,self.factor,self.sqr_dev=self.fitt_bfacts()
        

    def mk_contact_map(self,system,cutoff):

        self.system=system
        comap=f_enm.contact_map(cutoff,system.coors[0].xyz,system.num_atoms)
        return comap

    def fitt_bfacts(self):
        
        bfacts_pdb=[]
        for ii in range(len(self.contact_map)):
            bfacts_pdb.append(self.system.atom[ii].bfactor)

        aa=0.0
        bb=0.0

        for ii in range(len(self.contact_map)):
            aa+=bfacts_pdb[ii]*self.bfacts[ii]
            bb+=self.bfacts[ii]*self.bfacts[ii]

        aa=aa/bb

        bb=0.0
        for ii in range(len(self.contact_map)):
            bb+=(bfacts_pdb[ii]-aa*self.bfacts[ii])**2
            
        return bfacts_pdb,aa,bb

    def best_cutoff(self):

        ctoff=[]
        r_2=[]
        l=1.0*len(self.system.atom)
        for ii in arange(8.0,16.0,0.2):
            ctoff.append(ii)
            aa=anm_classic(self.system,cutoff=ii)
            r_2.append((aa.sqr_dev)/l)
            del(aa)

        pylab.plot(ctoff,r_2,'yo')
        pylab.ylabel('<R^2>|atom')
        pylab.xlabel('Cut Off (A)')
        self.best_cutoff=[]
        self.best_cutoff.append(ctoff)
        self.best_cutoff.append(r_2)
        return pylab.show()

    def plot_bfacts(self):

        pylab.plot(self.bfacts_pdb,color="blue")
        pylab.plot(self.factor*self.bfacts,color="red")
        return pylab.show()

    def plot_dispersion_bfacts(self):

        pylab.plot(self.bfacts,self.bfacts_pdb,'yo')
        pylab.plot(self.bfacts,self.factor*self.bfacts,'r--')
        return pylab.show()

    def plot_contact_map(self):

        pylab.gray()
        pylab.matshow(self.contact_map,cmap='binary')
        return pylab.show()

    def plot_inverse(self):

        pylab.gray()
        pylab.matshow(self.inverse,cmap='binary')
        return pylab.show()
    
    def plot_correl_norm_2(self):
        
        #pylab.imshow(self.correl,origin='lower',interpolation=None) 
        vmin=ma.minimum(self.correl)
        vmax=ma.maximum(self.correl)
        vmax=max([abs(vmin),vmax])
        #ref_white=(-vmin)/(vmax-vmin)
        cdict = {                                                                            
            'red'  :  ((0.0,0.0,0.0), (0.5,1.0,1.0), (1.0,1.0,1.0)),
            'green':  ((0.0,0.0,0.0), (0.5,1.0,1.0), (1.0,0.0,0.0)),
            'blue' :  ((0.0,1.0,1.0), (0.5,1.0,1.0), (1.0,0.0,0.0))
            }
        my_cmap = pylab.matplotlib.colors.LinearSegmentedColormap('my_colormap', cdict, 1024)
        pylab.matshow(self.correl,cmap=my_cmap,vmin=-vmax,vmax=vmax)
        pylab.colorbar()
        return pylab.show()

    def plot_correl_norm(self):
        
        cdict = {                                                                            
            'red'  :  ((0.0,0.0,0.0), (0.5,1.0,1.0), (1.0,1.0,1.0)),
            'green':  ((0.0,0.0,0.0), (0.5,1.0,1.0), (1.0,0.0,0.0)),
            'blue' :  ((0.0,1.0,1.0), (0.5,1.0,1.0), (1.0,0.0,0.0))
            }
        my_cmap = pylab.matplotlib.colors.LinearSegmentedColormap('my_colormap', cdict, 1024)
        #pylab.matshow(self.correl,cmap='RdBu',vmin=-1.0,vmax=1.0)
        #pylab.pcolor(self.correl,cmap=my_cmap,vmin=-1.0,vmax=1.0)
        #nx,ny=self.correl.shape
        #pylab.matshow(self.correl,cmap=my_cmap,vmin=-1.0,vmax=1.0,extent=[0,nx,0,ny])
        pylab.matshow(self.correl,cmap=my_cmap,vmin=-1.0,vmax=1.0)
        #if hasattr(self,'system'):
        #    pylab.xticks(arange(0,len(self.system.atom[:]),5),[x.resid_pdb_index for x in self.system.atom[:]],rotation=90)
        #    pylab.yticks(arange(0,len(self.system.atom[:]),5),[x.resid_pdb_index for x in self.system.atom[:]])
        pylab.colorbar()
        return pylab.show()

    def plot_correl(self):
        
        vmin=ma.minimum(self.inverse)
        vmax=ma.maximum(self.inverse)     
        vmax=max([abs(vmin),vmax])
        cdict = {                                                                            
            'red'  :  ((0.0,0.0,0.0), (0.5,1.0,1.0), (1.0,1.0,1.0)),
            'green':  ((0.0,0.0,0.0), (0.5,1.0,1.0), (1.0,0.0,0.0)),
            'blue' :  ((0.0,1.0,1.0), (0.5,1.0,1.0), (1.0,0.0,0.0))
            }
        my_cmap = pylab.matplotlib.colors.LinearSegmentedColormap('my_colormap', cdict, 1024)
        pylab.matshow(self.inverse,cmap=my_cmap,vmin=-vmax,vmax=vmax)
        pylab.colorbar()
        return pylab.show()


    def build_correl(self,modes='ALL'):

        list_modes=[]
        if modes=='ALL':
            num_modes=3*len(self.contact_map)
            for ii in range(num_modes):
                list_modes.append(ii+1)
        elif type(modes)==int:
            num_modes=1
            list_modes.append(modes)
        elif type(modes) in [list,tuple]:
            num_modes=len(modes)
            list_modes=list(modes)

        num_nodes=len(self.contact_map[0])
        self.correl=f_enm.correlation(self.eigenvects2,self.eigenvals,list_modes,num_nodes,num_modes)

    def involv_coefficient(self,modes='ALL',vect=None):

        if vect==None:
            print 'Error: vect=None'
            return

        self.ic={}
        list_modes=[]
        
        if modes=='ALL':
            for ii in range(self.num_modes):
                list_modes.append(ii+1)
        elif type(modes)==int:
            list_modes.append(modes)
        elif type(modes) in [list,tuple]:
            list_modes=modes

        for ii in list_modes:
            self.ic[ii]=f.aux_funcs_general.proj3d(self.eigenvects[ii],vect,len(self.eigenvects[ii]))

        return

        

    def write(self):

        f_map = open('contact_map.oup','w')
        
        for ii in range(len(self.contact_map)):
            for jj in range(ii+1,len(self.contact_map)):
                if self.contact_map[ii][jj] == True :
                    f_map.write("%s %s \n" %(self.system.atom[ii].pdb_index,self.system.atom[jj].pdb_index))
        f_map.close

        f_vects = open('anm_vects.oup','w')

        f_vects.write("%s Modes, %s Nodes \n" %(len(self.contact_map),len(self.contact_map)))
        f_vects.write(" \n")
        for aa in range(3*len(self.contact_map)):
            for ii in range(len(self.contact_map)):
                    f_vects.write("%s %f %f %f\n" %(self.system.atom[jj].pdb_index,self.eigenvects[aa,ii,0],self.eigenvects[aa,ii,1],self.eigenvects[aa,ii,2]))
                    f_vects.write(" \n")
