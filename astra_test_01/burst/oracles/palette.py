"""O1 CIE76 nearest swatch, percent outside tolerance, Lab KMeans centroids.
Calibration: dE_tol and max_off_pct must come from approved scope anchors;
cluster_count=3 is a descriptive summary budget, never an acceptance threshold.
"""
import numpy as np
from sklearn.cluster import KMeans
from .common import *

def adherence(rgba,swatches_hex,dE_tol,*,max_off_pct=None,cluster_count=3,alpha_min=ALPHA_MIN,display_scale=None,subject=''):
    a=image_array(rgba,display_scale);pixels=lab(a[...,:3])[a[...,3]>=alpha_min]
    if not len(pixels) or not swatches_hex:return report('O1',subject,None,max_off_pct,reason='Empty foreground or undeclared swatches')
    if dE_tol<0 or cluster_count<1:raise ValueError('Invalid palette parameters')
    dist=np.linalg.norm(pixels[:,None,:]-lab(swatches(swatches_hex))[None,:,:],axis=2).min(axis=1)
    off=pixels[dist>dE_tol];centers=[]
    if len(off):
        k=min(cluster_count,len(np.unique(off,axis=0)))
        centers=KMeans(n_clusters=k,random_state=0,n_init=10).fit(off).cluster_centers_.tolist()
    return report('O1',subject,float(100*len(off)/len(pixels)),max_off_pct,unit='percent',metrics={'off_palette_lab_centroids':centers,'mean_dE':float(dist.mean()),'dE_tol':dE_tol})
