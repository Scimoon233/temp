"""Assemble the existing n=16 matrix and inspect storage, without solving.

Optional dependencies: numpy, scipy, matplotlib.
Run in code/: python inspect_sparsity.py
The byte counts cover the final matrix arrays, not process peak memory or LU.
"""
from pathlib import Path
import os
import json
os.environ.setdefault('MPLCONFIGDIR', '/tmp/fem-p2-matplotlib')
import numpy as np
from scipy.sparse import coo_matrix
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import fem3d_p2 as f

def main():
    root=Path(__file__).resolve().parent.parent
    node,elem=f.mesh(16)
    edge,dof,bd,coords,_=f.topology(node,elem)
    _,vol,G=f.geometry(node,elem)
    nt=len(elem);nd=len(coords)
    a=(5+3*np.sqrt(5))/20;b=(5-np.sqrt(5))/20
    aq=np.full((4,4),b);np.fill_diagonal(aq,a)
    local=np.zeros((nt,10,10))
    for lam in aq:
        dp=f.dphi(lam,G)
        local+=vol[:,None,None]*np.einsum('tij,tkj->tik',dp,dp)/4
    rows=np.repeat(dof,10,axis=1).ravel()
    cols=np.tile(dof,(1,10)).ravel()
    A=coo_matrix((local.ravel(),(rows,cols)),shape=(nd,nd)).tocsr()
    data={
        'n':16,'NT':nt,'NV':len(node),'NE':len(edge),'N':nd,
        'format':A.format,'stored_entries_including_explicit_zeros':A.nnz,
        'explicit_zero_entries':int(np.sum(A.data==0)),
        'csr_arrays_bytes':int(A.data.nbytes+A.indices.nbytes+A.indptr.nbytes),
        'dense_float64_bytes':nd*nd*8,
        'assembly_local_rows_cols_bytes':int(local.nbytes+rows.nbytes+cols.nbytes),
        'scope':'Final full matrix arrays only; excludes factorization and process peak memory.'
    }
    (root/'data').mkdir(exist_ok=True)
    (root/'figures').mkdir(exist_ok=True)
    (root/'data/sparsity.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
    fig,ax=plt.subplots(figsize=(5.5,4.8))
    ax.spy(A,precision='present',markersize=.15,color='#007F82',rasterized=True)
    ax.xaxis.tick_bottom();ax.xaxis.set_label_position('bottom')
    ax.set_xlabel('Column index',fontsize=13);ax.set_ylabel('Row index',fontsize=13)
    ax.tick_params(labelsize=10)
    for spine in ax.spines.values():spine.set_color('#B9C9D3')
    fig.tight_layout()
    fig.savefig(root/'figures/sparsity.png',dpi=220,bbox_inches='tight')
    plt.close(fig)
    print(json.dumps(data,indent=2))

if __name__=='__main__':main()
