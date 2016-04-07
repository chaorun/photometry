# -*- coding: utf-8 -*-
"""
Need to convert all the pyfits procedures to astropy procedures.

"""

# 001V image has an airplane
# Some of the brighter stars are saturated


from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import robust as rb
import glob
import img_scale

def readimage(imfile,plot=False,siglo=3,sighi=7):
    image,header = fits.getdata(imfile,0,header=True)
    med = np.median(image)
    sig = rb.std(image)
    if plot:
        plt.ion()
        plt.figure(1)
        vmin = med - siglo*sig
        vmax = med + sighi*sig
        plt.imshow(image,vmin=vmin,vmax=vmax,cmap='gray')

    return image,header

def display_image(image,siglo=3,sighi=7):
    med = np.median(image)
    sig = rb.std(image)
    plt.ion()
    plt.figure(2)
    vmin = med - siglo*sig
    vmax = med + sighi*sig
    plt.imshow(image,vmin=vmin,vmax=vmax,cmap='gray')
    return


def makeband(band='V'):

    files = glob.glob('Mantis*[0-9]'+band+'.fit')
    zsz = len(files)
    image0,header0 = readimage(files[0])
    ysz,xsz = np.shape(image)
    
    stack = np.zeros((xsz,ysz,zsz))
    for i in range(zsz):
        image,header = readimage(files[i])
        
        stack[:,:,i] = image
        
    final = np.median(stack,axis=2)

    if band == 'V':
        tag = 'Blue'
        
    if band == 'R':
        tag = 'Green'
    
    if band == 'ip':
        tag = 'Red'
        
    fits.writeto(tag+'.fit', final, header)
    
    return
    
        
    
    
def make_RGB():
    
    Blue,header = fits.getdata('Blue.fit',0,header=True)
    Green,header = fits.getdata('Green.fit',0,header=True)    
    Red,header = fits.getdata('Red.fit',0,header=True)
    
    bmed = np.median(Blue)
    gmed = np.median(Green)
    rmed = np.median(Red)
    
    bsig = rb.std(Blue)
    gsig = rb.std(Green)                
    rsig = rb.std(Red)
        
    final = np.zeros((Blue.shape[0],Blue.shape[1],3),dtype=float)
    
    sigmin = 0.25
    sigmax = 5
    
    final[:,:,0] = img_scale.sqrt(Red,scale_min=rmed+sigmin*rsig,scale_max=rmed+0.6*sigmax*rsig)
    final[:,:,1] = img_scale.sqrt(Green,scale_min=gmed+sigmin*gsig,scale_max=gmed+0.6*sigmax*gsig)
    final[:,:,2] = img_scale.sqrt(Blue,scale_min=bmed+sigmin*bsig,scale_max=bmed+0.6*sigmax*bsig)

    plt.ion()
    plt.figure(99)
    plt.imshow(final,aspect='equal')
    
    
def junk():

    for i in range(zsz):
        print 'Reading image '+files[i]
        image,header = fits.getdata(files[i],0,header=True)
        stack[:,:,i] = image
   

    medstack = np.median(stack,axis=2)

#calimage = image - medstack

#med = np.median(calimage)
#sig = rb.std(calimage)
#vmin = med - 2*sig
#vmax = med + 5*sig

#plt.figure(2)
#plt.imshow(calimage,vmin=vmin,vmax=vmax,cmap='gray')

    return
